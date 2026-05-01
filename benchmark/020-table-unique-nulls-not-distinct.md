# Table-level `UNIQUE NULLS NOT DISTINCT`

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed),
> fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE NULLS NOT DISTINCT`
constraints were dumped as plain `UNIQUE (...)`, silently weakening the
constraint semantics. This is distinct from the already-solved standalone index
case in benchmark 016: PostgreSQL stores `NULLS NOT DISTINCT` for unique
indexes and for table constraints through different catalog paths, and pgschema
fixed only the table-constraint path in PR #413.

Current pg-delta already supports `NULLS NOT DISTINCT` on standalone unique
indexes. Its integration suite covers creating and toggling
`CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`, and the index model exposes
`indnullsnotdistinct`. However, the table-constraint model does not expose a
parallel field for `UNIQUE NULLS NOT DISTINCT`, and `table.diff.ts` does not
compare the full constraint definition for unique constraints. That means a
table-level constraint can be treated as unchanged even when the branch schema
adds `NULLS NOT DISTINCT`.

This matters because the difference is semantic, not cosmetic. A plain unique
constraint still treats `NULL` values as distinct, while `UNIQUE NULLS NOT
DISTINCT` rejects duplicate rows that match on all constrained columns
including `NULL` positions.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.pgschema_repro_nulls (
    a integer,
    b integer,
    CONSTRAINT pgschema_repro_nulls_uniq UNIQUE (a, b)
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.pgschema_repro_nulls
  DROP CONSTRAINT pgschema_repro_nulls_uniq;

ALTER TABLE test_schema.pgschema_repro_nulls
  ADD CONSTRAINT pgschema_repro_nulls_uniq
  UNIQUE NULLS NOT DISTINCT (a, b);
```

**Expected:** pg-delta detects the constraint definition change and emits
drop/recreate DDL preserving `NULLS NOT DISTINCT`.

**Actual:** pg-delta's table-constraint diff logic compares `constraint_type`,
deferrability, validation flags, `key_columns`, FK metadata, temporal flags,
and `check_expression`, but not a `nulls_not_distinct` field or the full
constraint definition. Because the constrained columns are identical, the
constraint can be treated as unchanged.

## How pgschema handled it

pgschema PR #413 preserved the modifier when dumping table-level unique
constraints. The upstream fix is intentionally separate from the earlier unique
index work in issue #355 / PR #356 because the table-constraint path required
its own extraction and serialization fix.

The upstream repro is minimal and directly usable as a parity test:

```sql
CREATE TABLE pgschema_repro_nulls (
    a integer,
    b integer,
    CONSTRAINT pgschema_repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b)
);
```

## Current pg-delta status

| Aspect | Status |
|---|---|
| Standalone unique indexes with `NULLS NOT DISTINCT` | ✅ Covered in `tests/integration/index-operations.test.ts` |
| Table constraint model field for `UNIQUE NULLS NOT DISTINCT` | ❌ Missing from `src/core/objects/table/table.model.ts` |
| Table diff detects `UNIQUE` → `UNIQUE NULLS NOT DISTINCT` | ❌ No explicit comparison in `src/core/objects/table/table.diff.ts` |
| Add-constraint serializer can preserve raw definition text | ✅ `AlterTableAddConstraint` reuses `constraint.definition` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during review |

**Source evidence** (`table.diff.ts` change detection):

```typescript
const changed =
  mainC.constraint_type !== branchC.constraint_type ||
  mainC.deferrable !== branchC.deferrable ||
  mainC.initially_deferred !== branchC.initially_deferred ||
  mainC.validated !== branchC.validated ||
  mainC.is_local !== branchC.is_local ||
  mainC.no_inherit !== branchC.no_inherit ||
  mainC.is_temporal !== branchC.is_temporal ||
  JSON.stringify(mainC.key_columns) !== JSON.stringify(branchC.key_columns) ||
  JSON.stringify(mainC.foreign_key_columns) !== JSON.stringify(branchC.foreign_key_columns) ||
  mainC.foreign_key_table !== branchC.foreign_key_table ||
  mainC.foreign_key_schema !== branchC.foreign_key_schema ||
  mainC.on_update !== branchC.on_update ||
  mainC.on_delete !== branchC.on_delete ||
  mainC.match_type !== branchC.match_type ||
  mainC.check_expression !== branchC.check_expression;
```

No table-constraint property captures `NULLS NOT DISTINCT`.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Solved standalone-index case** | Already fixed separately in #355/#356 | Already fixed separately in issue/PR #183/#185 |
| **Table-constraint metadata** | Fixed in PR #413 | No dedicated field for `NULLS NOT DISTINCT` on table constraints |
| **Diff behavior** | Preserves table-level modifier | Unique constraint can compare equal when only `NULLS NOT DISTINCT` differs |
| **Coverage** | Closed upstream regression | No integration test for table-level `UNIQUE NULLS NOT DISTINCT` |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   to expose a table-constraint `nulls_not_distinct`-style property for unique
   constraints, or compare a normalized form of `constraint.definition`.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `UNIQUE (...)` and `UNIQUE NULLS NOT DISTINCT (...)` are treated as a
   drop/recreate change.
3. Add PostgreSQL 15+ integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - creating `UNIQUE NULLS NOT DISTINCT` as a table constraint,
   - toggling an existing unique table constraint to/from `NULLS NOT DISTINCT`.
4. Reuse `AlterTableAddConstraint`'s definition-backed serializer so the final
   emitted DDL includes the modifier verbatim.
