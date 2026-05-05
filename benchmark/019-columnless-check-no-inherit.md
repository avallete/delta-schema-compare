# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reports that table-level CHECK constraints with no
referenced columns — especially `CHECK (FALSE) NO INHERIT` on inheritance
parents — were being silently dropped during plan/apply. That changes schema
semantics: the parent table loses its guard against direct inserts, while child
tables created with `INHERITS` continue to exist as if the constraint had been
preserved.

pgschema fixed this in PR #391 by keeping column-less CHECK constraints during
introspection, propagating `connoinherit`, and adding a dedicated regression
fixture. This benchmark entry is historical now: current pg-delta covers the
same scenario, including the inherited-table variant that originally exposed the
gap.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.parent_base (
    id uuid PRIMARY KEY,
    name text NOT NULL,
    CONSTRAINT no_direct_insert CHECK (FALSE) NO INHERIT
);

CREATE TABLE test_schema.child (
    CONSTRAINT child_pkey PRIMARY KEY (id)
) INHERITS (test_schema.parent_base);
```

**Expected:** pg-delta preserves the `no_direct_insert` constraint definition,
including `NO INHERIT`, when diffing or replaying the inherited-table schema.

## How pgschema handled it

pgschema PR #391 fixed the bug in two places. First, it stopped dropping CHECK
constraints just because no column name was returned from the `pg_constraint` /
`pg_attribute` join. Second, it added explicit `NO INHERIT` handling through the
constraint IR, query layer, and emitted DDL.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ✅ `tests/integration/constraint-operations.test.ts` has `"add CHECK (FALSE) NO INHERIT constraint on inheritance parent"` |
| Integration test for inherited-table variant | ✅ Same file has `"add CHECK (FALSE) NO INHERIT on parent with INHERITS child"` |
| Table constraint model stores `no_inherit` | ✅ `src/core/objects/table/table.model.ts` includes `no_inherit` |
| Empty `conkey` path is handled safely | ✅ Same extractor coalesces column-less `key_columns` to `[]` |
| Table diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` compares both fields |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ Issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed by merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

The integration assertions explicitly check for:

```sql
ADD CONSTRAINT no_direct_insert CHECK (false) NO INHERIT
```

and, in the second case, also verify that the generated SQL includes:

```sql
INHERITS (test_schema.parent_base)
```

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Dropped column-less CHECK constraints during introspection | Same historical blind spot before dedicated regression coverage |
| **Current extraction** | Preserves `connoinherit` and column-less CHECK definitions | Preserves `no_inherit` and coalesces empty `conkey` arrays safely |
| **Regression coverage** | Dedicated fixture for issue #386 | Dedicated roundtrip regressions for both parent-only and parent+child inheritance cases |

## Resolution in pg-delta

pg-delta now preserves column-less `CHECK (FALSE) NO INHERIT` constraints and
their inheritance scenario in the current test suite. This benchmark entry is
retained as historical context, but the parity gap is solved in the refreshed
snapshot.
