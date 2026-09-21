# Parity refresh report - 2026-08-03

This report records the 2026-08-03 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `325dac205047a7850a52ee9f9ff35ec18c145dcc`)
- checked-in and live `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-01.md`](./parity-refresh-2026-08-01.md).

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

## 2) Upstream delta on 2026-08-03

This refresh found **no checked-in/live code-head delta** versus
2026-08-01:

- checked-in `repos/pgschema`, live `pgschema/main`, checked-in
  `repos/pg-toolbelt`, and live `pg-toolbelt/main` all remain on the same SHAs
  as the 2026-08-01 refresh
- the open pgschema issue set is still
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#517](https://github.com/pgplex/pgschema/pull/517) is now the
  open upstream candidate fix for
  [#518](https://github.com/pgplex/pgschema/issues/518), and it still remains
  **not parity work** for pg-delta because it is specific to pgschema's
  temporary comparison environment stripping schema qualifiers from
  extension-owned types rather than diffing live catalogs directly
- pgschema [#520](https://github.com/pgplex/pgschema/pull/520) remains open as
  the upstream candidate fix for
  [#519](https://github.com/pgplex/pgschema/issues/519), and it still remains
  **not parity work** for pg-delta because it is specific to pgschema's
  temporary-schema view-normalization path
- pgschema [#521](https://github.com/pgplex/pgschema/issues/521) remains closed
  by merged [pgschema#522](https://github.com/pgplex/pgschema/pull/522) and
  still remains **not parity work** for pg-delta; the upstream bug came from
  temporary-schema type-resolution `CASE` expressions resolving to PostgreSQL's
  `name` type, while pg-delta reads live column types with `format_type(...)`
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- the only newer pg-toolbelt activity after the 2026-08-01 refresh is still
  adjacent rather than exact parity work:
  open [#367](https://github.com/supabase/pg-toolbelt/pull/367) is a docs-only
  roadmap PR, and open
  [#368](https://github.com/supabase/pg-toolbelt/pull/368) addresses
  case-colliding schema export paths for
  [#365](https://github.com/supabase/pg-toolbelt/issues/365) on the export path
  rather than any of the active benchmark gaps

Direct duplicate-search probes still found **no exact pg-toolbelt issue or PR**
for:

- active benchmarks **020**, **021**, and **022**
- older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444)
- open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
- closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)

The only ambiguous hits were still adjacent rather than exact duplicates:

- open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) and
  open PR [#299](https://github.com/supabase/pg-toolbelt/pull/299) remain
  generic alpha / extraction-fidelity follow-up work, not exact trackers for
  benchmarks **020** through **022**
- merged PR [#335](https://github.com/supabase/pg-toolbelt/pull/335) fixes a
  different partition path (`PARTITION BY` on subpartitions), not the
  child-specific `DEFAULT` / `NOT NULL` override gap from benchmark **021**
- open PR [#368](https://github.com/supabase/pg-toolbelt/pull/368) is a
  case-colliding schema export fix linked to
  [#365](https://github.com/supabase/pg-toolbelt/issues/365), not an exact
  duplicate of benchmarks **020** through **022**, the draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), or pgschema issues
  [#519](https://github.com/pgplex/pgschema/issues/519) /
  [#521](https://github.com/pgplex/pgschema/issues/521)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-03 delta is:

- add this report as the 2026-08-03 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged 2026-08-03 parity conclusions and the newly observed upstream PR
  context for pgschema [#518](https://github.com/pgplex/pgschema/issues/518)
  and pg-toolbelt [#368](https://github.com/supabase/pg-toolbelt/pull/368)
- leave `benchmark/review-memory.json` unchanged because the stored
  pgschema-issue fingerprints and checked-in/live submodule SHAs did not move
  versus 2026-08-01, so the review-memory verdict cache remains valid even
  though today's manual GitHub sweep refreshed adjacent PR state

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `git -C repos/pg-toolbelt ls-remote origin refs/heads/main`
- `git -C repos/pgschema ls-remote origin refs/heads/main`
- direct GitHub REST API checks for:
  - the unchanged open pgschema issue set
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
    [#365](https://github.com/supabase/pg-toolbelt/issues/365),
    [#367](https://github.com/supabase/pg-toolbelt/pull/367), and
    [#368](https://github.com/supabase/pg-toolbelt/pull/368)
- duplicate-search queries for benchmarks **020** through **022**, the
  draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), and issues
  [#519](https://github.com/pgplex/pgschema/issues/519) /
  [#521](https://github.com/pgplex/pgschema/issues/521)
- current pg-delta source/test evidence showing:
  - `NULLS NOT DISTINCT` coverage still exists only for unique indexes in
    `packages/pg-delta/tests/integration/index-operations.test.ts`, not the
    active table-constraint gap from benchmark **020**
  - `packages/pg-delta/src/core/objects/table/changes/table.create.ts` still
    returns the bare `PARTITION OF ... FOR VALUES ...` statement for partition
    children before column-definition serialization, leaving no path for the
    child-specific overrides from benchmark **021**
  - no `VIRTUAL` handling exists in the current pg-delta TypeScript source
    tree, and generated columns are still serialized as
    `GENERATED ALWAYS AS (...) STORED` in both `table.create.ts` and
    `table.alter.ts`, leaving benchmark **022** unresolved
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- those dry-run script runs still returned **0** parity items, which remains
  expected because the current parity-relevant pgschema items are still mostly
  missing the upstream `Bug` / `Feature` labels that the automation filters on,
  including open issues
  [#518](https://github.com/pgplex/pgschema/issues/518) and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- `git diff --check`
