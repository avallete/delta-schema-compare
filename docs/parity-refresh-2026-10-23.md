# Parity refresh report - 2026-10-23

This report records the 2026-10-23 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `265af521e462577886ea6fdbb5777e1a23811cce`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`63b3f653d99f936fa40c5a7689d771e829f09f45` to
`265af521e462577886ea6fdbb5777e1a23811cce` through merged PRs
[#550](https://github.com/supabase/pg-toolbelt/pull/550),
[#551](https://github.com/supabase/pg-toolbelt/pull/551),
[#556](https://github.com/supabase/pg-toolbelt/pull/556),
[#557](https://github.com/supabase/pg-toolbelt/pull/557), and release PR
[#547](https://github.com/supabase/pg-toolbelt/pull/547), while checked-in/live
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
  - merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) now
    records extra `INHERITS` parents as `inheritsAlso` and can emit
    `ALTER INDEX ... SET/RESET` so a non-subpartitioned child index keeps its
    own storage options. That is adjacent partition machinery, not the
    child-column element list
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence rather
    than the `VIRTUAL` versus `STORED` kind
  - merged PR [#556](https://github.com/supabase/pg-toolbelt/pull/556) moved
    `columnClause()` from `src/plan/rules/helpers.ts` into
    `src/plan/rules/tables.ts`. The helper still hard-codes
    `GENERATED ALWAYS AS (...) STORED`
  - a `VIRTUAL` search under `packages/pg-delta` still returns no matches
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18 `contype =
    'n'` rows remain outside diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - the `63b3f653...265af521` delta still lands no exact current pg-toolbelt
    issue or PR for this benchmark
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - stays solved. Merged PR
    [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains in the
    checked-in/live history
  - today's `src/plan/internal.ts` edit from PR
    [#550](https://github.com/supabase/pg-toolbelt/pull/550) adds a row-type
    cycle veto next to the existing same-table constraint fold guard

### Upstream movement since 2026-10-22

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-22'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-22'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-22'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --merged --updated '>=2026-10-22'`
  returned `[]`
- a direct open-issue listing still shows only
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
  [#653](https://github.com/pgplex/pgschema/issues/653)
- older open PR [#662](https://github.com/pgplex/pgschema/pull/662)
  (`updatedAt` `2026-10-17T15:35:33Z`) remains watch-only `MATCH FULL`
  context: exact duplicate searches for `"MATCH FULL"` and `confmatchtype`
  still found no pg-toolbelt issue or PR, while current pg-delta still
  preserves the clause via verbatim `pg_get_constraintdef(con.oid)`
  extraction plus verbatim `def` replay. The current tree still lacks a
  dedicated scenario test
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-22'`
  returned `[]`
- `gh search issues --repo supabase/pg-toolbelt --state closed --updated '>=2026-10-22'`
  returned `[]`
- `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-22'`
  surfaced open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#493](https://github.com/supabase/pg-toolbelt/pull/493),
  [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#555](https://github.com/supabase/pg-toolbelt/pull/555), and
  [#558](https://github.com/supabase/pg-toolbelt/pull/558)
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-22'`
  surfaced merged PRs [#547](https://github.com/supabase/pg-toolbelt/pull/547),
  [#550](https://github.com/supabase/pg-toolbelt/pull/550),
  [#551](https://github.com/supabase/pg-toolbelt/pull/551),
  [#556](https://github.com/supabase/pg-toolbelt/pull/556), and
  [#557](https://github.com/supabase/pg-toolbelt/pull/557)
- direct views keep these previously watched items open, with no update in
  today's date window: issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#518](https://github.com/supabase/pg-toolbelt/issues/518)
  (`updatedAt` `2026-10-20T13:17:30Z`), and
  [#554](https://github.com/supabase/pg-toolbelt/issues/554)
  (`updatedAt` `2026-10-21T15:42:52Z`)
- merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is the
  benchmark-adjacent code movement. It fixes three export round-trip gaps:
  multi-parent `INHERITS`, a partition child's own index storage options, and
  a `CHECK` that calls a function over the table row type. pgschema searches
  for `multi-parent`, `fillfactor`, and `row type` did not yield a new open
  parity issue. The PR leaves one known corpus gap for sub-partition index
  options in `docs/roadmap/pg-delta-next-follow-ups.md`
- merged PR [#556](https://github.com/supabase/pg-toolbelt/pull/556) is a pure
  helper move. It changes where benchmark **022**'s `STORED` keyword is
  emitted and does not change the keyword
- merged PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) explains
  unqualified routine failures under apply's `pg_catalog` search path. It
  stays unmatched on the pgschema side
- merged PR [#557](https://github.com/supabase/pg-toolbelt/pull/557) turns
  `synchronous_commit` off for shadow loads. Schema diff output is unchanged
- merged PR [#547](https://github.com/supabase/pg-toolbelt/pull/547) is the
  alpha release that includes the commits above
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) gained
  commits on 2026-10-22 (`settle renamed tables against the target's
  spelling`, `guard exact renames on the own-text settle pass`). It is still
  not in the checked-in/live head. pgschema searches for `settle spelling`
  returned `[]`
- open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) gained
  commits on 2026-10-22 that narrow skipped-column cascading. It remains
  unmatched policy-withheld-prerequisite context
- open PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) gained
  commits on 2026-10-22 for membership, password, and role-setting identity
  spelling. It remains adjacent global-state work around umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627)
- open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) show updated
  timestamps in today's window. Their latest commits are still from
  2026-09-10 and 2026-09-30
- open PR [#558](https://github.com/supabase/pg-toolbelt/pull/558) only splits
  the new export round-trip CI job into more shards
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore stays **021**, **022**, and **024**.
Benchmark **025** stays **Solved in pg-delta**. There is still **no open
uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-23

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

- merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is now in
  the checked-in/live head. Its three export fixes do not close benchmarks
  **021**, **022**, or **024**
- merged PR [#556](https://github.com/supabase/pg-toolbelt/pull/556) moves the
  benchmark **022** emission site into `tables.ts` and leaves `STORED`
  hard-coded
- merged PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) is now
  in the checked-in/live head as unmatched apply/search_path context
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) stays
  open for the user-function `DEFAULT` order case
- open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554) stays
  unmatched generated-column apply-failure context
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) stays
  unmatched rename/respell context, with new commits after the 2026-10-22
  refresh
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

- refresh `benchmark/README.md` to the 2026-10-23 latest-state snapshot
- add this report as the 2026-10-23 parity snapshot
- add 2026-10-23 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md),
  [024](../benchmark/024-pg18-not-null-validation.md), and
  [025](../benchmark/025-self-referencing-fk-nonpk-unique-ordering.md)
- point benchmark **022**'s current-status and fix plan at
  `src/plan/rules/tables.ts` `columnClause()`, where merged PR
  [#556](https://github.com/supabase/pg-toolbelt/pull/556) now keeps the
  hard-coded `STORED` keyword
- record adjacent merged PRs
  [#550](https://github.com/supabase/pg-toolbelt/pull/550) and
  [#556](https://github.com/supabase/pg-toolbelt/pull/556) against the gaps
  they do not close
- advance the `repos/pg-toolbelt` submodule pointer to
  `265af521e462577886ea6fdbb5777e1a23811cce`
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
  [#506](https://github.com/supabase/pg-toolbelt/pull/506), and
  [#548](https://github.com/supabase/pg-toolbelt/pull/548), still have no
  matching pgschema counterpart that should become a new benchmark
- merged PRs [#550](https://github.com/supabase/pg-toolbelt/pull/550) and
  [#551](https://github.com/supabase/pg-toolbelt/pull/551) close pg-delta-side
  export and apply behavior that the current pgschema open-issue list does
  not track
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
- `bun test packages/pg-delta/src/plan/constraint-fold.test.ts packages/pg-delta/src/plan/internal.test.ts packages/pg-delta/src/plan/rules/constraint-validated.test.ts`
  (**55 tests**, pass)
- `git diff --check`

Bun was not preinstalled; `curl -fsSL https://bun.sh/install | bash` plus
`bun install` in `repos/pg-toolbelt` worked. The submodule lockfile change
from that install was restored before commit. Containerized pg-delta tests
were not run because this pod has neither `docker` nor `dockerd`. The
benchmark verdicts therefore rely on the checked-in source at
`265af521e462577886ea6fdbb5777e1a23811cce`, the merged PR
[#550](https://github.com/supabase/pg-toolbelt/pull/550) /
[#556](https://github.com/supabase/pg-toolbelt/pull/556) diffs, and the
passing non-Docker planner unit tests above.
