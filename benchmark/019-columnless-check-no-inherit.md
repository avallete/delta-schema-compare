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
`repos/pgschema/testdata/diff/online/issue_386_check_no_inherit/`. Pg-delta now
has matching roundtrip coverage in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
for both the standalone `CHECK (FALSE) NO INHERIT` case and the inherited-table
variant from pgschema #386.

This matters because the gap is not cosmetic. If pg-delta misses or mis-diffs a
`CHECK (FALSE) NO INHERIT` constraint, users can ship a weaker schema than the
branch database intended, silently allowing writes that should have been blocked
on the parent table.

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

**Current pg-delta behavior:** pg-delta roundtrips this schema and keeps the
`NO INHERIT` modifier intact, including when the parent is later inherited by a
child table.

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
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Integration test for inherited-table variant | ✅ Present in `tests/integration/constraint-operations.test.ts` |
| Table constraint model stores `no_inherit` | ✅ `src/core/objects/table/table.model.ts` includes `no_inherit` |
| Table diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` compares both fields |
| Serializer can emit `NO INHERIT` | ✅ `src/core/plan/sql-format/*` has unit coverage for `NO INHERIT` output |
| Safe extraction path for empty `conkey` exercised end-to-end | ✅ Covered by the column-less CHECK roundtrip tests |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ Fixed by issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) / PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Explicitly fixed column-less CHECK introspection in PR #391 | Extracts `connoinherit` and now exercises the empty-`conkey` path end-to-end |
| **DDL fidelity** | Preserves both the CHECK body and `NO INHERIT` modifier | Roundtrip tests confirm `NO INHERIT` survives planner output |
| **Regression coverage** | Has a dedicated fixture for issue #386 | Has dedicated integration regressions for both standalone and inherited-table cases |
| **Inheritance scenario** | Regression fixture covers parent/child inheritance use case | Integration coverage now includes `INHERITS (...)` plus column-less CHECK |

## Resolution in pg-delta

pg-delta now includes the two focused regressions that were missing when this
benchmark entry was first written:

1. `add CHECK (FALSE) NO INHERIT constraint on inheritance parent`
2. `add CHECK (FALSE) NO INHERIT on parent with INHERITS child`

Those tests verify both planner fidelity and the end-to-end extraction path for
column-less CHECK constraints. This benchmark entry is therefore retained as
historical context, but the parity gap is solved in the current pg-delta
snapshot.
