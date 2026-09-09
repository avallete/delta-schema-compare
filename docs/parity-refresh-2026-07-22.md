# Parity refresh report - 2026-07-22

This report records the 2026-07-22 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `5f2b37bae6d51068b3a3b05fec3185c4219f8968`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`c0decd173d191bc470bf7b8c8dd3e862f08ae398`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-21.md`](./parity-refresh-2026-07-21.md).

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

### Newly closed upstream issue reviewed today

- pgschema [#515](https://github.com/pgplex/pgschema/issues/515):
  trigger comment omitted when adding a trigger to an existing table
  - merged upstream in
    [pgschema#516](https://github.com/pgplex/pgschema/pull/516)
  - **covered** in current pg-delta for the reported comment-on-create
    scenario, so no new benchmark file or duplicate pg-toolbelt tracker is
    needed

## 2) Upstream delta on 2026-07-22

This refresh found **no pg-delta code-head delta** relative to the
2026-07-21 sweep, but it did find a **pgschema code-head delta** plus new
upstream PR movement:

- `pgschema` `main` advanced from
  `e18d9ede7973537919c02f25eced5c97271af1dc` to
  `5f2b37bae6d51068b3a3b05fec3185c4219f8968` via merged
  [pgschema#516](https://github.com/pgplex/pgschema/pull/516)
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still matches it exactly
- the current open pgschema issue set is still
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#493](https://github.com/pgplex/pgschema/issues/493)
- pgschema [#493](https://github.com/pgplex/pgschema/issues/493) now has open
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514), but it still
  remains **not parity work** for pg-delta because it is a dump-only
  `--qualify-schema` follow-up rather than a live-catalog diff or planner gap
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- new pg-toolbelt activity since the previous sweep is open PR
  [#355](https://github.com/supabase/pg-toolbelt/pull/355) and open PR
  [#356](https://github.com/supabase/pg-toolbelt/pull/356); yesterday's PRs
  [#350](https://github.com/supabase/pg-toolbelt/pull/350) and
  [#354](https://github.com/supabase/pg-toolbelt/pull/354) are now merged,
  while issues [#344](https://github.com/supabase/pg-toolbelt/issues/344) and
  [#346](https://github.com/supabase/pg-toolbelt/issues/346) remain open
- a direct title/body scan confirms **#344**, **#346**, **#350**, **#354**,
  **#355**, and **#356** are adjacent rather than exact duplicates for
  benchmarks **020** through **023**, tracked issues
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) /
  [#219](https://github.com/supabase/pg-toolbelt/issues/219), or the older
  draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
- broader open pg-toolbelt backlog issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#333](https://github.com/supabase/pg-toolbelt/issues/333),
  [#339](https://github.com/supabase/pg-toolbelt/issues/339),
  [#340](https://github.com/supabase/pg-toolbelt/issues/340), plus open PR
  [#285](https://github.com/supabase/pg-toolbelt/pull/285), remain adjacent
  rather than exact duplicates
- direct issue-page rechecks confirm the tracked and older draft-only resolved
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
    [#501](https://github.com/pgplex/pgschema/issues/501),
    [#506](https://github.com/pgplex/pgschema/issues/506), and
    [#513](https://github.com/pgplex/pgschema/issues/513) keep the same
    pg-delta verdicts as the 2026-07-21 sweep

## 3) What changed in this refresh

This refresh is still a docs-and-memory update, but it records a real upstream
delta:

- add this report as the 2026-07-22 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth matrix records the new
  `pgschema` head, open pgschema PR [#514](https://github.com/pgplex/pgschema/pull/514),
  newly merged pgschema PR [#516](https://github.com/pgplex/pgschema/pull/516),
  and the latest non-overlapping pg-toolbelt activity
- record pgschema [#515](https://github.com/pgplex/pgschema/issues/515) in
  `benchmark/review-memory.json` as **covered**, and refresh the reviewed
  timestamps / fingerprints for the rechecked open, tracked, active-gap, and
  older draft-only items

## 4) Validation notes

This refresh was validated with:

- public GitHub API list checks for pgschema open/closed issues
- public GitHub API list checks for pg-toolbelt open issues and PRs
- direct public GitHub API detail checks for pgschema **#515**, pgschema
  PR **#514**, pgschema PR **#516**, pg-toolbelt PR **#285**, and pg-toolbelt
  PRs **#355** / **#356**
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `bun install --frozen-lockfile`
- a focused one-off pg-delta roundtrip probe for pgschema **#515**'s exact
  comment-on-create scenario against PostgreSQL 17; it converged with no repeat
  diff
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`
