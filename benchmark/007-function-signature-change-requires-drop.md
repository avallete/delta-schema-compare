# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
signature. Parameter types, arity, and certain other identity fields require
the old function to be dropped before the new one is created.

pgschema fixed this behavior, and the same parity gap is now resolved in
pg-delta. The refreshed pg-delta tree emits `DROP FUNCTION` before `CREATE
FUNCTION` when a signature change requires replacement, and it has end-to-end
coverage for several variants of the scenario.

Refresh note (2026-05-09): the original pg-toolbelt tracker
[#132](https://github.com/supabase/pg-toolbelt/issues/132) is closed, and
[pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214) is merged.

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

pgschema fixed the issue by treating signature changes as a replacement flow:
drop the old signature, then create the new one, instead of attempting an
invalid in-place `CREATE OR REPLACE`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| DROP before CREATE on parameter type change | ✅ `tests/integration/function-operations.test.ts` (`"function signature: parameter type change"`) |
| DROP before CREATE on arity change | ✅ `tests/integration/function-operations.test.ts` (`"function signature: parameter arity change"`) |
| DROP before CREATE on parameter rename or return-type change | ✅ Covered by dedicated integration cases |
| Dependent object handling during signature change | ✅ Covered by `"function signature change cascades through a dependent view"` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ issue [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed, PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical gap** | Reused `CREATE OR REPLACE` for signature changes | Same parity bug existed originally |
| **Current fix** | Emit replacement flow | Emit `DROP FUNCTION` plus `CREATE FUNCTION` for non-alterable signature changes |
| **Regression coverage** | Upstream fixture coverage | Focused integration coverage for type, arity, name, return-type, and dependent-view cases |

## Resolution in pg-delta

No active parity gap remains for this benchmark item in the refreshed pg-delta
snapshot. The historical issue remains documented here because it was a real
parity gap, but the current implementation now matches pgschema's fixed
behavior.
