## pgschema #412 -> proposed pg-toolbelt issue draft

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were dumped without the `NULLS NOT DISTINCT` modifier. pgschema now
preserves this in both dump and diff output, but pg-delta still has a distinct
parity gap on the table-constraint path.

In pg-delta, `packages/pg-delta/src/core/objects/table/table.model.ts` captures
the full constraint `definition` via `pg_get_constraintdef(...)`, and
`AlterTableAddConstraint` in
`packages/pg-delta/src/core/objects/table/changes/table.alter.ts` serializes
that definition verbatim. The remaining problem is change detection:
`packages/pg-delta/src/core/objects/table/table.diff.ts` compares structured
fields such as `constraint_type`, `deferrable`, `is_temporal`, and
`key_columns`, but it does not compare either the full definition or a dedicated
`NULLS NOT DISTINCT` flag for named table constraints. A plain
`UNIQUE (a, b)` constraint and a `UNIQUE NULLS NOT DISTINCT (a, b)` constraint
with the same name therefore look unchanged.

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

## Test Case to Reproduce

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

**Expected:** pg-delta detects the modifier-only change and emits the
drop/recreate DDL preserving `UNIQUE NULLS NOT DISTINCT (a, b)`.
**Actual:** the current table-constraint diff path can treat both constraint
variants as equivalent because the comparator does not inspect the modifier.

## Suggested Fix

1. Add PostgreSQL 15+ integration coverage in:
   - `packages/pg-delta/tests/integration/constraint-operations.test.ts`
   Include both:
   - adding a table-level `UNIQUE NULLS NOT DISTINCT` constraint, and
   - toggling an existing named constraint from plain `UNIQUE` to
     `UNIQUE NULLS NOT DISTINCT`.
2. If the test fails, extend the table-constraint diff in:
   - `packages/pg-delta/src/core/objects/table/table.diff.ts`
   so modifier-only changes on named UNIQUE constraints trigger a drop/recreate.
3. Implementation options:
   - compare `constraint.definition` for relevant constraint types, or
   - add an explicit `nulls_not_distinct` field to the table-constraint model in
     `packages/pg-delta/src/core/objects/table/table.model.ts`
4. Keep using the current definition-based serializer in:
   - `packages/pg-delta/src/core/objects/table/changes/table.alter.ts`
   once the diff layer correctly recognizes the change.

## pgschema #412 -> proposed pg-toolbelt issue draft

## Context

pgschema issue #412 reports that table-level
`UNIQUE NULLS NOT DISTINCT` constraints were dumped without the
`NULLS NOT DISTINCT` modifier. In current pg-delta, the table-constraint path is
close but still incomplete: `AlterTableAddConstraint` serializes
`constraint.definition` verbatim, but `packages/pg-delta/src/core/objects/table/table.diff.ts`
does not compare either the full constraint definition or an explicit
`nulls_not_distinct` flag for named table constraints.

That means an existing constraint such as
`CONSTRAINT uq_items UNIQUE (a, b)` and a desired constraint
`CONSTRAINT uq_items UNIQUE NULLS NOT DISTINCT (a, b)` can currently look
unchanged to the structured comparator because the constraint name and
`key_columns` stay the same. There is also no dedicated integration regression
covering this table-constraint path.

Relates to pgschema issue #412: https://github.com/pgplex/pgschema/issues/412

## Test Case to Reproduce

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

**Expected:** pg-delta detects the modifier change, emits a drop/recreate for
the named constraint, and preserves `NULLS NOT DISTINCT`.
**Actual:** current table-constraint diffing does not compare this modifier on
same-name / same-key UNIQUE constraints, and no dedicated integration test
locks the behavior in.

## Suggested Fix

1. Add PostgreSQL 15+ integration coverage in:
   - `packages/pg-delta/tests/integration/constraint-operations.test.ts`
   Cover both adding a table-level `UNIQUE NULLS NOT DISTINCT` constraint and
   toggling an existing named UNIQUE constraint to the `NULLS NOT DISTINCT`
   variant.
2. Update the table-constraint diff path in:
   - `packages/pg-delta/src/core/objects/table/table.diff.ts`
   So named UNIQUE constraints treat
   `UNIQUE (...)` vs `UNIQUE NULLS NOT DISTINCT (...)` as a drop/recreate
   change.
3. Implementation options:
   - compare `constraint.definition` for relevant constraint types, or
   - add an explicit `nulls_not_distinct` field to the table-constraint model in
     `packages/pg-delta/src/core/objects/table/table.model.ts`

---

## pgschema #414 -> proposed pg-toolbelt issue draft

## Context

pgschema issue #414 reports that when one migration both adds a column and
creates or replaces a view that references that new column, the generated plan
can emit the view DDL before the `ALTER TABLE ... ADD COLUMN`. PostgreSQL then
fails while parsing the view body because the referenced column does not yet
exist.

Current pg-delta has a suspiciously similar blind spot. `AlterTableAddColumn`
only requires the parent table stable ID in
`packages/pg-delta/src/core/objects/table/changes/table.alter.ts`, while
`CreateView.requires` in
`packages/pg-delta/src/core/objects/view/changes/view.create.ts` only depends on
the schema and owner. There is an integration scenario in
`packages/pg-delta/tests/integration/mixed-objects.test.ts` for "Add column and
update view", but that test manually overrides ordering with
`sortChangesCallback`, so it does not validate the default sorter.

Relates to pgschema issue #414: https://github.com/pgplex/pgschema/issues/414

## Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.data (
  id integer PRIMARY KEY,
  value text
);

CREATE VIEW test_schema.summary AS
  SELECT COUNT(*) AS cnt FROM test_schema.data;
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.data ADD COLUMN status text;

CREATE OR REPLACE VIEW test_schema.summary AS
  SELECT COUNT(*) AS cnt,
         COUNT(CASE WHEN status = 'active' THEN 1 END) AS active_cnt
  FROM test_schema.data;
```

**Expected:** pg-delta orders `ALTER TABLE ... ADD COLUMN status text` before
`CREATE OR REPLACE VIEW ... status ...`.
**Actual:** no default-ordering integration test currently proves that
column-add dependencies are enforced for view definitions, and the existing
regression masks the issue with a custom `sortChangesCallback`.

## Suggested Fix

1. Add a default-ordering integration regression in:
   - `packages/pg-delta/tests/integration/mixed-objects.test.ts`
   Remove the custom `sortChangesCallback` for the add-column + update-view case
   or add a second copy without it.
2. If the test fails, teach view creation/replacement to depend on referenced
   table columns or otherwise introduce an ordering edge between
   `AlterTableAddColumn` and `CreateView` / `CreateOrReplaceView`.
3. Candidate implementation areas:
   - `packages/pg-delta/src/core/objects/view/changes/view.create.ts`
   - `packages/pg-delta/src/core/objects/view/view.model.ts`
   - `packages/pg-delta/src/core/sort/` if a sorter-level rule is more robust

