# Parity issue drafts (2026-04-30)

This document records the draft issue text prepared during the 2026-04-30
pgschema <-> pg-delta parity refresh.

## Duplicate-check summary (pg-toolbelt)

Before drafting, we checked existing pg-toolbelt issues and PRs for the
table-constraint variant of `NULLS NOT DISTINCT` using searches around:

- `NULLS NOT DISTINCT`
- `unique constraint`
- `table constraint`
- pgschema issue number `412`

Result at draft time: no matching pg-toolbelt issue or PR was found for
the table-level constraint variant. The closest existing work is the
already-solved standalone-index issue
[pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183) /
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185), which
does not cover `ALTER TABLE ... ADD CONSTRAINT ... UNIQUE NULLS NOT DISTINCT`.

---

## Draft 1 - pgschema #412 (`UNIQUE NULLS NOT DISTINCT` table constraints)

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

### Context

pgschema issue #412 describes table-level `UNIQUE` constraints declared as
`UNIQUE NULLS NOT DISTINCT (...)` being dumped as plain `UNIQUE`
constraints. That silently weakens uniqueness semantics on PostgreSQL 15+
for nullable columns.

In pg-delta, the table-constraint extractor already captures the full
constraint `definition` from `pg_get_constraintdef(c.oid, true)`, and
`AlterTableAddConstraint` reuses that definition when creating a
constraint. However, the table diff path in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
does not compare the captured definition or a dedicated
`nulls_not_distinct` property for table constraints. As a result,
`UNIQUE (a, b)` and `UNIQUE NULLS NOT DISTINCT (a, b)` look identical to
the diff whenever the constraint name and key columns are unchanged.

This is distinct from the already-fixed standalone-index case tracked by
pg-toolbelt #183 / #185.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;
CREATE TABLE test_schema.example (
  a integer,
  b integer
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.example
  ADD CONSTRAINT example_ab_key
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta preserves `NULLS NOT DISTINCT` when creating the
constraint, and if the same constraint is toggled from plain `UNIQUE` to
`UNIQUE NULLS NOT DISTINCT`, it emits a drop / recreate.

**Actual:** pg-delta can serialize the clause when creating the
constraint from scratch, but the table diff logic has no dedicated signal
for the property and does not compare the constraint definition, so the
transition is not reliably detected as a semantic change.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so `UNIQUE` table constraints expose a dedicated
   `nulls_not_distinct`-style property, or compare `definition` for
   `UNIQUE` constraints in a stable way.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `UNIQUE (...)` and `UNIQUE NULLS NOT DISTINCT (...)` are treated as
   a drop / recreate change when the constrained columns are otherwise
   identical.
3. Add integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - creating a table-level `UNIQUE NULLS NOT DISTINCT` constraint, and
   - toggling an existing `UNIQUE` constraint to `NULLS NOT DISTINCT`.
