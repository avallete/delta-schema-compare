# Parity refresh report - 2026-08-06

This report records the 2026-08-06 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `b1d60e8d95cfc95508956e4c1e89572269410501`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `2929e83981fee139772cc1c60255f1b2592a6f3a`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `2929e83981fee139772cc1c60255f1b2592a6f3a`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-05.md`](./parity-refresh-2026-08-05.md).

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, and **023** remain solved in current pg-delta

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

## 2) Upstream delta on 2026-08-06

This refresh found **one new open upstream issue and several newly closed
upstream issues without changing the active benchmark matrix**:

- the checked-in `pg-delta` pointer now advances from
  `a974b83fc044788caa4ca538d112b62d1873843b` to
  `2929e83981fee139772cc1c60255f1b2592a6f3a`, matching the current
  `pg-toolbelt/main` head that earlier refreshes had already screened as
  adjacent rather than parity-changing
- `pgschema/main` remains
  `b1d60e8d95cfc95508956e4c1e89572269410501`; there is no newer upstream
  pgschema commit than the 2026-08-05 merge of
  [pgschema#529](https://github.com/pgplex/pgschema/pull/529)
- new open pgschema issue
  [#530](https://github.com/pgplex/pgschema/issues/530)
  ("Statement order causes `relation does not exist` error") is already
  **covered** in current pg-delta rather than a new parity gap:
  - pgschema opened upstream PR
    [#531](https://github.com/pgplex/pgschema/pull/531) for a create-ordering
    fix
  - current pg-delta already roundtrips the exact
    `function -> table -> function` chain cleanly by prefixing the plan with
    `SET check_function_bodies = false`, then creating the routines before the
    table and converging without remaining changes
  - existing pg-delta integration coverage already exercises the same family of
    table/function circular-dependency scenarios in
    `table-function-circular-dependency.test.ts` and
    `table-function-dependency-ordering.test.ts`
- newly closed pgschema issue
  [#528](https://github.com/pgplex/pgschema/issues/528)
  (long enum type names truncated in generated column definitions) is also
  **covered** in current pg-delta:
  - a focused pg17 roundtrip on current pg-delta emitted
    `CREATE TABLE repro.deal_area_market_info (... type repro.enum_deal_area_market_info_type NOT NULL)`
    with the full enum name preserved
  - current extraction and serialization path uses
    `format_type(a.atttypid, a.atttypmod)` through `data_type_str`, so there is
    no matching truncation behavior to benchmark
- newly closed pgschema issues
  [#523](https://github.com/pgplex/pgschema/issues/523),
  [#525](https://github.com/pgplex/pgschema/issues/525), and
  [#527](https://github.com/pgplex/pgschema/issues/527) remain **not parity
  work** for pg-delta:
  - `#523` is plan-JSON metadata for downstream migration tooling
  - `#525` is workflow scope about state-based vs migration-based flows
  - `#527` is embedded plan-database artifact availability rather than catalog
    diff or SQL planning behavior
- the open pgschema issue set is now
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518),
  [#519](https://github.com/pgplex/pgschema/issues/519), and
  [#530](https://github.com/pgplex/pgschema/issues/530)
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- adjacent pg-toolbelt work is still unchanged in parity terms:
  open [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains the
  `feat/pg-delta-next` cutover PR, while merged
  [#379](https://github.com/supabase/pg-toolbelt/pull/379),
  [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
  [#381](https://github.com/supabase/pg-toolbelt/pull/381) remain on
  `feat/pg-delta-next`, not on the current default-branch engine

Direct duplicate-search probes still found **no exact pg-toolbelt issue or PR**
for:

- active benchmarks **020**, **021**, and **022**
- older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444)
- the new open pgschema issue
  [#530](https://github.com/pgplex/pgschema/issues/530)
- the newly closed long-enum issue
  [#528](https://github.com/pgplex/pgschema/issues/528)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-06 delta is:

- advance the checked-in `repos/pg-toolbelt` submodule pointer from
  `a974b83fc044788caa4ca538d112b62d1873843b` to
  `2929e83981fee139772cc1c60255f1b2592a6f3a`
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged active gaps plus the newly reviewed open/closed pgschema issues
  [#530](https://github.com/pgplex/pgschema/issues/530),
  [#528](https://github.com/pgplex/pgschema/issues/528),
  [#527](https://github.com/pgplex/pgschema/issues/527),
  [#525](https://github.com/pgplex/pgschema/issues/525), and
  [#523](https://github.com/pgplex/pgschema/issues/523)
- add 2026-08-06 refresh notes to benchmark files **020**, **021**, and
  **022** with focused runtime-probe revalidation on the new checked-in/live
  pg-delta head
- refresh `benchmark/review-memory.json` review fingerprints and timestamps for
  the rechecked open issue set, the new open covered issue
  [#530](https://github.com/pgplex/pgschema/issues/530), the active benchmark
  gaps, and the newly closed issues
  [#523](https://github.com/pgplex/pgschema/issues/523),
  [#525](https://github.com/pgplex/pgschema/issues/525),
  [#527](https://github.com/pgplex/pgschema/issues/527), and
  [#528](https://github.com/pgplex/pgschema/issues/528)
- add this report as the 2026-08-06 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set including
    [#530](https://github.com/pgplex/pgschema/issues/530)
  - open pgschema PRs
    [#517](https://github.com/pgplex/pgschema/pull/517),
    [#520](https://github.com/pgplex/pgschema/pull/520), and
    [#531](https://github.com/pgplex/pgschema/pull/531)
  - newly closed pgschema issues
    [#523](https://github.com/pgplex/pgschema/issues/523),
    [#525](https://github.com/pgplex/pgschema/issues/525),
    [#527](https://github.com/pgplex/pgschema/issues/527), and
    [#528](https://github.com/pgplex/pgschema/issues/528)
  - the exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - adjacent pg-toolbelt work
    [#299](https://github.com/supabase/pg-toolbelt/pull/299),
    [#379](https://github.com/supabase/pg-toolbelt/pull/379),
    [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
    [#381](https://github.com/supabase/pg-toolbelt/pull/381)
- duplicate-search queries for benchmarks **020** through **022**, the
  draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), and the new issue
  [#530](https://github.com/pgplex/pgschema/issues/530) plus closed issue
  [#528](https://github.com/pgplex/pgschema/issues/528)
- a focused Docker-backed pg-delta probe suite showing:
  - pgschema [#530](https://github.com/pgplex/pgschema/issues/530) is already
    covered: the exact roundtrip converged cleanly with the plan prefix
    `SET check_function_bodies = false`
  - pgschema [#528](https://github.com/pgplex/pgschema/issues/528) is already
    covered: the generated `CREATE TABLE` preserved the full enum type name
  - benchmark **020** still plans **zero statements** when toggling an existing
    `UNIQUE` table constraint to `UNIQUE NULLS NOT DISTINCT`
  - benchmark **021** still emits only
    `CREATE TABLE ... PARTITION OF ... FOR VALUES ...` without child-specific
    `DEFAULT` / `NOT NULL` overrides
  - benchmark **022** still serializes the PostgreSQL 18 case as
    `GENERATED ALWAYS AS (...) STORED` instead of preserving `VIRTUAL`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- those dry-run script runs still remain expected to return **0** parity items
  because the parity-relevant pgschema issues are still mostly missing the
  upstream `Bug` / `Feature` labels that the automation filters on, including
  open issues [#518](https://github.com/pgplex/pgschema/issues/518),
  [#519](https://github.com/pgplex/pgschema/issues/519), and
  [#530](https://github.com/pgplex/pgschema/issues/530)
- `git diff --check`
