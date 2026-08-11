# Parity refresh report - 2026-08-07

This report records the 2026-08-07 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `2929e83981fee139772cc1c60255f1b2592a6f3a`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `2929e83981fee139772cc1c60255f1b2592a6f3a`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-06.md`](./parity-refresh-2026-08-06.md).

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

## 2) Upstream delta on 2026-08-07

This refresh found **newly merged upstream ordering fixes without changing the
active benchmark matrix**:

- the checked-in `pg-delta` pointer still matches live `pg-toolbelt/main` at
  `2929e83981fee139772cc1c60255f1b2592a6f3a`
- `pgschema/main` advanced from
  `b1d60e8d95cfc95508956e4c1e89572269410501` to
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`
- pgschema issue
  [#530](https://github.com/pgplex/pgschema/issues/530)
  ("Statement order causes `relation does not exist` error") is now **closed**
  by merged [#531](https://github.com/pgplex/pgschema/pull/531) and remains
  **covered** in current pg-delta:
  - the exact 2026-08-07 pg17 roundtrip still converged cleanly
  - current pg-delta prefixes the routine-bearing plan with
    `SET check_function_bodies = false`
  - the generated plan still applied successfully with zero remaining changes
- newly closed pgschema issue
  [#532](https://github.com/pgplex/pgschema/issues/532)
  (`FOREIGN KEY` depending on a later `UNIQUE` constraint) is also already
  **covered** in current pg-delta:
  - a focused 2026-08-07 pg17 runtime probe planned
    `ALTER TABLE ... ADD CONSTRAINT UNIQUE` before the dependent
    `ALTER TABLE ... ADD CONSTRAINT FOREIGN KEY`
  - the generated plan applied successfully with zero remaining changes
  - there is still no exact pg-toolbelt issue or PR to update because the
    current default-branch engine already converges on the scenario
- the open pgschema issue set is now
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- open pgschema parity-relevant PRs now narrow back to
  [#517](https://github.com/pgplex/pgschema/pull/517) and
  [#520](https://github.com/pgplex/pgschema/pull/520)
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- adjacent pg-toolbelt work remains unchanged in parity terms:
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
- the newly closed ordering issue
  [#532](https://github.com/pgplex/pgschema/issues/532)
- the previously open ordering issue
  [#530](https://github.com/pgplex/pgschema/issues/530), which is now closed
  upstream and still needs no duplicate tracker

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-07 delta is:

- advance the checked-in `repos/pgschema` submodule pointer from
  `b1d60e8d95cfc95508956e4c1e89572269410501` to
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  newly merged pgschema fixes for
  [#530](https://github.com/pgplex/pgschema/issues/530) and
  [#532](https://github.com/pgplex/pgschema/issues/532) while keeping the
  active gaps unchanged
- add 2026-08-07 refresh notes to benchmark files **020**, **021**, and
  **022** with focused runtime-probe revalidation on the unchanged pg-delta
  head
- refresh `benchmark/review-memory.json` review fingerprints and timestamps for
  the current open issue set, the still-active benchmark gaps, the draft-only
  uncovered items [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), and the newly closed
  issues [#530](https://github.com/pgplex/pgschema/issues/530) /
  [#532](https://github.com/pgplex/pgschema/issues/532)
- add this report as the 2026-08-07 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set
  - merged pgschema PRs
    [#531](https://github.com/pgplex/pgschema/pull/531) and
    [#533](https://github.com/pgplex/pgschema/pull/533)
  - still-open pgschema PRs
    [#517](https://github.com/pgplex/pgschema/pull/517) and
    [#520](https://github.com/pgplex/pgschema/pull/520)
  - exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - adjacent pg-toolbelt work
    [#285](https://github.com/supabase/pg-toolbelt/pull/285),
    [#299](https://github.com/supabase/pg-toolbelt/pull/299),
    [#379](https://github.com/supabase/pg-toolbelt/pull/379),
    [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
    [#381](https://github.com/supabase/pg-toolbelt/pull/381)
- duplicate-search queries for benchmarks **020** through **022**, the
  draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), and the newly closed
  issues [#530](https://github.com/pgplex/pgschema/issues/530) /
  [#532](https://github.com/pgplex/pgschema/issues/532)
- a focused Docker-backed pg-delta probe suite showing:
  - pgschema [#530](https://github.com/pgplex/pgschema/issues/530) is still
    covered: the exact pg17 roundtrip emitted
    `SET check_function_bodies = false`, applied cleanly, and left zero
    remaining changes
  - pgschema [#532](https://github.com/pgplex/pgschema/issues/532) is already
    covered: the exact pg17 plan ordered `UNIQUE` before the dependent
    `FOREIGN KEY`, applied cleanly, and left zero remaining changes
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
  open issues [#518](https://github.com/pgplex/pgschema/issues/518) and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- `git diff --check`
