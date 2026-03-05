# pg-delta Codebase Structure

> Reference guide for navigating `repos/pg-toolbelt/packages/pg-delta/`.

## Package overview

`@supabase/pg-delta` is a TypeScript/Bun tool that connects to two PostgreSQL
databases (source + target), extracts their catalogs, diffs them, and generates
ordered DDL migration scripts.

Repo root: `repos/pg-toolbelt/packages/pg-delta/`

## Directory map

```
src/
  index.ts                    Public API surface
  cli/                        CLI entry point (@stricli/core)
  core/
    catalog.diff.ts           Top-level catalog diff orchestration
    catalog.model.ts          Catalog data model
    change.types.ts           Change type definitions
    context.ts                Shared execution context
    depend.ts                 Dependency tracking
    fingerprint.ts            Schema fingerprinting
    expand-replace-dependencies.ts  Dependency expansion helpers
    postgres-config.ts        pg Pool factory (bigint, arrays, int2vector parsers)
    objects/                  Per-object-type modules:
      table/                  CREATE / ALTER / DROP TABLE, column changes
      function/               CREATE / REPLACE / DROP FUNCTION
      view/                   Regular views
      materialized-view/      Materialized views + REFRESH
      index/                  CREATE / DROP INDEX (incl. CONCURRENTLY)
      sequence/               CREATE / ALTER / DROP SEQUENCE
      type/                   Composite, enum, domain types
      policy/                 Row-level security policies
      trigger/                CREATE / DROP TRIGGER
      constraint/             PK, FK, unique, check constraints
      privilege/              GRANT / REVOKE
      aggregate/              Custom aggregates
      publication/            Logical replication publications
      subscription/           Logical replication subscriptions
      extension/              CREATE / DROP EXTENSION
      role/                   Role option changes
      rule/                   Rewrite rules
      foreign-data-wrapper/   FDW, server, user mapping
      event-trigger/          Event triggers
    integrations/             External tool integrations (e.g. Supabase remote)
    plan/                     Migration plan generation and SQL formatting
    sort/                     Dependency-aware change sorting (topological)

tests/
  utils.ts                    withDb / withDbIsolated helpers
  constants.ts                POSTGRES_VERSIONS config
  global-setup.ts             Container pool setup
  container-manager.ts        Singleton Docker container management
  integration/
    roundtrip.ts              roundtripFidelityTest() helper
    alter-table-operations.test.ts
    aggregate-operations.test.ts
    catalog-diff.test.ts
    catalog-model.test.ts
    check-constraint-ordering.test.ts
    complex-dependency-ordering.test.ts
    constraint-operations.test.ts
    default-privileges-*.test.ts
    dependencies-cycles.test.ts
    event-trigger-operations.test.ts
    extension-operations.test.ts
    fk-constraint-ordering.test.ts
    foreign-data-wrapper-operations.test.ts
    function-operations.test.ts
    index-operations.test.ts
    materialized-view-operations.test.ts
    mixed-objects.test.ts
    ordering-validation.test.ts
    partitioned-table-operations.test.ts
    policy-dependencies.test.ts
    privilege-operations.test.ts
    publication-operations.test.ts
    rls-operations.test.ts
    role-option.test.ts
    rule-operations.test.ts
    sequence-operations.test.ts
    subscription-operations.test.ts
    ...
```

## Integration test anatomy

Every integration test follows the same roundtrip pattern:

```typescript
import { describe, test } from "bun:test";
import { POSTGRES_VERSIONS } from "../constants.ts";
import { withDb } from "../utils.ts";
import { roundtripFidelityTest } from "./roundtrip.ts";

for (const pgVersion of POSTGRES_VERSIONS) {
  describe(`<feature> (pg${pgVersion})`, () => {
    test("<scenario>", withDb(pgVersion, async (db) => {
      await roundtripFidelityTest({
        mainSession: db.main,
        branchSession: db.branch,
        initialSetup: `
          -- SQL applied to *both* databases before the test
          CREATE SCHEMA test_schema;
          CREATE TABLE test_schema.users (id integer NOT NULL);
        `,
        testSql: `
          -- SQL representing the *change* to diff and migrate
          ALTER TABLE test_schema.users ADD COLUMN email text;
        `,
      });
    }));
  });
}
```

`roundtripFidelityTest` applies `testSql` to the branch database, diffs it
against the main database, and verifies the generated DDL brings main up to
date with branch.

## How to identify coverage gaps

A pgschema issue is **covered** in pg-delta when:
1. An integration test in `tests/integration/` exercises the *exact DDL
   operation* described in the issue.
2. The corresponding object-type module in `src/core/objects/` handles the
   change class.

A pgschema issue is **not covered** when:
- The object type has tests but the specific scenario (e.g. partial indexes on
  partitioned tables, `GENERATED ALWAYS AS` columns, composite enum mutation)
  has no dedicated test case.
- The feature is entirely missing from `src/core/objects/`.

## Running tests (requires Docker)

```bash
cd repos/pg-toolbelt
bun install
bun run test:pg-delta          # all pg-delta tests
bun test packages/pg-delta/tests/integration/<file>.test.ts  # single file
```
