# Parity refresh report - 2026-07-29

This report records the 2026-07-29 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `2d864f3282ea3f0ba4cfa749e366cfdff1ae4fb7`)
- checked-in and live `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-28.md`](./parity-refresh-2026-07-28.md).

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

## 2) Upstream delta on 2026-07-29

This refresh found **one code-head delta without a parity reclassification**:

- `pgschema/main` advanced from `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
  to `2d864f3282ea3f0ba4cfa749e366cfdff1ae4fb7` via the `v1.12.1` release-bump
  commit; the open pgschema issue set still remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- no pgschema issues closed upstream since the 2026-07-28 refresh
- no pgschema PRs merged upstream since the 2026-07-28 refresh
- live `pg-toolbelt/main` still remains
  `a974b83fc044788caa4ca538d112b62d1873843b`
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- the only newer pg-toolbelt activity is open issue
  [#365](https://github.com/supabase/pg-toolbelt/issues/365) plus
  closed-unmerged PR
  [#366](https://github.com/supabase/pg-toolbelt/pull/366) for case-colliding
  schema export paths on the `feat/pg-delta-next` / [#299](https://github.com/supabase/pg-toolbelt/pull/299)
  line; neither maps to the active benchmarks or the older draft-only gaps
- direct duplicate probes still found no exact pg-toolbelt issue or PR for
  active benchmarks **020** through **022**, the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), or open pgschema issue
  [#519](https://github.com/pgplex/pgschema/issues/519)
- the last focused pg17 runtime probes for
  [#404](https://github.com/pgplex/pgschema/issues/404) /
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218),
  [#366](https://github.com/pgplex/pgschema/issues/366) /
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219), and
  benchmark **023** still stand on unchanged `pg-toolbelt/main`, so those items
  keep the same tracked / solved classifications

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-07-29 delta is:

- advance the checked-in `repos/pgschema` submodule pointer from
  `a0acf0b9590a6bd7b3455d795f7e547490aa9699` to
  `2d864f3282ea3f0ba4cfa749e366cfdff1ae4fb7`
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged 2026-07-29 parity conclusions and the new checked-in pgschema head
- refresh `benchmark/review-memory.json` review fingerprints and timestamps for
  the rechecked open issues, exact tracked parity issues, active benchmark gaps,
  older draft-only uncovered findings, and the already-solved benchmark **023**
- correct the stored `issue_updated_at` value for open pgschema issue
  [#519](https://github.com/pgplex/pgschema/issues/519) so it matches the
  current upstream issue timestamp
- add this report as the 2026-07-29 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the unchanged open pgschema issue set
  - merged pgschema PRs since 2026-07-28 (**none**)
  - the new pg-toolbelt issue / PR pair
    [#365](https://github.com/supabase/pg-toolbelt/issues/365) /
    [#366](https://github.com/supabase/pg-toolbelt/pull/366)
  - the exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- current pg-delta source/test evidence showing:
  - `NULLS NOT DISTINCT` coverage still exists only for unique indexes in
    `packages/pg-delta/tests/integration/index-operations.test.ts`, not the
    active table-constraint gap from benchmark **020**
  - `packages/pg-delta/src/core/objects/table/changes/table.create.ts` still
    returns the bare `PARTITION OF ... FOR VALUES ...` statement for partition
    children before column-definition serialization, leaving no path for the
    child-specific overrides from benchmark **021**
  - `table.create.ts` / `table.alter.ts` still serialize generated columns as
    `GENERATED ALWAYS AS (...) STORED` with no current `VIRTUAL` handling for
    benchmark **022**
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
