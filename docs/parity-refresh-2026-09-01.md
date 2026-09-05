# Parity refresh report - 2026-09-01

This report records the 2026-09-01 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `97d8d60dd72a46704cc63b71b63aab2784847658`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `107ac3df4b889c527215d1f6a37df64b33154c16`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-31.md`](./parity-refresh-2026-08-31.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**
- checked-in/live `pg-delta` remains
  `107ac3df4b889c527215d1f6a37df64b33154c16`
  (`@supabase/pg-delta@1.0.0-alpha.48`)
- checked-in/live `pgschema` remains
  `97d8d60dd72a46704cc63b71b63aab2784847658`
  (`v1.12.5`)
- no new merged pgschema PRs landed after the 2026-08-31 refresh, and
  pg-toolbelt's open issue/PR set is unchanged, so today's comparison is still
  against the same checked-in/live code heads

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
  evidence for both active benchmarks, and there was no new pg-delta or
  pgschema code delta after 2026-08-31 that touches those active codepaths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#559`, `pgschema#564`,
  `pgschema#569`, `pgschema#571`, `pgschema#573`, and `pgschema#574` returned
  no dedicated pg-toolbelt issue or PR

## 2) Open pgschema watch-list delta on 2026-09-01

New current open pgschema watch-list items are:

- [#573](https://github.com/pgplex/pgschema/issues/573) - `not dumping sequences`
- [#574](https://github.com/pgplex/pgschema/issues/574) - `plan wrongly creates sequences`

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
- open issue [#569](https://github.com/pgplex/pgschema/issues/569) remains
  **covered** in current pg-delta's declarative `schema apply` flow
- open issue [#571](https://github.com/pgplex/pgschema/issues/571) remains
  **covered** in current pg-delta's dependency model
- open issue [#573](https://github.com/pgplex/pgschema/issues/573) appears
  **covered** in current pg-delta's sequence export/load path:
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
    emits real `CREATE SEQUENCE` plus sequence grants and keeps `OWNED BY` with
    the owning table file
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
    confirms the split sequence/table file model still converges
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts` renders
    explicit `CREATE SEQUENCE ...` statements instead of dropping sequence DDL
- open issue [#574](https://github.com/pgplex/pgschema/issues/574) appears
  **covered** in current pg-delta's explicit `DEFAULT nextval(...)` / sequence
  model:
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts` preserves user
    sequences as first-class `sequence` facts and keeps the
    `default -> sequence` dependency edge
  - `repos/pg-toolbelt/packages/pg-delta/corpus/sequence-default/b.sql` pins
    an explicit shared-sequence `DEFAULT nextval(...)` form
  - current pg-delta planner source has no `BIGSERIAL` rewrite path that would
    guess `<table>_id_seq` in place of a referenced shared sequence

There is still **no dedicated exact open pg-toolbelt parity tracker** for the
active benchmarks **021** / **022**, the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444), or the open
not-covered pgschema issue [#564](https://github.com/pgplex/pgschema/issues/564).
Current open pg-toolbelt issue
[#451](https://github.com/supabase/pg-toolbelt/issues/451) and open PRs
[#432](https://github.com/supabase/pg-toolbelt/pull/432),
[#303](https://github.com/supabase/pg-toolbelt/pull/303), and
[#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
adjacent context, but none is an exact duplicate of the active benchmarks or
the open #564 parity candidate.

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-09-01 latest-state snapshot
- refresh `benchmark/review-memory.json`:
  - update **#559** with its latest pgschema `updated_at`
  - add new open watch-list entries **#573** and **#574** as `covered`
- add this report as the 2026-09-01 latest-state sweep
- no benchmark file changed because the benchmark matrix did not change
- no new draft-only tracker markdown was added because open pgschema issue
  **#564** remains the only current not-covered open parity candidate

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current open pgschema issues
  **#49**, **#52**, **#84**, **#450**, **#559**, **#564**, **#569**, **#571**,
  **#573**, and **#574**
- GitHub CLI state checks for current pg-toolbelt issues / PRs and duplicate
  queries around the active benchmarks and open watch-list items
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/corpus/sequence-default/b.sql`
- `python3 -m pip install -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`

The dry-run script runs are still expected to return **0** parity items because
the manually tracked current open pgschema issues **#49**, **#52**, **#84**,
**#450**, **#559**, **#564**, **#569**, **#571**, **#573**, and **#574** do
not carry the upstream `Bug` / `Feature` labels that the automation currently
filters on.
