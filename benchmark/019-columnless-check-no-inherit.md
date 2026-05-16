# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reports that table-level CHECK constraints with no referenced
columns — especially `CHECK (FALSE) NO INHERIT` on inheritance parents — were
being silently dropped during plan / apply. That weakens the schema by removing
the parent-table guard while leaving the inheritance structure intact.

Refresh note (2026-05-16): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#198](https://github.com/supabase/pg-toolbelt/issues/198)
is closed, and
[pg-toolbelt#212](https://github.com/supabase/pg-toolbelt/pull/212) added the
exact integration coverage that earlier refreshes still lacked.

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

pgschema PR #391 fixed the bug by preserving column-less CHECK constraints
during introspection, propagating `NO INHERIT`, and locking the behavior in with
an issue-specific regression fixture.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Integration test for inherited-table variant | ✅ Present |
| Table constraint model stores `no_inherit` | ✅ Present in `src/core/objects/table/table.model.ts` |
| Safe extraction path for empty `conkey` | ✅ `table.model.ts` now falls back to `[]` for column-less constraints |
| Table diff compares `no_inherit` and `check_expression` | ✅ Present |
| Existing pg-toolbelt issue / PR | ✅ [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed by merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

Current integration coverage now includes both:

- `"add CHECK (FALSE) NO INHERIT constraint on inheritance parent"`
- `"add CHECK (FALSE) NO INHERIT on parent with INHERITS child"`

Those tests cover the exact end-to-end paths that were previously only inferred
from source.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Column-less CHECK constraints were dropped during introspection / planning | Earlier pg-delta review lacked end-to-end coverage for the empty-`conkey` path |
| **Current fix** | Preserve the constraint body and `NO INHERIT` metadata | Preserve `no_inherit`, normalize empty key-column extraction, and verify the inheritance cases explicitly |
| **Regression coverage** | Issue-specific upstream fixture | Dedicated integration tests for both the direct parent and inherited-child variants |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the current pg-delta
snapshot. The benchmark is retained as historical context because it explains
why column-less constraints get a special empty-array extraction path in the
table model.
