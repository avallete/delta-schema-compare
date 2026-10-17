# Self-referencing FK to a non-PK UNIQUE key stays inline in export

> pgschema issue [#534](https://github.com/pgplex/pgschema/issues/534) (closed), fixed by [pgschema#540](https://github.com/pgplex/pgschema/pull/540)

## Context

pgschema issue #534 is the self-referencing follow-up to the broader
constraint-ordering family around issues #532 and #506. The failing shape is a
table whose foreign key points back to the same table, but targets a non-PK
UNIQUE key that is created separately. Inlining that FK inside `CREATE TABLE`
is safe only when it references the table's primary key. When it depends on a
standalone UNIQUE constraint or unique index created later, PostgreSQL rejects
the definition with `SQLSTATE 42830`.

Current pg-delta now has the same outstanding gap on its declarative-export
path. Open pg-toolbelt issue
[#543](https://github.com/supabase/pg-toolbelt/issues/543) shows `schema export`
writing a self-referencing composite FK inline inside the table file, followed
later in the same file by the unique index that the FK depends on. The loader
cannot repair same-file statement order, so the exported schema does not load
into an empty database.

This is adjacent to benchmark
[023](023-fk-before-standalone-unique-index.md), but it is not the same
scenario. Benchmark 023 is the cross-table incremental-diff case on a
pre-existing referenced table and remains solved on current pg-delta heads.
Issue #534 is the same-table export/load case, so it now belongs in its own
active benchmark entry.

## Refresh note (2026-10-17)

This refresh keeps checked-in/live `pg-delta` at
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` and checked-in/live `pgschema` at
`24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`; neither submodule head moved since
the 2026-10-16 refresh.

Today's material parity movement is on the pg-delta tracker side rather than in
the checked-in source SHAs:

- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-16'`
  surfaced open PR
  [#661](https://github.com/pgplex/pgschema/pull/661) for covered issue
  [#638](https://github.com/pgplex/pgschema/issues/638) plus still-open PR
  [#645](https://github.com/pgplex/pgschema/pull/645); neither changes this
  self-referencing FK benchmark
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-16'`
  surfaced new issues
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544)
- issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) is the
  exact parity tracker for pgschema issue #534: the export path keeps a
  self-referencing FK inline even though its same-table non-PK UNIQUE target is
  created later
- targeted pgschema keyword searches found no matching counterpart for
  pg-toolbelt issue [#544](https://github.com/supabase/pg-toolbelt/issues/544)
  beyond unrelated closed issue
  [#445](https://github.com/pgplex/pgschema/issues/445), so #544 does not
  create a new parity benchmark item today
- `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
  still treats a genuine self-reference as safe to keep inline:
  `cyclicForeignKeys()` explicitly skips self-referencing FKs and only splits
  multi-table cycles into sibling `.fk.sql` files
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts` and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/internal.ts` still make
  validated FOREIGN KEY constraints eligible for export-only inline folding
- `repos/pg-toolbelt/packages/pg-delta/tests/export-fidelity.test.ts` still
  asserts that validated FKs fold inline into `CREATE TABLE`, but it only
  covers the safe PK-target slice and not a self-referencing FK backed by a
  later same-file unique index
- `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-reorder-on-failure.test.ts`
  still confirms the loader cannot repair same-file ordering hazards:
  `loadOrder cannot fix same-file order - edit or split the file.`
- exact search `pgschema#534` still returns no pg-toolbelt issue or PR, while
  keyword searches for the self-referencing unique-index failure now surface
  open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) only

The earlier August "covered" verdict for pgschema issue #534 was therefore too
broad: it validated a safe planner/export shape on the then-current head, but
today's open pg-toolbelt issue #543 shows the default by-object export path
still fails on the exact self-referencing non-PK UNIQUE-key family. This
benchmark now moves to **tracked** on the current head.

## Reproduction SQL

Source schema to export:

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.people (
    id bigint PRIMARY KEY,
    org_id integer NOT NULL,
    merge_target_id bigint
);

CREATE UNIQUE INDEX uq_people_org_id_id
  ON test_schema.people (org_id, id);

ALTER TABLE test_schema.people
  ADD CONSTRAINT people_merge_target_fkey
  FOREIGN KEY (org_id, merge_target_id)
  REFERENCES test_schema.people (org_id, id);
```

**Expected:** pg-delta exports a loadable declarative shape, either by keeping
the self-referencing FK as a trailing `ALTER TABLE ... ADD CONSTRAINT` or by
splitting it into a later sibling FK file so the non-PK UNIQUE key exists
first.

**Actual on current pg-delta:** open issue
[#543](https://github.com/supabase/pg-toolbelt/issues/543) shows the table file
still loads in the unsafe order:

```sql
create table "test_schema"."people" (
  "id" bigint not null,
  "org_id" integer not null,
  "merge_target_id" bigint,
  constraint "people_pkey" primary key (id),
  constraint "people_merge_target_fkey" foreign key (org_id, merge_target_id)
    references test_schema.people(org_id, id)
);

create unique index uq_people_org_id_id
  on test_schema.people using btree (org_id, id);
```

Loading that file into an empty database fails because there is still "no
unique constraint matching given keys for referenced table".

## How pgschema handled it

pgschema closed issue #534 in
[PR #540](https://github.com/pgplex/pgschema/pull/540) by refining the
self-reference decision instead of treating every same-table FK as inline-safe.
The merged fix teaches `shouldDeferConstraint` to compare the referenced column
set with the table's primary key:

1. self-referencing FK to the PK -> still safe to inline
2. self-referencing FK to a separate UNIQUE constraint or unique index ->
   defer to `ALTER TABLE ... ADD CONSTRAINT`

The PR added targeted regressions for both slices:
`issue_534_self_ref_fk_unique` (deferred) and
`issue_534_self_ref_fk_pk` (still inline).

## Current pg-delta status

| Aspect | Status |
|---|---|
| Cross-table mutual FK export cycle handling | Yes - `cyclicForeignKeys()` moves only multi-table cycles into sibling `.fk.sql` files |
| Self-referencing FK to the table PK | Assumed safe inline by current export heuristics |
| Self-referencing FK to a non-PK UNIQUE constraint or unique index | No - current export still keeps this FK inline, matching open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) |
| Same-file loader recovery once the FK and unique index land in one file | No - current load-assist explicitly says same-file order cannot be repaired via `loadOrder` |
| Exact committed pg-delta regression for this scenario | No - current export tests cover mutual cross-table cycles and generic validated FK folding, but not this same-table non-PK UNIQUE-key slice |
| Existing pg-toolbelt tracker | Yes - open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543), no fixing PR yet |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Key export decision** | Distinguishes self-ref-to-PK from self-ref-to-non-PK UNIQUE and defers the latter | Distinguishes only multi-table cycles from non-cycles; a genuine self-reference is assumed inline-safe |
| **Self-referencing FK to PK** | Inline | Inline |
| **Self-referencing FK to non-PK UNIQUE key** | Deferred until after the backing UNIQUE object exists | Still folded into the table file before the backing unique index |
| **Current parity state** | Fixed | Tracked via open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) |

## Plan to handle it in pg-delta

1. Add export-time analysis for self-referencing FKs whose referenced column
   set does not match the table's primary key, and exclude them from inline
   folding.
2. Keep self-ref-to-PK FKs inline, but emit the non-PK UNIQUE-key slice as a
   later `ALTER TABLE ... ADD CONSTRAINT` (or sibling `.fk.sql`) after the
   backing UNIQUE constraint/index is present.
3. Add a regression in
   `repos/pg-toolbelt/packages/pg-delta/tests/export-fidelity.test.ts` or a
   dedicated export test that round-trips the exact self-referencing
   unique-index case through `exportSqlFiles()` and `loadSqlFiles()`.
4. Treat load-assist only as a diagnostic fallback; the correct export shape
   should make this scenario load without manual file editing or splitting.
