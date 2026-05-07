# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
signature. Parameter types, arity, return type, and some parameter metadata are
part of the function identity, so the old function must be dropped before the
new definition is created.

pgschema originally emitted only `CREATE OR REPLACE FUNCTION` for these cases,
which failed at apply time. That behavior motivated issue #326.

Refresh note (2026-05-07): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#132](https://github.com/supabase/pg-toolbelt/issues/132)
is closed, and
[pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214) merged the
drop-and-recreate logic plus focused integration coverage for signature-change
scenarios.

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
CREATE OR REPLACE FUNCTION test_schema.process_item(param1 uuid)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  RAISE NOTICE 'Processing: %', param1::text;
END;
$$;
```

**Expected DDL:**

```sql
DROP FUNCTION test_schema.process_item(text);
CREATE FUNCTION test_schema.process_item(param1 uuid) ...;
```

## How pgschema handled it

pgschema fixed the issue by emitting `DROP FUNCTION` before `CREATE FUNCTION`
when the signature changes.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Detects signature changes that require replace semantics | ✅ Present in `src/core/objects/procedure/procedure.diff.ts` |
| Emits `DROP FUNCTION` before recreation | ✅ Fixed on current `main` |
| Integration coverage for parameter type / arity / return-type changes | ✅ Present in `tests/integration/function-operations.test.ts` |
| Integration coverage for dependent view cascade | ✅ Present in `tests/integration/function-operations.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed by merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) |

Current integration coverage includes:

- `function signature: parameter type change`
- `function signature: parameter arity change`
- `function signature: parameter name change only`
- `function signature: parameter default removed`
- `function signature: return type change`
- `function signature change cascades through a dependent view`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Used `CREATE OR REPLACE` for non-alterable signature changes | Same |
| **Current fix** | Drops the old signature before re-creating the function | Drops and recreates procedures when non-alterable signature fields change |
| **Coverage** | Fixed upstream | Multiple end-to-end regressions on current `main` |

## Resolution in pg-delta

The current pg-delta snapshot now matches pgschema's handling for function
signature changes. This benchmark entry remains as historical context only and
is no longer an active parity gap.
