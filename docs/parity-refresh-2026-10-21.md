# Parity refresh report - 2026-10-21

This report records the 2026-10-21 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `72e47ea0d5c33bd28c2beef0486126f5c63f44d3`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from `7931d4167c18c9d849a4ea5737dfcc13f09e36aa` to
`72e47ea0d5c33bd28c2beef0486126f5c63f44d3` through merged PRs
[#546](https://github.com/supabase/pg-toolbelt/pull/546),
[#549](https://github.com/supabase/pg-toolbelt/pull/549), and
[#552](https://github.com/supabase/pg-toolbelt/pull/552), while checked-in/live
`pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. There **is one benchmark-status
reclassification today**:

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, **023**, and now **025** are solved in current
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
  - newer merged PRs [#546](https://github.com/supabase/pg-toolbelt/pull/546),
    [#549](https://github.com/supabase/pg-toolbelt/pull/549), and
    [#552](https://github.com/supabase/pg-toolbelt/pull/552) do not touch that
    extract / plan path
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence rather
    than the `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - the `7931d416...72e47ea0` delta only touches export/global-state paths and
    declarative-e2e harness files, not `relations.ts` or `helpers.ts`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18 `contype =
    'n'` rows remain outside diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - the `7931d416...72e47ea0` delta still lands no exact current pg-toolbelt
    issue or PR for this benchmark
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) closes
    issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) and is now
    in the checked-in/live head
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/internal.ts` now refuses to
    inline a same-table constraint when one of its dependencies is emitted
    after `CREATE TABLE`
  - `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` plus
    `packages/declarative-e2e/scenarios/self-fk-on-unique-index/` now cover the
    exact self-referencing non-PK UNIQUE-key export/reload slice

### Upstream movement since 2026-10-20

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-20'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-20'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-20'`
  returned `[]`
- older open PR [#662](https://github.com/pgplex/pgschema/pull/662) remains
  watch-only `MATCH FULL` context: exact duplicate searches for `"MATCH FULL"`
  and `confmatchtype` still found no pg-toolbelt issue or PR, while current
  pg-delta still appears to preserve the clause via verbatim
  `pg_get_constraintdef(con.oid)` extraction plus verbatim `def` replay, but
  the current tree still lacks a dedicated scenario test
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-20'`
  surfaced open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518)
- `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-20'`
  surfaced open PRs [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#547](https://github.com/supabase/pg-toolbelt/pull/547),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#550](https://github.com/supabase/pg-toolbelt/pull/550),
  [#551](https://github.com/supabase/pg-toolbelt/pull/551), and
  [#553](https://github.com/supabase/pg-toolbelt/pull/553)
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-20'`
  surfaced merged PRs [#546](https://github.com/supabase/pg-toolbelt/pull/546),
  [#549](https://github.com/supabase/pg-toolbelt/pull/549), and
  [#552](https://github.com/supabase/pg-toolbelt/pull/552)
- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) is the
  only benchmark-relevant movement in today's checked-in/live delta: it closes
  benchmark **025** on the current head
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) plus
  open PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) are
  unmatched pg-toolbelt-side export column-order context only; today's
  `declarative export column order` / `generated expression column order`
  searches on pgschema returned `[]`
- open PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) adds an
  export round-trip gate plus three unrelated export-fidelity fixes, but it is
  not in the checked-in/live head and today's pgschema keyword sweeps still
  find no matching benchmark item
- merged PR [#549](https://github.com/supabase/pg-toolbelt/pull/549) plus open
  PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) are adjacent
  global-state / user-mapping work; today's pgschema keyword sweeps still only
  land on umbrella issue [#627](https://github.com/pgplex/pgschema/issues/627),
  which this repo does not promote into a benchmark item
- open PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) remains
  unmatched apply/search_path context
- open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
  unmatched policy-withheld-prerequisite context
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore narrows to **021**, **022**, and **024**.
Benchmark **025** now moves to **Solved in pg-delta**. There is still **no
open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-21

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
- resolved benchmark issue **#534** now moves to **covered**
- resolved benchmark issue **#564** remains **not covered**
- there is currently **no open uncovered parity candidate**

The new manual-review notes today are all pg-toolbelt-side tracker updates:

- merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) is now in
  the checked-in/live head and closes benchmark **025** on the current pg-delta
  source tree
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) plus
  open PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) are new
  unmatched export column-order context only
- open PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is new
  unmatched export-roundtrip context only
- issues [#525](https://github.com/supabase/pg-toolbelt/issues/525) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544) remain unmatched
  pg-toolbelt-side context only
- issues [#476](https://github.com/supabase/pg-toolbelt/issues/476) /
  [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus PRs
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) /
  [#549](https://github.com/supabase/pg-toolbelt/pull/549) remain adjacent
  global-state work on the pg-delta side, but today's pgschema keyword sweeps
  still only land on umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627)
- PR [#662](https://github.com/pgplex/pgschema/pull/662) remains watch-only
  `MATCH FULL` context even though it did not move in today's updated-since
  sweep

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-21 latest-state snapshot
- add this report as the 2026-10-21 parity snapshot
- refresh benchmark
  [025](../benchmark/025-self-referencing-fk-nonpk-unique-ordering.md) because
  it now moves from tracked to solved
- update `benchmark/review-memory.json` fingerprints for the current open
  watch list and active resolved benchmarks because the checked-in/live
  `pg-delta` head advanced today and issue **#534** now moves to `covered`

No new local tracker issue draft was needed:

- benchmark **025** is now already covered by merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546)
- issues [#518](https://github.com/supabase/pg-toolbelt/issues/518),
  [#525](https://github.com/supabase/pg-toolbelt/issues/525), and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544) still have no
  matching pgschema counterpart
- issue [#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
  [#339](https://github.com/supabase/pg-toolbelt/issues/339), PRs
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) /
  [#549](https://github.com/supabase/pg-toolbelt/pull/549), PR
  [#551](https://github.com/supabase/pg-toolbelt/pull/551), and PR
  [#506](https://github.com/supabase/pg-toolbelt/pull/506) still sit in the
  repo's explicit global-state / non-benchmark bucket

## 4) Validation notes

This refresh was validated with:

- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH` when needed:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true python3 scripts/compare_resolved.py`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `bun test packages/pg-delta/src/plan/constraint-fold.test.ts packages/pg-delta/src/plan/internal.test.ts`
- `git diff --check`

The dry-run compare scripts still returned **0 labeled open issues** and
**0 labeled resolved issues**, which means manual unlabeled sweeps remain
required. Today's review would not have surfaced pg-toolbelt issue
[#518](https://github.com/supabase/pg-toolbelt/issues/518), open PRs
[#550](https://github.com/supabase/pg-toolbelt/pull/550),
[#551](https://github.com/supabase/pg-toolbelt/pull/551),
[#553](https://github.com/supabase/pg-toolbelt/pull/553), or the merged
benchmark-closing PR [#546](https://github.com/supabase/pg-toolbelt/pull/546)
from the label-filtered pgschema issue scripts alone.

The exact containerized export regression
`packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` could not be
executed in this environment because neither `docker` nor `dockerd` is
installed on the pod. The benchmark-025 verdict therefore relies on the merged
upstream PR [#546](https://github.com/supabase/pg-toolbelt/pull/546), its
checked-in regression file, and the passing focused non-Docker planner/
compaction unit tests above rather than a local export-reload container run.
