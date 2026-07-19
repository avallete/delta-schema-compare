# Parity refresh report - 2026-07-19

This report records the 2026-07-19 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`c0decd173d191bc470bf7b8c8dd3e862f08ae398`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-18.md`](./parity-refresh-2026-07-18.md).

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

## 2) Upstream delta on 2026-07-19

This refresh found **no pgschema issue-set delta** and **no pg-delta
code-head delta** relative to the 2026-07-18 sweep:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still matches it exactly
- the current open pgschema issue set remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493), and
  [#513](https://github.com/pgplex/pgschema/issues/513)
- no new open pgschema issue appeared after
  [#513](https://github.com/pgplex/pgschema/issues/513), and #513 remains
  **not parity work** for pg-delta because it is workflow /
  migration-history orchestration rather than a live-catalog diff or current
  planner gap
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- the only fresh pg-toolbelt activity since the 2026-07-18 sweep is open PR
  [#343](https://github.com/supabase/pg-toolbelt/pull/343)
  (`feat(pg-delta): add statement-level debugging to schema apply`), which is
  apply observability rather than extraction, diff, or dependency work for
  benchmarks **020** through **023**
- broader open pg-toolbelt backlog issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#333](https://github.com/supabase/pg-toolbelt/issues/333),
  [#339](https://github.com/supabase/pg-toolbelt/issues/339), and
  [#340](https://github.com/supabase/pg-toolbelt/issues/340) remain adjacent
  rather than exact duplicates; a title/body scan found no references to
  pgschema **#412**, **#499**, **#501**, **#506**, or the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
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
    upstream with the same pg-delta verdicts as the 2026-07-18 sweep

## 3) What changed in this refresh

Because the latest-state sweep found no parity-state movement and no submodule
movement, this refresh is documentation and memory only:

- add this report as the 2026-07-19 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth matrix points to this
  follow-up and records that new pg-toolbelt activity is still non-overlapping
  with the active benchmark gaps
- refresh the reviewed timestamps in `benchmark/review-memory.json` for the
  rechecked open, tracked, active-gap, and older draft-only items

## 4) Validation notes

This refresh was validated with:

- GraphQL inventory checks for the live open pgschema issue set and the current
  open pg-toolbelt issue / PR set
- direct GitHub REST issue checks for pgschema **#49**, **#52**, **#84**,
  **#366**, **#404**, **#412**, **#439**, **#444**, **#450**, **#493**,
  **#499**, **#501**, **#506**, and **#513**
- direct GitHub REST issue / PR checks for pg-toolbelt **#218**, **#219**,
  **#332**, **#333**, **#339**, **#340**, and **#343**
- exact-reference duplicate searches on pg-toolbelt for pgschema **#412**,
  **#499**, **#501**, **#506**, **#439**, and **#444**, all of which again
  returned no exact tracker
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`

Repository-local validation after the doc refresh is listed in the final PR
diff and was rerun before commit.
