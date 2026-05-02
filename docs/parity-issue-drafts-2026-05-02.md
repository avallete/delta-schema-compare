# Parity issue drafts (2026-05-02)

This document records the current draft text for parity scenarios discovered in
the 2026-05-02 refresh that are **not yet represented by an existing
pg-toolbelt issue or PR**.

At the time of this refresh:

- pgschema open issues #366 and #404 were already tracked by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219) and
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  respectively.
- Most historical benchmark items (005, 007, 008, 013, 015, 016, 017, 018,
  019) were solved in current pg-delta and therefore did **not** need new issue
  drafts.
- The only newly confirmed unresolved historical parity scenario was pgschema
  [#412](https://github.com/pgplex/pgschema/issues/412).

---

## Draft 1 — pgschema #412 (`UNIQUE NULLS NOT DISTINCT` table constraints)

Relates to pgschema issue #412:
https://github.com/pgplex/pgschema/issues/412

### Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were silently downgraded to plain `UNIQUE (...)` in dump/plan
output. pgschema fixed that in
[pgschema#413](https://github.com/pgplex/pgschema/pull/413).

pg-delta already handles the **index** form of this feature and has dedicated
integration coverage for `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT` via
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185). However,
the **table constraint** form is distinct: it is extracted through table
constraints, serialized through `ALTER TABLE ... ADD CONSTRAINT ...`, and
diffed by `src/core/objects/table/table.diff.ts`.

Current pg-delta evidence suggests:

- adding a brand-new `UNIQUE NULLS NOT DISTINCT` table constraint should work,
  because `AlterTableAddConstraint` serializes the captured
  `pg_get_constraintdef(...)` definition verbatim;
- but pg-delta does **not** currently compare the rendered constraint
  definition, and table-constraint diffs have no dedicated
  `nulls_not_distinct`-style field;
- therefore a transition between plain `UNIQUE (a, b)` and
  `UNIQUE NULLS NOT DISTINCT (a, b)` on the **same named table constraint**
  may be missed.

This is a meaningful parity gap because the modifier changes uniqueness
semantics for rows containing `NULL`.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.example (
  a integer,
  b integer,
  CONSTRAINT example_ab_key UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.example DROP CONSTRAINT example_ab_key;
ALTER TABLE test_schema.example
  ADD CONSTRAINT example_ab_key UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the constraint-definition change and emits a
drop/recreate preserving `NULLS NOT DISTINCT`.

**Actual (current parity evidence):**

- `table.model.ts` extracts `definition` via `pg_get_constraintdef(...)`, which
  can include `UNIQUE NULLS NOT DISTINCT (...)`;
- `AlterTableAddConstraint` reuses that definition verbatim;
- but `table.diff.ts` only compares structured scalar fields plus key-column
  arrays and does **not** compare the rendered `definition`, so an in-place
  `UNIQUE` → `UNIQUE NULLS NOT DISTINCT` transition is not explicitly covered.

### Suggested Fix

1. Add a roundtrip regression in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for table-level `UNIQUE NULLS NOT DISTINCT`.
2. Update `src/core/objects/table/table.diff.ts` so the table-constraint diff
   can detect this modifier change explicitly. Options:
   - compare `definition` for relevant constraint types, or
   - add an explicit `nulls_not_distinct` field to the table constraint model
     and compare it structurally.
3. Verify both add-create and toggle/recreate flows:
   - no constraint → `UNIQUE NULLS NOT DISTINCT`
   - `UNIQUE` → `UNIQUE NULLS NOT DISTINCT`
   - `UNIQUE NULLS NOT DISTINCT` → plain `UNIQUE`
