# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
signature. Parameter types are part of function identity, and even some
signature-adjacent changes such as parameter-name-only rewrites still require a
drop/create flow because PostgreSQL rejects in-place rewrites of the existing
signature.

pgschema fixed this gap in its planner. Current pg-delta now handles the same
family of cases by explicitly treating signature-breaking changes as a replace
operation and letting dependency expansion cascade to dependent objects.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE FUNCTION test_schema.process_item(param1 text)
RETURNS void
LANGUAGE plpgsql
AS $function$
BEGIN
  RAISE NOTICE 'Processing: %', param1;
END;
$function$;
```

**Change to diff:**

```sql
DROP FUNCTION test_schema.process_item(text);
CREATE FUNCTION test_schema.process_item(param1 uuid)
RETURNS void
LANGUAGE plpgsql
AS $function$
BEGIN
  RAISE NOTICE 'Processing: %', param1::text;
END;
$function$;
```

## How pgschema handled it

pgschema moved signature-breaking procedure changes onto a drop/create path
instead of attempting `CREATE OR REPLACE FUNCTION`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Detects signature-breaking changes | ✅ `procedure.diff.ts` computes `signatureChanged` |
| Emits `DROP FUNCTION` before recreate | ✅ `DropProcedure` is pushed before create |
| Integration coverage for parameter type / arity changes | ✅ `tests/integration/function-operations.test.ts` |
| Dependency-aware replacement expansion | ✅ covered by `expand-replace-dependencies.test.ts` |
| Existing pg-toolbelt issue / PR | ✅ [#132](https://github.com/supabase/pg-toolbelt/issues/132) / [#214](https://github.com/supabase/pg-toolbelt/pull/214) |

**Source evidence** (`procedure.diff.ts`):

```typescript
if (signatureChanged) {
  changes.push(new DropProcedure({ procedure: mainProcedure }));
  appendCreateProcedureChanges(branchProcedure);
}
```

**Integration evidence** (`tests/integration/function-operations.test.ts`):

- `"function signature: parameter type change"`
- `"function signature: parameter arity change"`
- `"function signature: parameter name change only"`

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Current state** | Fixed | Fixed |
| **Planner behavior** | Uses drop/create for signature changes | Uses drop/create for signature changes |
| **Regression coverage** | Present upstream | Present in pg-delta integration tests |

## Latest refresh note (2026-05-01)

This benchmark item is now solved in current pg-delta. The older benchmark text
describing a missing `DropProcedure` path is stale relative to
`repos/pg-toolbelt@c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`.
