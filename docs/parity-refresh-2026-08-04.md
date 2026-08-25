# Parity refresh report - 2026-08-04

This report records the 2026-08-04 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `325dac205047a7850a52ee9f9ff35ec18c145dcc`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `2929e83981fee139772cc1c60255f1b2592a6f3a`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-03.md`](./parity-refresh-2026-08-03.md).

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

## 2) Upstream delta on 2026-08-04

This refresh found **no benchmark verdict changes**, but it did find a new
checked-in/live pg-delta head delta since 2026-08-03:

- checked-in `repos/pgschema` and live `pgschema/main` both remain at
  `325dac205047a7850a52ee9f9ff35ec18c145dcc`
- checked-in `repos/pg-toolbelt` remains at
  `a974b83fc044788caa4ca538d112b62d1873843b`
- live `pg-toolbelt/main` advanced to
  `2929e83981fee139772cc1c60255f1b2592a6f3a`
- the live pg-delta delta is adjacent rather than benchmark-moving: merged
  [pg-toolbelt#372](https://github.com/supabase/pg-toolbelt/pull/372)
  (`fix(pg-topo): slice statements by byte offsets so non-ASCII SQL is carried
  verbatim`) plus the alpha release
  [pg-toolbelt#374](https://github.com/supabase/pg-toolbelt/pull/374)
- open pgschema issues still remain
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#517](https://github.com/pgplex/pgschema/pull/517) remains the
  open upstream candidate fix for
  [#518](https://github.com/pgplex/pgschema/issues/518); its 2026-08-04 update
  is still specific to pgschema's temporary comparison environment rather than
  pg-delta parity
- pgschema [#520](https://github.com/pgplex/pgschema/pull/520) remains the
  open upstream candidate fix for
  [#519](https://github.com/pgplex/pgschema/issues/519) and still remains
  temporary-schema view-normalization work rather than pg-delta parity
- pgschema [#521](https://github.com/pgplex/pgschema/issues/521) remains
  closed by merged [pgschema#522](https://github.com/pgplex/pgschema/pull/522)
  and still remains **not parity work** for pg-delta because the bug came from
  pgschema's temporary-schema type-resolution `CASE` expressions resolving to
  PostgreSQL's `name` type, while pg-delta reads live column types with
  `format_type(...)`
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- adjacent pg-toolbelt work also changed state:
  [#367](https://github.com/supabase/pg-toolbelt/pull/367) remains open as a
  docs-only roadmap PR, while
  [#368](https://github.com/supabase/pg-toolbelt/pull/368) is now merged for
  [#365](https://github.com/supabase/pg-toolbelt/issues/365), but it still
  remains a schema-export filesystem fix rather than an exact parity duplicate

Direct duplicate-search probes still found **no exact pg-toolbelt issue or PR**
for:

- active benchmarks **020**, **021**, and **022**
- older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444)
- open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
- closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-04 delta is:

- add this report as the 2026-08-04 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot records the new
  live `pg-toolbelt/main` head, the merged state of pg-toolbelt PR #368, and
  the unchanged active gaps
- add 2026-08-04 refresh notes to benchmark files **020**, **021**, **022**,
  and **023** with focused runtime probe results on live pg-delta `main`
- update `.github/agents/delta-schema-agent.md` so the benchmark-file count
  matches the current benchmark set
- leave `benchmark/review-memory.json` unchanged because the checked-in
  benchmark baseline and cached checked-in verdict fingerprints did not move;
  this refresh records an adjacent live-head revalidation rather than a new
  checked-in benchmark baseline

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `git -C repos/pg-toolbelt ls-remote origin refs/heads/main`
- `git -C repos/pgschema ls-remote origin refs/heads/main`
- direct GitHub REST checks for:
  - open pgschema issues
    [#49](https://github.com/pgplex/pgschema/issues/49),
    [#52](https://github.com/pgplex/pgschema/issues/52),
    [#84](https://github.com/pgplex/pgschema/issues/84),
    [#450](https://github.com/pgplex/pgschema/issues/450),
    [#493](https://github.com/pgplex/pgschema/issues/493),
    [#518](https://github.com/pgplex/pgschema/issues/518), and
    [#519](https://github.com/pgplex/pgschema/issues/519)
  - open pgschema issue [#518](https://github.com/pgplex/pgschema/issues/518)
    plus open PR [#517](https://github.com/pgplex/pgschema/pull/517)
  - open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
    plus open PR [#520](https://github.com/pgplex/pgschema/pull/520)
  - closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)
    plus merged PR [#522](https://github.com/pgplex/pgschema/pull/522)
  - exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - adjacent pg-toolbelt work
    [#365](https://github.com/supabase/pg-toolbelt/issues/365),
    [#367](https://github.com/supabase/pg-toolbelt/pull/367),
    [#368](https://github.com/supabase/pg-toolbelt/pull/368),
    [#372](https://github.com/supabase/pg-toolbelt/pull/372), and
    [#374](https://github.com/supabase/pg-toolbelt/pull/374)
- duplicate-search queries for benchmarks **020** through **022**, the
  draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), and issues
  [#519](https://github.com/pgplex/pgschema/issues/519) /
  [#521](https://github.com/pgplex/pgschema/issues/521)
- focused live pg-delta runtime probes showing:
  - benchmark **020** still plans **zero statements** for toggling an existing
    `UNIQUE` table constraint to `UNIQUE NULLS NOT DISTINCT`
  - benchmark **021** still emits only
    `CREATE TABLE ... PARTITION OF ... FOR VALUES ...` without child-specific
    `DEFAULT` / `NOT NULL` overrides
  - benchmark **022** still serializes the PostgreSQL 18 case as
    `GENERATED ALWAYS AS (...) STORED` instead of preserving `VIRTUAL`
  - benchmark **023** still emits `CREATE UNIQUE INDEX ...` before the child
    foreign key and applies with no remaining changes
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN=\"<remote-token>\" DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN=\"<remote-token>\" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`
