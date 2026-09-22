# Parity refresh report - 2026-09-22

This report records the 2026-09-22 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`0882fc4cb6b792b79b599a414b434e4e048b6672` to
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` through merged release PR
[#481](https://github.com/supabase/pg-toolbelt/pull/481), while checked-in/live
`pgschema` remains unchanged at
`580f4040d0f3c1bfad1497918200c9c1f638a020`.

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - the pg-delta delta between the checked-in/live heads is release-only:
    merged PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) only
    bumps `packages/pg-delta/CHANGELOG.md` and
    `packages/pg-delta/package.json`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; issues
    [#476](https://github.com/supabase/pg-toolbelt/issues/476),
    [#477](https://github.com/supabase/pg-toolbelt/issues/477),
    [#482](https://github.com/supabase/pg-toolbelt/issues/482),
    [#483](https://github.com/supabase/pg-toolbelt/issues/483), PR
    [#478](https://github.com/supabase/pg-toolbelt/pull/478), and merged PRs
    [#480](https://github.com/supabase/pg-toolbelt/pull/480) /
    [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
    rather than benchmark-closing
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - the pg-delta delta between the checked-in/live heads is release-only:
    merged PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) only
    bumps `packages/pg-delta/CHANGELOG.md` and
    `packages/pg-delta/package.json`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; there is still no exact pg-toolbelt
    issue or PR for the generated-kind gap itself
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - the pg-delta delta between the checked-in/live heads is release-only:
    merged PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) only
    bumps `packages/pg-delta/CHANGELOG.md` and
    `packages/pg-delta/package.json`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - new issue [#482](https://github.com/supabase/pg-toolbelt/issues/482) is a
    domain `NOT NULL` rendering bug rather than this table-column PG18 native
    validation workflow
  - duplicate searches still find no exact current pg-toolbelt issue or PR for
    this benchmark; the only historical hit is merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which patched
    the pre-clean-room
    `packages/pg-delta/src/core/objects/table/table.model.ts` path and does
    not close the current `src/extract/relations.ts` /
    `src/plan/rules/tables.ts` gap

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-22

There is no new pgschema issue or PR delta since the 2026-09-21 refresh:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-21'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-21'`
  returned `[]`

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain
  **not parity work for pg-delta**
- open issue [#598](https://github.com/pgplex/pgschema/issues/598) remains
  **covered** in current pg-delta; open PR
  [#611](https://github.com/pgplex/pgschema/pull/611) is still the upstream
  fix path
- unrelated security-update PR
  [#605](https://github.com/pgplex/pgschema/pull/605) remains open
- there is currently **no open uncovered parity candidate** on the pgschema
  side

## 3) What changed in this refresh

- advance the checked-in `repos/pg-toolbelt` submodule pointer to
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- keep the checked-in `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-22 latest-state snapshot
- add fresh 2026-09-22 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- refresh `benchmark/review-memory.json` bookkeeping on the new pg-delta SHA:
  - open watch-list entries **#49** / **#52** / **#84** / **#559** /
    **#597** / **#598**
  - active benchmark entries **#499** / **#501** / **#564**
  - changed resolved-context entries **#596** / **#599** / **#600** /
    **#601** / **#602** / **#603** / **#607**
- add this report as the 2026-09-22 latest-state sweep
- no new benchmark files and no new draft-only uncovered issue docs were
  needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-21' --limit 100 --json number,title,state,updatedAt,url,labels` (**returned `[]`**)
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-21' --limit 100 --json number,title,state,isDraft,mergedAt,updatedAt,url` (**returned `[]`**)
  - `gh pr list -R pgplex/pgschema --state open --limit 20 --json number,title,updatedAt,url,isDraft,headRefName,baseRefName`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 100 --search 'sort:updated-desc' --json number,title,updatedAt,url,state`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 200 --json number,title,updatedAt,url`
  - `gh pr list -R supabase/pg-toolbelt --state merged --limit 20 --search 'merged:>=2026-09-20 sort:updated-desc' --json number,title,mergedAt,url,headRefName,baseRefName`
  - `gh pr view 481 -R supabase/pg-toolbelt --json number,title,state,mergedAt,url,body,commits`
  - `gh issue view 482 -R supabase/pg-toolbelt --json number,title,body,url,comments`
  - `gh issue view 483 -R supabase/pg-toolbelt --json number,title,body,url,comments`
  - `gh pr view 174 -R supabase/pg-toolbelt --json number,title,state,mergedAt,baseRefName,headRefName,body,files,commits,url`
  - focused duplicate / adjacency searches for benchmarks **021**, **022**,
    and **024** with `gh issue list` / `gh pr list` searches on the
    pg-toolbelt repo
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 120 --json number,title,state,updatedAt,url` (**returned `[]`**)
- repo Python validation:
  - `python3 -m pip install -r requirements.txt`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this refresh because the only
  pg-delta delta between the checked-in/live heads is release metadata, and
  the active gap verdicts are unchanged at the source / codepath level
