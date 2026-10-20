# Parity refresh report - 2026-10-20

This report records the 2026-10-20 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `7931d4167c18c9d849a4ea5737dfcc13f09e36aa`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from `0abee28a54bd855c13d45e2d7ebb5cb647b46693` to
`7931d4167c18c9d849a4ea5737dfcc13f09e36aa` through merged PR
[#541](https://github.com/supabase/pg-toolbelt/pull/541), while checked-in/live
`pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. There is **no benchmark-status
reclassification today**:

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, **024**, and **025** remain the active
  unresolved parity set
- there is still **no open uncovered parity candidate** on the pgschema side

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) closes
    rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    but it only touches `packages/pg-delta/src/proof/prove.ts` plus new
    inherited-rewrite corpus cases
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    inherited child columns gated by `a.attislocal`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no child column
    elements for local `DEFAULT` / `NOT NULL` overrides
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - the `0abee28...7931d416` pg-delta delta never touches
    `src/extract/relations.ts` or `src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence rather
    than the `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - the `0abee28...7931d416` pg-delta delta never touches
    `src/extract/relations.ts` or `src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18 `contype =
    'n'` rows remain outside diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
    still treats a genuine self-reference as inline-safe by skipping it in
    `cyclicForeignKeys()`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts` and
    `repos/pg-toolbelt/packages/pg-delta/src/plan/internal.ts` still allow
    validated FOREIGN KEY constraints to fold inline during export
  - open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus
    open PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) now form
    the exact tracker / fix-in-progress path, but PR #546 is not yet in the
    checked-in/live head

### Upstream movement since 2026-10-19

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-19'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-19'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-19'`
  returned `[]`
- older open PR [#662](https://github.com/pgplex/pgschema/pull/662) remains
  watch-only `MATCH FULL` context: exact duplicate searches for `"MATCH FULL"`
  and `confmatchtype` still found no pg-toolbelt issue or PR, while current
  pg-delta still appears to preserve the clause via verbatim
  `pg_get_constraintdef(con.oid)` extraction plus verbatim `def` replay, but
  the current tree still lacks a dedicated scenario test
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-19'`
  surfaced open issues
  [#339](https://github.com/supabase/pg-toolbelt/issues/339),
  [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  [#525](https://github.com/supabase/pg-toolbelt/issues/525),
  [#543](https://github.com/supabase/pg-toolbelt/issues/543), and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544)
- `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-19'`
  surfaced open PRs
  [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#546](https://github.com/supabase/pg-toolbelt/pull/546),
  [#547](https://github.com/supabase/pg-toolbelt/pull/547),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548), and
  [#549](https://github.com/supabase/pg-toolbelt/pull/549)
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-19'`
  surfaced merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
  only
- issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546) are the only exact
  parity-tracker movement for an active benchmark item
- issue [#544](https://github.com/supabase/pg-toolbelt/issues/544) still has
  no matching pgschema counterpart from today's `BETWEEN` / `nested AND`
  keyword sweeps
- issue [#525](https://github.com/supabase/pg-toolbelt/issues/525) still has
  no matching pgschema counterpart from today's `union alias` / `?column?`
  keyword sweeps
- issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus PR
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
  [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus PR
  [#549](https://github.com/supabase/pg-toolbelt/pull/549) are adjacent
  global-state / role-management work; today's pgschema keyword sweeps still
  only land on umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627), which this repo does
  not promote into a benchmark item
- open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
  unmatched policy-withheld-prerequisite context
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore remains **021**, **022**, **024**, and
**025**. There is still **no open uncovered parity candidate** on the
pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-20

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
- resolved benchmark issues **#499**, **#501**, and **#534** remain
  **tracked**
- resolved benchmark issue **#564** remains **not covered**
- there is currently **no open uncovered parity candidate**

The new manual-review notes today are all pg-toolbelt-side tracker updates:

- merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) is now in
  the checked-in/live head, but it only closes the adjacent rewrite-risk proof
  bug for benchmark **021**, not the child-local partition override gap itself
- open PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) now exists
  as the exact fix-in-progress for benchmark **025**, but it is not merged or
  checked in yet
- issues [#525](https://github.com/supabase/pg-toolbelt/issues/525) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544) remain unmatched
  pg-toolbelt-side context only
- issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus PR
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
  [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus PR
  [#549](https://github.com/supabase/pg-toolbelt/pull/549) add adjacent
  global-state work on the pg-delta side, but today's pgschema keyword sweeps
  still only land on umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627)
- PR [#662](https://github.com/pgplex/pgschema/pull/662) remains watch-only
  `MATCH FULL` context even though it did not move in today's updated-since
  sweep

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-20 latest-state snapshot
- add this report as the 2026-10-20 parity snapshot
- refresh the active benchmark notes for
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [025](../benchmark/025-self-referencing-fk-nonpk-unique-ordering.md)
- update `benchmark/review-memory.json` fingerprints for the current open
  watch list and active resolved benchmarks because the checked-in/live
  `pg-delta` head advanced today

No new local tracker issue draft was needed:

- benchmark **025** already has open pg-toolbelt issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus open PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546)
- issues [#525](https://github.com/supabase/pg-toolbelt/issues/525) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544) still have no
  matching pgschema counterpart
- issue [#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
  [#339](https://github.com/supabase/pg-toolbelt/issues/339), and PRs
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) /
  [#549](https://github.com/supabase/pg-toolbelt/pull/549) still sit in the
  repo's explicit global-state / non-benchmark bucket

## 4) Validation notes

This refresh was validated with:

- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH` when needed:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true python3 scripts/compare_resolved.py`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `git diff --check`

The dry-run compare scripts still returned **0 labeled open issues** and
**0 labeled resolved issues**, which means manual unlabeled sweeps remain
required. Today's review would not have surfaced pg-toolbelt issues
[#339](https://github.com/supabase/pg-toolbelt/issues/339),
[#476](https://github.com/supabase/pg-toolbelt/issues/476),
[#525](https://github.com/supabase/pg-toolbelt/issues/525),
[#543](https://github.com/supabase/pg-toolbelt/issues/543), or
[#544](https://github.com/supabase/pg-toolbelt/issues/544), the new open fix PR
[#546](https://github.com/supabase/pg-toolbelt/pull/546), or the merged
adjacent PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) from the
label-filtered pgschema issue scripts alone.
