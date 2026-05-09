# Table Constraint `UNIQUE ... NULLS NOT DISTINCT`

> pgschema issue [#412](https://github.com/pgplex/pgschema/issues/412) (closed), fixed by [pgschema#413](https://github.com/pgplex/pgschema/pull/413)

## Context

pgschema issue #412 reported that `pgschema dump` dropped `NULLS NOT DISTINCT`
from **table-level** unique constraints. That is distinct from the already
solved unique-index scenario tracked in [016](016-unique-index-nulls-not-distinct.md):
here the PostgreSQL object is a named table constraint,
`CONSTRAINT ... UNIQUE NULLS NOT DISTINCT (...)`, not a standalone
`CREATE UNIQUE INDEX`.

This distinction matters because current pg-delta already covers the index form
from pgschema #355, but the table-constraint diff path still has a blind spot.
`table.model.ts` captures the rendered constraint definition via
`pg_get_constraintdef(c.oid, true)`, yet `table.diff.ts` does not compare the
full `definition` field when deciding whether a same-named constraint changed.
If the name and key columns stay the same, a transition between plain `UNIQUE`
and `UNIQUE NULLS NOT DISTINCT` can be missed.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.accounts (
    id integer PRIMARY KEY,
    email text,
    CONSTRAINT accounts_email_key UNIQUE (email)
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.accounts
  DROP CONSTRAINT accounts_email_key;

ALTER TABLE test_schema.accounts
  ADD CONSTRAINT accounts_email_key
  UNIQUE NULLS NOT DISTINCT (email);
```

**Expected:** pg-delta detects the unique-constraint definition change and emits
drop-and-recreate DDL that preserves `NULLS NOT DISTINCT`.

**Actual parity evidence:** current pg-delta has no integration regression for
the table-constraint form, and `src/core/objects/table/table.diff.ts` does not
compare the full constraint definition. The solved index benchmark in item 016
therefore should not be treated as proof that pgschema #412 is covered.

## How pgschema handled it

pgschema PR #413 preserved the `NULLS NOT DISTINCT` clause when dumping and
planning table-level unique constraints. The fix landed on 2026-04-29 and
closed issue #412.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Constraint extraction preserves full definition text | ✅ `src/core/objects/table/table.model.ts` uses `pg_get_constraintdef(c.oid, true)` |
| Diff compares `constraint_type`, deferrability, temporal flags, and key columns | ✅ `src/core/objects/table/table.diff.ts` |
| Diff compares the full constraint `definition` for same-name constraints | ❌ Missing |
| Integration test for `UNIQUE NULLS NOT DISTINCT` as a table constraint | ❌ Missing from `tests/integration/constraint-operations.test.ts` |
| Equivalent **index** form already covered | ✅ benchmark [016](016-unique-index-nulls-not-distinct.md) / `tests/integration/index-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during this refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Object shape** | Table constraint with `UNIQUE NULLS NOT DISTINCT (...)` | Table constraints are modeled separately from indexes |
| **Current behavior** | Fixed in merged PR #413 | Extracts the definition text, but does not use it to detect same-name definition-only changes |
| **Coverage** | Covered by the upstream fix | No dedicated roundtrip coverage for the table-constraint form |
| **Risk** | Addressed upstream | A same-name unique constraint can silently keep weaker semantics if the planner misses the change |

## Plan to handle it in pg-delta

1. Add a regression case to
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   for a named table constraint using `UNIQUE NULLS NOT DISTINCT (...)`.
2. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so definition-only changes on same-name constraints are treated as a
   drop-and-recreate change. Comparing `definition` directly is the simplest
   first step.
3. Keep benchmark item [016](016-unique-index-nulls-not-distinct.md) scoped to
   the **index** case so this table-constraint gap is not hidden by the solved
   index work.
