# Parity refresh report - 2026-10-12

This report records the 2026-10-12 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`)

## 1) Benchmark status refresh

This refresh keeps checked-in/live `pg-delta` at
`7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4` and keeps checked-in/live
`pgschema` at `580f4040d0f3c1bfad1497918200c9c1f638a020`; neither submodule head
moved since the 2026-10-11 refresh.

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
  - exact duplicate search `pgschema#499` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"PARTITION OF"` still only surfaces
    umbrella / adjacent partition context rather than an exact child-local
    override tracker
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence, not the
    `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - exact duplicate search `pgschema#501` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"VIRTUAL" generated` still only surfaces
    umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    plus historical merged PRs
    [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
    [#299](https://github.com/supabase/pg-toolbelt/pull/299)
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows still do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - exact duplicate search `pgschema#564` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"NOT NULL" "NOT VALID"` still only
    surfaced merged PR [#484](https://github.com/supabase/pg-toolbelt/pull/484)
    on this sweep

### Upstream movement since 2026-10-11

- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-11'`
  surfaced only open PR
  [#637](https://github.com/pgplex/pgschema/pull/637)
  (`feat: manage global roles and ownership`); it still belongs to the
  separate global-state cluster rather than the schema-diff benchmark set
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-11'`
  returned `[]`, so there is no new pg-toolbelt issue or PR delta beyond the
  existing active-gap tracker context
- direct exact searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#627`, `pgschema#638`, `pgschema#639`, `pgschema#640`, and
  `pgschema#641` still returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-12

The current open pgschema watch list remains:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
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
  [#628](https://github.com/pgplex/pgschema/issues/628),
  [#629](https://github.com/pgplex/pgschema/issues/629),
  [#630](https://github.com/pgplex/pgschema/issues/630),
  [#631](https://github.com/pgplex/pgschema/issues/631),
  [#632](https://github.com/pgplex/pgschema/issues/632),
  [#633](https://github.com/pgplex/pgschema/issues/633),
  [#634](https://github.com/pgplex/pgschema/issues/634),
  [#635](https://github.com/pgplex/pgschema/issues/635),
  [#636](https://github.com/pgplex/pgschema/issues/636),
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641)
- open PR [#637](https://github.com/pgplex/pgschema/pull/637)

Current verdicts remain:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, and **#623**
  remain **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**,
  **#640**, and **#641** remain **covered**
- the global-state cluster **#627 - #636** / **#637** is still **not added as
  a benchmark parity gap in this repo**
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- closed issues **#599**, **#600**, **#601**, **#602**, **#603**, and **#606**
  remain **covered**
- closed issues **#596** and **#607** remain **not parity work**
- there is currently **no open uncovered parity candidate**

No benchmark item changed status in this refresh, and no duplicate local
tracker issue exists in this repository.

## 3) What changed in this refresh

- keep the checked-in/live `repos/pg-toolbelt` submodule pointer at
  `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-10-12 latest-state snapshot
- append 2026-10-12 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` for open issue
  [#623](https://github.com/pgplex/pgschema/issues/623) so the cached
  fingerprint matches the live `updated_at` without changing its
  `not_parity` verdict
- add this report as the 2026-10-12 no-new-pg-toolbelt-delta sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git merge --ff-only origin/avallete/schema-comparison-benchmark-c001`
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-11' --limit 100 --json number,title,updatedAt,state,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-11' --limit 100 --json number,title,updatedAt,state,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#499' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#501' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#564' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#627' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#638' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#639' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#640' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#641' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs '"PARTITION OF"' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs '"VIRTUAL" generated' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs '"NOT NULL" "NOT VALID"' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
- repo validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `USER_SITE=$(python3 -m site --user-site) && PYTHONPATH="$USER_SITE${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="<token>" DRY_RUN=true python3 scripts/compare_issues.py`
  - `USER_SITE=$(python3 -m site --user-site) && PYTHONPATH="$USER_SITE${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="<token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`

The dry-run compare scripts still returned **0** labeled open issues and **0**
labeled resolved issues on this environment, so the manual unlabeled-watch-list
refresh remains necessary for current parity coverage.
