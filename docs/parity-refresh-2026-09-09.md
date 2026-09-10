# Parity refresh report - 2026-09-09

This report records the 2026-09-09 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`)

## 1) Benchmark status refresh

This refresh **changes** the benchmark matrix versus
[`docs/parity-refresh-2026-09-08.md`](./parity-refresh-2026-09-08.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021** and **022** remain active unresolved gaps
- resolved pgschema issue [#564](https://github.com/pgplex/pgschema/issues/564)
  is now promoted from the open watch list into new benchmark
  [024](../benchmark/024-pg18-not-null-validation.md)
- the active resolved-issue benchmark gap set is now **021**, **022**, and
  **024**
- checked-in `pg-delta` remains
  `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`)
- live `pg-delta/main` advanced to
  `ce61f01c24962fe21b9d02b319d8c26be0b5fd13` through merged PRs
  [#460](https://github.com/supabase/pg-toolbelt/pull/460),
  [#461](https://github.com/supabase/pg-toolbelt/pull/461),
  [#462](https://github.com/supabase/pg-toolbelt/pull/462),
  [#464](https://github.com/supabase/pg-toolbelt/pull/464),
  [#467](https://github.com/supabase/pg-toolbelt/pull/467), and
  [#469](https://github.com/supabase/pg-toolbelt/pull/469)
- checked-in/live `pgschema` advances from
  `b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd` to
  `738a3bb40cf6b062928eeb564e3a98ec7f3c6989` through merged PRs
  [#585](https://github.com/pgplex/pgschema/pull/585),
  [#586](https://github.com/pgplex/pgschema/pull/586),
  [#587](https://github.com/pgplex/pgschema/pull/587), and
  [#590](https://github.com/pgplex/pgschema/pull/590)

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
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and extracts table constraints only
    when `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18
    `contype = 'n'` state is invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
- among the live pg-delta delta since checked-in alpha.49, only
  `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  changed from the previously cited neighboring active-gap files; the current
  `relations.ts`, `tables.ts`, and `helpers.ts` gap codepaths remain unchanged
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, and `pgschema#589` returned no dedicated pg-toolbelt issue
  or PR
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for benchmarks **021** / **022**; benchmark **024** is promoted from
  the earlier draft-only #564 note based on current source-level parity
  evidence

## 2) Open / resolved pgschema delta on 2026-09-09

Today's upstream delta is mostly on the pgschema side again, but it changes the
watch list materially:

- pgschema issues
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#564](https://github.com/pgplex/pgschema/issues/564), and
  [#584](https://github.com/pgplex/pgschema/issues/584) all closed on
  2026-09-08 through merged PRs
  [#586](https://github.com/pgplex/pgschema/pull/586),
  [#587](https://github.com/pgplex/pgschema/pull/587), and
  [#585](https://github.com/pgplex/pgschema/pull/585)
- pgschema issue [#588](https://github.com/pgplex/pgschema/issues/588) opened
  on 2026-09-08
- pgschema issue [#589](https://github.com/pgplex/pgschema/issues/589) opened
  and closed on 2026-09-09 through merged PR
  [#590](https://github.com/pgplex/pgschema/pull/590)

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84), and
  [#588](https://github.com/pgplex/pgschema/issues/588) are all
  **not parity work for pg-delta**
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### Newly closed pgschema issues

- resolved issue [#589](https://github.com/pgplex/pgschema/issues/589)
  appears **covered** in current pg-delta:
  - `TABLE_CONSTRAINTS_SQL` in
    `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    canonical `pg_get_constraintdef(con.oid)` text as the constraint `def`
  - current diff keys table constraints on that `def`, and
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts`
    replays foreign-key definitions verbatim through
    `ADD CONSTRAINT ... ${def}`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts` already asserts
    canonical constraint-definition extraction
- resolved issue [#564](https://github.com/pgplex/pgschema/issues/564)
  remains **not covered** in current pg-delta and now belongs in the resolved
  benchmark set as [024](../benchmark/024-pg18-not-null-validation.md):
  - pgschema PR [#566](https://github.com/pgplex/pgschema/pull/566) adds the
    PostgreSQL 18 native `NOT NULL ... NOT VALID` + `VALIDATE CONSTRAINT` path
  - pgschema PR [#587](https://github.com/pgplex/pgschema/pull/587) closes the
    follow-up visibility gap for pending invalid PG18 not-null constraints
  - current pg-delta still lacks both the planner rewrite and the extracted
    pending-validation state
- resolved issue [#450](https://github.com/pgplex/pgschema/issues/450)
  remains **not parity work for pg-delta**; the fix is about stubbing
  referenced roles into pgschema's embedded/external plan database
- resolved issue [#584](https://github.com/pgplex/pgschema/issues/584)
  remains **not parity work for pg-delta**; the fix mirrors target extensions
  into pgschema's embedded plan database and folds the roles half into #450

There is still **no dedicated exact open pg-toolbelt parity tracker** for the
active benchmarks **021** / **022** / **024** or the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444). The target repository
`avallete/delta-schema-compare` still has no existing issues, so there were no
repo-local tracker issues to update in this refresh either.

## 3) What changed in this refresh

- advance the checked-in `pgschema` submodule pointer to
  `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`
- refresh `benchmark/README.md` to the 2026-09-09 latest-state snapshot,
  including the new benchmark **024**, the closed **#450 / #564 / #584**
  watch-list movement, and the new covered resolved issue **#589**
- refresh `benchmark/review-memory.json` review timestamps/fingerprints for the
  current open watch-list items **#49 / #52 / #84 / #588**, move
  **#450 / #564 / #584** from the open bucket into the resolved bucket, add
  resolved **#589**, and refresh active benchmark issue fingerprints
  **#499** / **#501**
- add a fresh 2026-09-09 refresh note to benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md)
- promote the previous draft-only #564 note into new benchmark
  [024](../benchmark/024-pg18-not-null-validation.md)
- add a promotion note back to
  [`docs/parity-issue-drafts-2026-08-31.md`](./parity-issue-drafts-2026-08-31.md)
- add this report as the 2026-09-09 latest-state sweep
- leave the checked-in `pg-delta` pointer at
  `08219f1a8832f86e7287e50bab793a498129db7a` while recording a live-head
  revalidation against `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, because the
  recent pg-delta delta stays adjacent to the active parity gaps

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-since queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-08 sort:updated-desc'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-08 sort:updated-desc'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-08 sort:updated-desc'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-08 sort:updated-desc'`
- GitHub CLI state checks for current open pgschema issues
  **#49**, **#52**, **#84**, and **#588**
- GitHub CLI state checks for resolved pgschema issues
  **#450**, **#564**, **#584**, **#589**, **#499**, and **#501**
- GitHub CLI state checks for current pgschema PR context:
  **#585**, **#586**, **#587**, and **#590**
- GitHub CLI exact duplicate queries around the active benchmarks, the newly
  benchmarked **#564** scenario, the new resolved **#589** scenario, and the
  current open watch-list item **#588**, plus
  `gh issue list -R avallete/delta-schema-compare`, which is still empty
- dry-run compare scripts:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - both still return **0** labeled parity items, so manual unlabeled sweeps
    remain required
- repo Python regression tests:
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - **9 tests passed**
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts`
  - `repos/pgschema/internal/diff/column.go`
  - `repos/pgschema/internal/diff/constraint.go`
  - `repos/pgschema/internal/plan/rewrite.go`
  - `repos/pgschema/testdata/diff/online/add_not_null/`
  - `repos/pgschema/testdata/diff/create_table/add_fk/`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `git diff --check`
