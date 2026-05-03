# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reports that table-level CHECK constraints with no
referenced columns - especially `CHECK (FALSE) NO INHERIT` on inheritance
parents - were being silently dropped during plan / apply.

pg-delta used to lack focused end-to-end coverage for the same shape, so
this benchmark tracked the gap through pg-toolbelt issue
[#198](https://github.com/supabase/pg-toolbelt/issues/198).

Refresh note (2026-05-03): pg-delta now covers both the column-less
constraint shape and the inheritance-parent variant. Issue
[#198](https://github.com/supabase/pg-toolbelt/issues/198) is closed and the
fix landed in merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212).

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

pgschema PR #391 fixed both the column-less CHECK extraction path and the
`NO INHERIT` handling needed for inheritance-parent scenarios.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Column-less constraint extraction keeps empty `conkey` stable | ✅ `src/core/objects/table/table.model.ts` falls back to `[]` for empty / missing `conkey` |
| `no_inherit` tracked in the table constraint model | ✅ `src/core/objects/table/table.model.ts` exposes `no_inherit` |
| Diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` compares both fields |
| Integration regression coverage | ✅ `tests/integration/constraint-operations.test.ts` covers `CHECK (FALSE) NO INHERIT` on a parent and on a parent with an `INHERITS` child |
| Existing pg-toolbelt issue / PR | ✅ [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed, [#212](https://github.com/supabase/pg-toolbelt/pull/212) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Column-less CHECK constraints were dropped and `NO INHERIT` was not preserved | Same parity question originally existed |
| **Current fix** | Preserves both the CHECK body and `NO INHERIT` | Preserves empty-key CHECK constraints, tracks `no_inherit`, and validates the inheritance case end-to-end |
| **Regression coverage** | Dedicated upstream fixture | Focused integration coverage in `constraint-operations.test.ts` |

## Resolution in pg-delta

This benchmark entry is now historical. Current pg-delta keeps column-less
`CHECK ... NO INHERIT` constraints intact and exercises both the plain
parent-table form and the inheritance-parent variant in integration tests.
