# Parity refresh report - 2026-07-12

This report records the 2026-07-12 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)
- live `pg-toolbelt` `main` (`d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`), which is still the same CI-only commit ahead already seen on 2026-07-10 and 2026-07-11

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-11.md`](./parity-refresh-2026-07-11.md).

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Active resolved-issue benchmark gaps

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#499](https://github.com/pgplex/pgschema/issues/499):
  child-specific column overrides in `PARTITION OF` create path
  - benchmark file:
    [`benchmark/021-partition-child-column-overrides.md`](../benchmark/021-partition-child-column-overrides.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#501](https://github.com/pgplex/pgschema/issues/501):
  PostgreSQL 18 `VIRTUAL` generated columns
  - benchmark file:
    [`benchmark/022-virtual-generated-columns.md`](../benchmark/022-virtual-generated-columns.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#506](https://github.com/pgplex/pgschema/issues/506):
  new-table FK ordered before a standalone unique index on the referenced table
  - benchmark file:
    [`benchmark/023-fk-before-standalone-unique-index.md`](../benchmark/023-fk-before-standalone-unique-index.md)
  - no matching pg-toolbelt issue or PR was found through this refresh

### Rechecked local parity probe on the checked-in engine

A focused local pg-delta probe was rerun against the checked-in
`ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` baseline and still produced:

```json
{
  "issue020_toggle_change_count": 0,
  "issue020_toggle_sql": [],
  "issue020_create_change_count": 1,
  "issue020_create_sql": [
    "AlterTableAddConstraint: ALTER TABLE test_schema.pgschema_repro_nulls_new ADD CONSTRAINT pgschema_repro_nulls_new_uniq UNIQUE NULLS NOT DISTINCT (a, b)"
  ],
  "issue021_sql": "CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')",
  "issue022_create_sql": "CREATE TABLE test_schema.users (first_name text, last_name text, full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED)",
  "issue022_alter_sql": "ALTER TABLE test_schema.users ADD COLUMN full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED",
  "issue506_variant1_order": [
    "CreateTable: CREATE TABLE public.child (id uuid NOT NULL, parent_id uuid, tenant text NOT NULL)",
    "AlterTableAddConstraint: ALTER TABLE public.parent ADD CONSTRAINT parent_id_tenant_key UNIQUE (id, tenant)",
    "AlterTableAddConstraint: ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES public.parent(id, tenant)"
  ],
  "issue506_variant2_order": [
    "CreateTable: CREATE TABLE public.child (id uuid NOT NULL, parent_id uuid, tenant text NOT NULL)",
    "AlterTableAddConstraint: ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES public.parent(id, tenant)",
    "CreateIndex: CREATE UNIQUE INDEX parent_id_tenant_key ON public.parent (id, tenant)"
  ]
}
```

Interpretation:

- **#412 / benchmark 020** still reproduces as a **zero-change** diff when
  toggling an existing plain `UNIQUE` table constraint to
  `UNIQUE NULLS NOT DISTINCT`, even though creating a brand-new `NULLS NOT
  DISTINCT` table constraint still works
- **#499 / benchmark 021** still serializes only the bare
  `PARTITION OF ... FOR VALUES ...` statement, confirming that child-specific
  column overrides are still dropped
- **#501 / benchmark 022** still serializes generated columns as `... STORED`
  in both create and add-column paths, confirming that pg-delta still does not
  preserve PostgreSQL 18 `VIRTUAL` generated-column semantics
- **#506 / benchmark 023** still splits the scenario the same way:
  - variant 1 (new `UNIQUE` table constraint on the existing referenced table)
    is **covered**
  - variant 2 (new standalone unique index on the existing referenced table) is
    **not covered**, because the child FK still sorts before the index create

## 2) Upstream delta on 2026-07-12

This refresh found **no new upstream parity movement** after the 2026-07-11
sweep:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- the highest live pgschema issue remains **#509**; higher visible numbers
  **#510**, **#511**, and **#512** are PRs rather than issues, and **#513+**
  still do not exist
- the only open pgschema issue with recent upstream activity in this area is
  [#450](https://github.com/pgplex/pgschema/issues/450), and it remains **not
  parity work for pg-delta**
- checked-in `pg-delta` remains
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`, while live `pg-toolbelt` `main`
  remains `d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`
- the diff between those two pg-toolbelt SHAs is still limited to CI /
  repo-meta files:
  - `.github/MAINTAINERS.md`
  - `.github/scripts/contribution-gate.test.ts`
  - `.github/scripts/contribution-gate.ts`
  - `.github/workflows/contribution-gate.yml`
- no `packages/pg-delta/**` source files or pg-delta integration tests changed,
  so benchmarks **020**, **021**, **022**, and **023** keep the same
  `Not covered` verdicts
- exact open pg-toolbelt trackers still exist only for
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- no new exact pg-toolbelt issue or PR was found for benchmarks **020**, **021**,
  **022**, or **023**, nor for the older draft-only resolved items
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
- open pg-toolbelt rewrite work remains adjacent rather than duplicative:
  - [#299](https://github.com/supabase/pg-toolbelt/pull/299) is still an
    unmerged `pg-delta-next` promotion PR
  - [#329](https://github.com/supabase/pg-toolbelt/pull/329) is still open on
    `pg-delta-next`
  - neither PR changes the current default-branch parity matrix until that
    rewrite stack merges and the benchmark is re-baselined

## 3) What changed in this refresh

Because the latest-state sweep found no parity change, this refresh keeps the
benchmark matrix and checked-in submodule pointers unchanged and records the
result as another dated no-delta report:

- add this report as the 2026-07-12 latest-state sweep
- annotate `benchmark/README.md` so the source-of-truth matrix points to this
  follow-up, states that there was no fresh parity movement after 2026-07-11,
  and notes that the open `pg-delta-next` rewrite stack is still out of scope
  for the current default-branch matrix
- refresh the reviewed timestamps in `benchmark/review-memory.json` for the
  rechecked open, tracked, active-gap, and draft-only items

## 4) Validation notes

This refresh was validated with:

- targeted pg-delta unit tests:
  - `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  - `bun test packages/pg-delta/src/core/objects/table/changes/table.create.test.ts`
  - `bun test packages/pg-delta/src/core/sort/sort-changes.test.ts`
  - `bun test packages/pg-delta/src/core/objects/index/index.diff.test.ts`
  - result: **37 pass / 0 fail**
- the focused local probe output shown above from
  `bun packages/pg-delta/tmp_parity_probe.ts`
- live GitHub issue / PR checks for pgschema **#366**, **#404**, **#412**,
  **#439**, **#444**, **#450**, **#493**, **#499**, **#501**, **#506**, and
  **#509**, plus pg-toolbelt **#218**, **#219**, **#263**, **#273**, **#285**,
  **#291**, **#299**, **#307**, **#310**, **#315**, **#323**, and **#329**
- direct git diff of live pg-toolbelt `main` versus the checked-in baseline,
  confirming the same CI-only `.github/**` delta as the 2026-07-10 and
  2026-07-11 sweeps
- repository maintenance checks:
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `git diff --check`

The unlabeled-issue caveat still applies: the parity-relevant pgschema issues
remain mostly unlabeled, so `compare_issues.py` and `compare_resolved.py` can
still return zero candidates even when the manual latest-state sweep finds
useful parity updates.
