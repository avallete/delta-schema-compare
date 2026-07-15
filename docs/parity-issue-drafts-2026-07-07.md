# Parity issue drafts (2026-07-07)

This document records draft-only text from the 2026-07-07 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. This draft is saved so
the finding can be reviewed in a PR first and then promoted to a real
pg-toolbelt issue only if it still looks correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing exact parity trackers already cover:
  - pgschema #404 ->
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 ->
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Related but not duplicate work:
  - [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285) and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) cover broader
    replacement-dependency recreation, not the specific FK-before-unique-index
    ordering slice below
  - [pg-toolbelt#307](https://github.com/supabase/pg-toolbelt/pull/307)
    remains adjacent `pg-delta-next` planner work rather than an exact tracker
    for the current default-branch engine
- No exact pg-toolbelt issue or PR was found for:
  - the standalone unique-index slice of pgschema #506

---

## Draft 1 - pgschema #506 (new table FK before standalone unique index)

Relates to pgschema issue #506:
https://github.com/pgplex/pgschema/issues/506

### Context

pgschema issue #506 actually contains two parity shapes:

1. a new table whose FK depends on a new `UNIQUE` **table constraint** added to
   an existing referenced table
2. a new table whose FK depends on a new standalone **unique index** added to
   an existing referenced table

Current pg-delta already covers the first slice. In a focused local ordering
probe, the table-constraint case sorted as:

```text
CREATE TABLE public.child ...
ALTER TABLE public.parent ADD CONSTRAINT parent_id_tenant_key UNIQUE (id, tenant)
ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (...)
```

That means the newly added `UNIQUE` table constraint is created before the FK.
The remaining uncovered slice is narrower: when the referenced uniqueness is a
standalone unique index, current pg-delta instead sorts:

```text
CREATE TABLE public.child ...
ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (...)
CREATE UNIQUE INDEX parent_id_tenant_key ON public.parent (id, tenant)
```

That ordering can fail on apply with PostgreSQL `SQLSTATE 42830` because the FK
lands before the uniqueness that makes the reference legal.

Why the gap remains:

- `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
  emits FKs for created tables as follow-up `ALTER TABLE ... ADD CONSTRAINT`
  changes
- `repos/pg-toolbelt/packages/pg-delta/src/core/depend.ts` adds FK dependencies
  to matching `PRIMARY KEY` / `UNIQUE` **constraints** via `constraint_deps`
- there is no matching dependency edge for a brand-new standalone **unique
  index**, so the FK can still sort ahead of the index create

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.parent (
  id uuid PRIMARY KEY,
  tenant text NOT NULL
);
```

**Change to diff (branch only):**

```sql
CREATE UNIQUE INDEX parent_id_tenant_key
  ON test_schema.parent (id, tenant);

CREATE TABLE test_schema.child (
  id uuid PRIMARY KEY,
  parent_id uuid,
  tenant text NOT NULL,
  FOREIGN KEY (parent_id, tenant)
    REFERENCES test_schema.parent (id, tenant)
);
```

**Expected:** pg-delta creates the standalone unique index before the child FK,
or otherwise defers the FK until after the referenced uniqueness exists.

**Actual:** current pg-delta sorts the child FK before the unique index create,
so the plan can apply the FK while the referenced `(id, tenant)` uniqueness is
not yet present.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/depend.ts`
   so branch-catalog dependency extraction can map an FK to a newly created
   standalone unique index when that index is the object satisfying the
   reference.
2. If dependency extraction alone is awkward, teach the created-table path in
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   to defer just the affected FK out of the new table's immediate post-create
   constraint batch when the target uniqueness is created later in the same
   plan.
3. Add focused regression coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/fk-constraint-ordering.test.ts`
   (or a nearby dependency-ordering test file) for **both** variants:
   - new `UNIQUE` table constraint on existing parent -> still covered
   - new standalone unique index on existing parent -> fixed by the new logic
4. Assert the generated order explicitly so the standalone unique-index slice
   cannot regress back to `ADD child FK` before `CREATE UNIQUE INDEX`.
