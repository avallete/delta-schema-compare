# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed), fixed by [pgschema#327](https://github.com/pgplex/pgschema/pull/327)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a
function's signature when the parameter types, arity, defaults, or return
type require a new function identity. Those changes must be applied as
`DROP FUNCTION <old-signature>` followed by `CREATE FUNCTION <new-signature>`.

pgschema issue #326 covered this class of failure. pg-delta used to have
the same bug, but it is now fixed by
[pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214), which
closed [pg-toolbelt#132](https://github.com/supabase/pg-toolbelt/issues/132).

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE OR REPLACE FUNCTION test_schema.process_item(param1 text)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  RAISE NOTICE 'Processing: %', param1;
END;
$$;
```

**Change to diff:**

```sql
DROP FUNCTION test_schema.process_item(text);

CREATE FUNCTION test_schema.process_item(param1 uuid)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  RAISE NOTICE 'Processing: %', param1::text;
END;
$$;
```

**Expected:** pg-delta emits `DROP FUNCTION ...` before `CREATE FUNCTION ...`.

## How pgschema handled it

pgschema fixed the planner so signature changes use `DROP + CREATE`
instead of `CREATE OR REPLACE`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Detects signature-changing function differences | Yes |
| Emits `DROP FUNCTION` before recreate | Yes |
| Integration test: parameter type change | Yes - `function signature: parameter type change` |
| Integration test: parameter arity change | Yes - `function signature: parameter arity change` |
| Integration test: input-parameter rename-only case | Yes - `function signature: parameter name change only` |
| Integration test: default removal / return-type change | Yes |
| Integration test: dependent-object cascade through a view | Yes |
| Existing pg-toolbelt issue / PR | Yes - issue [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed by merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) |

The coverage lives in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/function-operations.test.ts`.
It now exercises parameter-type changes, arity changes, parameter-name
rewrites, default removal, return-type changes, and a dependent-view
cascade.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| Historical root cause | Used `CREATE OR REPLACE` when signature changes required replacement | Same |
| Current upstream state | Fixed in merged PR #327 | Fixed in merged PR #214 |
| Regression coverage | pgschema fixture coverage | Multiple end-to-end function replacement regressions |

## Resolution in pg-delta

pg-delta now treats function signature changes as replacement operations
and covers the benchmark scenario directly in integration tests. This
benchmark entry remains only as historical context.
