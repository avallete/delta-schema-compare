# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reports that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause. That
silently weakens the index semantics: rows that should conflict because they
share `NULL` values can be inserted successfully.

pgschema fixed this in PR #356 by explicitly tracking the property in its index
IR and re-emitting the clause in diff and plan output. In pg-delta, the index
catalog model already exposes `nulls_not_distinct`, and index create SQL is
serialized from the captured catalog definition, but there is still no
integration scenario that proves roundtrip fidelity for this exact PostgreSQL
15+ feature.

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
| Create SQL preserves captured index definition | ✅ Likely via `src/core/objects/index/changes/index.create.ts` |
| Integration test for `NULLS NOT DISTINCT` unique indexes | ❌ Missing from `tests/integration/index-operations.test.ts` |
| Existing pg-toolbelt open issue / PR for this exact scenario | ❌ None found during review |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Current state** | Fixed in merged PR #356 with regression fixture | Source appears partially ready, but exact roundtrip coverage is missing |
| **Evidence level** | Verified by merged fix + diff/plan fixtures | Implementation hints exist, but behavior is unproven by integration test |
| **Risk** | Addressed | High-confidence blind spot for a correctness-sensitive unique-index feature |

## Plan to handle it in pg-delta

1. Add a PostgreSQL 15+ integration test in
   `tests/integration/index-operations.test.ts` covering
   `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`.
2. Add a second roundtrip case that changes an existing unique index between
   plain unique and `NULLS NOT DISTINCT` to verify the recreate path in
   `src/core/objects/index/index.diff.ts`.
3. If the roundtrip fails, adjust index definition extraction or serialization
   in `src/core/objects/index/index.model.ts` and
   `src/core/objects/index/changes/index.create.ts` so the clause is preserved
   across diff/apply.
