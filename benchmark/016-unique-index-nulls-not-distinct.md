# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reports that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause. That
silently weakens index semantics: rows that should conflict because they
share `NULL` values can be inserted successfully.

This benchmark originally tracked whether pg-delta preserved the same
PostgreSQL 15+ modifier on standalone unique indexes.

Refresh note (2026-05-03): pg-delta now covers this scenario end-to-end.
pg-toolbelt issue [#183](https://github.com/supabase/pg-toolbelt/issues/183)
is closed and the fix landed in merged PR
[#185](https://github.com/supabase/pg-toolbelt/pull/185).

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

## How pgschema handled it

pgschema added a `NullsNotDistinct` field to its index IR and re-emits the
modifier in diff and plan output.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from the catalog | ✅ `src/core/objects/index/index.model.ts` reads `pg_index.indnullsnotdistinct` |
| Diff recreates indexes when the modifier changes | ✅ `src/core/objects/index/index.diff.ts` treats `nulls_not_distinct` as non-alterable |
| Integration regression coverage | ✅ `tests/integration/index-operations.test.ts` covers create + toggle to / from `NULLS NOT DISTINCT` |
| Existing pg-toolbelt issue / PR | ✅ [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed, [#185](https://github.com/supabase/pg-toolbelt/pull/185) merged |
| Scope note | ✅ This benchmark covers standalone unique indexes; the table-constraint variant is tracked separately in [020](020-unique-constraint-nulls-not-distinct.md) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Dropped the modifier from unique index output | Same parity question originally existed |
| **Current fix** | Tracks the modifier explicitly in index IR | Tracks the modifier in the index model and recreates indexes when it changes |
| **Regression coverage** | Fixture-backed upstream | PG15+ integration coverage in `index-operations.test.ts` |

## Resolution in pg-delta

This benchmark entry is now historical. Current pg-delta preserves `NULLS
NOT DISTINCT` for standalone unique indexes and validates both creation and
modifier toggles in integration tests.
