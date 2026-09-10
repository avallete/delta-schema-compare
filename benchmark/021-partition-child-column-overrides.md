# Partition child column overrides in `PARTITION OF` create path

> pgschema issue [#499](https://github.com/pgplex/pgschema/issues/499) (closed), fixed by [pgschema#500](https://github.com/pgplex/pgschema/pull/500)

## Context

pgschema issue #499 is the follow-up to the earlier partition-child create-
path bug from issue #496. After pgschema learned to emit
`CREATE TABLE ... PARTITION OF ... FOR VALUES ...` for new partition
children, it still omitted the optional typed table element list that
PostgreSQL allows on partition children for per-child column overrides.

That remaining slice matters when a partition child needs metadata that
differs from its parent, such as a child-specific `DEFAULT` or `NOT NULL`.
In the upstream fix, pgschema only needed `DEFAULT` and `NOT NULL`
overrides, but the gap is still real for pg-delta because the current plan
rule emits only the bare `PARTITION OF ... <bound>` form.

## Refresh note (2026-09-10)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main`
still at `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, and keeps
checked-in/live `pgschema` at `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`.

Open pg-toolbelt PR [#470](https://github.com/supabase/pg-toolbelt/pull/470)
now touches partition extraction/planning, but the active child-override gap
remains open:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
  `COLUMNS_SQL` gated by `a.attislocal`, so child-local overrides on inherited
  partition columns remain absent from diff-visible facts.
- open PR [#470](https://github.com/supabase/pg-toolbelt/pull/470) improves
  attached child-index extraction and `PARTITION OF` ordering, but its current
  `tables.ts` branch still emits `CREATE TABLE ... PARTITION OF ... ${bound}`
  with no typed child column-element list for local `DEFAULT` / `NOT NULL`
  overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and there is still no dedicated exact pg-toolbelt issue or PR
for `pgschema#499`. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332), unrelated open
issue [#451](https://github.com/supabase/pg-toolbelt/issues/451), and open PR
[#470](https://github.com/supabase/pg-toolbelt/pull/470) remain only adjacent
tracker context. Benchmark 021 therefore remains **behaviorally uncovered**
with **in-progress but non-exact tracker context**.

## Refresh note (2026-09-09)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main` at
`ce61f01c24962fe21b9d02b319d8c26be0b5fd13` through merged PRs
[#460](https://github.com/supabase/pg-toolbelt/pull/460),
[#461](https://github.com/supabase/pg-toolbelt/pull/461),
[#462](https://github.com/supabase/pg-toolbelt/pull/462),
[#464](https://github.com/supabase/pg-toolbelt/pull/464),
[#467](https://github.com/supabase/pg-toolbelt/pull/467), and
[#469](https://github.com/supabase/pg-toolbelt/pull/469), and advances
checked-in/live `pgschema` from
`b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd` to
`738a3bb40cf6b062928eeb564e3a98ec7f3c6989` through merged PRs
[#585](https://github.com/pgplex/pgschema/pull/585),
[#586](https://github.com/pgplex/pgschema/pull/586),
[#587](https://github.com/pgplex/pgschema/pull/587), and
[#590](https://github.com/pgplex/pgschema/pull/590).

Today's upstream delta reshapes the watch list and promotes resolved
pgschema issue [#564](https://github.com/pgplex/pgschema/issues/564) into new
benchmark [024](024-pg18-not-null-validation.md), but it still does not touch
the active partition-child extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and direct exact searches for `pgschema#499`, `pgschema#564`,
and `pgschema#589` still return no dedicated pg-toolbelt issue or PR.
Umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
plus unrelated open issue [#451](https://github.com/supabase/pg-toolbelt/issues/451)
remain the only adjacent tracker context. Benchmark 021 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-08)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main` at
`a982dfab6a87fa97f47130a1754dbd48d69446ce` through merged PR
[#458](https://github.com/supabase/pg-toolbelt/pull/458), and advances
checked-in/live `pgschema` from `fe7c64bfa410e7f9e8235eae3b912eb163b255f4` to
`b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd` through merged PRs
[#582](https://github.com/pgplex/pgschema/pull/582) and
[#583](https://github.com/pgplex/pgschema/pull/583).

The new live pg-delta delta is adjacent rather than gap-closing: PR #458 only
guards checked-out clients from connection errors in apply/extract/load
callers, so the active partition-child extract / plan path is still unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

Today's pgschema delta is also outside the active partition-child path.
Merged PR [#582](https://github.com/pgplex/pgschema/pull/582) broadens the
already-covered multi-file ordering family around
[#580](https://github.com/pgplex/pgschema/issues/580), merged PR
[#583](https://github.com/pgplex/pgschema/pull/583) closes
[#559](https://github.com/pgplex/pgschema/issues/559) as config-data work
outside pg-delta's schema-diff scope, and new issue
[#584](https://github.com/pgplex/pgschema/issues/584) plus open PR
[#585](https://github.com/pgplex/pgschema/pull/585) remain embedded-plan
ergonomics rather than this benchmark.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and direct exact searches for `pgschema#499`, `pgschema#564`,
and `pgschema#584` still return no dedicated pg-toolbelt issue or PR. Umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus
unrelated open issue [#451](https://github.com/supabase/pg-toolbelt/issues/451)
remain the only adjacent tracker context. Benchmark 021 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-07)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `c6ed06f6fd5f1e36a00787b7034e35bda025e86b` to
`fe7c64bfa410e7f9e8235eae3b912eb163b255f4` through merged PR
[#581](https://github.com/pgplex/pgschema/pull/581).

Today's upstream delta is still outside the active partition-child path.
pgschema issues [#579](https://github.com/pgplex/pgschema/issues/579) and
[#580](https://github.com/pgplex/pgschema/issues/580) closed on 2026-09-07,
and follow-up PR [#582](https://github.com/pgplex/pgschema/pull/582) remains
open, but current pg-delta's partition-child extract / plan path is unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and direct exact searches for `pgschema#499`, `pgschema#579`,
and `pgschema#580` still return no dedicated pg-toolbelt issue or PR. Umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus
unrelated open issue [#451](https://github.com/supabase/pg-toolbelt/issues/451)
remain the only adjacent tracker context. Benchmark 021 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-06)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and keeps checked-in/live `pgschema` at
`c6ed06f6fd5f1e36a00787b7034e35bda025e86b`.

No upstream code, issue, or PR delta landed since the 2026-09-05 refresh:
`gh issue list` / `gh pr list` updated-since checks returned empty arrays for
both `pgplex/pgschema` and `supabase/pg-toolbelt`, so the active
partition-child extract / plan path remains unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and exact duplicate searches for `pgschema#499` still return no
dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus unrelated open
issue [#451](https://github.com/supabase/pg-toolbelt/issues/451) remain the
only adjacent tracker context. Benchmark 021 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-05)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `89265906bd4d1a5c65971529989a81eb8b159d96` to
`c6ed06f6fd5f1e36a00787b7034e35bda025e86b` through merged PR
[#578](https://github.com/pgplex/pgschema/pull/578).

The upstream delta since the 2026-09-04 refresh is still on the pgschema side
only. It is the ownership-only follow-up in the already-resolved
[#573](https://github.com/pgplex/pgschema/issues/573) sequence family and does
not touch the active partition-child extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and the proof loop still returned `proofOk: true` with zero
drift after omitting them. Direct exact searches for `pgschema#499` still
return no dedicated pg-toolbelt issue or PR, while keyword duplicate searches
for `PARTITION OF` still surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus unrelated open
issue [#451](https://github.com/supabase/pg-toolbelt/issues/451). Benchmark 021
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-09-04)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` to
`89265906bd4d1a5c65971529989a81eb8b159d96` through merged PR
[#577](https://github.com/pgplex/pgschema/pull/577).

The upstream delta since the 2026-09-03 refresh is on the pgschema side only.
It fixes sequence ownership / SERIAL collapsing for issues
[#573](https://github.com/pgplex/pgschema/issues/573),
[#574](https://github.com/pgplex/pgschema/issues/574), and
[#576](https://github.com/pgplex/pgschema/issues/576), and does not touch the
active partition-child extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and the proof loop still returned `proofOk: true` with zero
drift after omitting them. Direct exact searches for `pgschema#499` still
return no dedicated pg-toolbelt issue or PR, while keyword duplicate searches
for `PARTITION OF` still surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus unrelated open
issue [#451](https://github.com/supabase/pg-toolbelt/issues/451). Benchmark 021
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-09-03)

This recheck advances checked-in/live `pg-delta` from
`107ac3df4b889c527215d1f6a37df64b33154c16`
(`@supabase/pg-delta@1.0.0-alpha.48`) to
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) through merged PR
[#455](https://github.com/supabase/pg-toolbelt/pull/455) and release
[#457](https://github.com/supabase/pg-toolbelt/pull/457), and advances
checked-in/live `pgschema` from
`97d8d60dd72a46704cc63b71b63aab2784847658`
(`v1.12.5`) to `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` through merged PR
[#572](https://github.com/pgplex/pgschema/pull/572).

The new pg-delta delta only touches `packages/pg-delta/src/plan/internal.ts`
plus enum/default ordering tests and corpus fixtures, while the new pgschema
delta only touches quoted-identifier dependency detection for issue
[#571](https://github.com/pgplex/pgschema/issues/571). The active
partition-child extract / plan path is unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The last focused 2026-08-14 runtime observation therefore still stands and
emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, and the proof loop still returned `proofOk: true` with zero
drift after omitting them. Direct exact searches for `pgschema#499` still
return no dedicated pg-toolbelt issue or PR, while keyword duplicate searches
for `PARTITION OF` still surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus unrelated open
issue [#451](https://github.com/supabase/pg-toolbelt/issues/451). Benchmark 021
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-08-31)

This recheck keeps checked-in/live `pg-delta` at
`107ac3df4b889c527215d1f6a37df64b33154c16`
(`@supabase/pg-delta@1.0.0-alpha.48`) and advances checked-in/live
`pgschema` to `97d8d60dd72a46704cc63b71b63aab2784847658`
(`v1.12.5`) through merged PRs
[#565](https://github.com/pgplex/pgschema/pull/565),
[#566](https://github.com/pgplex/pgschema/pull/566),
[#567](https://github.com/pgplex/pgschema/pull/567), and
[#568](https://github.com/pgplex/pgschema/pull/568).

A source recheck on the current pg-delta head still finds the same uncovered
path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

The upstream delta since the 2026-08-30 refresh is on the pgschema side rather
than the pg-delta side. Those new pgschema changes land in online rewrite,
constraint-validation, docs, and release surfaces, not in the current
partition-child extract / plan codepaths above, so the last focused 2026-08-14
runtime observation still stands and emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted. More importantly, the current proof loop still returned
`proofOk: true` with zero drift after omitting them, which means the new
engine is not surfacing those child-local overrides as diff-visible state
end-to-end yet.

There is still no dedicated exact pg-toolbelt issue or PR for this scenario on
2026-08-31. Direct exact searches for `pgschema#499` still return nothing, and
keyword duplicate searches for `PARTITION OF` now surface umbrella fidelity
tracker [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus
unrelated open issue [#451](https://github.com/supabase/pg-toolbelt/issues/451).
Comments on the open #332 thread (not the original issue body) still carry the
inherited-column local-override note. Benchmark 021 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.orders (
    id bigint NOT NULL,
    region text NOT NULL,
    priority integer DEFAULT 0,
    notes text
) PARTITION BY LIST (region);

CREATE TABLE test_schema.orders_eu PARTITION OF test_schema.orders
FOR VALUES IN ('eu');
```

**Change to diff:**

```sql
CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders (
    priority DEFAULT 10,
    notes NOT NULL
) FOR VALUES IN ('us');
```

**Expected:** pg-delta emits either the inline `PARTITION OF (...)` element
list or equivalent follow-up DDL that converges to the same catalog state,
preserving the child-specific `priority DEFAULT 10` and `notes NOT NULL`
overrides.

**Actual on current pg-delta:** current pg-delta emits only the bare
`CREATE TABLE ... PARTITION OF ... FOR VALUES ...` statement and drops the
child-specific column overrides entirely. The focused 2026-08-14 proof also
reported zero drift afterward, which indicates the current model/proof path
is not surfacing the missing child-local overrides as a mismatch yet.

## How pgschema handled it

pgschema fixed the issue in PR #500 by comparing child columns to the
parent table during partition-child creation and emitting per-child
`DEFAULT` and `NOT NULL` overrides inside the `PARTITION OF (...)` element
list when they differ from the inherited parent definition.

The merged fix added regression data under:

- `repos/pgschema/testdata/diff/create_table/issue_499_partition_column_overrides/`

## Current pg-delta status

| Aspect | Status |
|---|---|
| Base `PARTITION OF ... FOR VALUES ...` create support | Yes - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` emits the partition-child create statement |
| Typed table-element list for partition children | No - the partition-child create path in `src/plan/rules/tables.ts` hard-codes `CREATE TABLE ... PARTITION OF ... ${bound}` and never serializes the child element list |
| Child-local `DEFAULT` / `NOT NULL` overrides survive the current extract + diff + proof path | No - `extract/relations.ts` still filters inherited child columns with `a.attislocal`, and the focused 2026-08-14 probe omitted the overrides yet still produced `proofOk: true` |
| Existing exact pg-toolbelt issue / PR | No dedicated exact tracker or PR yet; keyword duplicate searches only surface umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332), and comments on that issue thread now carry the inherited-column local-override note |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Partition-child create path** | Emits `PARTITION OF ... FOR VALUES ...` | Emits `PARTITION OF ... FOR VALUES ...` |
| **Per-child column overrides** | Compares child columns to parent and emits `DEFAULT` / `NOT NULL` overrides | Drops the overrides on create and does not surface the loss as proof drift yet |
| **Current parity state** | Fixed | Only umbrella-thread context under [#332](https://github.com/supabase/pg-toolbelt/issues/332); still behaviorally uncovered |

## Plan to handle it in pg-delta

1. Extend the current fact/extract path so child-local partition overrides
   are preserved as diff-visible desired state.
2. Update `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
   so partition children can serialize PostgreSQL's typed table element
   list before `FOR VALUES ...` when child columns differ from the parent.
3. If some child-local properties cannot be expressed inline, emit
   equivalent immediate follow-up column alters after `CreateTable`.
4. Add a focused regression under `packages/pg-delta/tests/` for a child
   partition with `DEFAULT` and `NOT NULL` overrides, and make sure the
   proof loop fails until those overrides are preserved end-to-end.
