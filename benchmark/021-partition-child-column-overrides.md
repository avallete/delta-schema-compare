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

## Refresh note (2026-08-21)

This refresh advances checked-in/live `pg-delta` to
`18562f9a2eb01f181f1412dfeac1c1cea17ec579`, and advances checked-in/live
`pgschema` to `9c81d465d76c20588d670ede188c6939febdf3ac`.

A source recheck on the current pg-delta head still finds the same uncovered
path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  relation columns with `a.attislocal`, so child-local overrides on inherited
  partition columns never become diff-visible facts.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
  serializes partition-child creation as
  `CREATE TABLE ... PARTITION OF ... ${bound}` and has no branch that emits
  PostgreSQL's typed table element list for child-local overrides.

Nothing in the 2026-08-21 state changes the last focused 2026-08-14 runtime
observation, which still emitted only:

```sql
CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')
ALTER TABLE "test_schema"."orders_us" OWNER TO "test"
```

The child-specific `priority DEFAULT 10` and `notes NOT NULL` overrides
were still omitted. More importantly, the current proof loop still returned
`proofOk: true` with zero drift after omitting them, which means the new
engine is not surfacing those child-local overrides as diff-visible state
end-to-end yet.

There is still no dedicated exact pg-toolbelt issue or PR for this scenario on
2026-08-21. Direct exact searches for `pgschema#499` still return nothing, and
keyword duplicate searches still only surface umbrella fidelity tracker
[pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332) plus the
generic closed backlog issue
[#333](https://github.com/supabase/pg-toolbelt/issues/333) for the broad
`PARTITION OF` term. Comments on the open #332 thread (not the original issue
body) still carry the inherited-column local-override note. Benchmark 021
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

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
