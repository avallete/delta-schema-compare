# Parity refresh report - 2026-07-21

This report records the 2026-07-21 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`c0decd173d191bc470bf7b8c8dd3e862f08ae398`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-20.md`](./parity-refresh-2026-07-20.md).

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
- pgschema [#506](https://github.com/pgplex/pgschema/issues/506):
  new-table FK ordered before a standalone unique index on the referenced table
  - benchmark file:
    [`benchmark/023-fk-before-standalone-unique-index.md`](../benchmark/023-fk-before-standalone-unique-index.md)
  - no matching pg-toolbelt issue or PR was found through this refresh

## 2) Upstream delta on 2026-07-21

This refresh found **no pg-delta code-head delta** relative to the
2026-07-20 sweep, but it did find a small **pgschema issue-set delta**:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still matches it exactly
- pgschema
  [#513](https://github.com/pgplex/pgschema/issues/513) closed on 2026-07-20
  as `COMPLETED`; it moves out of the open-screening set but still remains
  **not parity work** for pg-delta because it is workflow / migration-history
  orchestration rather than a live-catalog diff or current planner gap
- the current open pgschema issue set is now
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#493](https://github.com/pgplex/pgschema/issues/493)
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- new pg-toolbelt activity since the previous sweep is open issue
  [#344](https://github.com/supabase/pg-toolbelt/issues/344), open issue
  [#346](https://github.com/supabase/pg-toolbelt/issues/346), open PR
  [#350](https://github.com/supabase/pg-toolbelt/pull/350), and open PR
  [#354](https://github.com/supabase/pg-toolbelt/pull/354)
- a direct title/body scan confirms **#344**, **#346**, **#350**, and **#354**
  are adjacent rather than exact duplicates for benchmarks **020** through
  **023** or the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
- broader open pg-toolbelt backlog issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#333](https://github.com/supabase/pg-toolbelt/issues/333),
  [#339](https://github.com/supabase/pg-toolbelt/issues/339), and
  [#340](https://github.com/supabase/pg-toolbelt/issues/340) remain adjacent
  rather than exact duplicates
- direct issue-page checks confirm the tracked and older draft-only resolved
  items keep the same parity state:
  - [#366](https://github.com/pgplex/pgschema/issues/366) remains closed as
    `not_planned` and is still tracked by
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - [#404](https://github.com/pgplex/pgschema/issues/404) remains closed as
    completed and is still tracked by
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - [#412](https://github.com/pgplex/pgschema/issues/412),
    [#439](https://github.com/pgplex/pgschema/issues/439),
    [#444](https://github.com/pgplex/pgschema/issues/444),
    [#499](https://github.com/pgplex/pgschema/issues/499),
    [#501](https://github.com/pgplex/pgschema/issues/501), and
    [#506](https://github.com/pgplex/pgschema/issues/506) remain resolved
    upstream with the same pg-delta verdicts as the 2026-07-20 sweep

## 3) What changed in this refresh

Because the latest-state sweep found no code-head movement and no benchmark
state movement, this refresh is documentation and memory only:

- add this report as the 2026-07-21 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth matrix records the
  closure of pgschema #513 and the latest non-overlapping pg-toolbelt activity
- move pgschema #513 from `review-memory.open` to `review-memory.resolved`
  and refresh the reviewed timestamps for the rechecked open, tracked,
  active-gap, and older draft-only items

## 4) Validation notes

This refresh was validated with:

- live open/closed issue list checks for pgschema
- live open issue and PR list checks for pg-toolbelt
- direct GitHub issue detail checks for pgschema **#513**
- direct GitHub issue / PR detail checks for pg-toolbelt **#344**, **#346**,
  **#350**, and **#354**
- direct issue-page rechecks for pgschema **#366**, **#404**, **#412**,
  **#439**, **#444**, **#499**, **#501**, and **#506**, plus pg-toolbelt
  **#218** and **#219**
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `bun install --frozen-lockfile`
- `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  `packages/pg-delta/src/core/objects/table/changes/table.create.test.ts`
  `packages/pg-delta/src/core/objects/index/index.diff.test.ts`
  `packages/pg-delta/src/core/sort/sort-changes.test.ts`
  (**37 tests**, pass)
- `DRY_RUN=true python3 scripts/compare_issues.py` (**0 issues found** because
  the upstream `Bug` / `Feature` label filter still misses the relevant
  unlabeled parity issues)
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  (**0 issues found** for the same label-filter reason)
- `git diff --check`
