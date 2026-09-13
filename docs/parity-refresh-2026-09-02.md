# Parity refresh report - 2026-09-02

This report records the 2026-09-02 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `97d8d60dd72a46704cc63b71b63aab2784847658`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `107ac3df4b889c527215d1f6a37df64b33154c16`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-09-01.md`](./parity-refresh-2026-09-01.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**
- checked-in/live `pg-delta` remains
  `107ac3df4b889c527215d1f6a37df64b33154c16`
  (`@supabase/pg-delta@1.0.0-alpha.48`)
- checked-in/live `pgschema` remains
  `97d8d60dd72a46704cc63b71b63aab2784847658`
  (`v1.12.5`)
- no new merged pgschema PRs landed after the 2026-09-01 refresh, and the
  pg-toolbelt open issue / PR set is unchanged, so today's comparison is still
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
  pgschema code delta after 2026-09-01 that touches those active codepaths
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#559`, `pgschema#564`,
  `pgschema#571`, `pgschema#573`, `pgschema#574`, and `pgschema#576` returned
  no dedicated pg-toolbelt issue or PR

## 2) Open pgschema watch-list delta on 2026-09-02

Today's watch-list delta versus 2026-09-01 is:

- new open issue
  [#576](https://github.com/pgplex/pgschema/issues/576) -
  `extra sequences created for custom-named sequence defaults`
- previously open issue
  [#569](https://github.com/pgplex/pgschema/issues/569) closed on 2026-09-02
  after the already-merged pgschema fix
  [#570](https://github.com/pgplex/pgschema/pull/570)
- pgschema also now has open PR
  [#572](https://github.com/pgplex/pgschema/pull/572) for still-open issue
  [#571](https://github.com/pgplex/pgschema/issues/571)

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
- open issue [#571](https://github.com/pgplex/pgschema/issues/571) remains
  **covered** in current pg-delta's dependency model; upstream PR
  [#572](https://github.com/pgplex/pgschema/pull/572) does not change the
  current pg-delta verdict
- open issue [#573](https://github.com/pgplex/pgschema/issues/573) remains
  **covered** in current pg-delta's sequence export/load path:
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
    emits real `CREATE SEQUENCE` plus sequence grants and keeps `OWNED BY` with
    the owning table file
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
    confirms the split sequence/table file model still converges
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts` renders
    explicit `CREATE SEQUENCE ...` statements instead of dropping sequence DDL
- open issue [#574](https://github.com/pgplex/pgschema/issues/574) remains
  **covered** in current pg-delta's explicit `DEFAULT nextval(...)` / sequence
  model:
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts` preserves user
    sequences as first-class `sequence` facts and keeps the
    `default -> sequence` dependency edge
  - `repos/pg-toolbelt/packages/pg-delta/corpus/sequence-default/b.sql` pins
    an explicit shared-sequence `DEFAULT nextval(...)` form
  - current pg-delta planner source has no `BIGSERIAL` rewrite path that would
    guess `<table>_id_seq` in place of a referenced shared sequence
- open issue [#576](https://github.com/pgplex/pgschema/issues/576) appears
  **covered** in current pg-delta; it is a narrower custom-sequence-default
  variant of the same family surfaced by #574:
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts` preserves the
    user sequence fact plus the `default -> sequence` dependency edge
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts` round-trips an
    explicit `CREATE SEQUENCE` plus `DEFAULT nextval(...)` pair
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
    still files real sequence DDL under `sequences/`, and
    `src/plan/rules/sequences.ts` renders explicit `CREATE SEQUENCE` instead of
    inventing default `<table>_<column>_seq` names
- closed issue [#569](https://github.com/pgplex/pgschema/issues/569) now moves
  to the resolved bucket and remains **covered** in current pg-delta;
  `src/frontends/sql-order.ts` can split and topo-order SQL-file statements,
  `src/frontends/load-sql-files.ts` still retries file-granular dependency
  rounds, and `tests/reorder-shadow.test.ts` plus
  `tests/load-sql-files.test.ts` already pin wrong-order shadow-load cases

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
the open #564 parity candidate. Exact duplicate searches for #571, #573, #574,
and #576 were also empty, but those issues appear already covered.

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-09-02 latest-state snapshot
- refresh `benchmark/review-memory.json`:
  - move **#569** from `open` to `resolved` as `covered`
  - refresh **#571**, **#573**, and **#574** with their latest pgschema
    `updated_at` values
  - add new open watch-list entry **#576** as `covered`
- add this report as the 2026-09-02 latest-state sweep
- no benchmark file changed because the benchmark matrix did not change
- no new draft-only tracker markdown was added because open pgschema issue
  **#564** remains the only current not-covered open parity candidate

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current open pgschema issues
  **#49**, **#52**, **#84**, **#450**, **#559**, **#564**, **#571**, **#573**,
  **#574**, and **#576**
- GitHub CLI state checks for the newly closed pgschema issue **#569** and the
  related pgschema PRs **#570** (merged) and **#572** (open)
- GitHub CLI state checks for current pg-toolbelt issues / PRs and duplicate
  queries around the active benchmarks and current watch-list items
- GitHub CLI check of `avallete/delta-schema-compare` issues, which is still
  empty, so there were no existing repo-local tracker issues to update
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/reorder-shadow.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/sql-order.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts`
  - `repos/pg-toolbelt/packages/pg-delta/corpus/sequence-default/b.sql`

The dry-run compare-script behavior is still expected to return **0** parity
items because the manually tracked current open pgschema issues **#49**,
**#52**, **#84**, **#450**, **#559**, **#564**, **#571**, **#573**, **#574**,
and **#576** do not carry the upstream `Bug` / `Feature` labels that the
automation currently filters on.
