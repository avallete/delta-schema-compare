# Parity issue drafts (2026-05-03)

This document records draft tracker issue text for parity gaps confirmed in
the 2026-05-03 refresh that do not yet have a matching pg-toolbelt issue.

## Draft 1 - pgschema #412 (table-level `UNIQUE NULLS NOT DISTINCT`)

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

### Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were being rendered without the `NULLS NOT DISTINCT` modifier.
pgschema fixed this in PR #413 and now has both dump and diff fixtures for
the constraint variant.

In pg-delta, the standalone index form is already covered by the work for
pgschema #355 / pg-toolbelt #183. The table-constraint variant is still a
gap: table constraint extraction stores the rendered definition, but
`src/core/objects/table/table.diff.ts` does not compare `definition` or a
dedicated constraint-level `nulls_not_distinct` field. The index diff path
cannot rescue this case because `src/core/objects/index/index.diff.ts`
intentionally skips constraint-owned indexes.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
  a integer,
  b integer,
  CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.pgschema_repro_nulls
  DROP CONSTRAINT pgschema_repro_nulls_uniq;

ALTER TABLE test_schema.pgschema_repro_nulls
  ADD CONSTRAINT pgschema_repro_nulls_uniq
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the semantic change and emits a drop / add
flow that preserves `NULLS NOT DISTINCT`.

**Actual:** current table-constraint diffing can treat the change as
unchanged because the same named constraint keeps the same type and key
columns while the rendered definition is not compared.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   to detect `UNIQUE` vs `UNIQUE NULLS NOT DISTINCT` changes. Either:
   - add an explicit constraint-level `nulls_not_distinct` property, or
   - compare the canonical `definition` for unique constraints.
2. Add PG15+ integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - creating a table-level `UNIQUE NULLS NOT DISTINCT` constraint, and
   - toggling a same-named constraint between plain unique and
     `NULLS NOT DISTINCT`.
3. Add focused unit coverage showing this semantic diff must live in the
   table-constraint path, since `index.diff.ts` intentionally skips
   constraint-owned indexes.
