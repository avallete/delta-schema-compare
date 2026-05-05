# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
signature. Changing argument types, return types, or arity requires dropping
the old function identity first and then creating the new one.

pgschema used to emit `CREATE OR REPLACE FUNCTION` for these signature changes,
which fails at runtime or leaves the old overload behind. That behavior is now
fixed upstream.

This benchmark entry is historical now: current pg-delta also handles the same
class of change correctly. The pg-toolbelt tracking issue
[#132](https://github.com/supabase/pg-toolbelt/issues/132) is closed and
[pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214) merged the
DROP+CREATE behavior plus dedicated integration coverage.

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

pgschema now drops the old signature before recreating the function when the
function identity changes.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Signature changes emit `DROP FUNCTION` first | ✅ `src/core/objects/procedure/procedure.diff.ts` now pushes `new DropProcedure(...)` before recreate when `signatureChanged` is true |
| Body-only non-alterable changes still use `CREATE OR REPLACE` | ✅ Same diff keeps `orReplace: true` only for non-signature changes |
| Parameter type change regression | ✅ `tests/integration/function-operations.test.ts` has `"function signature: parameter type change"` |
| Parameter arity change regression | ✅ Same file has `"function signature: parameter arity change"` |
| Return-type change regression | ✅ Same file has `"function signature: return type change"` |
| Dependent-object cascade regression | ✅ Same file has `"function signature change cascades through a dependent view"` |
| Existing pg-toolbelt issue / PR | ✅ Issue [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed by merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) |

The current diff logic now explicitly does:

```typescript
if (signatureChanged) {
  changes.push(new DropProcedure({ procedure: mainProcedure }));
  appendCreateProcedureChanges(branchProcedure);
}
```

That is the exact behavior the benchmark originally identified as missing.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical bug** | Replaced signatures without dropping old identity first | Same historical gap |
| **Current implementation** | Fixed upstream | Fixed in current diff logic |
| **Coverage** | Resolved upstream issue | Multiple integration regressions plus source-level DROP+CREATE handling |

## Resolution in pg-delta

This benchmark entry is retained as historical context, but the parity gap is
now solved in the current pg-delta snapshot.
