# PostgreSQL 18 `VIRTUAL` generated columns

> pgschema issue [#501](https://github.com/pgplex/pgschema/issues/501) (closed), fixed by [pgschema#503](https://github.com/pgplex/pgschema/pull/503)

## Context

pgschema issue #501 reports that PostgreSQL 18 `VIRTUAL` generated columns were
being rewritten into invalid non-generated SQL during pgschema's plan output.
pg-delta does not share that exact desired-state SQL rewrite path, but the
user-visible parity gap still exists: current pg-delta does not preserve the
generated-column kind and collapses the PostgreSQL catalog signal down to a
single generated/not-generated boolean.

That means pg-delta can still lose the distinction between `VIRTUAL` and
`STORED` generated columns even though it avoids the precise upstream bug
mechanism. This benchmark tracks the now-resolved upstream scenario after
pgschema merged its fix on `main`, while pg-delta's checked-in default-branch
engine still lacks exact coverage.

## Refresh note (2026-07-08)

This refresh advanced both checked-in submodules:

- `pg-delta` from `9284412d71635308ebb0c1537e0b0183d2cfa4da` to
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- `pgschema` from `62d09975eaac726f055aa62a5baa2961ef7e5a83` to
  `e18d9ede7973537919c02f25eced5c97271af1dc`

The newer upstream pgschema head merges follow-up fixes for issues #505, #506,
#508, and #509, but none of that changes this exact generated-column-kind
scenario.

During this refresh, a focused local pg-delta probe against the current create
path still serialized the PostgreSQL 18 case as:

```sql
CREATE TABLE test_schema.users (first_name text, last_name text, full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED)
```

The `VIRTUAL` keyword was lost and replaced by `STORED`, so this scenario
remains not covered. No exact open or closed pg-toolbelt issue / PR was found
for this narrow generated-column-kind gap through the 2026-07-08 refresh.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
    first_name text,
    last_name text
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.users
  ADD COLUMN full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL;
```

**Expected:** pg-delta preserves the PostgreSQL 18 `VIRTUAL` generated-column
kind when diffing and serializing the migration plan.

**Actual:** current pg-delta models generated columns only as a boolean
`is_generated` flag and serializes generated expressions as `... STORED`, so
`VIRTUAL` is not represented in the current table model or create/alter SQL
output.

## How pgschema handled it

pgschema fixed the issue in PR #503 by preserving the generated-column kind
through inspection and diff planning instead of collapsing it to a single
generated/not-generated state.

The merged fix added regression data under:

- `repos/pgschema/testdata/diff/create_table/issue_501_virtual_generated_column/`

That fixture now records `GENERATED ALWAYS AS (...) VIRTUAL` in the expected
plan output, confirming that upstream keeps the PostgreSQL 18 keyword intact in
the resolved scenario.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Table model preserves generated/not-generated state | Partially - `table.model.ts` records only `is_generated: boolean` |
| Table model preserves `VIRTUAL` vs `STORED` kind | No - `attgenerated` is collapsed to a boolean |
| `CREATE TABLE` serialization preserves `VIRTUAL` | No - `table.create.ts` hard-codes `... STORED` |
| `ALTER TABLE ... ADD COLUMN` serialization preserves `VIRTUAL` | No - `table.alter.ts` hard-codes `... STORED` |
| Integration regression for PostgreSQL 18 `VIRTUAL` generated columns | No - `alter-table-operations.test.ts` covers only `STORED` cases |
| Existing exact pg-toolbelt issue / PR | No - none found through the 2026-07-08 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog / IR representation** | Preserves generated-column kind through the resolved fix | Collapses `attgenerated` to `is_generated: boolean` |
| **Plan / SQL emission** | Emits `VIRTUAL` when the schema requires it | Emits `GENERATED ALWAYS AS (...) STORED` for generated expressions |
| **Coverage** | Regression fixture for the upstream PG18 scenario | No exact integration regression for `VIRTUAL` |
| **Current parity state** | Fixed | Not covered |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/base.model.ts` and
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   so generated columns preserve the actual PostgreSQL `attgenerated` kind
   instead of only a boolean.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so `VIRTUAL` vs `STORED` is treated as a meaningful change rather than being
   collapsed into a single generated/not-generated state.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.create.ts`
   and
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.alter.ts`
   so generated-column SQL preserves the correct PostgreSQL 18 keyword.
4. Add focused roundtrip coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/alter-table-operations.test.ts`
   for PostgreSQL 18 `VIRTUAL` generated columns.
5. Add lower-level unit coverage around
   `CreateTable.serialize()` / `AlterTableAddColumn.serialize()` so future
   regressions cannot silently convert `VIRTUAL` back to `STORED`.
