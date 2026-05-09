# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reported that table-level CHECK constraints with no
referenced columns — especially `CHECK (FALSE) NO INHERIT` on inheritance
parents — were being silently dropped.

That parity gap is now closed in current pg-delta. The refreshed pg-delta tree
has dedicated integration coverage for both the column-less `CHECK (FALSE) NO
INHERIT` case and the inherited-table variant, on top of the existing source
support for `no_inherit`.

Refresh note (2026-05-09): the original pg-toolbelt tracker
[#198](https://github.com/supabase/pg-toolbelt/issues/198) is closed, and
[pg-toolbelt#212](https://github.com/supabase/pg-toolbelt/pull/212) is merged.

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

pgschema PR #391 preserved column-less CHECK constraints during introspection
and added explicit handling for the `NO INHERIT` modifier in emitted DDL.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table constraint model stores `no_inherit` | ✅ `src/core/objects/table/table.model.ts` |
| Table diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` |
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ✅ `tests/integration/constraint-operations.test.ts` |
| Integration test for inherited-table variant | ✅ `tests/integration/constraint-operations.test.ts` |
| Emitted SQL asserts `NO INHERIT` is preserved | ✅ integration assertions check for `ADD CONSTRAINT ... NO INHERIT` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed, PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped column-less CHECK / `NO INHERIT` constraints | Same parity risk existed originally |
| **Current fix** | Preserve the constraint during introspection and output | Preserve `no_inherit` and verify it end-to-end in integration tests |
| **Regression coverage** | Dedicated upstream fixture | Dedicated integration cases for both parent-only and inherited-table variants |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the refreshed pg-delta
snapshot.
