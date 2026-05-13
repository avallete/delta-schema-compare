# Unique Index `NULLS NOT DISTINCT`

> pgschema issue [#355](https://github.com/pgplex/pgschema/issues/355) (closed), fixed by [pgschema#356](https://github.com/pgplex/pgschema/pull/356)

## Context

pgschema issue #355 reports that `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT`
was being planned and applied without the `NULLS NOT DISTINCT` clause. That
changes uniqueness semantics: rows that should conflict because they share
`NULL` values are allowed to coexist.

Refresh note (2026-05-13): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183)
is closed, and
[pg-toolbelt#185](https://github.com/supabase/pg-toolbelt/pull/185) added the
PG15+ roundtrip coverage that earlier refreshes were still missing.

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

pgschema fixed the issue by carrying a `NullsNotDistinct` flag through its index
IR and by re-emitting the clause during diff / plan generation. The upstream
fix ships with regression coverage in the `create_index/add_index` fixtures.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `nulls_not_distinct` extracted from catalog | ✅ Present in `src/core/objects/index/index.model.ts` |
| Diff treats clause changes as index recreation | ✅ Present in `src/core/objects/index/index.diff.ts` |
| Create SQL preserves captured index definition | ✅ Present |
| Integration test for `NULLS NOT DISTINCT` unique indexes | ✅ `tests/integration/index-operations.test.ts` covers create and both toggle directions |
| Existing pg-toolbelt issue / PR | ✅ [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed by merged PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) |

Current integration coverage now includes:

- `"create unique index with NULLS NOT DISTINCT"`
- `"toggle unique index to NULLS NOT DISTINCT"`
- `"toggle unique index from NULLS NOT DISTINCT"`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Index modifier dropped during dump / plan output | Earlier pg-delta review lacked end-to-end proof for the modeled flag |
| **Current fix** | Preserve the modifier in index IR and emitted DDL | Preserve the modeled flag and verify it with explicit PG15+ roundtrip tests |
| **Regression coverage** | Upstream fixtures for add-index flows | Dedicated integration cases for create and recreate paths |

## Resolution in pg-delta

No active parity gap remains for the **index** variant of `NULLS NOT DISTINCT`
in the current pg-delta snapshot.

One related scenario is still unresolved separately: the **table-constraint**
variant from pgschema
[#412](https://github.com/pgplex/pgschema/issues/412), which is now documented
as benchmark [020](020-table-constraint-unique-nulls-not-distinct.md).
