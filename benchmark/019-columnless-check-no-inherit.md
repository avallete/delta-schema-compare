# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

Table-level `CHECK (FALSE) NO INHERIT` constraints are often used on
inheritance parents to block direct inserts while still allowing child
tables to inherit the structure. If the constraint disappears, the schema
becomes weaker in a way that is easy to miss.

pgschema issue #386 covered that exact failure mode. pg-delta now handles
the same scenario correctly; the parity gap was closed by
[pg-toolbelt#212](https://github.com/supabase/pg-toolbelt/pull/212), which
resolved [pg-toolbelt#198](https://github.com/supabase/pg-toolbelt/issues/198).

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

## How pgschema handled it

pgschema fixed the extraction and output path so column-less check
constraints are retained and `NO INHERIT` is preserved in generated DDL.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | Yes - `add CHECK (FALSE) NO INHERIT constraint on inheritance parent` |
| Integration test for inherited-table variant | Yes - `add CHECK (FALSE) NO INHERIT on parent with INHERITS child` |
| Table constraint model stores `no_inherit` | Yes |
| Table diff compares `no_inherit` and `check_expression` | Yes |
| Empty `conkey` extraction path falls back to `[]` | Yes - `src/core/objects/table/table.model.ts` uses an explicit `coalesce(..., '[]'::json)` fallback |
| Existing pg-toolbelt issue / PR | Yes - issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed by merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

The focused regression coverage lives in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
and asserts both the `ADD CONSTRAINT ... CHECK (false) NO INHERIT` SQL and
the inherited-table variant.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| Historical root cause | Column-less check constraints were dropped from introspection / output | Same parity risk |
| Current upstream state | Fixed in merged PR #391 | Fixed in merged PR #212 |
| Regression coverage | Dedicated upstream fixture | Two focused roundtrip regressions plus the empty-`conkey` fallback in the extractor |

## Resolution in pg-delta

pg-delta now preserves column-less `CHECK (FALSE) NO INHERIT` constraints
and covers both the parent-table and `INHERITS (...)` variants from the
benchmark scenario.
