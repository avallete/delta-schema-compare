# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a
function's parameter types because the parameter types are part of the
function identity. To change a function signature, the old signature must
be dropped before the new one is created.

pgschema originally emitted only `CREATE OR REPLACE FUNCTION` for these
changes. pg-delta used to have the same bug, which this benchmark tracked
through pg-toolbelt issue
[#132](https://github.com/supabase/pg-toolbelt/issues/132).

Refresh note (2026-05-03): pg-delta now handles signature-changing function
updates correctly. pg-toolbelt issue
[#132](https://github.com/supabase/pg-toolbelt/issues/132) is closed and the
fix landed in merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214).

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

pgschema now drops the old signature before creating the replacement
function whenever a signature or another non-alterable function property
changes.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Detects non-alterable function changes | ✅ Present in `src/core/objects/procedure/procedure.diff.ts` |
| Emits `DROP FUNCTION` before replacement create | ✅ Current diff path drops the old signature before creating the new definition |
| Integration regression coverage | ✅ `tests/integration/function-operations.test.ts` covers parameter type change, arity change, parameter rename, default removal, and return-type change |
| Existing pg-toolbelt issue / PR | ✅ [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed, [#214](https://github.com/supabase/pg-toolbelt/pull/214) merged |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Attempted in-place replace for signature changes | Same |
| **Current fix** | Drop old signature then create new function | Same |
| **Regression coverage** | Fixed upstream with regression tests | Integration coverage in `function-operations.test.ts` |

## Resolution in pg-delta

This benchmark entry is now historical. Current pg-delta treats signature
changes as drop-and-create operations and exercises the main failure modes
in integration tests, matching the pgschema fix direction.
