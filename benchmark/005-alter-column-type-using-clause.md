# Column Type Change Missing `USING` Clause

> pgschema issue [#190](https://github.com/pgplex/pgschema/issues/190) (closed)

## Context

When changing a column's type (for example `text` -> custom enum), PostgreSQL
requires a `USING` clause if the cast is not implicit. If the column also has a
default that no longer matches the new type, the default must be dropped before
the type change and re-applied afterwards.

pgschema originally emitted `ALTER COLUMN ... TYPE ...` without the `USING`
clause and without the default-safe sequencing, so the migration failed at
runtime.

Refresh note (2026-05-13): this parity gap is now fixed in pg-delta. The old
draft implementation in
[pg-toolbelt#146](https://github.com/supabase/pg-toolbelt/pull/146) was
superseded; the landed fix is
[pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231), and the
tracking issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) is
closed.

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

pgschema fixed the issue by emitting the required `USING` cast for type changes
that cannot be applied implicitly and by sequencing default removal /
reapplication around the `ALTER COLUMN ... TYPE` statement.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `AlterTableAlterColumnType` serializer | ✅ Adds `USING <column>::<new_type>` when the previous type differs |
| Default-safe type-change flow | ✅ `table.diff.ts` emits `DROP DEFAULT` -> `TYPE ... USING ...` -> `SET DEFAULT` when needed |
| Unit coverage | ✅ `src/core/objects/table/table.diff.test.ts` asserts the full three-statement flow |
| Integration coverage | ✅ `tests/integration/alter-table-operations.test.ts` covers `text -> enum`, `varchar -> integer`, and `enum -> text` default-preserving cases |
| Existing pg-toolbelt issue / PR | ✅ [#130](https://github.com/supabase/pg-toolbelt/issues/130) closed by merged PR [#231](https://github.com/supabase/pg-toolbelt/pull/231) |

Current local pg-delta now emits the exact sequence that was missing in earlier
refreshes:

```typescript
expect(typeChangesWithDefault.map((c) => c.serialize())).toEqual([
  "ALTER TABLE public.t2 ALTER COLUMN a DROP DEFAULT",
  "ALTER TABLE public.t2 ALTER COLUMN a TYPE test_schema.status USING a::test_schema.status",
  "ALTER TABLE public.t2 ALTER COLUMN a SET DEFAULT 'active'::test_schema.status",
]);
```

That expectation lives in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.test.ts`.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Missing `USING` and default-safe sequencing | Same historical gap in ALTER COLUMN TYPE planning |
| **Current fix** | Emit explicit cast + default choreography | `AlterTableAlterColumnType` adds `USING`; `diffTables()` wraps type changes with default drop/set |
| **Regression coverage** | Fixture-backed fix in pgschema | Unit and integration coverage for both cast and default-sensitive paths |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the current pg-delta
snapshot. The remaining historical context is useful mainly to explain why
`ALTER COLUMN TYPE` now carries both explicit `USING` casts and default-safe
statement ordering.
