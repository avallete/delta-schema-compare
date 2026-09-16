# Parity refresh report - 2026-07-28

This report records the 2026-07-28 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`)
- checked-in and live `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)

## 1) Benchmark status refresh

This refresh found **one benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-27.md`](./parity-refresh-2026-07-27.md):
benchmark **023** is now **Solved in pg-delta**.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, and now **023** remain solved in current pg-delta

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

## 2) Upstream delta on 2026-07-28

This refresh found one real upstream issue-state delta and one already-live
code delta worth reclassifying:

- `pgschema/main` still remains `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- the current open pgschema issue set still remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#519](https://github.com/pgplex/pgschema/issues/519) was updated on
  2026-07-27 and now links to open upstream candidate fix
  [pgschema#520](https://github.com/pgplex/pgschema/pull/520); it still remains
  **not parity work** for pg-delta because the repeated diff depends on
  pgschema's temporary desired-state schema normalization path rather than
  live-catalog diff behavior
- live `pg-toolbelt/main` advanced from `b732ce6b45eb9f3344ba3fc531ee28822730362e`
  to `a974b83fc044788caa4ca538d112b62d1873843b` via CI-only PR
  [#364](https://github.com/supabase/pg-toolbelt/pull/364), while the parity-
  relevant code already in that head includes merged privilege-diff work from
  [#357](https://github.com/supabase/pg-toolbelt/pull/357) /
  [#358](https://github.com/supabase/pg-toolbelt/pull/358), merged pg-topo
  ordering work from
  [#361](https://github.com/supabase/pg-toolbelt/pull/361), and release PR
  [#363](https://github.com/supabase/pg-toolbelt/pull/363)
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- focused pg17 runtime probes for the tracked
  [#404](https://github.com/pgplex/pgschema/issues/404) /
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#366](https://github.com/pgplex/pgschema/issues/366) /
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  scenarios both converged on current pg-delta, so those items remain tracked
  **coverage** issues rather than benchmark promotions
- direct duplicate probes still found no exact pg-toolbelt issue or PR for
  active benchmarks **020** through **022**, the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), or open pgschema issue
  [#519](https://github.com/pgplex/pgschema/issues/519)

## 3) What changed in this refresh

The 2026-07-28 delta is:

- advance the checked-in `repos/pg-toolbelt` submodule pointer from
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398` to
  `a974b83fc044788caa4ca538d112b62d1873843b`
- mark benchmark **023**
  ([pgschema#506](https://github.com/pgplex/pgschema/issues/506)) as solved in
  `benchmark/README.md` and refresh the historical benchmark file
  [`benchmark/023-fk-before-standalone-unique-index.md`](../benchmark/023-fk-before-standalone-unique-index.md)
- leave benchmarks **020**, **021**, and **022** active and unchanged because
  the current live pg-delta delta does not touch their unresolved table-
  constraint, partition-child override, or generated-column-kind paths
- refresh `benchmark/review-memory.json` review fingerprints and timestamps for
  the rechecked open issues, tracked parity issues, active benchmark gaps, and
  older draft-only uncovered findings, including moving resolved issue **#506**
  from `not_covered` to `covered`
- add this report as the 2026-07-28 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the unchanged open pgschema issue set
  - updated pgschema issue / PR pair
    [#519](https://github.com/pgplex/pgschema/issues/519) /
    [#520](https://github.com/pgplex/pgschema/pull/520)
  - exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - direct duplicate probes for benchmarks **020** through **022**, older
    draft-only gaps **#439** / **#444**, and open pgschema issue **#519**
- focused local pg17 pg-delta runtime probes showing:
  - the **#404 / #218** `UNIQUE ... DEFERRABLE INITIALLY DEFERRED` scenario
    still roundtrips cleanly
  - the **#366 / #219** enum-arg function privilege scenario still roundtrips
    cleanly
  - the benchmark **023 / #506** standalone unique-index slice now plans
    `CREATE UNIQUE INDEX parent_id_tenant_key` before `ADD child FK` and
    roundtrips cleanly end-to-end
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
  returned **0 issues found**
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  returned **0 resolved issues found**
- those dry-run script results remain expected because the parity-relevant
  pgschema items are still mostly missing the upstream `Bug` / `Feature`
  labels that the automation filters on, including open issues
  [#518](https://github.com/pgplex/pgschema/issues/518) and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- `git diff --check`
