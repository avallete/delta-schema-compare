# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` to a custom enum),
PostgreSQL requires a `USING` clause if the cast is not implicit. If the
column also has an incompatible default, that default must be dropped before
the type change and then re-applied afterward.

pgschema originally emitted `ALTER COLUMN ... TYPE enum_type` without the
`USING` clause and without a default-safe flow. That made the migration fail
for the exact enum conversion reproduced below.

pg-delta had the same gap when this benchmark entry was first written, but the
current upstream submodule now covers the scenario. The earlier draft PR
[#146](https://github.com/supabase/pg-toolbelt/pull/146) was closed and
superseded by the merged fix PR
[#231](https://github.com/supabase/pg-toolbelt/pull/231), which also closed
the tracking issue [#130](https://github.com/supabase/pg-toolbelt/issues/130).

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TYPE test_schema.status AS ENUM ('active', 'inactive', 'archived');

CREATE TABLE test_schema.items (
    id serial PRIMARY KEY,
    state text NOT NULL DEFAULT 'active'
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.items
  ALTER COLUMN state DROP DEFAULT;
ALTER TABLE test_schema.items
  ALTER COLUMN state TYPE test_schema.status USING state::test_schema.status;
ALTER TABLE test_schema.items
  ALTER COLUMN state SET DEFAULT 'active'::test_schema.status;
```

## How pgschema handled it

pgschema fixed the issue by emitting the `USING` cast when a custom-type
conversion requires it and by handling the default drop/re-set sequence around
the type change.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` change class | Yes |
| USING clause in serialize() | Yes - generated when the previous and new column types differ |
| Default drop/re-set around type change | Yes - emitted in the table diff flow when a type change collides with an existing default |
| Integration regression for `text -> enum` with default | Yes - present in `tests/integration/alter-table-operations.test.ts` |
| Existing pg-toolbelt issue / PR | Yes - [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed, [#146](https://github.com/supabase/pg-toolbelt/pull/146) closed, replacement [#231](https://github.com/supabase/pg-toolbelt/pull/231) merged |

**Source evidence** in the refreshed pg-delta submodule:

- `src/core/objects/table/changes/table.alter.ts` now appends
  `USING <column>::<new_type>` when `previousColumn.data_type_str` differs from
  the target type.
- `src/core/objects/table/table.diff.ts` emits
  `DROP DEFAULT -> ALTER TYPE -> SET DEFAULT` when a type change would leave an
  incompatible default in place.
- `tests/integration/alter-table-operations.test.ts` includes
  `"change column type to enum with default"`, which exercises the same
  `text -> enum` + default flow as the pgschema repro.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Original gap** | Missing `USING` and default-safe sequencing | Same |
| **Current upstream state** | Fixed | Fixed |
| **Coverage** | Regression fixture in pgschema | Roundtrip integration test in pg-delta |
| **Remaining follow-up** | None for issue #190 | A separate skipped reverse-direction enum regression still exists, but it does not block the pgschema #190 direction |

## Resolution in pg-delta

pg-delta now resolves the benchmark scenario end-to-end:

1. `AlterTableAlterColumnType.serialize()` adds a `USING` cast for true type
   changes.
2. `diffTables()` wraps the type change in a default-safe drop/re-set flow when
   the original column had a default.
3. The integration suite covers the exact `text -> enum` path with live row
   data and a default value.

## Latest refresh note (2026-08-14)

This refresh advanced checked-in/live `pg-delta` from
`17bfd13b49e94d4e073154921df738707fd03d87` to
`551e88b42977db673a7a9d74f7b7876c2a5e5377`, while checked-in/live
`pgschema` remained `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`.

New open pgschema issue [#537](https://github.com/pgplex/pgschema/issues/537)
re-raises the same `ALTER COLUMN TYPE ... USING` family for a built-in
`text -> integer` conversion without a default. A focused 2026-08-14 pg17
proof probe on current pg-delta emitted:

```sql
ALTER TABLE "public"."nokia_cell_info" ALTER COLUMN "arfcn_dl" DROP DEFAULT
ALTER TABLE "public"."nokia_cell_info" ALTER COLUMN "arfcn_dl" TYPE integer USING "arfcn_dl"::integer
```

That plan still proved cleanly with zero drift, so current pg-delta continues
to cover the broader USING-clause family and benchmark 005 remains **Solved in
pg-delta**.

## Latest refresh note (2026-05-23)

This benchmark entry moved from **tracked** to **solved in pg-delta** after
refreshing to `repos/pg-toolbelt@ee9385daf75f72d443882020247ffd2599050090`.
