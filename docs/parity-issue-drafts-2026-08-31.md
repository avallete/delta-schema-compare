# Parity issue drafts (2026-08-31)

This document records draft-only text from the 2026-08-31 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. This draft is saved so
the finding can be reviewed in a PR first and then promoted to a real
pg-toolbelt issue only if it still looks correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing umbrella context only:
  - [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
    tracks extraction/model fidelity follow-ups for the active benchmark
    gaps **021** / **022**, but it does not cover a PG18-native
    `NOT NULL ... NOT VALID` rewrite for nullability changes
- Related but not duplicate work:
  - closed [pg-toolbelt#333](https://github.com/supabase/pg-toolbelt/issues/333)
    is the broader correctness-backlog tracker from the clean-room rewrite, but
    it does not contain an exact `SET NOT NULL` / PG18 invalid-not-null item
- No exact open or closed pg-toolbelt issue or PR was found for:
  - pgschema [#564](https://github.com/pgplex/pgschema/issues/564)
  - `ADD COLUMN NOT NULL`
  - `ALTER COLUMN SET NOT NULL`
  - `NOT NULL NOT VALID`

---

## Draft 1 - pgschema issue #564 (safer NOT NULL additions / PG18 native path)

Relates to pgschema issue #564:
https://github.com/pgplex/pgschema/issues/564

Related upstream implementation:
https://github.com/pgplex/pgschema/pull/566

### Context

pgschema issue #564 asks for safer handling when a migration introduces a
`NOT NULL` requirement that may need phased validation or a manual backfill.
The related pgschema implementation in PR #566 now uses PostgreSQL 18's native
invalid `NOT NULL` constraint form on PG18+ targets, emitting:

```sql
ALTER TABLE ... ADD CONSTRAINT ... NOT NULL <column> NOT VALID;
ALTER TABLE ... VALIDATE CONSTRAINT ...;
```

instead of always relying on a direct `SET NOT NULL`-style step.

Current pg-delta does not have an equivalent plan path. In the current table
rules:

- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  `columnClause()` still appends `NOT NULL` inline for added columns
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  `notNull.alter` still emits a plain
  `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

pg-delta already understands ordinary `NOT VALID` / `VALIDATE CONSTRAINT`
flows for constraints, but it does not currently reuse that machinery for
nullable -> `NOT NULL` transitions. That leaves pg-delta without the PG18-native
two-step path pgschema now offers.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
  id integer PRIMARY KEY,
  email text
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.users
  ALTER COLUMN email SET NOT NULL;
```

**Expected:** on PostgreSQL 18+, pg-delta can emit a dependency-safe,
online-friendlier nullability plan such as:

```sql
ALTER TABLE test_schema.users
  ADD CONSTRAINT users_email_not_null NOT NULL email NOT VALID;

ALTER TABLE test_schema.users
  VALIDATE CONSTRAINT users_email_not_null;
```

or an equivalent two-step plan that preserves the same semantics without
falling back to a single immediate `SET NOT NULL`.

**Actual:** current pg-delta emits a direct
`ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`, and there is no PG18-specific
rewrite path for invalid `NOT NULL` constraints.

### Suggested Fix

1. Add a focused regression for the nullable -> `NOT NULL` path under
   `repos/pg-toolbelt/packages/pg-delta/tests/` (likely in the table / plan
   rule coverage) that asserts the emitted PG18 plan does **not** collapse to a
   single `SET NOT NULL`.
2. Thread the target PostgreSQL major version into the nullability planning
   path so the planner can choose a PG18-native strategy.
3. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
   so `notNull.alter` can emit a two-step
   `ADD CONSTRAINT ... NOT NULL <col> NOT VALID` +
   `VALIDATE CONSTRAINT` plan on PG18+, reusing the existing
   `VALIDATE CONSTRAINT` safety / lock metadata patterns already present in
   `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts`.
4. Keep older PostgreSQL versions on the current fallback path, or introduce a
   separate pre-PG18 staged rewrite if the maintainers decide the broader
   safe-migration behavior belongs in pg-delta as well.
