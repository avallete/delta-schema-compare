# Parity refresh report - 2026-08-26

This report records the 2026-08-26 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9a09fe5861575ccfc71c7387ce3524b502992a97`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `6f480e6ed707133e13bd76c5ff3a8df6102806ee`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-25.md`](./parity-refresh-2026-08-25.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
    relation columns with `a.attislocal`, so child-local overrides on inherited
    partition columns never become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child-element
    list
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence as
    `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes `GENERATED ALWAYS AS (...) STORED`
  - `repos/pg-toolbelt/docs/roadmap/pg-delta-next-follow-ups.md` still lists
    PG18 virtual generated columns as an open follow-up item
- the live pg-toolbelt head advanced from
  `d19314ac6586bfaabfaa7c2408038e44fdc7bb6a` to
  `6f480e6ed707133e13bd76c5ff3a8df6102806ee`, but the direct
  `packages/pg-delta` diff only touches `CHANGELOG.md` and `package.json`
- the functional upstream delta is adjacent pg-topo privilege-payload work
  (`.changeset/pg-topo-privilege-payload.md`, `packages/pg-topo/*`) plus
  roadmap/docs updates, not the active benchmark codepaths above
- there was no fresh targeted runtime probe today; the 2026-08-14 runtime
  probes remain the latest direct runtime evidence, and today's source recheck
  does not change them
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, and `pgschema#557` returned no dedicated
  pg-toolbelt issue or PR
- keyword searches for `VIRTUAL generated` and `PARTITION OF` still only surface
  open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)

## 2) Upstream delta on 2026-08-26

- checked-in/live `pg-delta` advanced to
  `6f480e6ed707133e13bd76c5ff3a8df6102806ee`
  (`@supabase/pg-delta@1.0.0-alpha.47`)
- `packages/pg-delta/CHANGELOG.md` records the release as a dependency update
  to `@supabase/pg-topo@1.0.0-alpha.6`
- the current open pgschema issue set is unchanged:
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#557](https://github.com/pgplex/pgschema/issues/557)
- there are still no open pgschema PRs, and no newly merged parity-adjacent
  pgschema PRs since 2026-08-21
- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  closest pg-toolbelt tracker context for active benchmarks **021** / **022**
- current open pg-toolbelt PRs
  [#449](https://github.com/supabase/pg-toolbelt/pull/449),
  [#444](https://github.com/supabase/pg-toolbelt/pull/444),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303),
  [#302](https://github.com/supabase/pg-toolbelt/pull/302), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
  context, but none is an exact duplicate of the active benchmarks, the
  older draft-only gaps, or issue
  [#557](https://github.com/pgplex/pgschema/issues/557)

## 3) What changed in this refresh

- advance checked-in/live `repos/pg-toolbelt` to
  `6f480e6ed707133e13bd76c5ff3a8df6102806ee`
- refresh `benchmark/README.md` to the 2026-08-26 latest-state snapshot
- refresh active benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) with the new
  pg-toolbelt head recheck notes
- refresh `benchmark/review-memory.json` reviewed timestamps and fingerprints for
  still-open watch-list issues **#49**, **#52**, **#84**, **#450**, and
  **#557**, plus the rechecked known gaps **#439**, **#444**, **#499**, and
  **#501**
- add this report as the 2026-08-26 latest-state sweep
- no benchmark status rows changed, no new benchmark files were added, and no
  new draft-only pg-toolbelt issue markdown was needed

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current pgschema issues/PRs and pg-toolbelt
  issues/PRs, plus exact duplicate searches for `pgschema#499`,
  `pgschema#501`, `pgschema#439`, `pgschema#444`, `pgschema#557`,
  `VIRTUAL generated`, `PARTITION OF`, and `lock timeout`
- direct source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/CHANGELOG.md`
  - `repos/pg-toolbelt/docs/roadmap/pg-delta-next-follow-ups.md`
  - `repos/pg-toolbelt/.changeset/pg-topo-privilege-payload.md`
- `git -C repos/pg-toolbelt diff --name-only d19314ac6586bfaabfaa7c2408038e44fdc7bb6a..6f480e6ed707133e13bd76c5ff3a8df6102806ee -- packages/pg-delta`
- `python3 -m pip install -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`

The dry-run script runs still return **0** parity items because the manually
tracked current open pgschema issues **#49**, **#52**, **#84**, **#450**, and
**#557** do not carry the upstream `Bug` / `Feature` labels the automation
filters on.

Bun is not installed in this pod, so no fresh pg-delta / pg-topo test run was
available locally today. The 2026-08-26 verdict therefore rests on GitHub state
checks, direct source inspection, the checked-in changelog/diff evidence, and
the unchanged active-gap codepaths on the new head.
