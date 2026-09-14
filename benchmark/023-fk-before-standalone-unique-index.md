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

The remaining parity gap was narrower and more precise: when the referenced
uniqueness was a standalone unique index, older pg-delta builds sorted the
child foreign key before the unique index create. PostgreSQL could reject that
order with `SQLSTATE 42830` because the referenced `(id, tenant)` uniqueness did
not exist yet when the foreign key was applied.

## Refresh note (2026-08-04)

This refresh kept the checked-in `pg-delta` baseline at
`a974b83fc044788caa4ca538d112b62d1873843b` while live
`pg-toolbelt/main` advanced to `2929e83981fee139772cc1c60255f1b2592a6f3a`;
`pgschema` remained at `325dac205047a7850a52ee9f9ff35ec18c145dcc`.

The new live pg-delta delta is the alpha.5 `pg-topo` byte-offset parser fix
from [pg-toolbelt#372](https://github.com/supabase/pg-toolbelt/pull/372),
released by [pg-toolbelt#374](https://github.com/supabase/pg-toolbelt/pull/374).
A focused live pg17 plan + apply probe for this exact benchmark still emitted
the dependency-safe order:

```text
CREATE TABLE test_schema.child (id uuid NOT NULL, parent_id uuid, tenant text NOT NULL)
ALTER TABLE test_schema.child ADD CONSTRAINT child_pkey PRIMARY KEY (id)
CREATE UNIQUE INDEX parent_id_tenant_key ON test_schema.parent (id, tenant)
ALTER TABLE test_schema.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES test_schema.parent(id, tenant)
```

The plan still applied cleanly with no remaining changes, so the exact
standalone unique-index slice remains **Solved in pg-delta**.

## Refresh note (2026-07-28)

This refresh advanced the checked-in `pg-delta` baseline from
`c0decd173d191bc470bf7b8c8dd3e862f08ae398` to
`a974b83fc044788caa4ca538d112b62d1873843b`, while `pgschema` remained at
`a0acf0b9590a6bd7b3455d795f7e547490aa9699`.

The new checked-in/live pg-delta state now includes the adjacent pg-topo
ordering fix from [pg-toolbelt#361](https://github.com/supabase/pg-toolbelt/pull/361).
A focused local pg17 plan probe for this exact benchmark now emits:

```text
CREATE TABLE test_schema.child (id uuid NOT NULL, parent_id uuid, tenant text NOT NULL)
ALTER TABLE test_schema.child ADD CONSTRAINT child_pkey PRIMARY KEY (id)
CREATE UNIQUE INDEX parent_id_tenant_key ON test_schema.parent (id, tenant)
ALTER TABLE test_schema.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES test_schema.parent(id, tenant)
```

A matching pg17 roundtrip probe also converged successfully. The exact
standalone unique-index slice is therefore now **covered** in current
pg-delta even though no exact pg-toolbelt issue was ever opened for it. This
benchmark file is retained as a historical record, but benchmark 023 now moves
to **Solved in pg-delta**.

## Refresh note (2026-07-18)

This refresh advanced the checked-in `pg-delta` baseline from
`ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` to
`c0decd173d191bc470bf7b8c8dd3e862f08ae398`, while `pgschema` remained at
`e18d9ede7973537919c02f25eced5c97271af1dc`.

The new pg-delta delta was the alpha.32 non-superuser extraction fix. Its only
`depend.ts` edits were in the `pg_user_mapping` extraction queries, so it did
not change the foreign-key-versus-standalone-unique-index dependency path
behind this benchmark. Targeted duplicate searches still found no exact
pg-toolbelt issue or PR for this standalone-index slice, so benchmark 023
still remained **Not covered** at that time.

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

**Actual on current pg-delta:** this scenario now converges. The generated plan
creates the standalone unique index before adding the child foreign key, and a
focused pg17 roundtrip probe succeeded end-to-end.

## How pgschema handled it

pgschema closed issue #506 in PR #507 by deferring the problematic new-table
foreign key until the referenced uniqueness exists later in the same plan. That
upstream fix originally left the remaining standalone-unique-index parity gap on
pg-delta's side, but current pg-delta now covers the same exact slice as well.

The updated pgschema source also keeps comments in `internal/diff/table.go`
explaining that foreign keys depending on replacement or newly introduced
uniqueness may need to be deferred until after the create / modify phase.

## Current pg-delta status

| Aspect | Status |
|---|---|
| New-table FK depending on a new `UNIQUE` table constraint | Yes - covered by current dependency extraction and sort behavior |
| New-table FK depending on a new standalone unique index | Yes - focused 2026-07-28 pg17 plan + roundtrip probes converge on the exact scenario |
| Dependency edge from FK to referenced PK / `UNIQUE` constraint | Yes - current plan ordering already handles this case |
| Dependency edge from FK to referenced standalone unique index | Covered in behavior - current plan ordering now places `CREATE UNIQUE INDEX` before `ADD child FK` on the exact benchmark SQL |
| Integration regression for the standalone unique-index slice | No exact committed regression yet - coverage was revalidated with focused 2026-07-28 local probes |
| Existing exact pg-toolbelt issue / PR | No exact issue; current behavior is covered after adjacent merged pg-topo fix [#361](https://github.com/supabase/pg-toolbelt/pull/361) |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Planner representation** | Detects that the FK must wait for the referenced uniqueness | Current checked-in/live planner now also emits the safe order on the exact benchmark SQL |
| **Constraint-backed uniqueness** | Defers correctly | Already covered |
| **Standalone unique-index-backed uniqueness** | Fixed upstream in the resolved issue | Now covered on current pg-delta |
| **Current parity state** | Fixed | Covered |

## Plan to handle it in pg-delta

1. No additional planner change is currently needed for the exact
   standalone-unique-index slice; current pg-delta now emits the dependency-safe
   order on the benchmark SQL.
2. Promote the focused 2026-07-28 probe into a permanent committed regression
   in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/fk-constraint-ordering.test.ts`
   if the pg-toolbelt maintainers want this exact slice locked in explicitly.
3. Retain this benchmark file as historical parity evidence that the slice used
   to be uncovered and is now solved.
