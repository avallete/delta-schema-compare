# Self-referencing FK to a non-PK UNIQUE key in export

> pgschema issue [#534](https://github.com/pgplex/pgschema/issues/534) (closed), fixed by [pgschema#540](https://github.com/pgplex/pgschema/pull/540)

## Context

## Refresh note (2026-10-28)

This recheck leaves checked-in/live `pg-delta` at
`6b82eff84dba925a176f0c6a78e5a16843885366`. Checked-in/live `pgschema`
advanced to `36a38ff3c25db956ae8b5be2eee552d8bc69fb47`. Merged PR
[#668](https://github.com/pgplex/pgschema/pull/668) is partition
detach/attach and is benchmark **026**. It does not touch this fold guard.

The solved verdict stays in place:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains
  in the checked-in/live history
- `packages/pg-delta/src/plan/internal.ts` still refuses an export constraint
  fold when a same-table column or a same-table dependent is emitted after
  `CREATE TABLE` (lines 779-793)
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` remains
  the committed regression
- exact search for `pgschema#534` still returns no dedicated pg-toolbelt
  issue or PR. Closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546) remain the
  effective tracker
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) gained
  commit `67793ef`. That commit edits `src/frontends/settle-desired.ts` and
  leaves the checked-in fold guard untouched

Benchmark 025 therefore stays **Solved in pg-delta**.

## Refresh note (2026-10-27)

This recheck leaves checked-in/live `pg-delta` at
`6b82eff84dba925a176f0c6a78e5a16843885366`. Checked-in/live `pgschema`
advanced to `8703c276c3ee4bab6d4e30b14e6e8982ace14b89`. Merged PR
[#662](https://github.com/pgplex/pgschema/pull/662) now preserves
`MATCH FULL` on foreign keys upstream. That clause is separate from this
benchmark: pg-delta already replays it through verbatim
`pg_get_constraintdef` text.

The solved verdict stays in place:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains
  in the checked-in/live history
- `packages/pg-delta/src/plan/internal.ts` still refuses an export constraint
  fold when a same-table column or a same-table dependent is emitted after
  `CREATE TABLE` (lines 779-793)
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` remains
  the committed regression
- exact search for `pgschema#534` still returns no dedicated pg-toolbelt
  issue or PR. Closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546) remain the
  effective tracker
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) did not
  update. Its `internal.ts` edit is still absent from the checked-in head

Benchmark 025 therefore stays **Solved in pg-delta**.

## Refresh note (2026-10-26)

This recheck leaves both checked-in heads unchanged: `pg-delta` at
`6b82eff84dba925a176f0c6a78e5a16843885366` and `pgschema` at
`24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`.

The solved verdict stays in place:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains
  in the checked-in/live history
- `packages/pg-delta/src/plan/internal.ts` still refuses an export constraint
  fold when a same-table column or a same-table dependent is emitted after
  `CREATE TABLE` (lines 779-793)
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` remains
  the committed regression
- exact search for `pgschema#534` still returns no dedicated pg-toolbelt
  issue or PR. Closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546) remain the
  effective tracker
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) also
  edits `internal.ts`, but only to skip same-schema renames when building
  the alterer index. That edit is not in the checked-in head, and the merge
  of `main` at `a638ed1` does not touch the fold guard

Benchmark 025 therefore stays **Solved in pg-delta**.

## Refresh note (2026-10-25)

This recheck leaves both checked-in heads unchanged: `pg-delta` at
`6b82eff84dba925a176f0c6a78e5a16843885366` and `pgschema` at
`24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`.

The solved verdict stays in place:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains
  in the checked-in/live history
- `packages/pg-delta/src/plan/internal.ts` still refuses an export constraint
  fold when a same-table column or a same-table dependent is emitted after
  `CREATE TABLE` (lines 779-793)
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` remains
  the committed regression
- exact search for `pgschema#534` still returns no dedicated pg-toolbelt
  issue or PR. Closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546) remain the
  effective tracker

Benchmark 025 therefore stays **Solved in pg-delta**.

## Refresh note (2026-10-24)

This recheck advances checked-in/live `pg-delta` from
`265af521e462577886ea6fdbb5777e1a23811cce` to
`6b82eff84dba925a176f0c6a78e5a16843885366` through merged PR
[#559](https://github.com/supabase/pg-toolbelt/pull/559), while
checked-in/live `pgschema` stays at
`24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. That commit only edits
`.github/CODEOWNERS`, so `packages/pg-delta` is unchanged.

The solved verdict stays in place:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains
  in the checked-in/live history
- `packages/pg-delta/src/plan/internal.ts` still refuses an export constraint
  fold when a same-table column or a same-table dependent is emitted after
  `CREATE TABLE` (lines 779-793)
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` remains
  the committed regression
- exact search for `pgschema#534` still returns no dedicated pg-toolbelt
  issue or PR. Closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546) remain the
  effective tracker

Benchmark 025 therefore stays **Solved in pg-delta**.

## Refresh note (2026-10-23)

This recheck advances checked-in/live `pg-delta` from
`63b3f653d99f936fa40c5a7689d771e829f09f45` to
`265af521e462577886ea6fdbb5777e1a23811cce`, while checked-in/live `pgschema`
stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`.

The solved verdict stays in place:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains
  in the checked-in/live history
- `packages/pg-delta/src/plan/internal.ts` still refuses an export constraint
  fold when a same-table column or a same-table dependent (including the
  unique index a self-referencing FK targets) is emitted after `CREATE TABLE`
- merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) adds a
  neighboring veto for a predecessor that itself needs the fold target, such
  as a `CHECK` calling a function over the table's row type. That veto sits
  beside the same-table guard and does not reopen this benchmark
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` remains
  the committed regression for the exact export-reload scenario

Benchmark 025 therefore stays **Solved in pg-delta**.

## Refresh note (2026-10-21)

This recheck advances checked-in/live `pg-delta` from
`7931d4167c18c9d849a4ea5737dfcc13f09e36aa` to `72e47ea0d5c33bd28c2beef0486126f5c63f44d3` through merged PRs
[#546](https://github.com/supabase/pg-toolbelt/pull/546),
[#549](https://github.com/supabase/pg-toolbelt/pull/549), and
[#552](https://github.com/supabase/pg-toolbelt/pull/552), while
checked-in/live `pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`.

Today's upstream activity closes this exact export parity gap on the
checked-in/live head:

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-20'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-20'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-20'`
  returned `[]`
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-20'`
  surfaced merged PRs [#546](https://github.com/supabase/pg-toolbelt/pull/546),
  [#549](https://github.com/supabase/pg-toolbelt/pull/549), and
  [#552](https://github.com/supabase/pg-toolbelt/pull/552); PR #546 is the
  benchmark-relevant change here
- PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) closes issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) and is now in the
  checked-in/live head; it updates
  `packages/pg-delta/src/plan/internal.ts` so export-time compaction refuses
  to inline a same-table constraint when one of its dependencies is emitted
  after `CREATE TABLE`
- `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` now covers
  export -> reload -> `rootHash` for the exact self-referencing non-PK
  UNIQUE-key case, and
  `packages/declarative-e2e/scenarios/self-fk-on-unique-index/` now exercises
  the same shape through the declarative-e2e harness
- merged PR [#549](https://github.com/supabase/pg-toolbelt/pull/549) and
  merged PR [#552](https://github.com/supabase/pg-toolbelt/pull/552) are
  adjacent global-state / harness work; they do not change this benchmark's
  verdict
- exact `pgschema#534` text search still returns no dedicated pg-toolbelt issue
  or PR, but the exact tracker history is now closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546)

Benchmark 025 therefore now moves to **Solved in pg-delta** on the
checked-in/live head. The historical notes below are retained as the record of
when this slice was still tracked.

## Refresh note (2026-10-20)

This recheck advances checked-in/live `pg-delta` from
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` to `7931d4167c18c9d849a4ea5737dfcc13f09e36aa` through merged PR
[#541](https://github.com/supabase/pg-toolbelt/pull/541), while
checked-in/live `pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`.

Today's upstream activity sharpens the tracker picture for this active export
parity gap without yet closing it on the checked-in/live head:

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-19'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-19'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-19'`
  returned `[]`
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-19'`
  surfaced the exact tracker issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543), while
  `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-19'`
  surfaced the exact fix PR [#546](https://github.com/supabase/pg-toolbelt/pull/546)
- PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) is not in the
  checked-in/live head yet; it patches
  `packages/pg-delta/src/plan/internal.ts` and adds
  `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts`, but the
  current checked-in/live source still keeps the failing export shape
- `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
  still treats a genuine self-reference as safe to keep inline:
  `cyclicForeignKeys()` explicitly skips self-referencing FKs and only splits
  multi-table cycles into sibling `.fk.sql` files
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts` and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/internal.ts` still make
  validated FOREIGN KEY constraints eligible for export-only inline folding on
  the checked-in/live head
- `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-reorder-on-failure.test.ts`
  still confirms the loader cannot repair same-file ordering hazards:
  `loadOrder cannot fix same-file order - edit or split the file.`
- pg-toolbelt issue [#544](https://github.com/supabase/pg-toolbelt/issues/544)
  remains a separate unmatched CHECK-constraint normalization bug, not a fix or
  duplicate for this benchmark

Benchmark 025 therefore remains **tracked** rather than solved: the exact
pg-toolbelt issue and fix PR now exist, but they have not landed in the
checked-in/live head yet.

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

**Actual on current pg-delta:** this exact scenario now converges. Merged PR
[#546](https://github.com/supabase/pg-toolbelt/pull/546) keeps the
self-referencing non-PK UNIQUE-key FK out of the exported `CREATE TABLE` until
its same-table unique index exists, and the committed regression
`packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` now round-
trips the export -> reload -> hash-compare path for this SQL.

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
| Self-referencing FK to the table PK | Yes - current export still allows the safe PK-target slice to stay inline |
| Self-referencing FK to a non-PK UNIQUE constraint or unique index | Yes - merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) keeps this FK out of `CREATE TABLE` when its same-table dependency is emitted later |
| Same-file loader recovery once the FK and unique index land in one file | Still no - current load-assist still cannot repair same-file order, but the export no longer relies on that fallback for this benchmark |
| Exact committed pg-delta regression for this scenario | Yes - `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` plus the declarative-e2e `self-fk-on-unique-index` scenario |
| Existing pg-toolbelt tracker | Yes - closed issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) are now in the checked-in/live head |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Key export decision** | Distinguishes self-ref-to-PK from self-ref-to-non-PK UNIQUE and defers the latter | Current checked-in/live export now also refuses to inline the same-table non-PK UNIQUE-key slice when the dependency emits after `CREATE TABLE` |
| **Self-referencing FK to PK** | Inline | Inline |
| **Self-referencing FK to non-PK UNIQUE key** | Deferred until after the backing UNIQUE object exists | Deferred on the current checked-in/live head |
| **Current parity state** | Fixed | Covered |

## Plan to handle it in pg-delta

1. No additional engine change is currently required for the exact
   self-referencing non-PK UNIQUE-key export slice on the checked-in/live head.
2. Retain `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts`
   and the declarative-e2e `self-fk-on-unique-index` scenario as regression
   coverage for future export compaction refactors.
3. If a future export/planner change touches same-table dependency checks,
   rerun this benchmark before altering the fold rules or relaxing the current
   regression coverage.
