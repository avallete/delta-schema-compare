# Function Signature Change Requires DROP Before CREATE

> pgschema issue [#326](https://github.com/pgplex/pgschema/issues/326) (closed)

## Context

PostgreSQL does not allow `CREATE OR REPLACE FUNCTION` to change a function's
parameter types because the parameter types are part of the function's identity
(OID). To change parameter types, you must `DROP FUNCTION` the old signature
first, then `CREATE FUNCTION` with the new signature.

pgschema was generating only `CREATE OR REPLACE FUNCTION` for signature changes,
which fails with `ERROR: cannot change name of input parameter`.

pg-delta has the **same bug**. When non-alterable fields change (including
`argument_types`), the diff logic in `procedure.diff.ts` generates
`CreateProcedure` with `orReplace: true` — but never emits a `DropProcedure`
for the old signature.

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

**Actual pg-delta DDL (buggy):**

```sql
CREATE OR REPLACE FUNCTION test_schema.process_item(param1 uuid) ...;
-- ERROR: cannot change name of input parameter "param1"
-- (or creates a second overload instead of replacing)
```

## How pgschema handled it

pgschema now emits `DROP FUNCTION` before `CREATE FUNCTION` when the function
signature (argument types) changes.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Detects signature changes via NON_ALTERABLE_FIELDS | ✅ |
| Generates DROP before CREATE on signature change | ❌ **Bug** |
| Integration test for signature change | ❌ None |

**Source evidence** (`procedure.diff.ts` lines 198–201):
```typescript
if (nonAlterablePropsChanged) {
  changes.push(
    new CreateProcedure({ procedure: branchProcedure, orReplace: true }),
  );
}
```

No `DropProcedure` is pushed before the `CreateProcedure`.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Missing DROP for signature changes | Same — only CREATE OR REPLACE emitted |
| **Fix scope** | Diff planner | `procedure.diff.ts` lines 198–201 |
| **Severity** | 🔴 Migration fails at runtime | 🔴 Same |

## Plan to handle it in pg-delta

1. **Fix `procedure.diff.ts`** — when `nonAlterablePropsChanged` is true AND
   `argument_types` differ, emit `DropProcedure` for the old signature
   **before** `CreateProcedure` for the new one:
   ```typescript
   if (nonAlterablePropsChanged) {
     // If argument types changed, DROP old signature first
     if (!deepEqual(mainProcedure.argument_types, branchProcedure.argument_types)) {
       changes.push(new DropProcedure({ procedure: mainProcedure }));
     }
     changes.push(
       new CreateProcedure({ procedure: branchProcedure, orReplace: !needsDrop }),
     );
   }
   ```
2. **Add integration test** in `tests/integration/function-operations.test.ts`:
   - Change a function parameter from `text` to `uuid`
   - Change parameter count
   - Verify the DDL contains DROP then CREATE (not CREATE OR REPLACE)
3. **Handle cascading dependencies** — dropping a function may require
   dropping dependent objects first (triggers, views, defaults). Verify the
   dependency sorter handles this.
