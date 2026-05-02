# Column-less `CHECK ... NO INHERIT` constraints

> pgschema issue [#386](https://github.com/pgplex/pgschema/issues/386) (closed), fixed by [pgschema#391](https://github.com/pgplex/pgschema/pull/391)

## Context

pgschema issue #386 reports that table-level CHECK constraints with no referenced
columns — especially `CHECK (FALSE) NO INHERIT` on inheritance parents — were
being silently dropped during plan/apply. That changes schema semantics: the
parent table loses its guard against direct inserts, while child tables created
with `INHERITS` continue to exist as if the constraint had been preserved.

pgschema fixed this in PR #391 by keeping column-less CHECK constraints during
introspection, propagating `connoinherit`, and adding a regression fixture in
`repos/pgschema/testdata/diff/online/issue_386_check_no_inherit/`.

This parity gap is now also fixed in pg-delta. The relevant work landed in
[pg-toolbelt#212](https://github.com/supabase/pg-toolbelt/pull/212) and is
tracked by the now-closed issue
[pg-toolbelt#198](https://github.com/supabase/pg-toolbelt/issues/198).

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

**Current pg-delta behavior:** the refreshed pg-delta tree now covers both the
standalone and inherited-table variants in its constraint integration suite.

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
| Table constraint model stores `no_inherit` | ✅ `src/core/objects/table/table.model.ts` includes `no_inherit` |
| Table diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` compares both fields |
| Empty-`conkey` extraction path returns a stable empty array | ✅ `table.model.ts` uses `coalesce(..., '[]'::json)` for column-less constraints |
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ✅ `constraint-operations.test.ts` includes `"add CHECK (FALSE) NO INHERIT constraint on inheritance parent"` |
| Integration test for inherited-table variant | ✅ `constraint-operations.test.ts` includes `"add CHECK (FALSE) NO INHERIT on parent with INHERITS child"` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed by merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Explicitly fixed column-less CHECK introspection in PR #391 | Handles empty-`conkey` constraints without collapsing to `null` |
| **DDL fidelity** | Preserves both the CHECK body and `NO INHERIT` modifier | Preserves `NO INHERIT` through table-constraint diffing and serialization |
| **Regression coverage** | Has a dedicated fixture for issue #386 | Has dedicated roundtrip tests for both standalone and inherited variants |
| **Current parity state** | Fixed | Fixed |

## Resolution in pg-delta

pg-delta now keeps column-less `CHECK (FALSE) NO INHERIT` constraints through
catalog extraction, diffing, and roundtrip application, including the
inheritance-parent scenario from pgschema #386.

This benchmark entry is therefore retained as historical context, but the parity
gap is solved in the current pg-delta snapshot.
