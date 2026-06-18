# Parity issue drafts (2026-06-17)

This document records draft-only text from the 2026-06-17 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. This draft is saved so
the finding can be reviewed in a PR first and then promoted to a real
pg-toolbelt issue only if it still looks correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing parity trackers already cover:
  - pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Related but not duplicate work:
  - [pg-toolbelt#147](https://github.com/supabase/pg-toolbelt/pull/147)
    covers composite FK referenced-column order
  - [pg-toolbelt#229](https://github.com/supabase/pg-toolbelt/pull/229)
    covers FK cycle breaking during lazy sort-phase dispatch
- No matching pg-toolbelt issue or PR was found for:
  - pgschema PR #475

---

## Draft 1 - pgschema PR #475 (modified FK depends on added UNIQUE / PRIMARY KEY)

Relates to pgschema PR #475:
https://github.com/pgplex/pgschema/pull/475

### Context

pgschema PR #475 fixes a dependency-ordering bug where a migration adds a new
`UNIQUE` or `PRIMARY KEY` constraint on the parent table and, in the same plan,
recreates a foreign key so it now references that newly added key. PostgreSQL
requires the referenced `UNIQUE` / `PRIMARY KEY` to exist before the foreign key
is recreated; otherwise the apply fails because there is no matching unique
constraint for the referenced columns.

The upstream PR is concrete rather than speculative: it ships dedicated diff
fixtures (`issue_modified_fk_to_new_unique` and
`issue_modified_fk_to_new_unique_reverse_order`) plus a topological-ordering
test. Those fixtures show the required order is "add parent unique first, then
recreate the child FK", even when table names appear in reverse lexical order.

Current pg-delta has adjacent work for composite FK shape correctness and FK
cycle-breaking, but there is no exact issue, PR, or dedicated regression for
"modified FK depends on newly added referenced `UNIQUE` / `PRIMARY KEY`". The
current dependency modeling appears to key on the referenced table / columns,
not explicitly on the newly added referenced key constraint itself, so parity
for this exact scenario remains unverified and is a plausible gap.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.parent_entities (
  id integer PRIMARY KEY
);

CREATE TABLE test_schema.parent_variants (
  id integer PRIMARY KEY,
  parent_entity_id integer NOT NULL,
  CONSTRAINT parent_variants_parent_entity_id_fkey
    FOREIGN KEY (parent_entity_id)
    REFERENCES test_schema.parent_entities (id)
    ON DELETE CASCADE
);

CREATE TABLE test_schema.child_links (
  parent_variant_id integer NOT NULL,
  parent_entity_id integer NOT NULL,
  CONSTRAINT child_links_parent_variant_fkey
    FOREIGN KEY (parent_variant_id)
    REFERENCES test_schema.parent_variants (id)
    ON DELETE CASCADE
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.parent_variants
  ADD CONSTRAINT parent_variants_parent_entity_id_id_key
  UNIQUE (parent_entity_id, id);

ALTER TABLE test_schema.child_links
  DROP CONSTRAINT child_links_parent_variant_fkey;

ALTER TABLE test_schema.child_links
  ADD CONSTRAINT child_links_parent_variant_fkey
  FOREIGN KEY (parent_entity_id, parent_variant_id)
  REFERENCES test_schema.parent_variants (parent_entity_id, id)
  ON DELETE CASCADE;
```

**Expected:** pg-delta adds the parent-side `UNIQUE (parent_entity_id, id)`
before recreating the child foreign key, and the migration converges.

**Actual (current parity evidence):** there is no dedicated pg-delta regression
or exact tracker for this ordering case, and the current dependency graph does
not clearly model the new referenced key as an explicit prerequisite for the
modified FK.

### Suggested Fix

1. Add a focused regression in:
   - `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`
   - or `repos/pg-toolbelt/packages/pg-delta/tests/integration/dependencies-cycles.test.ts`
2. Reproduce the exact sequence above and assert the generated plan orders the
   parent `ADD CONSTRAINT ... UNIQUE` before the child FK recreation.
3. If the test fails, inspect and update dependency modeling and sort behavior
   in:
   - `src/core/objects/table/table.diff.ts`
   - `src/core/expand-replace-dependencies.ts`
   - `src/core/sort/graph-builder.ts`
   - `src/core/sort/cycle-breakers.ts`
4. Keep the new regression even if the eventual implementation routes through
   broader dependency-ordering work, because the distinguishing behavior here is
   "modified FK references a newly added parent key in the same migration".
