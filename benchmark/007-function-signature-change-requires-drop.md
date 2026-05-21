# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
parameter types because the parameter list is part of the function identity.
When the signature changes, the old function must be dropped first and the new
signature created afterwards.

pgschema originally emitted only `CREATE OR REPLACE FUNCTION` for signature
changes, which failed at runtime.

Refresh note (2026-05-16): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#132](https://github.com/supabase/pg-toolbelt/issues/132)
is closed, and
[pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214) merged the
required `DROP FUNCTION` + `CREATE FUNCTION` behavior together with focused
integration coverage.

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

pgschema now emits `DROP FUNCTION` before `CREATE FUNCTION` whenever a function
signature changes in a way PostgreSQL cannot alter in place.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Detects non-alterable signature changes | ✅ Present in `procedure.diff.ts` |
| Emits `DROP FUNCTION` before recreation | ✅ Fixed |
| Integration coverage for parameter type / arity / rename changes | ✅ Present in `tests/integration/function-operations.test.ts` |
| Dependency-aware signature-change coverage | ✅ Includes a signature change that cascades through a dependent view |
| Existing pg-toolbelt issue / PR | ✅ [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed by merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) |

Current integration coverage now includes:

- `"function signature: parameter type change"`
- `"function signature: parameter arity change"`
- `"function signature: parameter name change only"`
- `"function signature: return type change"`
- `"function signature change cascades through a dependent view"`

All of those cases assert that pg-delta emits `DROP FUNCTION ...` before the
replacement `CREATE FUNCTION ...`.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Missing DROP before CREATE on signature changes | Same historical gap |
| **Current fix** | Emit explicit drop/recreate flow | Detect signature changes and switch from `OR REPLACE` to drop + create |
| **Regression coverage** | Issue-driven upstream fix | Multiple integration regressions, including dependency fallout through views |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the current pg-delta
snapshot. The benchmark entry now serves as historical context for why function
signature diffs use a full drop/recreate path instead of `CREATE OR REPLACE`.
