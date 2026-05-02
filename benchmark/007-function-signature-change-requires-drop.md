# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed),
> fixed by [pgschema#327](https://github.com/pgplex/pgschema/pull/327)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
signature. Parameter types, return type, and some other signature-level fields
are part of the function identity, so changing them requires `DROP FUNCTION`
followed by `CREATE FUNCTION`.

pgschema originally emitted only a replacement-style create and failed at apply
time. pg-delta had the same parity gap until
[pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214) merged.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE OR REPLACE FUNCTION test_schema.process_item(param1 text)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE NOTICE 'Processing: %', param1;
END;
$$;
```

**Change to diff:**

```sql
DROP FUNCTION test_schema.process_item(text);

CREATE FUNCTION test_schema.process_item(param1 uuid)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE NOTICE 'Processing: %', param1::text;
END;
$$;
```

**Expected:** pg-delta emits `DROP FUNCTION ...` before recreating the new
signature.

## How pgschema handled it

pgschema PR #327 switched signature-changing routine diffs to an explicit
drop-and-recreate flow so PostgreSQL receives valid DDL for parameter-type,
parameter-name, and return-type changes.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Signature-changing routine diffs use DROP + CREATE | ✅ Fixed in [pg-toolbelt#214](https://github.com/supabase/pg-toolbelt/pull/214) |
| Integration test for parameter type change | ✅ Present in `tests/integration/function-operations.test.ts` |
| Integration test for arity / parameter-name / return-type changes | ✅ Present |
| Historical pg-toolbelt issue | ✅ [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed |

Current integration coverage includes:

- `function signature: parameter type change`
- `function signature: parameter arity change`
- `function signature: parameter name change only`
- `function signature: return type change`

all in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/function-operations.test.ts`.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | Replacement path ignored function identity rules | Same |
| **Current fix** | Explicit DROP + CREATE on signature changes | Explicit DROP + CREATE on signature changes |
| **Regression coverage** | Merged fix PR + fixtures | Multiple end-to-end integration cases |

## Resolution in pg-delta

This benchmark entry is now historical. The parity gap is solved in current
pg-delta: the relevant integration tests assert that signature-level changes
roundtrip through the required `DROP FUNCTION` + `CREATE FUNCTION` flow.
