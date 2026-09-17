# Parity refresh report - 2026-07-18

This report records the 2026-07-18 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `e18d9ede7973537919c02f25eced5c97271af1dc`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`c0decd173d191bc470bf7b8c8dd3e862f08ae398`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-17.md`](./parity-refresh-2026-07-17.md).

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

## 2) Upstream delta on 2026-07-18

This refresh found **no pgschema issue-set delta** and **no parity-state delta**
relative to 2026-07-17, but it **did** find a new checked-in pg-delta code-head
delta:

- `pgschema` `main` remains `e18d9ede7973537919c02f25eced5c97271af1dc`
- the open pgschema issue set remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493), and
  [#513](https://github.com/pgplex/pgschema/issues/513)
- no new open pgschema issue appeared after
  [#513](https://github.com/pgplex/pgschema/issues/513), and #513 remains
  **not parity work** for pg-delta because it is workflow / migration-history
  orchestration rather than a live-catalog diff or current planner gap
- checked-in `pg-delta` advanced from
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` to
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`
- the pg-delta delta is `1.0.0-alpha.32`, whose substantive change is
  [pg-toolbelt#337](https://github.com/supabase/pg-toolbelt/pull/337):
  non-superuser catalog extraction now reads user mappings from
  `pg_user_mappings`, conditionally redacts subscription `subconninfo`, and
  adds a new integration regression for that extraction path
- the changed `packages/pg-delta/**` files in this delta are limited to:
  - `src/core/catalog.model.ts`
  - `src/core/depend.ts`
  - `src/core/objects/foreign-data-wrapper/user-mapping/user-mapping.model.ts`
  - `src/core/objects/subscription/subscription.model.ts`
  - `tests/integration/non-superuser-extraction.test.ts`
  - package/changelog metadata
- none of those files touch the active benchmark modules for table-constraint
  `NULLS NOT DISTINCT`, partition-child `PARTITION OF (...)` overrides,
  generated-column kind preservation, or FK-vs-standalone-unique-index
  ordering, so benchmarks **020**, **021**, **022**, and **023** keep the same
  `Not covered` verdicts
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- older draft-only uncovered items
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444) still have no exact
  pg-toolbelt issue or PR
- adjacent pg-toolbelt work in
  [#263](https://github.com/supabase/pg-toolbelt/issues/263),
  [#285](https://github.com/supabase/pg-toolbelt/pull/285),
  [#291](https://github.com/supabase/pg-toolbelt/pull/291),
  [#299](https://github.com/supabase/pg-toolbelt/pull/299),
  [#308](https://github.com/supabase/pg-toolbelt/issues/308),
  [#310](https://github.com/supabase/pg-toolbelt/pull/310),
  [#334](https://github.com/supabase/pg-toolbelt/pull/334), and
  [#335](https://github.com/supabase/pg-toolbelt/pull/335) still does not
  exactly cover benchmarks **020** through **023** or the older draft-only
  items **#439** and **#444**

## 3) What changed in this refresh

Because the latest-state sweep found a pg-delta code-head delta but no
benchmark-matrix delta, this refresh updates the checked-in pg-toolbelt
submodule pointer and records the result as another dated no-matrix-delta
report:

- advance `repos/pg-toolbelt` to
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`
- add this report as the 2026-07-18 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth matrix points to this
  code-head update and notes that the active benchmarks still have no exact
  pg-toolbelt trackers
- refresh the active benchmark docs
  ([020](../benchmark/020-unique-constraint-nulls-not-distinct.md),
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [023](../benchmark/023-fk-before-standalone-unique-index.md))
  with a short 2026-07-18 note explaining why the new alpha.32 delta does not
  change their parity verdicts
- refresh the reviewed timestamps and fingerprints in
  `benchmark/review-memory.json` for the rechecked open, tracked, active-gap,
  and older draft-only items

## 4) Validation notes

This refresh was validated with:

- live GitHub issue-page checks for the current pgschema open set
  (**#49**, **#52**, **#84**, **#450**, **#493**, **#513**) and the rechecked
  tracked / active-gap / draft-only issues (**#366**, **#404**, **#412**,
  **#439**, **#444**, **#499**, **#501**, **#506**)
- live GitHub issue / PR checks for pg-toolbelt **#218**, **#219**, **#263**,
  **#285**, **#291**, **#299**, **#308**, **#310**, **#334**, and **#335**
- title-based duplicate searches on pg-toolbelt for the active benchmark
  scenarios and the older draft-only gaps, all of which returned empty results
- direct git diff of the pg-delta delta between
  `ee285b51bcfdeba4e7139b2b20d6e8192b606a0e` and
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, confirming the change is limited
  to non-superuser extraction plus release metadata
- targeted pg-delta unit tests (non-Docker):
  - `bun test packages/pg-delta/src/core/catalog.model.test.ts`
    `packages/pg-delta/src/core/expand-replace-dependencies.test.ts`
    `packages/pg-delta/src/core/objects/foreign-data-wrapper/user-mapping/user-mapping.diff.test.ts`
    `packages/pg-delta/src/core/objects/foreign-data-wrapper/user-mapping/changes/user-mapping.create.test.ts`
    `packages/pg-delta/src/core/objects/foreign-data-wrapper/user-mapping/changes/user-mapping.alter.test.ts`
    `packages/pg-delta/src/core/objects/foreign-data-wrapper/user-mapping/changes/user-mapping.drop.test.ts`
    `packages/pg-delta/src/core/objects/subscription/subscription.diff.test.ts`
    `packages/pg-delta/src/core/objects/subscription/changes/subscription.create.test.ts`
    `packages/pg-delta/src/core/objects/subscription/changes/subscription.alter.test.ts`
    `packages/pg-delta/src/core/objects/subscription/changes/subscription.comment.test.ts`
    `packages/pg-delta/src/core/objects/subscription/changes/subscription.drop.test.ts`
    `packages/pg-delta/src/core/objects/subscription/changes/subscription.traits.test.ts`
    `packages/pg-delta/src/core/objects/table/table.diff.test.ts`
    `packages/pg-delta/src/core/objects/table/changes/table.create.test.ts`
    `packages/pg-delta/src/core/objects/index/index.diff.test.ts`
    `packages/pg-delta/src/core/sort/sort-changes.test.ts`
- repository maintenance checks:
  - `bun install --frozen-lockfile`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `git diff --check`

Docker-backed pg-delta integration tests were not runnable in this runner
because neither `docker`, `dockerd`, `podman`, nor `nerdctl` is installed, so
the refresh used focused unit tests plus live GitHub and git-diff evidence
instead of container-backed roundtrip probes.
