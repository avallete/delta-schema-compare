# Parity issue draft (2026-10-30)

Draft only. Exact searches for `pgschema#674`, `constraint comment`, and
`COMMENT ON CONSTRAINT` on `supabase/pg-toolbelt` returned no issue or pull
request for inherited partition-constraint comments. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) item 4 is view and
materialized-view column comments. This refresh does not open a tracker.

pgschema [#673](https://github.com/pgplex/pgschema/issues/673) (`INCLUDE` on
PRIMARY KEY and UNIQUE) is already covered by verbatim `pg_get_constraintdef`
replay, so it has no draft. pgschema
[#677](https://github.com/pgplex/pgschema/issues/677) is covered by replace
recreation of comment children, so it has no draft.

## Draft — pgschema #674 (comments on inherited partition constraints)

## Context

pgschema issue #674 reports that dump and replay drop comments on table
constraints, including a child partition constraint whose comment differs
from the parent's. The issue is still open. There is no merged pgschema fix
yet.

pg-delta already models comments on constraints it extracts. `pushWithMeta`
(`src/extract/scope.ts`) turns `obj_description(..., 'pg_constraint')` into a
comment satellite. Comment text changes render as `COMMENT ON` without
replacing the constraint (`src/plan/rules/metadata.ts`). `commentTarget`
renders `COMMENT ON CONSTRAINT ... ON schema.table`
(`src/plan/render.ts` lines 51-52). `src/plan/domain-constraint-comment.test.ts`
pins that table form.

Inherited partition constraints are a different path. The constraint query in
`src/extract/relations.ts` keeps only `con.conislocal` rows (line 360). A
partition child's primary key is `conislocal = false`. It is skipped on
purpose: `PARTITION OF` already clones the constraint, and a second
`ADD CONSTRAINT` would fail. `tests/diagnostic-noise.test.ts` records that
skip as a pre-existing gap. Because the comment is a satellite of the
constraint fact, the skipped row takes the child comment with it.
PostgreSQL does not copy the parent's comment onto the clone, so a from-empty
replay leaves the child comment NULL.

Local constraint comments, including the comment on the partitioned parent,
are covered. The uncovered case is a child comment that differs from the
parent.

Relates to pgschema issue #674: https://github.com/pgplex/pgschema/issues/674

## Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE TABLE public.events (
    id integer PRIMARY KEY
) PARTITION BY RANGE (id);

CREATE TABLE public.events_leaf PARTITION OF public.events
    FOR VALUES FROM (0) TO (10);

COMMENT ON CONSTRAINT events_pkey ON public.events IS 'parent key';
```

**Change to diff (branch only):**

```sql
COMMENT ON CONSTRAINT events_leaf_pkey ON public.events_leaf IS 'child key';
```

**Expected:** pg-delta emits `COMMENT ON CONSTRAINT "events_leaf_pkey" ON "public"."events_leaf" IS 'child key'` and does not `DROP` or `ADD` the inherited primary key.
**Actual:** the child constraint is not extracted, so the comment change is invisible. A from-empty plan that creates the partition also never emits the child comment.

## Suggested Fix

Keep inherited (`conislocal = false`) primary-key, unique, and check rows out
of the normal constraint diff. Emitting them as ordinary constraint facts
would `ADD CONSTRAINT` a key `PARTITION OF` already created.

Comments still need a parent fact. `pruneOrphanedSatellites` drops a comment
whose target is absent, and the comment id is `{ kind: "comment", target }`
pointing at the constraint. Two shapes fit the current model:

- Emit a reference-only constraint fact for the inherited row, flagged so
  `constraint` create and drop stay suppressed, and attach the comment
  satellite to that fact with the existing `pushWithMeta` path.
- Or parent the comment on the child table and extend `commentTarget` with a
  payload that still renders `COMMENT ON CONSTRAINT <name> ON <table>`.

The first shape keeps comment identity stable across comment-only edits. A
planner test should show that a child comment change emits only
`COMMENT ON CONSTRAINT`, and that a from-empty plan comments the child after
`CREATE TABLE ... PARTITION OF` without a second `ADD CONSTRAINT`.

Add that test beside `src/plan/domain-constraint-comment.test.ts`. An
integration case in `tests/integration/constraint-operations.test.ts` can
follow once the fact shape exists.
