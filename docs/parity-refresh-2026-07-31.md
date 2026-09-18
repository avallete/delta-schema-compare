# Parity refresh report - 2026-07-31

This report records the 2026-07-31 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `325dac205047a7850a52ee9f9ff35ec18c145dcc`)
- checked-in and live `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-29.md`](./parity-refresh-2026-07-29.md).

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

## 2) Upstream delta on 2026-07-31

This refresh found **one new upstream merge without a parity reclassification**:

- `pgschema/main` advanced from `2d864f3282ea3f0ba4cfa749e366cfdff1ae4fb7`
  to `325dac205047a7850a52ee9f9ff35ec18c145dcc` via merged
  [pgschema#522](https://github.com/pgplex/pgschema/pull/522), which closes
  [#521](https://github.com/pgplex/pgschema/issues/521)
- pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)
  ("Enum names being truncated in 1.12.1") remains **not parity work** for
  pg-delta; the upstream root cause was temporary-schema type-resolution
  `CASE` expressions resolving to PostgreSQL's `name` type and truncating long
  schema-qualified enum names before the outer cast, while pg-delta reads live
  column types with `format_type(a.atttypid, a.atttypmod)` and does not build
  temporary-schema-qualified type names in this path
- the open pgschema issue set remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- live `pg-toolbelt/main` still remains
  `a974b83fc044788caa4ca538d112b62d1873843b`
- no pg-toolbelt issues or PRs were updated after the 2026-07-29 refresh
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- direct duplicate probes still found no exact pg-toolbelt issue or PR for
  active benchmarks **020** through **022**, the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), newly closed
  pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521), or
  open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-07-31 delta is:

- advance the checked-in `repos/pgschema` submodule pointer from
  `2d864f3282ea3f0ba4cfa749e366cfdff1ae4fb7` to
  `325dac205047a7850a52ee9f9ff35ec18c145dcc`
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged 2026-07-31 parity conclusions plus the new pgschema head
- refresh `benchmark/review-memory.json` review fingerprints and timestamps for
  the rechecked open issues, exact tracked parity issues, active benchmark
  gaps, older draft-only uncovered findings, and newly closed pgschema issue
  [#521](https://github.com/pgplex/pgschema/issues/521)
- add this report as the 2026-07-31 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the unchanged open pgschema issue set
  - closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)
    plus merged PR
    [#522](https://github.com/pgplex/pgschema/pull/522)
  - the exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - duplicate-search queries for benchmarks **020** through **022**, the
    draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) /
    [#444](https://github.com/pgplex/pgschema/issues/444), and issue
    [#521](https://github.com/pgplex/pgschema/issues/521)
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
  - `packages/pg-delta/src/core/objects/table/table.model.ts` still reads live
    column type strings through `format_type(a.atttypid, a.atttypmod)`, which
    is why pgschema issue **#521** remains an upstream-only temp-schema bug
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
