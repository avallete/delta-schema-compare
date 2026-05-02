# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reports that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause. That
silently weakens the index semantics: rows that should conflict because they
share `NULL` values can be inserted successfully.

pgschema fixed this in PR #356 by explicitly tracking the property in its index
IR and re-emitting the clause in diff and plan output. pg-delta now also has
merged parity coverage for this exact PostgreSQL 15+ feature.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.example (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    middle_name text
);
```

**Change to diff:**

```sql
CREATE UNIQUE INDEX example_name_unique
    ON test_schema.example (first_name, last_name, middle_name)
    NULLS NOT DISTINCT;
```

**Expected:** generated DDL preserves `NULLS NOT DISTINCT` on the unique index.

**Risky behavior if not preserved:** generated DDL falls back to a plain unique
index, allowing duplicate rows that differ only by `NULL` handling and changing
application-visible uniqueness semantics.

## How pgschema handled it

pgschema added a `NullsNotDistinct` field to its index IR, detected the clause
from inspected index definitions, and re-emitted it during diff and plan
rewrites. The fix is covered by the existing `create_index/add_index` fixture in
`repos/pgschema/testdata/diff/create_index/add_index/`, which now includes a
`CREATE UNIQUE INDEX ... NULLS NOT DISTINCT` regression case.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from catalog | ✅ Present in `src/core/objects/index/index.model.ts` |
| Diff treats clause changes as index recreation | ✅ Present in `src/core/objects/index/index.diff.ts` |
| Create SQL preserves captured index definition | ✅ Serialized from the catalog-backed index definition |
| Integration test for `NULLS NOT DISTINCT` unique indexes | ✅ Present in `tests/integration/index-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ [#183](https://github.com/supabase/pg-toolbelt/issues/183) / [#185](https://github.com/supabase/pg-toolbelt/pull/185) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Current state** | Fixed in merged PR #356 with regression fixture | Fixed with merged integration coverage in pg-toolbelt #185 |
| **Evidence level** | Verified by merged fix + diff/plan fixtures | Verified by dedicated roundtrip coverage for create/toggle/remove flows |
| **Risk** | Addressed | Addressed |

## Plan to handle it in pg-delta

1. Keep the dedicated PostgreSQL 15+ roundtrip coverage in
   `tests/integration/index-operations.test.ts`.
2. Use the existing create / toggle / remove cases as the regression baseline
   for future index-definition refactors.
3. Treat any future regression here as a parity bug because the historical gap
   is now solved in current pg-delta.

## Resolution in pg-delta

pg-delta now has dedicated integration coverage for:

- creating a unique index with `NULLS NOT DISTINCT`
- toggling a unique index to `NULLS NOT DISTINCT`
- toggling back from `NULLS NOT DISTINCT`

Those cases live in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/index-operations.test.ts`
and were merged in
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185).

This benchmark entry is therefore retained as historical context, but the
parity gap is solved in the current pg-delta snapshot.
