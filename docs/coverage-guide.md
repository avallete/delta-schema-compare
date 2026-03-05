# Coverage Guide — How to Evaluate and Track Issues

This guide explains how to decide whether a pgschema issue is already covered
in `@supabase/pg-delta`, and how to write a good tracking issue when it is not.

---

## Step 1 — Understand the pgschema issue

Read the issue title and body and answer:

1. What **PostgreSQL object type** is involved?
   (table column, index, constraint, view, function, trigger, type, policy, …)
2. What **specific DDL operation** or **behaviour** is wrong/missing?
   (e.g. "ADD COLUMN with generated expression", "CREATE INDEX CONCURRENTLY on
   partitioned table", "DROP CONSTRAINT when referenced by foreign key")
3. What **SQL** reproduces the problem (if given)?

---

## Step 2 — Search for coverage in pg-delta

### 2a. Find the right test file

Integration tests live in:

```
repos/pg-toolbelt/packages/pg-delta/tests/integration/
```

File names follow the pattern `<object-type>-operations.test.ts` or
`<feature>.test.ts`.  Quick lookup:

| Object type | Test file |
|---|---|
| TABLE / columns | `alter-table-operations.test.ts` |
| INDEX | `index-operations.test.ts` |
| CONSTRAINT | `constraint-operations.test.ts` |
| FUNCTION | `function-operations.test.ts` |
| VIEW | (search `catalog-diff.test.ts` or `mixed-objects.test.ts`) |
| MATERIALIZED VIEW | `materialized-view-operations.test.ts` |
| POLICY / RLS | `rls-operations.test.ts`, `policy-dependencies.test.ts` |
| SEQUENCE | `sequence-operations.test.ts` |
| TYPE (enum / composite) | search `catalog-diff.test.ts` |
| TRIGGER | search `catalog-diff.test.ts` |
| AGGREGATE | `aggregate-operations.test.ts` |
| PUBLICATION | `publication-operations.test.ts` |
| SUBSCRIPTION | `subscription-operations.test.ts` |
| EXTENSION | `extension-operations.test.ts` |
| FDW | `foreign-data-wrapper-operations.test.ts` |
| EVENT TRIGGER | `event-trigger-operations.test.ts` |

### 2b. Check whether the *specific scenario* is tested

Opening the test file, look for `initialSetup` / `testSql` blocks that match
the scenario.  Simply having a test for the *object type* is not enough —
the exact behaviour (e.g. column generation expression, NOT VALID constraint,
partial index predicate) must be present.

Quick grep:

```bash
grep -rni "<keyword>" repos/pg-toolbelt/packages/pg-delta/tests/
```

### 2c. Check the source object module

```
repos/pg-toolbelt/packages/pg-delta/src/core/objects/<object-type>/
```

If the handler class or the change type for the specific operation is missing,
the issue is definitely not covered.

---

## Step 3 — Verdict

| Situation | Verdict |
|---|---|
| Integration test covers the exact scenario | **Covered** – skip |
| Test exists for object type but not the specific scenario | **Not covered** |
| Object type module exists but no test at all | **Not covered** |
| Object type is entirely absent from `src/core/objects/` | **Not covered** |

---

## Step 4 — Write the tracking issue

Use this template when coverage is missing.  All three sections are required.

---

### Template

```markdown
## Context

<!-- 1-3 paragraphs explaining the gap:
  - What the pgschema issue describes
  - Which pg-delta object module / test file is involved
  - Why this matters for users migrating schemas -->

Relates to pgschema issue #<N>: <URL>

## Test Case to Reproduce

<!-- Runnable SQL that demonstrates the scenario.
     Model it on the roundtripFidelityTest pattern in pg-delta. -->

**Initial state (both databases):**
```sql
CREATE SCHEMA test_schema;
-- ... base objects ...
```

**Change to diff (branch only):**
```sql
-- ... the DDL that pgschema handles but pg-delta does not ...
```

**Expected:** pg-delta generates the correct migration DDL.
**Actual:** pg-delta either generates incorrect DDL or throws an error.

## Suggested Fix

<!-- Be specific.  Reference actual file paths in the pg-delta source.
     Examples:
       - "Add a new `ChangeClass` in `src/core/objects/table/` for ..."
       - "Extend `src/core/catalog.diff.ts` to detect ..."
       - "Add an integration test in `tests/integration/alter-table-operations.test.ts`" -->
```

---

## Labelling

All tracking issues must have:
- **`from-pgschema`** – links back to the upstream source
- **`needs-test`** – signals that a pg-delta test case is needed
