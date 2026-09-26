# Parity refresh report - 2026-07-07

This report records the 2026-07-07 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `62d09975eaac726f055aa62a5baa2961ef7e5a83`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

This refresh does **not** change the benchmark matrix versus 2026-07-06.

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

## 2) Upstream delta on 2026-07-07

This refresh had a pgschema code-head delta but no pg-delta head delta:

- `git submodule update --remote --merge` advanced `pgschema` from
  `d2410fc47267a5c623e62ad4f78edeeee0106e71` to
  `62d09975eaac726f055aa62a5baa2961ef7e5a83`
- `git submodule update --remote --merge` kept `pg-delta` at
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`

Targeted GitHub reads showed:

- [#502](https://github.com/pgplex/pgschema/issues/502) is now **closed** by
  merged [#504](https://github.com/pgplex/pgschema/pull/504) and remains **not
  parity work for pg-delta**
- [#505](https://github.com/pgplex/pgschema/issues/505) is still **open** and
  is already **covered** in current pg-delta by existing trigger drop-order
  coverage
- [#506](https://github.com/pgplex/pgschema/issues/506) is still **open** and
  splits into two pg-delta parity slices:
  - the new-`UNIQUE` table-constraint variant is already **covered**
  - the standalone unique-index variant remains **not covered**
- [#508](https://github.com/pgplex/pgschema/issues/508) is still **open** and
  is **covered** in current pg-delta's normal `CREATE INDEX` path
- [#509](https://github.com/pgplex/pgschema/issues/509) is still **open** and
  remains **not parity work for pg-delta's current default-branch planner**
- the highest live pgschema issue number is now **#509**

On the pg-toolbelt side:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  remains open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  remains open
- no exact pg-toolbelt issue / PR exists yet for benchmark **020**,
  benchmark **021**, benchmark **022**, resolved pgschema
  [#439](https://github.com/pgplex/pgschema/issues/439), resolved pgschema
  [#444](https://github.com/pgplex/pgschema/issues/444), or the newly isolated
  pgschema [#506](https://github.com/pgplex/pgschema/issues/506)
  standalone-unique-index slice

## 3) Executed pg-delta evidence

Focused local source-level probes against the checked-in pg-delta head produced:

```json
{
  "issue020_change_count": 0,
  "issue020_change_types": [],
  "issue021_sql": "CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')",
  "issue022_create_sql": "CREATE TABLE test_schema.users (first_name text, last_name text, full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED)",
  "issue502_comment_sql": "COMMENT ON COLUMN catalog.catalog.title IS 'kept'",
  "issue506_variant1_order": [
    "CreateTable: CREATE TABLE public.child (id uuid, parent_id uuid, tenant text NOT NULL)",
    "AlterTableAddConstraint: ALTER TABLE public.parent ADD CONSTRAINT parent_id_tenant_key UNIQUE (id, tenant)",
    "AlterTableAddConstraint: ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES public.parent(id, tenant)"
  ],
  "issue506_variant2_order": [
    "CreateTable: CREATE TABLE public.child (id uuid, parent_id uuid, tenant text NOT NULL)",
    "AlterTableAddConstraint: ALTER TABLE public.child ADD CONSTRAINT child_parent_id_tenant_fkey FOREIGN KEY (parent_id, tenant) REFERENCES public.parent(id, tenant)",
    "CreateIndex: CREATE UNIQUE INDEX parent_id_tenant_key ON public.parent (id, tenant)"
  ],
  "issue508_create_index_sql": "CREATE INDEX t_cov ON public.parent (id) INCLUDE (tenant)",
  "issue509_order": [
    "DropIndex: DROP INDEX public.idx_notifications_tenant_user",
    "AlterTableDropColumn: ALTER TABLE public.notifications DROP COLUMN valid_period",
    "CreateIndex: CREATE INDEX idx_notifications_tenant_user ON public.notifications (tenant_id, user_id)"
  ]
}
```

Interpretation:

- **#412 / benchmark 020** still diffs to **zero changes**, confirming that the
  table-constraint `NULLS NOT DISTINCT` modifier is still ignored
- **#499 / benchmark 021** still serializes only the bare
  `PARTITION OF ... FOR VALUES ...` statement, confirming that child-specific
  column overrides are still dropped
- **#501 / benchmark 022** still serializes generated columns as `... STORED`,
  confirming that pg-delta still does not preserve PostgreSQL 18 `VIRTUAL`
  generated-column semantics
- **#502** remains non-parity: current column-comment serialization fully
  qualifies `schema.table.column`, so the upstream desired-state SQL rewrite bug
  does not map to pg-delta
- **#506** is now narrowed precisely:
  - variant 1 (new `UNIQUE` table constraint on the existing referenced table)
    is **covered**
  - variant 2 (new standalone unique index on the existing referenced table) is
    **not covered**, because the FK still sorts before the index
- **#508** is **covered** in current pg-delta: `CreateIndex.serialize()`
  preserves `INCLUDE (...)`
- **#509** is not an exact parity gap for current pg-delta: the analogous
  default-branch order is already `DROP INDEX` -> `DROP COLUMN` -> `CREATE
  INDEX`

## 4) Existing tracked and draft-only items

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
- pgschema [#506](https://github.com/pgplex/pgschema/issues/506):
  new table FK before standalone unique index on the pre-existing referenced
  table
  - still open upstream
  - still no exact pg-toolbelt issue or PR found
  - draft tracker text is now saved in
    [`docs/parity-issue-drafts-2026-07-07.md`](./parity-issue-drafts-2026-07-07.md)

## 5) What changed in this refresh

This refresh is primarily an open-issue-state reconciliation pass:

- fast-forward this working branch from the stale April benchmark state to the
  latest 2026-07-06 parity baseline from
  `origin/avallete-ia/schema-comparison-benchmark-929b`
- advance the checked-in `repos/pgschema` submodule pointer to
  `62d09975eaac726f055aa62a5baa2961ef7e5a83`
- keep the `repos/pg-toolbelt` pointer unchanged
- refresh `benchmark/README.md` to the 2026-07-07 snapshot date and update the
  open / resolved screening narrative
- update the benchmark refresh notes in
  `benchmark/020-unique-constraint-nulls-not-distinct.md`,
  `benchmark/021-partition-child-column-overrides.md`, and
  `benchmark/022-virtual-generated-columns.md`
- move `#502` from `review-memory.open` to `review-memory.resolved`
- add current open-screening outcomes for `#505`, `#506`, `#508`, and `#509`
- add a new dated draft note for the uncovered standalone unique-index slice of
  `#506`
- add this dated report

## 6) Validation notes

This refresh validated the state using:

- focused local pg-delta probes (no Docker required) covering:
  - benchmark 020 table-constraint `NULLS NOT DISTINCT`
  - benchmark 021 partition-child column overrides
  - benchmark 022 PostgreSQL 18 `VIRTUAL` generated columns
  - issue 502 column-comment qualification
  - both issue 506 variants
  - issue 508 `INCLUDE` preservation
  - issue 509 index-drop ordering
- repository-local validation:

```bash
python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark
python3 -m json.tool benchmark/review-memory.json >/dev/null
GITHUB_TOKEN="$TOKEN" DRY_RUN=true python3 scripts/compare_issues.py
GITHUB_TOKEN="$TOKEN" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py
git diff --check
```

As in prior refreshes, the dry-run scripts are still expected to return zero
items because they filter on upstream `Bug` / `Feature` labels while the
parity-relevant pgschema items remain mostly unlabeled. The manual unlabeled
issue sweep remains necessary.
