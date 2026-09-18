# Parity issue drafts (2026-07-03)

This document records draft-only text from the 2026-07-03 pgschema ->
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
- Exact in-flight work already exists for:
  - pgschema PR #479 trigger enabled / disabled state ->
    [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
- Related but not duplicate work:
  - historical partition create support and partition-clone constraint handling
    are already present in current pg-delta
  - open [pg-toolbelt#307](https://github.com/supabase/pg-toolbelt/pull/307)
    remains adjacent `pg-delta-next` work rather than an exact tracker for
    child-specific `PARTITION OF` column elements

No exact open or closed pg-toolbelt issue / PR was found for pgschema #499.

---

## Draft 1 - pgschema #499 (`PARTITION OF` child-specific column elements)

Relates to pgschema issue #499:
https://github.com/pgplex/pgschema/issues/499

### Context

pgschema issue #499 is the low-impact follow-up to pgschema issue #496 /
PR #498. The base `PARTITION OF ... FOR VALUES ...` create path is already
covered in current pg-delta, so detached partition children are **not** the
gap here. The remaining parity slice is narrower: PostgreSQL allows child
partitions to carry per-column `WITH OPTIONS` elements inside the
`PARTITION OF` statement, for example child-specific defaults or `NOT NULL`
overrides.

Current pg-delta extracts the child column metadata, but
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.create.ts`
returns early for partition children and serializes only:

```sql
CREATE TABLE <child> PARTITION OF <parent> FOR VALUES ...
```

That early return means the optional typed table element list is never emitted
for partition children. The created-table branch in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
adds owner / RLS / constraint / comment / privilege changes, but it does not
add follow-up `ALTER COLUMN SET DEFAULT`, `SET NOT NULL`, identity, or
generated-expression changes to recover the missing child-specific column
elements.

In a focused local probe against current pg-delta, a branch-side child
partition with a column default override serialized as:

```sql
CREATE TABLE test_schema.measurements_2024 PARTITION OF test_schema.measurements FOR VALUES IN (2024)
```

The child-column override was dropped entirely.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.measurements (
  partition_year integer NOT NULL,
  reading integer
) PARTITION BY LIST (partition_year);
```

**Change to diff (branch only):**

```sql
CREATE TABLE test_schema.measurements_2024
PARTITION OF test_schema.measurements (
  reading WITH OPTIONS DEFAULT 0
)
FOR VALUES IN (2024);
```

**Expected:** pg-delta emits a `CREATE TABLE ... PARTITION OF ...` statement
that preserves the child-specific column element list, including
`reading WITH OPTIONS DEFAULT 0`, or an equivalent plan that converges to the
same catalog state.

**Actual:** current pg-delta emits only the bare `PARTITION OF ... FOR VALUES`
statement and drops the child-specific column element list entirely.

### Suggested Fix

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/changes/table.create.ts`
   so partition children can optionally serialize PostgreSQL's typed table
   element list before `FOR VALUES ...` when any child column differs from its
   parent on default, nullability, identity, generated expression, or other
   supported `WITH OPTIONS` metadata.
2. If inline serialization is too invasive, teach the created-table path in
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   to emit follow-up column alters for the child-specific metadata right after
   `CreateTable`.
3. Add focused roundtrip coverage in either
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/table-operations.test.ts`
   or
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/partitioned-table-operations.test.ts`
   for a child partition that uses `WITH OPTIONS DEFAULT` (and ideally a second
   case for `WITH OPTIONS NOT NULL`).
