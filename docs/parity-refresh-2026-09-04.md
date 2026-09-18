# Parity refresh report - 2026-09-04

This report records the 2026-09-04 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `89265906bd4d1a5c65971529989a81eb8b159d96`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-09-03.md`](./parity-refresh-2026-09-03.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**
- checked-in/live `pg-delta` remains
  `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`)
- checked-in/live `pgschema` advanced from
  `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` to
  `89265906bd4d1a5c65971529989a81eb8b159d96` through merged PR
  [#577](https://github.com/pgplex/pgschema/pull/577)
- the new pgschema delta is adjacent to the active gaps: it fixes sequence
  ownership / SERIAL collapsing for
  [#573](https://github.com/pgplex/pgschema/issues/573),
  [#574](https://github.com/pgplex/pgschema/issues/574), and
  [#576](https://github.com/pgplex/pgschema/issues/576)

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
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#564`, and `pgschema#573` returned
  no dedicated pg-toolbelt issue or PR

## 2) Open / resolved pgschema watch-list delta on 2026-09-04

Today's watch-list delta versus 2026-09-03 is:

- previously open issue
  [#573](https://github.com/pgplex/pgschema/issues/573) closed on 2026-09-03
  after the merged fix in
  [#577](https://github.com/pgplex/pgschema/pull/577)
- issue [#573](https://github.com/pgplex/pgschema/issues/573) also gained a
  follow-up comment on 2026-09-04 questioning how strictly `SERIAL` should be
  recognized, but that does not change pg-delta's existing coverage verdict

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
- resolved issue [#573](https://github.com/pgplex/pgschema/issues/573) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts` preserves user
    sequences as first-class facts and keeps the `default -> sequence` edge
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts` round-trips an
    explicit `CREATE SEQUENCE` plus `DEFAULT nextval(...)` pair
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
    confirms export emits real `CREATE SEQUENCE` plus grants while keeping
    `OWNED BY` with the owning table file
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
    confirms the split sequence/table file model still converges
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts` still
    renders explicit `CREATE SEQUENCE` statements instead of inventing
    `<table>_<column>_seq` names

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
the open #564 watch-list item. Resolved issue
[#573](https://github.com/pgplex/pgschema/issues/573) also still has no
dedicated pg-toolbelt tracker, but current pg-delta already covers that
behavior family.

## 3) What changed in this refresh

- update the checked-in `repos/pgschema` pointer to
  `89265906bd4d1a5c65971529989a81eb8b159d96` (merged
  [pgschema#577](https://github.com/pgplex/pgschema/pull/577))
- refresh `benchmark/README.md` to the 2026-09-04 latest-state snapshot
- refresh `benchmark/review-memory.json`:
  - move **#573** from `open` to `resolved` as `covered`
  - refresh fingerprints for the current open watch-list items plus active
    benchmark issues **#499** / **#501** and draft-only gaps **#439** / **#444**
- add a fresh 2026-09-04 refresh note to benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md)
- add this report as the 2026-09-04 latest-state sweep
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
  duplicates **#574** / **#576**, and merged PR **#577**
- GitHub CLI state checks for current pg-toolbelt issues / PRs and exact
  duplicate queries around the active benchmarks and current watch-list items
- GitHub CLI check of `avallete/delta-schema-compare` issues, which is still
  empty, so there were no existing repo-local tracker issues to update
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-serial-owned-by.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-statement-fallback.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/sequences.ts`
