# Parity refresh report - 2026-07-11

This report records the 2026-07-11 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`)
- live `pg-toolbelt` `main` (`d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`), which is still the same CI-only commit ahead already seen on 2026-07-10

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-10.md`](./parity-refresh-2026-07-10.md).

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

## 2) Upstream delta on 2026-07-11

This refresh found **no new parity-state movement** after the 2026-07-10 sweep:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- the latest created pgschema issue remains **#509**; higher visible numbers
  **#510**, **#511**, and **#512** are PRs rather than issues
- the only open pgschema issue with fresh upstream activity since the prior
  sweep is [#450](https://github.com/pgplex/pgschema/issues/450), updated at
  `2026-07-11T04:04:29Z`, and it remains **not parity work for pg-delta**
- checked-in `pg-delta` remains
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e`, while live `pg-toolbelt` `main`
  remains `d3b3c8b6b7f5e9a85c765284a2a5e9f69cbb97f5`
- the diff between those two pg-toolbelt SHAs is still limited to CI /
  repo-meta files:
  - `.github/MAINTAINERS.md`
  - `.github/scripts/contribution-gate.test.ts`
  - `.github/scripts/contribution-gate.ts`
  - `.github/workflows/contribution-gate.yml`
- no `packages/pg-delta/**` source files or pg-delta integration tests changed,
  so benchmarks **020**, **021**, **022**, and **023** keep the same
  `Not covered` verdicts
- exact open pg-toolbelt trackers still exist only for
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- no new exact pg-toolbelt issue or PR was found for benchmarks **020**, **021**,
  **022**, or **023**, nor for the older draft-only resolved items
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)
- newer pg-toolbelt activity remains adjacent rather than duplicative:
  - [#329](https://github.com/supabase/pg-toolbelt/pull/329) is open, but its
    scope is non-superuser Supabase profile apply behavior rather than any
    current pgschema parity gap
  - [#323](https://github.com/supabase/pg-toolbelt/pull/323) is now merged, but
    its export / profile-baseline scope does not replace any current benchmark
    gap or draft-only item
  - [#307](https://github.com/supabase/pg-toolbelt/pull/307) and
    [#315](https://github.com/supabase/pg-toolbelt/pull/315) are now
    closed/merged as adjacent `pg-delta-next` work; they still do not affect the
    current-engine benchmark verdicts

## 3) What changed in this refresh

Because the latest-state sweep found no parity change, this refresh keeps the
benchmark matrix and checked-in submodule pointers unchanged and records the
result as another dated no-delta report:

- add this report as the 2026-07-11 latest-state sweep
- annotate `benchmark/README.md` so the source-of-truth matrix points to this
  follow-up, notes the fresh non-parity update on pgschema #450, and corrects
  the stale status note for adjacent pg-toolbelt PRs #307 / #315
- refresh the reviewed timestamps in `benchmark/review-memory.json` for the
  rechecked open, tracked, and active-gap items, and update the #450 fingerprint
  to its new upstream `updated_at` value

## 4) Validation notes

This refresh was validated with:

- live GitHub REST checks for pgschema **#366**, **#404**, **#412**, **#439**,
  **#444**, **#450**, **#499**, **#501**, **#506**, and **#509**
- live GitHub REST checks for pg-toolbelt **#218**, **#219**, **#263**,
  **#273**, **#285**, **#291**, **#299**, **#301**, **#304**, **#305**,
  **#307**, **#308**, **#310**, **#311**, **#313**, **#314**, **#315**,
  **#316**, **#323**, and **#329**
- direct git diff of live pg-toolbelt `main` versus the checked-in baseline,
  confirming the same CI-only `.github/**` delta as the 2026-07-10 sweep
- repository maintenance checks (`benchmark/review-memory.json` JSON parsing,
  targeted repository tests, dry-run compare scripts, and `git diff --check`)

The unlabeled-issue caveat still applies: the parity-relevant pgschema issues
remain mostly unlabeled, so `compare_issues.py` and `compare_resolved.py` can
still return zero candidates even when the manual latest-state sweep finds
useful parity updates.
