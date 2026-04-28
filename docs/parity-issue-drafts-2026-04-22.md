# Parity issue drafts (2026-04-22)

This document records issue candidates from the latest
pgschema ↔ pg-delta parity refresh.

Status update: these two draft issues have now been created in pg-toolbelt:

- #218 — https://github.com/supabase/pg-toolbelt/issues/218
- #219 — https://github.com/supabase/pg-toolbelt/issues/219

## Duplicate-check summary (pg-toolbelt)

Before drafting, we checked for existing pg-toolbelt issues with relevant
keywords:

- `deferrable unique`
- `enum function privilege`
- `numeric precision`
- `SETOF table dependency`

Result at draft time: no matching open/closed pg-toolbelt issues were found
for the first two scenarios below.

Current state: the scenarios are now tracked by #218 and #219.

---

## Draft 1 — pgschema #404 (DEFERRABLE UNIQUE constraints)

Relates to pgschema issue #404: https://github.com/pgplex/pgschema/issues/404

### Context

pgschema issue #404 describes a gap where `DEFERRABLE INITIALLY DEFERRED` on
`UNIQUE` constraints is dropped during dump/plan/apply. In pg-delta, current
table diff logic compares `deferrable` and `initially_deferred` metadata in
`table.diff.ts`, but there is no dedicated integration scenario that asserts
roundtrip fidelity for a `UNIQUE ... DEFERRABLE INITIALLY DEFERRED` table
constraint.

Because this exact scenario is not currently covered by integration tests, we
should track it as a parity regression-risk and add explicit coverage. If
coverage fails, the same issue should include the code fix.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;
CREATE TABLE test_schema.items (
  id integer PRIMARY KEY,
  code text NOT NULL
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.items
  ADD CONSTRAINT uq_items_code
  UNIQUE (code)
  DEFERRABLE INITIALLY DEFERRED;
```

**Expected:** pg-delta emits migration SQL that preserves
`DEFERRABLE INITIALLY DEFERRED` and roundtrip converges.

**Actual (current parity evidence):** no dedicated integration test exists for
this exact scenario, so behavior is unverified by regression tests.

### Suggested Fix

1. Add a new integration case in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   covering add/alter/drop behavior of `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`.
2. Assert emitted SQL contains `DEFERRABLE INITIALLY DEFERRED` terms.
3. If the test fails, fix constraint serialization/diff handling in:
   - `src/core/objects/table/table.diff.ts`
   - `src/core/objects/table/changes/table.alter.ts`
   - (if needed) constraint extraction fields in `table.model.ts`.

---

## Draft 2 — pgschema #366 (function privileges + enum arg types)

Relates to pgschema issue #366: https://github.com/pgplex/pgschema/issues/366

### Context

pgschema issue #366 reports privilege SQL on functions using enum arguments
being emitted with temporary schema qualification (e.g. `pgschema_tmp_...`).

pg-delta procedure extraction uses `format_type(...)` for `argument_types` and
privilege SQL serialization in `procedure.privilege.ts` reuses these argument
types directly in function signatures. There is currently no integration test
that exercises GRANT/REVOKE on a function with enum-typed arguments and checks
that emitted signatures remain stable and correctly schema-qualified.

This is therefore a parity-risk and missing regression test scenario.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE ROLE app_user;
CREATE SCHEMA test_schema;
CREATE TYPE test_schema.entity_kind AS ENUM ('person', 'company', 'organization');

CREATE FUNCTION test_schema.create_entity(p_name text, p_kind test_schema.entity_kind)
RETURNS uuid
LANGUAGE sql
AS $$ SELECT gen_random_uuid(); $$;
```

**Change to diff (branch only):**

```sql
REVOKE ALL ON FUNCTION test_schema.create_entity(text, test_schema.entity_kind) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION test_schema.create_entity(text, test_schema.entity_kind) TO app_user;
```

**Expected:** pg-delta emits stable `GRANT/REVOKE ... ON FUNCTION ...` SQL
without temporary-schema artifacts and converges roundtrip.

**Actual (current parity evidence):** no dedicated integration test currently
covers privilege diffs for enum-typed function signatures.

### Suggested Fix

1. Add an integration test in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/function-operations.test.ts`
   (or privilege-focused integration suite) that:
   - creates enum type + function(enum arg),
   - modifies function privileges,
   - validates serialized privilege SQL and roundtrip.
2. If serialization is unstable, normalize signature typing in:
   - `src/core/objects/procedure/procedure.model.ts` (argument type extraction)
   - `src/core/objects/procedure/changes/procedure.privilege.ts`
3. Add a regression assertion ensuring no temporary schema names leak into SQL.
