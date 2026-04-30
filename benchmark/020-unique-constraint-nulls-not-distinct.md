# Table-level `UNIQUE NULLS NOT DISTINCT` constraints

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE` constraints declared as
`UNIQUE NULLS NOT DISTINCT (...)` were dumped as plain `UNIQUE` constraints,
silently weakening their semantics. Unlike standalone unique indexes
(benchmark 016), this variant lives in the table-constraint path.

pgschema fixed this in PR #413 by preserving the `NULLS NOT DISTINCT` modifier
on `UNIQUE` table constraints during dump and diff output. In pg-delta, the
table constraint extractor already captures the full catalog definition via
`pg_get_constraintdef(c.oid, true)`, and `AlterTableAddConstraint` reuses that
definition when creating a constraint. However, `table.diff.ts` does not compare
either the captured definition or a dedicated `nulls_not_distinct`-style field
for table constraints. As a result, a plain `UNIQUE` constraint and a
`UNIQUE NULLS NOT DISTINCT` constraint look identical to the diff as long as the
constraint name and constrained columns are the same.

This matters because `NULLS NOT DISTINCT` changes real uniqueness behavior on
PostgreSQL 15+: multiple rows whose constrained columns are equal except for
`NULL` values should conflict instead of being treated as distinct. Missing the
modifier can allow data that the branch schema intended to reject.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.example (
    a integer,
    b integer
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.example
  ADD CONSTRAINT example_ab_key
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta either creates the constraint with `NULLS NOT DISTINCT`
or, when toggling an existing `UNIQUE` constraint, detects the semantic change
and emits a drop/recreate preserving the modifier.

**Actual:** pg-delta can serialize the clause when creating the constraint from
scratch because `constraint.definition` is reused, but it has no
table-constraint metadata or diff rule that distinguishes `UNIQUE (a, b)` from
`UNIQUE NULLS NOT DISTINCT (a, b)` once both constraints share the same name and
key columns.

## How pgschema handled it

pgschema PR #413 taught the dump / diff path to preserve
`UNIQUE NULLS NOT DISTINCT` on table constraints instead of normalizing it to a
plain `UNIQUE`. The merged PR adds regression coverage around the exact
constraint form reported in issue #412.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table constraint definition extracted from catalog | ✅ `src/core/objects/table/table.model.ts` captures `definition` via `pg_get_constraintdef(c.oid, true)` |
| Add-constraint SQL preserves captured definition | ✅ `src/core/objects/table/changes/table.alter.ts` reuses `constraint.definition` |
| Dedicated table-constraint field for `NULLS NOT DISTINCT` | ❌ Missing |
| Diff detects plain `UNIQUE` -> `UNIQUE NULLS NOT DISTINCT` transition | ❌ `src/core/objects/table/table.diff.ts` compares structured scalar fields and key columns only |
| Integration test for table-constraint `UNIQUE NULLS NOT DISTINCT` | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during review |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Affected path** | Table-constraint dump / plan output | Table-constraint catalog diffing |
| **Current fix** | Preserves `NULLS NOT DISTINCT` in PR #413 | Standalone index path is covered, but table-constraint diffing still lacks the property |
| **Why index coverage is not enough** | N/A | Benchmark 016 only covers standalone unique indexes, not `ALTER TABLE ... ADD CONSTRAINT ... UNIQUE NULLS NOT DISTINCT` |
| **Residual risk** | Addressed | High: semantic drift can go unnoticed when toggling uniqueness behavior on nullable columns |

## Plan to handle it in pg-delta

1. Extend `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so `UNIQUE` table constraints expose a dedicated `nulls_not_distinct`-style
   field, or compare the captured `definition` for `UNIQUE` constraints in a
   stable way.
2. Update `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `UNIQUE (...)` and `UNIQUE NULLS NOT DISTINCT (...)` are treated as a
   drop/recreate change when the constrained columns are otherwise identical.
3. Add integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - creating a table-level `UNIQUE NULLS NOT DISTINCT` constraint, and
   - toggling an existing `UNIQUE` constraint to `NULLS NOT DISTINCT`.
4. Once the behavior is implemented and covered, open a matching pg-toolbelt
   tracking issue using the draft in `docs/parity-issue-drafts-2026-04-30.md`
   if the gap is still untracked upstream.
