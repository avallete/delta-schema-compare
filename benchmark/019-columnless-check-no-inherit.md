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
`repos/pgschema/testdata/diff/online/issue_386_check_no_inherit/`. In pg-delta,
the closest integration coverage is
`repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`,
but it only exercises column-based CHECK constraints such as `CHECK (price > 0)`.
There is no roundtrip test for a column-less CHECK, `NO INHERIT`, or the
inherited-table scenario from pgschema #386.

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

**Actual:** pg-delta has no integration regression covering this exact scenario.
The table constraint model already records `no_inherit`, but the extraction query
in `src/core/objects/table/table.model.ts` builds `key_columns` from
`json_agg(unnest(c.conkey))` without an explicit empty-array fallback for
column-less CHECK constraints, and no end-to-end test exercises that path.

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
| Integration test for column-less `CHECK (FALSE) NO INHERIT` | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Integration test for inherited-table variant | ❌ Missing from `tests/integration/` |
| Table constraint model stores `no_inherit` | ✅ `src/core/objects/table/table.model.ts` includes `no_inherit` |
| Table diff compares `no_inherit` and `check_expression` | ✅ `src/core/objects/table/table.diff.ts` compares both fields |
| Serializer can emit `NO INHERIT` | ✅ `src/core/plan/sql-format/*` has unit coverage for `NO INHERIT` output |
| Safe extraction path for empty `conkey` exercised end-to-end | ❌ No exact coverage found |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during review |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Explicitly fixed column-less CHECK introspection in PR #391 | Extracts `connoinherit`, but the empty-`conkey` path is not covered end-to-end |
| **DDL fidelity** | Preserves both the CHECK body and `NO INHERIT` modifier | Formatter can output `NO INHERIT`, but exact roundtrip coverage is missing |
| **Regression coverage** | Has a dedicated fixture for issue #386 | Only tests ordinary column-based CHECK constraints |
| **Inheritance scenario** | Regression fixture covers parent/child inheritance use case | No integration case for `INHERITS (...)` plus column-less CHECK |

## Plan to handle it in pg-delta

1. Add an integration regression in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for `CHECK (FALSE) NO INHERIT`.
2. Add a second integration case covering
   `CREATE TABLE ... INHERITS (parent_base)` with the constraint on the parent.
3. Verify `src/core/objects/table/table.model.ts` returns a stable empty array
   for column-less CHECK `key_columns` rather than `null` when `conkey` is empty.
4. Re-run the constraint integration suite to confirm pg-delta preserves the
   constraint definition and does not regress ordinary CHECK handling.
