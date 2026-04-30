# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

PostgreSQL 15 introduced `NULLS NOT DISTINCT` for unique indexes. That
modifier changes real uniqueness semantics for nullable columns: rows that
would previously be considered distinct because of `NULL` values can now
conflict.

pgschema issue #355 covered the standalone index form of that feature.
pg-delta now handles the same case correctly; the gap was closed by
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185), which
resolved [pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183).

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.example (
    id serial PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
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

pgschema added explicit `NullsNotDistinct` handling to its index IR and
preserved the clause during diff / plan generation.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from catalog | Yes - `src/core/objects/index/index.model.ts` |
| Diff treats clause changes as index recreation | Yes - `src/core/objects/index/index.diff.ts` |
| Create SQL preserves the captured definition | Yes |
| Integration test: create unique index with `NULLS NOT DISTINCT` | Yes |
| Integration test: toggle to `NULLS NOT DISTINCT` | Yes |
| Integration test: toggle from `NULLS NOT DISTINCT` back to plain unique | Yes |
| Existing pg-toolbelt issue / PR | Yes - issue [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed by merged PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) |

The focused coverage lives in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/index-operations.test.ts`
with the test cases:

- `create unique index with NULLS NOT DISTINCT`
- `toggle unique index to NULLS NOT DISTINCT`
- `toggle unique index from NULLS NOT DISTINCT`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| Historical root cause | Lost `NULLS NOT DISTINCT` on standalone unique indexes | Same parity gap |
| Current upstream state | Fixed in merged PR #356 | Fixed in merged PR #185 |
| Regression coverage | Upstream diff / plan fixtures | Three focused roundtrip regressions |

## Resolution in pg-delta

The standalone unique-index form from pgschema #355 is now solved in
pg-delta. A separate table-constraint variant remains active as benchmark
020, but that is a distinct table-constraint diff path rather than the
standalone index path covered here.
