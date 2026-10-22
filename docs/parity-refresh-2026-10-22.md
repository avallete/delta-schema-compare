# Parity refresh report - 2026-10-22

This report records the 2026-10-22 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `63b3f653d99f936fa40c5a7689d771e829f09f45`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`72e47ea0d5c33bd28c2beef0486126f5c63f44d3` to
`63b3f653d99f936fa40c5a7689d771e829f09f45` through merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553), while checked-in/live
`pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. There is **no
benchmark-status reclassification today**:

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, **023**, and **025** stay solved in current
  pg-delta
- benchmarks **021**, **022**, and **024** remain the active unresolved parity
  set
- there is still **no open uncovered parity candidate** on the pgschema side

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    inherited child columns gated by `a.attislocal`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no child column
    elements for local `DEFAULT` / `NOT NULL` overrides
  - merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) edits
    the column-create fold hint in that same file and does not change the
    partition-child create string
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence rather
    than the `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) now
    folds generated columns into `CREATE TABLE` through `columnClause()`, so
    the hard-coded `STORED` keyword is also what an inline create emits. A
    `VIRTUAL` search under `packages/pg-delta` still returns no matches
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18 `contype =
    'n'` rows remain outside diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - the `72e47ea0...63b3f653` delta still lands no exact current pg-toolbelt
    issue or PR for this benchmark
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - stays solved. Merged PR
    [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains in the
    checked-in/live history, and today's `src/plan/internal.ts` edit is a
    comment update beside the same-table constraint fold guard

### Upstream movement since 2026-10-21

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-21'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-21'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-21'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --merged --updated '>=2026-10-21'`
  returned `[]`
- older open PR [#662](https://github.com/pgplex/pgschema/pull/662) remains
  watch-only `MATCH FULL` context: exact duplicate searches for `"MATCH FULL"`
  and `confmatchtype` still found no pg-toolbelt issue or PR, while current
  pg-delta still preserves the clause via verbatim
  `pg_get_constraintdef(con.oid)` extraction plus verbatim `def` replay. The
  current tree still lacks a dedicated scenario test. A formatter fixture in
  `src/frontends/sql-format/wrap.test.ts` mentions `MATCH FULL` only as wrapping
  sample text
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-21'`
  surfaced open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554)
- `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-21'`
  surfaced open PRs [#547](https://github.com/supabase/pg-toolbelt/pull/547)
  and [#555](https://github.com/supabase/pg-toolbelt/pull/555)
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-21'`
  surfaced merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553)
- direct views keep these previously watched items open, with no update in
  today's date window: issue
  [#518](https://github.com/supabase/pg-toolbelt/issues/518) and PRs
  [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#550](https://github.com/supabase/pg-toolbelt/pull/550), and
  [#551](https://github.com/supabase/pg-toolbelt/pull/551)
- merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) is the
  only checked-in/live code movement. It references issue
  [#518](https://github.com/supabase/pg-toolbelt/issues/518), folds generated
  columns into `CREATE TABLE`, and chains later column creates by `attnum`.
  The issue stays open for a `DEFAULT` that calls a user function
- open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554) is the
  follow-up where `canLead` in `src/plan/phases/action-graph.ts` lets a
  generated column on a newly created table lead the position chain, and a
  zero-argument `IMMUTABLE` function can still fail apply. pgschema searches
  for `zero-arg` and `generated expression column order` returned `[]`
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) settles
  deparsed spelling before rename matching and owner checks. It is not in the
  checked-in/live head. pgschema searches for `settle spelling` returned `[]`
- open PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) remains
  unmatched export-roundtrip context and is still outside the checked-in head
- open PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) remains
  adjacent global-state / user-mapping work around umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627)
- open PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) remains
  unmatched apply/search_path context
- open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
  unmatched policy-withheld-prerequisite context
- open PR [#547](https://github.com/supabase/pg-toolbelt/pull/547) is an alpha
  release chore
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore stays **021**, **022**, and **024**.
Benchmark **025** stays **Solved in pg-delta**. There is still **no open
uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-22

The current open pgschema issue watch list is unchanged:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639), and
[#653](https://github.com/pgplex/pgschema/issues/653).

Current verdicts remain:

- open issues **#49**, **#52**, **#84**, **#559**, and **#597** remain
  **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**, and
  **#653** remain **covered**
- the broader global-state cluster remains open umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637); it is still **not added
  as a benchmark parity gap in this repo**
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#534** remains **covered**
- resolved benchmark issue **#564** remains **not covered**
- there is currently **no open uncovered parity candidate**

The new manual-review notes today are pg-toolbelt-side tracker updates:

- merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) is now in
  the checked-in/live head. It changes generated-column ordering and does not
  close benchmarks **021**, **022**, or **024**
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) stays
  open for the user-function `DEFAULT` order case
- open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554) is new
  unmatched generated-column apply-failure context
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) is new
  unmatched rename/respell context
- issues [#525](https://github.com/supabase/pg-toolbelt/issues/525) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544) remain unmatched
  pg-toolbelt-side context only
- PR [#662](https://github.com/pgplex/pgschema/pull/662) remains watch-only
  `MATCH FULL` context even though it did not move in today's updated-since
  sweep

Exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
`pgschema#534`, and `pgschema#653` still returned `[]`. Keyword
`"VIRTUAL" generated` still surfaces only umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus historical
merged PRs [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
[#299](https://github.com/supabase/pg-toolbelt/pull/299). Keyword
`"NOT NULL" "NOT VALID"` still surfaces only merged PR
[#484](https://github.com/supabase/pg-toolbelt/pull/484).

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-22 latest-state snapshot
- add this report as the 2026-10-22 parity snapshot
- add 2026-10-22 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md) so the generated-column
  fold change is recorded against the gaps it does not close
- record adjacent merged PR
  [#553](https://github.com/supabase/pg-toolbelt/pull/553) on the benchmark
  **022** status-matrix row
- advance the `repos/pg-toolbelt` submodule pointer to
  `63b3f653d99f936fa40c5a7689d771e829f09f45`
- update `benchmark/review-memory.json` fingerprints for the current open
  watch list and active resolved benchmarks **#499**, **#501**, **#534**, and
  **#564** because the checked-in/live `pg-delta` head advanced. Verdicts stay
  the same

No new local tracker issue draft was needed:

- benchmarks **021**, **022**, and **024** already have benchmark files, and
  today's code movement does not close them or create a new pgschema scenario
- issues [#518](https://github.com/supabase/pg-toolbelt/issues/518) and
  [#554](https://github.com/supabase/pg-toolbelt/issues/554), plus PRs
  [#555](https://github.com/supabase/pg-toolbelt/pull/555),
  [#550](https://github.com/supabase/pg-toolbelt/pull/550),
  [#551](https://github.com/supabase/pg-toolbelt/pull/551), and
  [#506](https://github.com/supabase/pg-toolbelt/pull/506), still have no
  matching pgschema counterpart
- issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) and PR
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) still sit in the
  repo's explicit global-state / non-benchmark bucket

## 4) Validation notes

This refresh was validated with:

- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH`:
  - `DRY_RUN=true python3 scripts/compare_issues.py` returned **0 labeled open
    issues**
  - `DRY_RUN=true python3 scripts/compare_resolved.py` returned **0 labeled
    resolved issues**
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `bun test packages/pg-delta/src/plan/constraint-fold.test.ts packages/pg-delta/src/plan/internal.test.ts`
  (**53 tests**, pass)
- `git diff --check`

Containerized pg-delta tests, including
`packages/pg-delta/tests/compaction.test.ts` and
`packages/pg-delta/tests/column-order-from-empty.test.ts`, were not run
because this pod has neither `docker` nor `dockerd`. The benchmark verdicts
therefore rely on the checked-in source at
`63b3f653d99f936fa40c5a7689d771e829f09f45`, the merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553) diff, and the passing
non-Docker planner unit tests above.
