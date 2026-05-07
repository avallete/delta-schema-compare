# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed),
> fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reports that table-level CHECK constraints with no
referenced columns — especially `CHECK (FALSE) NO INHERIT` on inheritance
parents — were being silently dropped during plan/apply.

Refresh note (2026-05-07): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#198](https://github.com/supabase/pg-toolbelt/issues/198)
is closed, and
[pg-toolbelt#212](https://github.com/supabase/pg-toolbelt/pull/212) added the
missing integration coverage for both the plain parent-table case and the
`INHERITS (...)` variant.

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

pgschema fixed the bug by preserving column-less CHECK constraints during
introspection and by keeping `NO INHERIT` in its constraint representation and
emitted DDL.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table constraint model stores `no_inherit` | ✅ Present in `src/core/objects/table/table.model.ts` |
| Table diff compares `no_inherit` and `check_expression` | ✅ Present in `src/core/objects/table/table.diff.ts` |
| Integration test for `CHECK (FALSE) NO INHERIT` on parent table | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Integration test for `INHERITS (...)` child variant | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed by merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

Current integration coverage includes:

- `add CHECK (FALSE) NO INHERIT constraint on inheritance parent`
- `add CHECK (FALSE) NO INHERIT on parent with INHERITS child`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped column-less CHECK constraints and `NO INHERIT` | Needed dedicated coverage for the same constraint shape |
| **Current fix** | Preserves the constraint during extraction and emission | Preserves the constraint and validates both the parent and inherited-table flows end-to-end |
| **Coverage** | Fixed upstream | Dedicated integration coverage on current `main` |

## Resolution in pg-delta

The current pg-delta snapshot now covers the column-less `CHECK (FALSE)
NO INHERIT` scenarios from pgschema #386. This benchmark entry is therefore
historical context, not an active parity gap.
