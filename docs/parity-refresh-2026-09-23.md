# Parity refresh report - 2026-09-23

This report records the 2026-09-23 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live heads unchanged from the 2026-09-22
snapshot:

- `pg-delta` remains at `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- `pgschema` remains at `580f4040d0f3c1bfad1497918200c9c1f638a020`

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only open tracker context; issue
    [#483](https://github.com/supabase/pg-toolbelt/issues/483), PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484), PR
    [#485](https://github.com/supabase/pg-toolbelt/pull/485), issue
    [#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
    [#477](https://github.com/supabase/pg-toolbelt/issues/477), PR
    [#478](https://github.com/supabase/pg-toolbelt/pull/478), and merged PRs
    [#480](https://github.com/supabase/pg-toolbelt/pull/480) /
    [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
    rather than benchmark-closing
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
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
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - PR [#484](https://github.com/supabase/pg-toolbelt/pull/484) is adjacent
    domain `NOT NULL` work only
  - PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) touches the
    same PG18 `contype = 'n'` catalog family, but its summary explicitly says
    the change is diagnostics-only and leaves the fact base, content hashes,
    and resulting plans unchanged
  - benchmark **024** therefore still has no exact current pg-toolbelt issue
    or PR; the only direct historical duplicate-search hit remains merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which landed on
    the pre-clean-room engine

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-23

There is no new pgschema issue or PR delta since the 2026-09-22 refresh:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-22'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-22'`
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

- keep the checked-in/live `repos/pg-toolbelt` submodule pointer at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-23 latest-state snapshot
- add fresh 2026-09-23 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- refresh `benchmark/review-memory.json` reviewed timestamps for:
  - open watch-list entries **#49** / **#52** / **#84** / **#559** /
    **#597** / **#598**
  - active benchmark entries **#499** / **#501** / **#564**
- add this report as the 2026-09-23 latest-state sweep
- no new benchmark files and no new draft-only uncovered issue docs were
  needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state open --limit 200 --json number,title,updatedAt,url,labels`
  - `gh issue list -R pgplex/pgschema --state closed --limit 200 --json number,title,updatedAt,closedAt,url,labels`
  - `gh pr list -R pgplex/pgschema --state open --limit 100 --json number,title,updatedAt,url,headRefName,baseRefName`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 200 --json number,title,updatedAt,url,labels`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 100 --json number,title,updatedAt,url,headRefName,baseRefName`
  - `gh issue view 483 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 484 -R supabase/pg-toolbelt --json number,title,body,state,isDraft,updatedAt,url,baseRefName,headRefName`
  - `gh pr view 485 -R supabase/pg-toolbelt --json number,title,body,state,isDraft,updatedAt,url,baseRefName,headRefName`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 120 --json number,title,state,updatedAt,url` (**returned `[]`**)
- repo Python validation:
  - `python3 -m pip install -r requirements.txt`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this refresh because the
  checked-in/live heads are unchanged from 2026-09-22 and the only new
  upstream pg-toolbelt movement is adjacent issue / PR work rather than merged
  code on `main`
