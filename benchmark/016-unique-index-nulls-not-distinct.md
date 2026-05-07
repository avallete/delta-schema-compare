# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed),
> fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reports that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause. That
silently weakens the index semantics because rows that should conflict on NULL
keys can then coexist.

Refresh note (2026-05-07): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183)
is closed, and
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185) merged
dedicated integration coverage for creating and toggling unique indexes with
`NULLS NOT DISTINCT`.

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

pgschema fixed the issue by tracking the property in its index IR and
re-emitting the clause during diff/plan/apply.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from catalog | ✅ Present in `src/core/objects/index/index.model.ts` |
| Diff treats clause changes as index recreation | ✅ Covered by current index diff logic |
| Integration coverage for creating the feature | ✅ Present in `tests/integration/index-operations.test.ts` |
| Integration coverage for toggling to/from the feature | ✅ Present in `tests/integration/index-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed by merged PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) |

Current integration coverage includes:

- `create unique index with NULLS NOT DISTINCT`
- `toggle unique index to NULLS NOT DISTINCT`
- `toggle unique index from NULLS NOT DISTINCT`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped the index modifier during dump/plan/apply | Needed dedicated index coverage for the same feature |
| **Current fix** | Tracks the flag in the index IR | Extracts the flag from `pg_index` and exercises create/toggle flows end-to-end |
| **Coverage** | Fixed upstream | Dedicated integration coverage on current `main` |

## Resolution in pg-delta

The unique-index form of `NULLS NOT DISTINCT` is now solved in pg-delta. This
entry intentionally remains separate from benchmark item 020, which covers the
still-unresolved **table-constraint** variant from pgschema #412.
