# Parity issue drafts — 2026-05-16

This refresh did **not** produce any new draft issues for open pgschema
items, and the draft set is unchanged from the prior unmerged May refresh.
The only live open parity trackers remain:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

The draft below is still the one remaining **historical** gap that is
still missing from pg-toolbelt tracking.

## Draft — pg-delta: preserve `UNIQUE NULLS NOT DISTINCT` on table constraints (pgschema #412)

## Context

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were being dumped as plain `UNIQUE (...)`, silently dropping the
PostgreSQL 15+ modifier. pgschema fixed that in
[pgschema#413](https://github.com/pgplex/pgschema/pull/413).

Current pg-delta already covers the **index** variant of this feature
(`CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`) through
`packages/pg-delta/src/core/objects/index/` plus
`tests/integration/index-operations.test.ts`, but the **table-constraint** path
still does not model the modifier. In
`packages/pg-delta/src/core/objects/table/table.model.ts`, table constraints are
extracted with fields such as `deferrable`, `no_inherit`, `is_temporal`,
`key_columns`, and `definition`, but no `nulls_not_distinct` flag. In
`packages/pg-delta/src/core/objects/table/table.diff.ts`, the diff compares
those structured fields yet never compares the full rendered constraint
definition, so a same-name constraint changed from `UNIQUE (a, b)` to
`UNIQUE NULLS NOT DISTINCT (a, b)` can be treated as unchanged.

This matters because the modifier changes data semantics. Plain `UNIQUE`
treats `NULL` values as distinct; `UNIQUE NULLS NOT DISTINCT` makes `NULL`
values collide.

## Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.repro_nulls (
    a integer,
    b integer,
    CONSTRAINT repro_nulls_uniq UNIQUE (a, b)
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.repro_nulls
  DROP CONSTRAINT repro_nulls_uniq;

ALTER TABLE test_schema.repro_nulls
  ADD CONSTRAINT repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the semantic change and emits a drop / recreate
that preserves `NULLS NOT DISTINCT`.

**Actual:** pg-delta can preserve the clause on a pure add-constraint path
because `AlterTableAddConstraint` reuses `constraint.definition`, but it does
not model `NULLS NOT DISTINCT` as a first-class table-constraint property, so
same-name toggles can be diffed as unchanged.

## Suggested Fix

- Extend
  `packages/pg-delta/src/core/objects/table/table.model.ts`
  to read the PG15+ `indnullsnotdistinct` flag from the backing unique index
  referenced by `c.conindid`, using a PostgreSQL-version-safe `to_jsonb(...)`
  expression.
- Add the new field to `tableConstraintPropsSchema`.
- Update
  `packages/pg-delta/src/core/objects/table/table.diff.ts`
  so `UNIQUE` vs `UNIQUE NULLS NOT DISTINCT` becomes a semantic drop / recreate
  change.
- Add integration coverage in
  `packages/pg-delta/tests/integration/constraint-operations.test.ts`
  for both create-only and toggle scenarios.
