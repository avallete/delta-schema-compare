# New-table FK ordered before standalone unique index on the referenced table

> pgschema issue [#506](https://github.com/pgplex/pgschema/issues/506) (closed), fixed by [pgschema#507](https://github.com/pgplex/pgschema/pull/507)

## Context

pgschema issue #506 reports an apply-time ordering failure when a new table
introduces a foreign key that depends on uniqueness being added to an existing
referenced table in the same plan. The upstream issue bundled two related
shapes:

1. the referenced uniqueness is added as a new `UNIQUE` **table constraint**
2. the referenced uniqueness is added as a new standalone **unique index**

Current pg-delta already covers the first slice. A focused July 8 planner probe
against the new head still sorts the table-constraint case as:

```text
CREATE TABLE public.child ...
ALTER TABLE public.parent ADD CONSTRAINT parent_id_tenant_key UNIQUE (id, tenant)
ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (...)
```

The remaining parity gap is narrower and more precise: when the referenced
uniqueness is a standalone unique index, current pg-delta still sorts the child
foreign key before the unique index create. PostgreSQL can reject that order
with `SQLSTATE 42830` because the referenced `(id, tenant)` uniqueness does not
exist yet when the foreign key is applied.

## Refresh note (2026-07-18)

This refresh advanced the checked-in `pg-delta` baseline from
`ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` to
`c0decd173d191bc470bf7b8c8dd3e862f08ae398`, while `pgschema` remained at
`e18d9ede7973537919c02f25eced5c97271af1dc`.

The new pg-delta delta is the alpha.32 non-superuser extraction fix. Its only
`depend.ts` edits are in the `pg_user_mapping` extraction queries, so it does
not change the foreign-key-versus-standalone-unique-index dependency path
behind this benchmark. Targeted duplicate searches still found no exact
pg-toolbelt issue or PR for this standalone-index slice, so benchmark 023
remains **Not covered**.

## Refresh note (2026-07-08)

This benchmark is newly promoted from the draft note saved in
[`docs/parity-issue-drafts-2026-07-07.md`](../docs/parity-issue-drafts-2026-07-07.md).

The July 8 refresh advanced both checked-in submodules:

- `pg-delta` from `9284412d71635308ebb0c1537e0b0183d2cfa4da` to
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- `pgschema` from `62d09975eaac726f055aa62a5baa2961ef7e5a83` to
  `e18d9ede7973537919c02f25eced5c97271af1dc`

Upstream closed pgschema issue #506 by merging
[pgschema#507](https://github.com/pgplex/pgschema/pull/507). A focused local
planner probe against the new pg-delta head still emits the uncovered
standalone-index slice in this order:

```text
CreateTable: CREATE TABLE public.child (id uuid NOT NULL, parent_id uuid, tenant text NOT NULL)
AlterTableAddConstraint: ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES public.parent(id, tenant)
CreateIndex: CREATE UNIQUE INDEX parent_id_tenant_key ON public.parent (id, tenant)
```

No exact open or closed pg-toolbelt issue / PR was found for this standalone
unique-index slice through the 2026-07-08 refresh, so it now belongs in the
resolved-issue benchmark set.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.parent (
    id uuid PRIMARY KEY,
    tenant text NOT NULL
);
```

**Change to diff:**

```sql
CREATE UNIQUE INDEX parent_id_tenant_key
  ON test_schema.parent (id, tenant);

CREATE TABLE test_schema.child (
    id uuid PRIMARY KEY,
    parent_id uuid,
    tenant text NOT NULL,
    CONSTRAINT child_parent_id_tenant_fkey
      FOREIGN KEY (parent_id, tenant)
      REFERENCES test_schema.parent (id, tenant)
);
```

**Expected:** pg-delta defers the child foreign key until after the standalone
unique index exists, or otherwise emits an equivalent dependency-safe plan.

**Actual:** current pg-delta sorts the child foreign key before the standalone
unique index create. The broader issue is partially covered because the
table-constraint variant already orders correctly, but the standalone
unique-index variant is still not covered.

## How pgschema handled it

pgschema closed issue #506 in PR #507 by deferring the problematic new-table
foreign key until the referenced uniqueness exists later in the same plan. The
upstream fix resolves the ordering failure on the pgschema side, so the
remaining parity gap is now entirely on pg-delta's default-branch planner.

The updated pgschema source also keeps comments in `internal/diff/table.go`
explaining that foreign keys depending on replacement or newly introduced
uniqueness may need to be deferred until after the create / modify phase.

## Current pg-delta status

| Aspect | Status |
|---|---|
| New-table FK depending on a new `UNIQUE` table constraint | Yes - covered by current dependency extraction and sort behavior |
| New-table FK depending on a new standalone unique index | No - the FK still sorts before the index create |
| Dependency edge from FK to referenced PK / `UNIQUE` constraint | Yes - `src/core/depend.ts` emits `constraint_deps` for referenced constraints |
| Dependency edge from FK to referenced standalone unique index | No - there is no equivalent dependency extraction for a brand-new standalone unique index |
| Integration regression for the standalone unique-index slice | No - `tests/integration/fk-constraint-ordering.test.ts` has no exact case for this scenario |
| Existing exact pg-toolbelt issue / PR | No - none found through the 2026-07-18 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Planner representation** | Detects that the FK must wait for the referenced uniqueness | Treats the FK like a normal post-create table constraint |
| **Constraint-backed uniqueness** | Defers correctly | Already covered |
| **Standalone unique-index-backed uniqueness** | Fixed upstream in the resolved issue | Still missing an exact dependency edge |
| **Current parity state** | Fixed | Not covered |

## Plan to handle it in pg-delta

1. Extend `repos/pg-toolbelt/packages/pg-delta/src/core/depend.ts` so branch
   dependency extraction can map a foreign key to a newly created standalone
   unique index when that index is what satisfies the reference.
2. If catalog dependency extraction alone is awkward, teach the created-table
   path in
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   to defer just the affected foreign key out of the immediate post-create
   batch when the referenced uniqueness is created later in the same plan.
3. Add focused regression coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/fk-constraint-ordering.test.ts`
   (or a nearby dependency-ordering test file) for both variants:
   - new `UNIQUE` table constraint on existing parent -> stays covered
   - new standalone unique index on existing parent -> fixed by the new logic
4. Assert the final order explicitly so the standalone unique-index slice
   cannot regress back to `ADD child FK` before `CREATE UNIQUE INDEX`.
