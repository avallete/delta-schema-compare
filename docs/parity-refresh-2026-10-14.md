# Parity refresh report - 2026-10-14

This report records the 2026-10-14 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `2bb3352d40c5fc55c3c43abcce395dd11cd22450`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0abee28a54bd855c13d45e2d7ebb5cb647b46693`)

## 1) Benchmark status refresh

This refresh keeps checked-in/live `pg-delta` at
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` and checked-in/live `pgschema` at
`2bb3352d40c5fc55c3c43abcce395dd11cd22450`; neither head moved since the
2026-10-13 refresh.

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain the only active unresolved
  gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    inherited child columns gated by `a.attislocal`, so child-local partition
    overrides never become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list
  - open PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) closes
    rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    but it only touches `packages/pg-delta/src/proof/prove.ts` plus corpus
    data; it does not model child-local partition column elements
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    reads `attgenerated`, but only preserves generated-expression presence,
    not the `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows still do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

### Upstream movement since 2026-10-13

- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-13'`
  surfaced open issue [#644](https://github.com/pgplex/pgschema/issues/644)
  (`dump and plan are slow over high-latency connections: one query per
  privilege row and per constraint column`) plus open PR
  [#643](https://github.com/pgplex/pgschema/pull/643)
  (`fix: preserve partition-index names and attachments in dumps`)
- PR #643 is still open and outside the checked-in/live `pgschema` head, so it
  is not being promoted into a new benchmark item in this repo yet
- issue #644 is not a new pg-delta parity gap: the main report is pgschema's
  high-latency inspector architecture, while current pg-delta already resolves
  ACL grantees in bulk and preserves constraint key order with
  `unnest(con.conkey) WITH ORDINALITY`
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-13'`
  surfaced only open PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
- direct exact searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#627`, `pgschema#638`, `pgschema#639`, `pgschema#640`,
  `pgschema#641`, and `pgschema#644` still returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-14

The current open pgschema issue watch list now includes new issue
[#644](https://github.com/pgplex/pgschema/issues/644) alongside the existing
open items from the 2026-10-13 refresh.

Current verdicts remain:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, **#623**, and
  **#644** remain **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**,
  **#640**, and **#641** remain **covered**
- the global-state cluster **#627 - #636** / **#637** is still **not added as
  a benchmark parity gap in this repo**
- open PR **#643** is upstream partition-index / nested-partition work that is
  still open and not yet promoted into a new benchmark item here
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- there is currently **no open uncovered parity candidate**

No benchmark item changed status in this refresh, and no duplicate local
tracker issue exists in this repository.

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-14 latest-state snapshot
- append 2026-10-14 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` by adding the new open watch-list
  entry for issue **#644**
- add this report as the 2026-10-14 no-sha-change / new-watch-item sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-13' --limit 100`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-13' --limit 100`
  - exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
    `pgschema#627`, `pgschema#638`, `pgschema#639`, `pgschema#640`,
    `pgschema#641`, and `pgschema#644`
  - keyword searches for `"PARTITION OF"`, `"VIRTUAL" generated`, and
    `"NOT NULL" "NOT VALID"`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`

The dry-run compare scripts and repo tests are re-run after the documentation
and review-memory edits in this branch.
