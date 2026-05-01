# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reported that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause. That
silently weakens the index semantics: rows that should conflict because they
share `NULL` values can be inserted successfully.

pgschema fixed this in PR #356 by explicitly tracking the property in its index
IR and re-emitting the clause in diff and plan output. pg-delta now matches that
behavior in current source and integration coverage.

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

## How pgschema handled it

pgschema added a `NullsNotDistinct` field to its index IR, detected the clause
from inspected index definitions, and re-emitted it during diff and plan
rewrites. The fix is covered by the existing `create_index/add_index` fixture in
`repos/pgschema/testdata/diff/create_index/add_index/`, which includes a
`CREATE UNIQUE INDEX ... NULLS NOT DISTINCT` regression case.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from catalog | ✅ Present in `src/core/objects/index/index.model.ts` |
| Diff treats clause changes as index recreation | ✅ Present in `src/core/objects/index/index.diff.ts` |
| Create SQL preserves captured index definition | ✅ Serialized from the catalog-backed index definition |
| Integration test for `NULLS NOT DISTINCT` unique indexes | ✅ Present in `tests/integration/index-operations.test.ts` |
| Toggle coverage (plain unique ↔ `NULLS NOT DISTINCT`) | ✅ Present in `tests/integration/index-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed by [#185](https://github.com/supabase/pg-toolbelt/pull/185) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Current state** | Fixed in merged PR #356 with regression fixture | Fixed with integration coverage |
| **Evidence level** | Verified by merged fix + diff/plan fixtures | Verified by catalog extraction, diff logic, and integration tests |
| **Residual gap** | None for this scenario | None for this scenario |

## Latest refresh note (2026-05-01)

This benchmark item is solved in the current pg-delta snapshot:

- `tests/integration/index-operations.test.ts` includes:
  - `create unique index with NULLS NOT DISTINCT`
  - `toggle unique index to NULLS NOT DISTINCT`
  - `toggle unique index from NULLS NOT DISTINCT`
- The current source still tracks the feature explicitly through
  `index.model.ts` and `index.diff.ts`.
- The remaining unresolved `NULLS NOT DISTINCT` parity work is a different
  scenario: pgschema [#412](https://github.com/pgplex/pgschema/issues/412),
  which concerns table-level `UNIQUE` constraints rather than standalone
  indexes.
