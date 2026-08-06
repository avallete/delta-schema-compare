# Partition child column overrides in `PARTITION OF` create path

> pgschema issue [#499](https://github.com/pgplex/pgschema/issues/499) (closed), fixed by [pgschema#500](https://github.com/pgplex/pgschema/pull/500)

## Context

pgschema issue #499 is the follow-up to the earlier partition-child create-path
bug from issue #496. After pgschema learned to emit
`CREATE TABLE ... PARTITION OF ... FOR VALUES ...` for new partition children,
it still omitted the optional typed table element list that PostgreSQL allows on
partition children for per-child column overrides.

That remaining slice matters when a partition child needs metadata that differs
from its parent, such as a child-specific `DEFAULT` or `NOT NULL`. In the
upstream fix, pgschema only needed `DEFAULT` and `NOT NULL` overrides, but the
gap is still real for pg-delta because the current serializer returns early for
partition children and emits only the bare `PARTITION OF ... <bound>` form.

Current pg-delta already covers the base attach path from pgschema #496, so
this benchmark is intentionally narrower. The missing behavior is not partition
creation itself; it is preserving child-specific column overrides when a new
partition child is created.

## Refresh note (2026-08-06)

This refresh advanced the checked-in `pg-delta` baseline from
`a974b83fc044788caa4ca538d112b62d1873843b` to
`2929e83981fee139772cc1c60255f1b2592a6f3a`, matching live
`pg-toolbelt/main`; `pgschema` remained at
`b1d60e8d95cfc95508956e4c1e89572269410501`.

The new upstream pgschema activity is a newly opened ordering issue,
[#530](https://github.com/pgplex/pgschema/issues/530), with open fix PR
[#531](https://github.com/pgplex/pgschema/pull/531), plus the newly closed
long-enum issue [#528](https://github.com/pgplex/pgschema/issues/528). Current
pg-delta already covers both of those scenarios, so they do not change this
benchmark's classification. A focused 2026-08-06 pg17 runtime probe for this
benchmark still emitted only:

```sql
CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, so the partition-child override gap remains unresolved. Direct
duplicate searches still found no exact pg-toolbelt issue or PR for this narrow
case, so benchmark 021 remains **Not covered**.

## Refresh note (2026-08-05)

This refresh advanced checked-in `pgschema` from
`325dac205047a7850a52ee9f9ff35ec18c145dcc` to
`b1d60e8d95cfc95508956e4c1e89572269410501` via merged
[pgschema#529](https://github.com/pgplex/pgschema/pull/529), while checked-in
`pg-delta` remained `a974b83fc044788caa4ca538d112b62d1873843b` and live
`pg-toolbelt/main` remained `2929e83981fee139772cc1c60255f1b2592a6f3a`.

The new upstream pgschema delta is the function `SET`-clause fix for issue
[#526](https://github.com/pgplex/pgschema/issues/526), which is already
covered in pg-delta rather than a new parity gap. A focused 2026-08-05 pg17
runtime probe for this benchmark still emitted only:

```sql
CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, so the partition-child override gap remains unresolved. Direct
duplicate searches still found no exact pg-toolbelt issue or PR for this narrow
case, so benchmark 021 remains **Not covered**.

## Refresh note (2026-08-04)

This refresh kept the checked-in `pg-delta` baseline at
`a974b83fc044788caa4ca538d112b62d1873843b` while live
`pg-toolbelt/main` advanced to `2929e83981fee139772cc1c60255f1b2592a6f3a`;
`pgschema` remained at `325dac205047a7850a52ee9f9ff35ec18c145dcc`.

The new live pg-delta delta is the alpha.5 `pg-topo` byte-offset parser fix
from [pg-toolbelt#372](https://github.com/supabase/pg-toolbelt/pull/372),
released by [pg-toolbelt#374](https://github.com/supabase/pg-toolbelt/pull/374).
A focused live pg17 plan probe still emitted only:

```sql
CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides were
still omitted, so the partition-child override gap remains unresolved. Direct
duplicate searches still found no exact pg-toolbelt issue or PR for this narrow
case, so benchmark 021 remains **Not covered**.

## Refresh note (2026-07-18)

This refresh advanced the checked-in `pg-delta` baseline from
`ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` to
`c0decd173d191bc470bf7b8c8dd3e862f08ae398`, while `pgschema` remained at
`e18d9ede7973537919c02f25eced5c97271af1dc`.

The new pg-delta delta is the alpha.32 non-superuser extraction fix, so it
does not touch `table.create.ts` or the partition-child create path behind this
benchmark. Targeted duplicate searches still found no exact pg-toolbelt issue
or PR for this narrow partition-child override case, so benchmark 021 remains
**Not covered**.

## Refresh note (2026-07-08)

This refresh advanced both checked-in submodules:

- `pg-delta` from `9284412d71635308ebb0c1537e0b0183d2cfa4da` to
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- `pgschema` from `62d09975eaac726f055aa62a5baa2961ef7e5a83` to
  `e18d9ede7973537919c02f25eced5c97271af1dc`

The newer upstream pgschema head merges follow-up fixes for issues #505, #506,
#508, and #509 and closes issue #506 via
[pgschema#507](https://github.com/pgplex/pgschema/pull/507), but none of that
changes this exact partition-child column-override gap.

During this refresh, a focused local `CreateTable` probe against the new
pg-delta head still emitted:

```sql
CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')
```

The child-specific overrides were omitted entirely, so this scenario remains
not covered. There is still no exact pg-toolbelt issue or PR for this narrow
partition-child override case.

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

**Expected:** pg-delta emits either the inline `PARTITION OF (...)` element list
or equivalent follow-up DDL that converges to the same catalog state, preserving
the child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides.

**Actual:** current pg-delta emits only the bare
`CREATE TABLE ... PARTITION OF ... FOR VALUES ...` statement and drops the
child-specific column overrides entirely.

## How pgschema handled it

pgschema fixed the issue in PR #500 by comparing child columns to the parent
table during partition-child creation and emitting per-child `DEFAULT` and
`NOT NULL` overrides inside the `PARTITION OF (...)` element list when they
differ from the inherited parent definition.

The merged fix added regression data under:

- `repos/pgschema/testdata/diff/create_table/issue_499_partition_column_overrides/`

It also updated the diff path so the parent table can be looked up from the
full target IR, not just the current creation batch, which lets the fix work
for incremental "add one new child partition" plans.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Base `PARTITION OF ... FOR VALUES ...` create support | Yes - covered in `src/core/objects/table/changes/table.create.ts` and integration tests |
| Child-specific `DEFAULT` / `NOT NULL` overrides on partition children | No - the serializer returns early for partition children before column metadata is emitted |
| Follow-up column alters for created partition children | No - `table.diff.ts` adds constraints/comments/privileges on create, but no column override recovery path |
| Integration regression for child partition column overrides | No - no roundtrip test covers `PARTITION OF (...)` typed table elements |
| Existing exact pg-toolbelt issue / PR | No - none found through the 2026-07-18 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Partition-child create path** | Emits `PARTITION OF ... FOR VALUES ...` | Emits `PARTITION OF ... FOR VALUES ...` |
| **Per-child column overrides** | Compares child columns to parent and emits `DEFAULT` / `NOT NULL` overrides | Drops overrides by returning early for partition children |
| **Coverage** | Regression fixture for incremental partition-child creation | No exact integration regression |
| **Current parity state** | Fixed | Not covered |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.create.ts`
   so partition children can optionally serialize PostgreSQL's typed table
   element list before `FOR VALUES ...` when child columns differ from the
   parent.
2. Teach the create path which child column properties are safely expressible in
   that element list, starting with `DEFAULT` and `NOT NULL`.
3. If inline serialization is too invasive for some properties, teach the
   created-table branch in
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   to emit equivalent follow-up column alters immediately after `CreateTable`
   where PostgreSQL supports them.
4. Add focused roundtrip coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/partitioned-table-operations.test.ts`
   for a child partition with `DEFAULT` and `NOT NULL` overrides.
5. Decide separately whether identity, generated-expression, or other future
   child-specific column metadata should be handled in the same fix or tracked
   as follow-up scope.
