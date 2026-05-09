# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reported that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause, silently
weakening uniqueness semantics.

That parity gap is now closed in current pg-delta. The refreshed pg-delta tree
extracts `nulls_not_distinct`, recreates indexes when the clause changes, and
has dedicated integration coverage for creating and toggling `NULLS NOT
DISTINCT` unique indexes.

Refresh note (2026-05-09): the original pg-toolbelt tracker
[#183](https://github.com/supabase/pg-toolbelt/issues/183) is closed, and
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185) is merged.

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

pgschema added explicit `NULLS NOT DISTINCT` tracking in its index
representation and re-emitted the clause in diff and plan output.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from catalog | ✅ `src/core/objects/index/index.model.ts` |
| Diff treats clause changes as index recreation | ✅ `src/core/objects/index/index.diff.ts` |
| Create SQL preserves captured index definition | ✅ current index create path |
| Integration test for `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT` | ✅ `tests/integration/index-operations.test.ts` (`"create unique index with NULLS NOT DISTINCT"`) |
| Integration test for toggling the clause on an existing index | ✅ `tests/integration/index-operations.test.ts` (`"toggle unique index to NULLS NOT DISTINCT"` / `"toggle unique index from NULLS NOT DISTINCT"`) |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed, PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Dropped `NULLS NOT DISTINCT` from unique indexes | Same parity gap existed originally |
| **Current fix** | Track and re-emit the clause in index IR | Track `nulls_not_distinct` and verify create/toggle roundtrips in integration tests |
| **Regression coverage** | Upstream fixture coverage | Dedicated PG15+ integration coverage |

## Scope note

This benchmark entry is specific to the **unique-index** form from pgschema
issue #355. The later pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412)
covers the distinct **table-constraint** form,
`UNIQUE NULLS NOT DISTINCT (...)`, which remains benchmarked separately as
[020](020-unique-constraint-nulls-not-distinct.md).

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the refreshed pg-delta
snapshot.
