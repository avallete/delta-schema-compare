# Table-level `UNIQUE NULLS NOT DISTINCT`

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed),
> fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reports that table-level `UNIQUE` constraints using the
PostgreSQL 15+ `NULLS NOT DISTINCT` modifier were being dumped and planned as
plain `UNIQUE (...)` constraints. That silently changes semantics: rows that
should conflict because `NULL` values are treated as equal can slip through.

This is distinct from the already-solved index-form scenario in benchmark entry
`016`. pg-delta has merged coverage for `CREATE UNIQUE INDEX ... NULLS NOT
DISTINCT`, but table constraints flow through the table-constraint model rather
than the index object model.

In current pg-delta, table constraints already preserve their raw
`pg_get_constraintdef(...)` text in `definition`, so adding a brand-new
`UNIQUE NULLS NOT DISTINCT` constraint can piggyback on that definition.
However, the structured table-constraint diff still has no dedicated
`nulls_not_distinct` signal for unique constraints and does not compare the raw
`definition` string. As a result, a transition between:

- `UNIQUE (a, b)` and
- `UNIQUE NULLS NOT DISTINCT (a, b)`

on the same constraint identity is not modeled explicitly and has no dedicated
roundtrip regression coverage.

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

**Expected:** pg-delta detects that the constraint semantics changed and emits
DDL that preserves `NULLS NOT DISTINCT`.

**Current risk in pg-delta:** add/create flows may preserve the raw definition,
but the structured diff path for same-name table constraints does not carry an
explicit `NULLS NOT DISTINCT` field or compare `definition`, so this specific
modifier is not covered as a first-class constraint diff.

## How pgschema handled it

pgschema PR #413 added support for table-constraint `NULLS NOT DISTINCT` by
propagating the modifier through its constraint IR and re-emitting it in both
dump and diff output. The merged PR added:

- dump regression coverage in
  `repos/pgschema/testdata/dump/issue_412_unique_nulls_not_distinct/`
- diff/plan regression coverage in
  `repos/pgschema/testdata/diff/create_table/add_unique_constraint_nulls_not_distinct/`

The pgschema fix notes that this needs PostgreSQL-version-safe extraction
because the underlying `pg_index.indnullsnotdistinct` field exists only on
PostgreSQL 15+.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Unique index `NULLS NOT DISTINCT` support | ✅ Solved separately in benchmark `016` |
| Table constraint raw `definition` captured | ✅ `src/core/objects/table/table.model.ts` stores `pg_get_constraintdef(c.oid, true)` |
| Dedicated `nulls_not_distinct` field on table constraints | ❌ Missing |
| Table-constraint diff compares `definition` text | ❌ Missing |
| Integration test for `UNIQUE NULLS NOT DISTINCT` table constraints | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found in current open pg-toolbelt issues / PRs |

Relevant source evidence:

- `table.model.ts` already records:
  ```typescript
  'definition', pg_get_constraintdef(c.oid, true),
  ```
- but `table.diff.ts` only compares structured scalar fields like
  `constraint_type`, `key_columns`, `deferrable`, `is_temporal`,
  `check_expression`, and related FK metadata. It does not compare either a
  dedicated `nulls_not_distinct` flag or the raw `definition`.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped `NULLS NOT DISTINCT` from unique table constraints | Index form solved, but table-constraint form lacks explicit diff coverage |
| **Current modeling** | Tracks the modifier in constraint IR | Only stores raw constraint definition text |
| **Diff behavior** | Re-emits the modifier in dump and diff output | Same-name constraint transitions rely on structured fields that omit this modifier |
| **Regression coverage** | Has merged dump + diff fixtures for issue #412 | No dedicated table-constraint integration case |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   to expose a table-constraint-level `nulls_not_distinct` flag for unique
   constraints, ideally via a PostgreSQL-version-safe join to `pg_index` on
   `c.conindid` using `to_jsonb(i) ->> 'indnullsnotdistinct'`.
2. Add the new field to `tableConstraintPropsSchema` and preserve it in the
   table constraint model.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so a regular unique constraint and a `NULLS NOT DISTINCT` unique constraint
   are treated as different definitions that require drop/recreate.
4. Add roundtrip coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for:
   - creating a table-level `UNIQUE NULLS NOT DISTINCT` constraint
   - toggling an existing same-name constraint between plain `UNIQUE` and
     `UNIQUE NULLS NOT DISTINCT`
5. Optionally add declarative-export coverage if pg-delta's export path needs to
   assert the same modifier in generated SQL from an inspected catalog.
