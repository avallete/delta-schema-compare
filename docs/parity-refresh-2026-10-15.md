# Parity refresh report - 2026-10-15

This report records the 2026-10-15 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `dcba3be89d42eeca1ede3b939672a6c3e9009f87`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0abee28a54bd855c13d45e2d7ebb5cb647b46693`)

## 1) Benchmark status refresh

This refresh keeps checked-in/live `pg-delta` at
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` and advances checked-in/live
`pgschema` from `2bb3352d40c5fc55c3c43abcce395dd11cd22450` to
`dcba3be89d42eeca1ede3b939672a6c3e9009f87` through merged PRs
[#643](https://github.com/pgplex/pgschema/pull/643) and
[#649](https://github.com/pgplex/pgschema/pull/649).

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

### Upstream movement since 2026-10-14

- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-14'`
  surfaced merged PRs [#643](https://github.com/pgplex/pgschema/pull/643) and
  [#649](https://github.com/pgplex/pgschema/pull/649), open PRs
  [#645](https://github.com/pgplex/pgschema/pull/645),
  [#646](https://github.com/pgplex/pgschema/pull/646), and
  [#647](https://github.com/pgplex/pgschema/pull/647), open issues
  [#641](https://github.com/pgplex/pgschema/issues/641) and
  [#644](https://github.com/pgplex/pgschema/issues/644), plus the new closed
  unlabeled issue [#648](https://github.com/pgplex/pgschema/issues/648)
- PR #643 is now in the checked-in/live `pgschema` head, but it lands in
  partition-index attachment / naming fidelity plus nested-partition
  generation rather than the active pg-delta benchmark gaps
- closed issue [#648](https://github.com/pgplex/pgschema/issues/648) /
  merged PR [#649](https://github.com/pgplex/pgschema/pull/649) is
  **covered / avoided** in current pg-delta: table CHECK constraints are
  extracted from `pg_get_constraintdef(con.oid)` in
  `src/extract/relations.ts`, passed through `deparsedDef()` unchanged, and
  rendered back verbatim by `src/plan/rules/constraints.ts`
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-14'`
  surfaced only open PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
- direct exact searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#627`, `pgschema#640`, `pgschema#641`, `pgschema#644`, and
  `pgschema#648` still returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-15

The current open pgschema issue watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#623](https://github.com/pgplex/pgschema/issues/623),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639),
[#640](https://github.com/pgplex/pgschema/issues/640),
[#641](https://github.com/pgplex/pgschema/issues/641), and
[#644](https://github.com/pgplex/pgschema/issues/644).

Current verdicts now are:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, **#623**, and
  **#644** remain **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**,
  **#640**, and **#641** remain **covered**
- the broader global-state cluster is now narrowed to open issue
  [#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637) after child issues
  **#628-#636** closed; it is still **not added as a benchmark parity gap in
  this repo**
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- new resolved issue **#648** is **covered / avoided** in current pg-delta
- there is currently **no open uncovered parity candidate**

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-15 latest-state snapshot
- append 2026-10-15 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` to:
  - update the open watch-list fingerprints to the new `pgschema` head
  - remove now-closed open entries **#628-#636**
  - add resolved **not_parity** entries for closed issues **#628-#636**
  - add resolved covered entry **#648**
- add this report as the 2026-10-15 merged-upstream / unlabeled-issue sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `python3 -m pip install --user -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH`:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true python3 scripts/compare_resolved.py`
- `git diff --check`

The dry-run compare scripts still returned **0 labeled open issues** and
**0 labeled resolved issues**, which means manual unlabeled sweeps remain
required. Today's closed issue
[#648](https://github.com/pgplex/pgschema/issues/648) would not have appeared
in the script-driven run without the manual updated-since issue / PR review.
