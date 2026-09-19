# Parity refresh report - 2026-09-08

This report records the 2026-09-08 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `a982dfab6a87fa97f47130a1754dbd48d69446ce`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-09-07.md`](./parity-refresh-2026-09-07.md).

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**
- checked-in `pg-delta` remains
  `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`)
- live `pg-delta/main` advanced to
  `a982dfab6a87fa97f47130a1754dbd48d69446ce` through merged PR
  [#458](https://github.com/supabase/pg-toolbelt/pull/458), but that delta
  only guards checked-out clients from connection errors in apply/extract/load
  callers and does not touch the active partition-child or generated-column
  codepaths
- checked-in/live `pgschema` advances from
  `fe7c64bfa410e7f9e8235eae3b912eb163b255f4` to
  `b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd` through merged PRs
  [#582](https://github.com/pgplex/pgschema/pull/582) and
  [#583](https://github.com/pgplex/pgschema/pull/583)

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    filters relation columns with `a.attislocal`, so child-local overrides on
    inherited partition columns never become diff-visible facts
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
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for both active scenarios; today's pg-delta delta is adjacent only
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, and `pgschema#584` returned no dedicated pg-toolbelt issue
  or PR
- keyword searches for `VIRTUAL generated` and `PARTITION OF` still surface
  umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332);
  `PARTITION OF` also still surfaces unrelated open issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451)

## 2) Open / resolved pgschema delta on 2026-09-08

Today's upstream delta is mostly on the pgschema side, plus one adjacent
pg-delta main change:

- pgschema issue [#559](https://github.com/pgplex/pgschema/issues/559) closed
  on 2026-09-08 through merged PR
  [#583](https://github.com/pgplex/pgschema/pull/583)
- pgschema issue [#584](https://github.com/pgplex/pgschema/issues/584) opened
  on 2026-09-08, with open PR
  [#585](https://github.com/pgplex/pgschema/pull/585)
- merged pgschema PR [#582](https://github.com/pgplex/pgschema/pull/582)
  broadened the resolved
  [#580](https://github.com/pgplex/pgschema/issues/580) family after the
  original merge in [#581](https://github.com/pgplex/pgschema/pull/581)
- live `pg-delta/main` advanced through merged PR
  [#458](https://github.com/supabase/pg-toolbelt/pull/458), but no exact new
  pg-toolbelt issue or PR duplicate was found for the active benchmarks or the
  current watch-list items

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84), and
  [#450](https://github.com/pgplex/pgschema/issues/450) remain
  **not parity work for pg-delta**
- open issue [#564](https://github.com/pgplex/pgschema/issues/564) remains the
  one **open not-covered parity candidate** from the current watch list; the
  existing draft-only tracker body remains in
  [`docs/parity-issue-drafts-2026-08-31.md`](./parity-issue-drafts-2026-08-31.md)
- open issue [#584](https://github.com/pgplex/pgschema/issues/584) is also
  **not parity work for pg-delta**:
  - open PR [#585](https://github.com/pgplex/pgschema/pull/585) mirrors target
    extensions into pgschema's embedded plan database, and explicitly treats
    the roles half as a duplicate of
    [#450](https://github.com/pgplex/pgschema/issues/450)
  - current pg-delta does not depend on an embedded plan database, already
    extracts extensions and roles as first-class facts in
    `repos/pg-toolbelt/packages/pg-delta/src/extract/extract.ts`, and has
    current extension / cluster-scope role coverage in
    `tests/vault-presence.test.ts` and
    `tests/supabase-cluster-scope-roles.test.ts`

### Newly closed / broadened resolved items

- resolved issue [#559](https://github.com/pgplex/pgschema/issues/559)
  remains **not parity work for pg-delta** even after the merged fix in
  [#583](https://github.com/pgplex/pgschema/pull/583), because current
  pg-delta still explicitly keeps row-level data comparison out of scope:
  `src/frontends/load-sql-files.ts` and
  `tests/load-sql-files.test.ts` both state that the loader deliberately never
  compares data
- resolved issue [#579](https://github.com/pgplex/pgschema/issues/579)
  remains **covered** in current pg-delta:
  - `src/extract/dependencies.ts` maps relation row types through
    `pg_type.typrelid` back to the owning table/view facts
  - `corpus/table-fn-dep--setof-function` plus
    `tests/composite-order-roundtrip.test.ts` still cover the same
    `RETURNS SETOF <relation>` dependency family
- resolved issue [#580](https://github.com/pgplex/pgschema/issues/580)
  still appears **covered** after merged follow-up
  [#582](https://github.com/pgplex/pgschema/pull/582):
  - `exportSqlFiles()` preserves plan order across files in the default
    `by-object` layout and offers filename-stable dependency order through
    `layout: "ordered"`
  - `tests/export.test.ts` and `tests/export-fidelity.test.ts` still gate
    `load(export(fb)) ≡ fb` across layouts
  - `src/frontends/load-sql-files.ts` and `src/plan/preamble.ts` both set
    `check_function_bodies = off`, so forward-referencing SQL function bodies
    remain replayable in the load/apply path
  - `src/extract/dependencies.ts` maps relation row types through
    `pg_type.typrelid` back to the owning table/view facts and resolves
    `pg_proc` aggregates (`prokind = 'a'`) as first-class dependency endpoints,
    so aggregates over view row types still sort after the view
  - no dedicated exact pg-toolbelt issue or PR was found

There is still **no dedicated exact open pg-toolbelt parity tracker** for the
active benchmarks **021** / **022**, the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444), or the one open
not-covered parity candidate
[#564](https://github.com/pgplex/pgschema/issues/564). The target repository
`avallete/delta-schema-compare` still has no existing issues, so there were no
repo-local trackers to update in this refresh.

## 3) What changed in this refresh

- advance the checked-in `pgschema` submodule pointer to
  `b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd`
- refresh `benchmark/README.md` to the 2026-09-08 latest-state snapshot,
  including the #559 -> resolved shift, the new #584 watch-list item, and the
  merged states of pgschema PRs #582 / #583
- refresh `benchmark/review-memory.json` review timestamps/fingerprints for the
  current watch-list items, move #559 from the open bucket to the resolved
  bucket, add #584, and refresh the active benchmark issue fingerprints
  **#499** / **#501** plus the recently closed **#579** / **#580**
- add fresh 2026-09-08 refresh notes to benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md)
- add this report as the 2026-09-08 latest-state sweep
- leave the checked-in `pg-delta` pointer at
  `08219f1a8832f86e7287e50bab793a498129db7a` while recording a live-head
  revalidation against `a982dfab6a87fa97f47130a1754dbd48d69446ce`, because PR
  #458 is adjacent only
- no benchmark row status changed, no new benchmark file was added, and no new
  draft-only tracker markdown was needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `git -C repos/pg-toolbelt ls-remote origin refs/heads/main`
- `git -C repos/pgschema ls-remote origin refs/heads/main`
- GitHub CLI updated-since queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-07 sort:updated-desc'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-07 sort:updated-desc'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-07 sort:updated-desc'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-07 sort:updated-desc'`
- GitHub CLI state checks for current open pgschema issues
  **#49**, **#52**, **#84**, **#450**, **#564**, and **#584**
- GitHub CLI state checks for resolved pgschema issues
  **#499**, **#501**, **#559**, **#579**, and **#580**
- GitHub CLI state checks for current pgschema PR context:
  **#582**, **#583**, and **#585**
- GitHub CLI state check for the current live pg-toolbelt delta:
  **#458**
- GitHub CLI exact duplicate queries around the active benchmarks and the
  current watch-list items, plus `gh issue list -R avallete/delta-schema-compare`,
  which is still empty
- dry-run compare scripts:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - both still return **0** labeled parity items, so manual unlabeled sweeps
    remain required
- repo Python regression tests:
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/preamble.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-fidelity.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/composite-order-roundtrip.test.ts`
- Bun was unavailable in this pod, so the live pg-delta revalidation for PR
  #458 stayed at source-diff inspection rather than a new runtime probe; that
  was acceptable here because the merged delta never touched the active
  benchmark codepaths
