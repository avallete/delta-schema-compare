# Parity refresh report - 2026-07-08

This report records the 2026-07-08 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- `pg-delta` (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)

## 1) Benchmark issue status refresh

This refresh **does** change the benchmark matrix versus 2026-07-07.

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

### Net-new benchmark delta

- pgschema [#506](https://github.com/pgplex/pgschema/issues/506) is now
  **closed upstream** by merged
  [pgschema#507](https://github.com/pgplex/pgschema/pull/507)
- current pg-delta still covers only the new-`UNIQUE` table-constraint slice,
  while the standalone unique-index slice remains uncovered
- that narrower residual slice is now promoted from
  [`docs/parity-issue-drafts-2026-07-07.md`](./parity-issue-drafts-2026-07-07.md)
  into new benchmark **023**

## 2) Upstream delta on 2026-07-08

This refresh had a code-head delta in **both** submodules:

- `git submodule update --remote --merge` advanced `pg-delta` from
  `9284412d71635308ebb0c1537e0b0183d2cfa4da` to
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- `git submodule update --remote --merge` advanced `pgschema` from
  `62d09975eaac726f055aa62a5baa2961ef7e5a83` to
  `e18d9ede7973537919c02f25eced5c97271af1dc`

Targeted GitHub reads showed:

- [#505](https://github.com/pgplex/pgschema/issues/505) is now **closed** by
  merged [#511](https://github.com/pgplex/pgschema/pull/511) and remains
  **covered** in current pg-delta
- [#506](https://github.com/pgplex/pgschema/issues/506) is now **closed** by
  merged [#507](https://github.com/pgplex/pgschema/pull/507)
  - the new-`UNIQUE` table-constraint variant remains **covered**
  - the standalone unique-index variant remains **not covered** and is now
    benchmarked as [023](../benchmark/023-fk-before-standalone-unique-index.md)
- [#508](https://github.com/pgplex/pgschema/issues/508) is now **closed** by
  merged [#512](https://github.com/pgplex/pgschema/pull/512) and remains
  **covered** in current pg-delta
- [#509](https://github.com/pgplex/pgschema/issues/509) is now **closed** by
  merged [#510](https://github.com/pgplex/pgschema/pull/510) and remains **not
  parity work for pg-delta's current default-branch planner**
- the highest live pgschema issue number remains **#509**; higher numbers
  visible today (**#510**, **#511**, **#512**) are PRs rather than issues

On the pg-toolbelt side:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  remains open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  remains open
- no exact pg-toolbelt issue / PR exists yet for benchmarks **020**, **021**,
  **022**, or **023**
- resolved pgschema [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444) still have no exact
  pg-toolbelt tracker; the historical drafts remain for review context

## 3) Executed pg-delta evidence

Focused local source-level probes against the checked-in pg-delta head produced:

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
- **#501 / benchmark 022** still serializes generated columns as `... STORED`,
  confirming that pg-delta still does not preserve PostgreSQL 18 `VIRTUAL`
  generated-column semantics
- **#506 / benchmark 023** is now pinned precisely:
  - variant 1 (new `UNIQUE` table constraint on the existing referenced table)
    is **covered**
  - variant 2 (new standalone unique index on the existing referenced table) is
    **not covered**, because the child FK still sorts before the index

## 4) Existing tracked and historical draft-only items

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still closed upstream
  - still no exact pg-toolbelt issue or PR found
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - still closed upstream
  - related pg-toolbelt work exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - there is still no exact tracker

## 5) What changed in this refresh

- fast-forward this working branch from the 2026-07-07 baseline
- advance the checked-in `repos/pg-toolbelt` pointer to
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`
- advance the checked-in `repos/pgschema` pointer to
  `e18d9ede7973537919c02f25eced5c97271af1dc`
- refresh `benchmark/README.md` to the 2026-07-08 snapshot date and add
  benchmark **023**
- refine benchmark **020** so it documents the exact active gap: toggling an
  existing plain `UNIQUE` table constraint to `UNIQUE NULLS NOT DISTINCT`
- refresh benchmark **021** and **022** notes against the new submodule heads
- move pgschema issues `#505`, `#506`, `#508`, and `#509` from
  `review-memory.open` to `review-memory.resolved`
- update `benchmark/review-memory.json` fingerprints for the actively reviewed
  open and benchmarked issues
- add this dated report

## 6) Validation notes

This refresh validated the state using:

- focused local pg-delta probes (no Docker required) covering:
  - benchmark 020 table-constraint `NULLS NOT DISTINCT` toggle and create path
  - benchmark 021 partition-child column overrides
  - benchmark 022 PostgreSQL 18 `VIRTUAL` generated columns
  - both issue 506 variants
- repository-local validation:

```bash
python3 -m json.tool benchmark/review-memory.json >/dev/null
GITHUB_TOKEN="$TOKEN" DRY_RUN=true python3 scripts/compare_issues.py
GITHUB_TOKEN="$TOKEN" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py
git diff --check
```

As in prior refreshes, the dry-run scripts are still expected to return zero
items because they filter on upstream `Bug` / `Feature` labels while the
parity-relevant pgschema items remain mostly unlabeled. The manual unlabeled
issue sweep remains necessary.
