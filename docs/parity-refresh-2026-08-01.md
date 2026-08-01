# Parity refresh report - 2026-08-01

This report records the 2026-08-01 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `325dac205047a7850a52ee9f9ff35ec18c145dcc`)
- checked-in and live `pg-delta` (`repos/pg-toolbelt` @ `a974b83fc044788caa4ca538d112b62d1873843b`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-31.md`](./parity-refresh-2026-07-31.md).

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

## 2) Upstream delta on 2026-08-01

This refresh found **no checked-in/live code-head delta** versus
2026-07-31:

- checked-in `repos/pgschema`, live `pgschema/main`, checked-in
  `repos/pg-toolbelt`, and live `pg-toolbelt/main` all remain on the same SHAs
  as the 2026-07-31 refresh
- the open pgschema issue set is still
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#520](https://github.com/pgplex/pgschema/pull/520) remains open
  as the upstream candidate fix for
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
- no newer pg-toolbelt issue or PR updates were found after the 2026-07-31
  refresh; the newest adjacent items are still open issue
  [#365](https://github.com/supabase/pg-toolbelt/issues/365) and closed-unmerged
  PR [#366](https://github.com/supabase/pg-toolbelt/pull/366)

Direct duplicate-search probes still found **no exact pg-toolbelt issue or PR**
for:

- active benchmarks **020**, **021**, and **022**
- older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444)
- open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
- closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)

The only ambiguous hits were still adjacent rather than exact duplicates:

- open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) and
  open PR [#299](https://github.com/supabase/pg-toolbelt/pull/299) are generic
  alpha / extraction-fidelity follow-up work, not exact trackers for
  benchmarks **020** through **022**
- merged PR [#335](https://github.com/supabase/pg-toolbelt/pull/335) fixes a
  different partition path (`PARTITION BY` on subpartitions), not the
  child-specific `DEFAULT` / `NOT NULL` override gap from benchmark **021**

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-01 delta is:

- add this report as the 2026-08-01 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot records the
  unchanged 2026-08-01 parity conclusions and links to this report
- leave `benchmark/review-memory.json` unchanged because the parity-relevant
  fingerprints and verdicts did not move versus 2026-07-31

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `git -C repos/pg-toolbelt ls-remote origin refs/heads/main`
- `git -C repos/pgschema ls-remote origin refs/heads/main`
- direct public GitHub API checks for:
  - the unchanged open pgschema issue set
  - open pgschema PR [#520](https://github.com/pgplex/pgschema/pull/520)
  - closed pgschema issue [#521](https://github.com/pgplex/pgschema/issues/521)
    plus merged PR
    [#522](https://github.com/pgplex/pgschema/pull/522)
  - the exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - adjacent pg-toolbelt work
    [#299](https://github.com/supabase/pg-toolbelt/pull/299),
    [#332](https://github.com/supabase/pg-toolbelt/issues/332),
    [#335](https://github.com/supabase/pg-toolbelt/pull/335),
    [#365](https://github.com/supabase/pg-toolbelt/issues/365), and
    [#366](https://github.com/supabase/pg-toolbelt/pull/366)
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
  - no `VIRTUAL` matches exist in the current pg-delta TypeScript source tree,
    and generated columns are still serialized as
    `GENERATED ALWAYS AS (...) STORED` in both `table.create.ts` and
    `table.alter.ts`, leaving benchmark **022** unresolved
