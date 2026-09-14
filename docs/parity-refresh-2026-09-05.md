# Parity refresh report - 2026-09-05

This report records the 2026-09-05 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `c6ed06f6fd5f1e36a00787b7034e35bda025e86b`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-09-04.md`](./parity-refresh-2026-09-04.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**
- checked-in/live `pg-delta` remains
  `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`)
- checked-in/live `pgschema` advanced from
  `89265906bd4d1a5c65971529989a81eb8b159d96` to
  `c6ed06f6fd5f1e36a00787b7034e35bda025e86b` through merged PR
  [#578](https://github.com/pgplex/pgschema/pull/578)
- the new pgschema delta is still adjacent to the active gaps: it adds
  `ALTER SEQUENCE ... OWNED BY` / `OWNED BY NONE` coverage for ownership-only
  changes in the already-resolved
  [#573](https://github.com/pgplex/pgschema/issues/573) sequence family

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
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for both active benchmarks, and today's upstream delta does not
  touch those active pg-delta codepaths
- resolved sequence issue
  [#573](https://github.com/pgplex/pgschema/issues/573) remains covered in
  current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts` still
    renders explicit `CREATE SEQUENCE` statements
  - `sequenceOwnedBySpecs()` in
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` already
    emits both `ALTER SEQUENCE ... OWNED BY ...` and `OWNED BY NONE`
  - `tests/export-serial-owned-by.test.ts`,
    `tests/export.test.ts`, and
    `tests/load-sql-files-statement-fallback.test.ts` still cover the explicit
    sequence + ownership path
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#564`, and `pgschema#573` returned
  no dedicated pg-toolbelt issue or PR

## 2) Open / resolved pgschema watch-list delta on 2026-09-05

Today's watch-list delta versus 2026-09-04 is narrow:

- the open watch list is unchanged:
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#564](https://github.com/pgplex/pgschema/issues/564)
- resolved issue [#573](https://github.com/pgplex/pgschema/issues/573) gained
  the merged follow-up
  [#578](https://github.com/pgplex/pgschema/pull/578), which fixes
  ownership-only sequence changes on the pgschema side without changing the
  current pg-delta parity verdict

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#559](https://github.com/pgplex/pgschema/issues/559) remain
  **not parity work for pg-delta**
- open issue [#564](https://github.com/pgplex/pgschema/issues/564) remains the
  one **open not-covered parity candidate** from the current watch list; the
  existing draft-only tracker body remains in
  [`docs/parity-issue-drafts-2026-08-31.md`](./parity-issue-drafts-2026-08-31.md)
- resolved issues [#573](https://github.com/pgplex/pgschema/issues/573),
  [#574](https://github.com/pgplex/pgschema/issues/574), and
  [#576](https://github.com/pgplex/pgschema/issues/576) remain **covered** in
  current pg-delta's explicit sequence + ownership model

There is still **no dedicated exact open pg-toolbelt parity tracker** for the
active benchmarks **021** / **022**, the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444), or the one open
not-covered parity candidate [#564](https://github.com/pgplex/pgschema/issues/564).
Current open pg-toolbelt issue
[#451](https://github.com/supabase/pg-toolbelt/issues/451) and open PRs
[#432](https://github.com/supabase/pg-toolbelt/pull/432),
[#303](https://github.com/supabase/pg-toolbelt/pull/303), and
[#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
adjacent context, but none is an exact duplicate of the active benchmarks or
the open #564 watch-list item.

## 3) What changed in this refresh

- update the checked-in `repos/pgschema` pointer to
  `c6ed06f6fd5f1e36a00787b7034e35bda025e86b` (merged
  [pgschema#578](https://github.com/pgplex/pgschema/pull/578))
- port the latest checked-in benchmark/docs baseline from the most recent parity
  refresh branch so this branch reflects the accumulated benchmark set through
  2026-09-04 before applying today's delta
- refresh `benchmark/README.md` to the 2026-09-05 latest-state snapshot
- refresh `benchmark/review-memory.json` fingerprints for the current open
  watch-list items, active benchmark issues **#499** / **#501**, and the
  rechecked resolved sequence/dependency items **#571** / **#573** / **#574** /
  **#576**
- add a fresh 2026-09-05 refresh note to benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md)
- add this report as the 2026-09-05 latest-state sweep
- no new benchmark file or draft-only tracker markdown was added because the
  benchmark matrix did not change and open pgschema issue **#564** remains the
  only current not-covered open parity candidate

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI state checks for current open pgschema issues
  **#49**, **#52**, **#84**, **#450**, **#559**, and **#564**
- GitHub CLI state checks for resolved pgschema issue **#573**, related
  duplicates **#574** / **#576**, and merged PR **#578**
- GitHub CLI state checks for current pg-toolbelt issues / PRs and exact
  duplicate queries around the active benchmarks and current watch-list items
- GitHub CLI check of `avallete/delta-schema-compare` issues, which is still
  empty, so there were no existing repo-local tracker issues to update
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
- `python3 -m pip install -r requirements.txt`
- `export GITHUB_TOKEN="$(gh auth token)" && DRY_RUN=true python3 scripts/compare_issues.py`
  (**0** labeled items found)
- `export GITHUB_TOKEN="$(gh auth token)" && DRY_RUN=true python3 scripts/compare_resolved.py`
  (**0** labeled items found)
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `git diff --check`

The dry-run compare scripts still returned **0** items because the current
parity-relevant pgschema watch-list issues remain unlabeled, so the manual
unlabeled sweep remains necessary.
