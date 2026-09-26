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
| **Remaining follow-up** | None for issue #190 | Open pg-toolbelt issue [#487](https://github.com/supabase/pg-toolbelt/issues/487) and open PR [#490](https://github.com/supabase/pg-toolbelt/pull/490) track a different enum-to-differently-named-enum cast path, but they do not block the exact pgschema #190 direction |

## Resolution in pg-delta

pg-delta now resolves the benchmark scenario end-to-end:

1. `AlterTableAlterColumnType.serialize()` adds a `USING` cast for true type
   changes.
2. `diffTables()` wraps the type change in a default-safe drop/re-set flow when
   the original column had a default.
3. The integration suite covers the exact `text -> enum` path with live row
   data and a default value.

## Latest refresh note (2026-09-26)

This refresh kept checked-in/live `pg-delta` at
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` and checked-in/live `pgschema` at
`580f4040d0f3c1bfad1497918200c9c1f638a020`.

Open pg-toolbelt PR
[#490](https://github.com/supabase/pg-toolbelt/pull/490) now carries the fix
for adjacent issue
[#487](https://github.com/supabase/pg-toolbelt/issues/487): it adds a focused
enum-to-differently-named-enum regression and changes
`repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` so that when
both the old and new types are enums, the retype routes through `::text` (or
`::text[]` for arrays) instead of emitting a direct enum-to-enum cast.

That remains adjacent to, but does not reopen, benchmark **005**:

- pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) is
  still the `text -> enum` + default-safe sequencing case
- current pg-delta still covers that exact direction in
  `tests/integration/alter-table-operations.test.ts`
- PR **#490** closes the different enum-to-differently-named-enum path and
  does not change the benchmark verdict

Benchmark **005** therefore remains **Solved in pg-delta**, with issue
**#487** / PR **#490** recorded as nearby follow-up context rather than a
parity regression.

## Latest refresh note (2026-09-24)

This refresh kept checked-in/live `pg-delta` at
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` and checked-in/live `pgschema` at
`580f4040d0f3c1bfad1497918200c9c1f638a020`.

New open pg-toolbelt issue
[#487](https://github.com/supabase/pg-toolbelt/issues/487) reports that current
`repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits a
direct enum-to-enum cast for the differently named-type path:

```sql
ALTER TABLE "public"."widgets"
  ALTER COLUMN "status" TYPE public.widget_status
  USING "status"::public.widget_status;
```

That is adjacent to, but does not reopen, benchmark **005**:

- pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) is the
  `text -> enum` + default-safe sequencing case
- current pg-delta still covers that exact direction in
  `tests/integration/alter-table-operations.test.ts`
- issue **#487** is the separate enum-to-differently-named-enum path, where the
  planner should route through `::text::new_enum` instead of a direct cast

Benchmark **005** therefore remains **Solved in pg-delta**, with issue
**#487** recorded as nearby follow-up context rather than a benchmark status
change.

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
