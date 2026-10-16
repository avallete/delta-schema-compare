# Parity refresh report - 2026-10-16

This report records the 2026-10-16 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0abee28a54bd855c13d45e2d7ebb5cb647b46693`)

## 1) Benchmark status refresh

This refresh keeps checked-in/live `pg-delta` at
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` and advances checked-in/live
`pgschema` from `dcba3be89d42eeca1ede3b939672a6c3e9009f87` to
`24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca` through merged PRs
[#646](https://github.com/pgplex/pgschema/pull/646),
[#647](https://github.com/pgplex/pgschema/pull/647),
[#655](https://github.com/pgplex/pgschema/pull/655),
[#656](https://github.com/pgplex/pgschema/pull/656),
[#657](https://github.com/pgplex/pgschema/pull/657),
[#658](https://github.com/pgplex/pgschema/pull/658), and release bumps
[#652](https://github.com/pgplex/pgschema/pull/652) /
[#659](https://github.com/pgplex/pgschema/pull/659).

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
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no child column
    elements for local `DEFAULT` / `NOT NULL` overrides
  - new pgschema issue [#653](https://github.com/pgplex/pgschema/issues/653) /
    PR [#645](https://github.com/pgplex/pgschema/pull/645) is **covered /
    avoided** rather than a new gap: the same table create path already
    consumes parent indexes and parent PK / UNIQUE constraints before creating
    the child partition, and
    `repos/pg-toolbelt/packages/pg-delta/src/plan/partition-index-attach.test.ts`
    already covers child-index attach / rename / replacement behavior
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence and not
    the `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows remain outside diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

### Upstream movement since 2026-10-15

- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-15'`
  surfaced new open issue [#653](https://github.com/pgplex/pgschema/issues/653),
  open PRs [#645](https://github.com/pgplex/pgschema/pull/645) and
  [#660](https://github.com/pgplex/pgschema/pull/660), newly closed issues
  [#623](https://github.com/pgplex/pgschema/issues/623),
  [#640](https://github.com/pgplex/pgschema/issues/640),
  [#641](https://github.com/pgplex/pgschema/issues/641),
  [#644](https://github.com/pgplex/pgschema/issues/644), and
  [#654](https://github.com/pgplex/pgschema/issues/654), plus the merged PRs
  above
- open PR [#660](https://github.com/pgplex/pgschema/pull/660) is the upstream
  fix path for issue [#639](https://github.com/pgplex/pgschema/issues/639),
  which current pg-delta already covers via diff-visible `partitionBound` /
  `parentTable` facts and the attach / detach corpuses
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-15'`
  surfaced only open issue [#542](https://github.com/supabase/pg-toolbelt/issues/542),
  which is an apply-time verification hook and does not touch the active gap
  files
- direct exact searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#639`, and `pgschema#653` still returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-16

The current open pgschema issue watch list is now:
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

Current verdicts now are:

- open issues **#49**, **#52**, **#84**, **#559**, and **#597** remain
  **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**, and
  **#653** remain **covered**
- the broader global-state cluster remains open umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637); it is still **not added
  as a benchmark parity gap in this repo**
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- newly closed issues **#623** and **#654** are **not parity**
- newly closed issues **#640** and **#641** remain **covered**
- newly closed issue **#644** remains **not parity**
- there is currently **no open uncovered parity candidate**

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-16 latest-state snapshot
- append 2026-10-16 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` to:
  - update the remaining open watch-list fingerprints to the new `pgschema`
    head
  - move closed issues **#623**, **#640**, **#641**, and **#644** out of the
    open watch list
  - add new open covered entry **#653**
  - add resolved **not_parity** entry **#654**
  - refresh active benchmark fingerprints for **#499**, **#501**, and **#564**
- advance the checked-in `repos/pgschema` submodule pointer to
  `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`
- add this report as the 2026-10-16 parity snapshot

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `python3 -m pip install --user -r requirements.txt`
- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH`:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true python3 scripts/compare_resolved.py`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `git diff --check`

The dry-run compare scripts still returned **0 labeled open issues** and
**0 labeled resolved issues**, which means manual unlabeled sweeps remain
required. Today's new open issue
[#653](https://github.com/pgplex/pgschema/issues/653) and newly closed issues
[#623](https://github.com/pgplex/pgschema/issues/623),
[#640](https://github.com/pgplex/pgschema/issues/640),
[#641](https://github.com/pgplex/pgschema/issues/641),
[#644](https://github.com/pgplex/pgschema/issues/644), and
[#654](https://github.com/pgplex/pgschema/issues/654) would not have been kept
current without the manual updated-since issue / PR review.
