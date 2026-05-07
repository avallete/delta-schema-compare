# Table constraint `UNIQUE NULLS NOT DISTINCT`

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed),
> fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE` constraints declared with
`NULLS NOT DISTINCT` were dumped without the modifier. That silently weakens the
constraint semantics on PostgreSQL 15+: rows that should conflict because their
NULL-bearing keys are considered equal become insertable again.

pgschema fixed this in PR #413 by reading the PostgreSQL 15+
`NULLS NOT DISTINCT` catalog bit through a version-safe `to_jsonb(...)`
extraction path and re-emitting the modifier in table-constraint DDL.

pg-delta already covers the **index-shaped** form of this feature through
benchmark item 016 / pg-toolbelt [#183](https://github.com/supabase/pg-toolbelt/issues/183)
and [#185](https://github.com/supabase/pg-toolbelt/pull/185), but table
constraints take a different implementation path. They are extracted into
`TableConstraintProps` in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
and compared in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`.
Current pg-delta stores the rendered constraint `definition`, but it does not
surface a dedicated `nulls_not_distinct` field for table constraints and the
table diff does not compare the rendered `definition` when deciding whether a
named UNIQUE constraint changed. As a result, a transition between
`UNIQUE (...)` and `UNIQUE NULLS NOT DISTINCT (...)` on the same named
constraint can remain invisible even though the NULL semantics differ.

## Reproduction SQL

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.accounts (
  a integer,
  b integer,
  CONSTRAINT accounts_ab_key UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.accounts DROP CONSTRAINT accounts_ab_key;
ALTER TABLE test_schema.accounts
  ADD CONSTRAINT accounts_ab_key
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the semantic change and emits the required
drop/recreate flow preserving `NULLS NOT DISTINCT`.

**Actual:** current table-constraint diff compares structured fields such as
`constraint_type`, `key_columns`, `deferrable`, `initially_deferred`,
`validated`, `no_inherit`, and `is_temporal`, but it has no table-constraint
`nulls_not_distinct` property and it does not compare the rendered
`definition`. A named UNIQUE constraint with the same key columns can therefore
be treated as unchanged even though its NULL semantics differ.

## How pgschema handled it

pgschema PR #413 adds support for table-level `UNIQUE NULLS NOT DISTINCT` by
extracting the PostgreSQL 15+ flag in a backward-compatible way and re-emitting
the modifier during dump/plan/apply. The merged PR text uses the concrete
example:

```sql
CREATE TABLE t (
  a int,
  b int,
  CONSTRAINT t_uniq UNIQUE NULLS NOT DISTINCT (a, b)
);
```

and fixes the previous incorrect output that downgraded it to plain
`UNIQUE (a, b)`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table-constraint create SQL preserves captured definition | ✅ `AlterTableAddConstraint` reuses `constraint.definition` from `pg_get_constraintdef(...)` |
| Dedicated table-constraint `nulls_not_distinct` field | ❌ Missing from `src/core/objects/table/table.model.ts` |
| Diff detects plain UNIQUE ↔ `NULLS NOT DISTINCT` transition | ❌ `src/core/objects/table/table.diff.ts` does not compare `definition` or any equivalent flag |
| Integration test for table-constraint `NULLS NOT DISTINCT` | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact table-constraint scenario | ❌ None found; index-only issue `#183` / PR `#185` are related but not duplicates |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads the table-constraint flag from PostgreSQL 15+ metadata with a version-safe fallback | Extracts the rendered constraint definition, but not a first-class `nulls_not_distinct` property |
| **Diff behavior** | Preserves the modifier in emitted table-constraint DDL | Can miss transitions when the constraint name and key columns stay the same |
| **Existing coverage** | Fixed by merged PR #413 | Only the index-form variant is covered today |
| **Duplicate risk** | Distinct from index support | Must be tracked separately from index issue #183 / PR #185 |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so table constraints expose a first-class `nulls_not_distinct` property (or
   another equally explicit signal) in addition to the rendered `definition`.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `UNIQUE (...)` and `UNIQUE NULLS NOT DISTINCT (...)` are treated as a
   drop/recreate change when the same named constraint exists on both sides.
3. Add focused integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for both:
   - creating a table constraint with `NULLS NOT DISTINCT`, and
   - converting an existing named UNIQUE constraint to `NULLS NOT DISTINCT`.
4. Keep the table-constraint case distinct from the already-solved unique-index
   case so future issue triage does not treat pg-toolbelt #183 / #185 as a
   duplicate fix.
