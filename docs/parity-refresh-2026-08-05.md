# Parity refresh report - 2026-08-05

This report records the 2026-08-05 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `b1d60e8d95cfc95508956e4c1e89572269410501`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `2929e83981fee139772cc1c60255f1b2592a6f3a`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-04.md`](./parity-refresh-2026-08-04.md).

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

## 2) Upstream delta on 2026-08-05

This refresh found **one new upstream merge without a parity reclassification**:

- `pgschema/main` advanced from `325dac205047a7850a52ee9f9ff35ec18c145dcc`
  to `b1d60e8d95cfc95508956e4c1e89572269410501` via merged
  [pgschema#529](https://github.com/pgplex/pgschema/pull/529), which closes
  [#526](https://github.com/pgplex/pgschema/issues/526)
- pgschema issue [#526](https://github.com/pgplex/pgschema/issues/526)
  ("Function SET clauses except search_path are dropped") is already
  **covered** in current pg-delta rather than a new parity gap:
  - `packages/pg-delta/src/core/objects/procedure/procedure.model.ts`
    already extracts `p.proconfig as config`
  - `packages/pg-delta/src/core/objects/procedure/procedure.diff.ts`
    already emits per-key `ALTER FUNCTION/PROCEDURE ... SET/RESET`
  - `packages/pg-delta/tests/integration/function-operations.test.ts`
    already roundtrips a function with multiple configuration parameters
  - a focused 2026-08-05 pg17 runtime probe emitted both
    `SET search_path TO 'public'` and `SET "TimeZone" TO 'UTC'`, then
    roundtripped cleanly with no remaining changes
- checked-in and live pg-delta heads remain unchanged from the 2026-08-04
  refresh:
  - checked-in `repos/pg-toolbelt` remains
    `a974b83fc044788caa4ca538d112b62d1873843b`
  - live `pg-toolbelt/main` remains
    `2929e83981fee139772cc1c60255f1b2592a6f3a`
- the open pgschema issue set remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#517](https://github.com/pgplex/pgschema/pull/517) remains the
  open upstream candidate fix for
  [#518](https://github.com/pgplex/pgschema/issues/518), and it still remains
  **not parity work** for pg-delta because it is specific to pgschema's
  temporary comparison environment stripping schema qualifiers from
  extension-owned types rather than diffing live catalogs directly
- pgschema [#520](https://github.com/pgplex/pgschema/pull/520) remains the
  open upstream candidate fix for
  [#519](https://github.com/pgplex/pgschema/issues/519), and it still remains
  **not parity work** for pg-delta because it is specific to pgschema's
  temporary-schema view-normalization path
- pgschema [#521](https://github.com/pgplex/pgschema/issues/521) remains
  closed by merged [pgschema#522](https://github.com/pgplex/pgschema/pull/522)
  and still remains **not parity work** for pg-delta; the upstream bug came
  from temporary-schema type-resolution `CASE` expressions resolving to
  PostgreSQL's `name` type, while pg-delta reads live column types with
  `format_type(...)`
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- newer pg-toolbelt activity after 2026-08-04 is still adjacent rather than
  exact parity work:
  - open [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains the
    `feat/pg-delta-next` cutover PR rather than `main`-branch parity work
  - merged [#379](https://github.com/supabase/pg-toolbelt/pull/379),
    [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
    [#381](https://github.com/supabase/pg-toolbelt/pull/381) all landed on
    `feat/pg-delta-next`, not on the current default-branch engine, and none is
    an exact duplicate of benchmarks **020** through **022** or issues
    [#519](https://github.com/pgplex/pgschema/issues/519),
    [#521](https://github.com/pgplex/pgschema/issues/521), or
    [#526](https://github.com/pgplex/pgschema/issues/526)

Direct duplicate-search probes still found **no exact pg-toolbelt issue or PR**
for:

- active benchmarks **020**, **021**, and **022**
- older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444)
- open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
- closed pgschema issues [#521](https://github.com/pgplex/pgschema/issues/521)
  and [#526](https://github.com/pgplex/pgschema/issues/526)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-05 delta is:

- advance the checked-in `repos/pgschema` submodule pointer from
  `325dac205047a7850a52ee9f9ff35ec18c145dcc` to
  `b1d60e8d95cfc95508956e4c1e89572269410501`
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged active gaps plus the newly closed covered issue
  [#526](https://github.com/pgplex/pgschema/issues/526)
- add 2026-08-05 refresh notes to benchmark files **020**, **021**, and
  **022** with focused runtime-probe revalidation
- refresh `benchmark/review-memory.json` review fingerprints and timestamps for
  the rechecked open issues, exact tracked parity issues, active benchmark
  gaps, older draft-only uncovered findings, previously closed upstream-only
  issue [#521](https://github.com/pgplex/pgschema/issues/521), and newly
  closed covered issue [#526](https://github.com/pgplex/pgschema/issues/526)
- add this report as the 2026-08-05 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub REST API checks for:
  - the unchanged open pgschema issue set
  - closed pgschema issue [#526](https://github.com/pgplex/pgschema/issues/526)
    plus merged PR
    [#529](https://github.com/pgplex/pgschema/pull/529)
  - open pgschema issue [#518](https://github.com/pgplex/pgschema/issues/518)
    plus open PR [#517](https://github.com/pgplex/pgschema/pull/517)
  - open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
    plus open PR [#520](https://github.com/pgplex/pgschema/pull/520)
  - closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)
    plus merged PR
    [#522](https://github.com/pgplex/pgschema/pull/522)
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
  [#444](https://github.com/pgplex/pgschema/issues/444), and issues
  [#519](https://github.com/pgplex/pgschema/issues/519) /
  [#521](https://github.com/pgplex/pgschema/issues/521) /
  [#526](https://github.com/pgplex/pgschema/issues/526)
- focused pg-delta runtime probes showing:
  - pgschema [#526](https://github.com/pgplex/pgschema/issues/526) is already
    covered: the generated plan emitted both `SET search_path TO 'public'` and
    `SET "TimeZone" TO 'UTC'`, and the roundtrip converged cleanly
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
