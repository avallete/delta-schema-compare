# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reported that table-level CHECK constraints with no
referenced columns — especially `CHECK (FALSE) NO INHERIT` on inheritance
parents — were being silently dropped during plan/apply. That weakens schema
semantics by removing the guard that blocks direct inserts into the parent
table.

Current pg-delta now has direct regression coverage for both the plain
column-less CHECK and the inheritance-parent variant. The table constraint model
extracts `connoinherit`, preserves empty `conkey` arrays via an explicit
`'[]'::json` fallback, and the constraint diff path compares both
`check_expression` and `no_inherit`.

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

**Actual in current pg-delta:** covered. The roundtrip suite asserts that the
generated SQL contains `ADD CONSTRAINT no_direct_insert CHECK (false) NO
INHERIT` and preserves the `INHERITS (test_schema.parent_base)` path.

## How pgschema handled it

pgschema PR #391 fixed the bug in two places. First, it stopped dropping CHECK
constraints just because no column name was returned from the `pg_constraint` /
`pg_attribute` join. Second, it added explicit `NO INHERIT` handling through the
constraint IR, query layer, and emitted DDL.

The merged PR also added regression coverage in
`repos/pgschema/testdata/diff/online/issue_386_check_no_inherit/`, which uses
the exact `CHECK (false) NO INHERIT` inheritance pattern from the issue so the
behavior stays locked in.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ✅ `constraint-operations.test.ts` |
| Integration test for inherited-table variant | ✅ `constraint-operations.test.ts` |
| Table constraint model stores `no_inherit` | ✅ `src/core/objects/table/table.model.ts` |
| Table diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` |
| Safe extraction path for empty `conkey` exercised end-to-end | ✅ explicit coverage via the two integration tests |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ [#198](https://github.com/supabase/pg-toolbelt/issues/198) / [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Fixed column-less CHECK introspection in PR #391 | Uses explicit empty-array fallback for `conkey` plus `connoinherit` extraction |
| **DDL fidelity** | Preserves both the CHECK body and `NO INHERIT` modifier | Preserves both through extracted definitions and table-constraint diffing |
| **Regression coverage** | Dedicated fixture for issue #386 | Dedicated integration cases for both plain and inherited-parent scenarios |
| **Current upstream state** | Fixed | Fixed |

## Latest refresh note (2026-05-01)

This benchmark item remains historically interesting but is no longer an active
gap.

- pg-delta now has direct integration coverage for:
  - `add CHECK (FALSE) NO INHERIT constraint on inheritance parent`
  - `add CHECK (FALSE) NO INHERIT on parent with INHERITS child`
- The corresponding pg-toolbelt work landed in
  [#212](https://github.com/supabase/pg-toolbelt/pull/212) and closed issue
  [#198](https://github.com/supabase/pg-toolbelt/issues/198)
