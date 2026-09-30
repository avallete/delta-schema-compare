# Parity refresh report - 2026-09-30

This report records the 2026-09-30 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `524c04f3c1cbd4290630e0a5ed87c15ca86663b2`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`e17c45925c3ddbf660dfb13c51029b605bcee448` to
`524c04f3c1cbd4290630e0a5ed87c15ca86663b2` through merged PRs
[#496](https://github.com/supabase/pg-toolbelt/pull/496),
[#495](https://github.com/supabase/pg-toolbelt/pull/495),
[#478](https://github.com/supabase/pg-toolbelt/pull/478),
[#473](https://github.com/supabase/pg-toolbelt/pull/473), and release PR
[#505](https://github.com/supabase/pg-toolbelt/pull/505), while
checked-in/live `pgschema` remains at
`580f4040d0f3c1bfad1497918200c9c1f638a020`.

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
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list
  - open issue [#497](https://github.com/supabase/pg-toolbelt/issues/497) plus
    open PR [#501](https://github.com/supabase/pg-toolbelt/pull/501), merged
    stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503), open
    issue [#502](https://github.com/supabase/pg-toolbelt/issues/502), and open
    PR [#504](https://github.com/supabase/pg-toolbelt/pull/504) sharpen nearby
    partition-key / dependency-edge behavior, but they still do not add
    child-local `PARTITION OF (...)` override extraction or rendering
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - the 2026-09-30 pg-delta delta lands in grants, pinned-extension schema
    export, identity-sequence privileges, and PK-redundant UNIQUE folding;
    none of those changes preserves generated kind
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; there is still no exact current
    pg-toolbelt issue or PR for the generated-kind gap
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows still do not become diff-visible facts and now only
    survive long enough to emit `table_not_null_comment_skipped` diagnostics
    for commented rows
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - the 2026-09-30 pg-delta delta lands in adjacent privilege / extension /
    PK-redundant-UNIQUE work rather than PG18 nullability modeling
  - benchmark **024** still has no exact current pg-toolbelt issue or PR; the
    only historical hit remains merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which targets
    the pre-clean-room engine only

### Upstream movement since 2026-09-29

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-29'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-29'`
  returned `[]`
- `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-29'`
  returned open issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) and
  [#502](https://github.com/supabase/pg-toolbelt/issues/502) plus closed
  issues [#451](https://github.com/supabase/pg-toolbelt/issues/451),
  [#477](https://github.com/supabase/pg-toolbelt/issues/477),
  [#486](https://github.com/supabase/pg-toolbelt/issues/486),
  [#489](https://github.com/supabase/pg-toolbelt/issues/489), and
  [#491](https://github.com/supabase/pg-toolbelt/issues/491)
- `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-29'`
  returned merged PRs
  [#473](https://github.com/supabase/pg-toolbelt/pull/473),
  [#478](https://github.com/supabase/pg-toolbelt/pull/478),
  [#496](https://github.com/supabase/pg-toolbelt/pull/496),
  [#498](https://github.com/supabase/pg-toolbelt/pull/498),
  [#503](https://github.com/supabase/pg-toolbelt/pull/503), and
  [#505](https://github.com/supabase/pg-toolbelt/pull/505), open PRs
  [#493](https://github.com/supabase/pg-toolbelt/pull/493),
  [#500](https://github.com/supabase/pg-toolbelt/pull/500),
  [#501](https://github.com/supabase/pg-toolbelt/pull/501),
  [#504](https://github.com/supabase/pg-toolbelt/pull/504), and
  [#506](https://github.com/supabase/pg-toolbelt/pull/506), and closed PR
  [#472](https://github.com/supabase/pg-toolbelt/pull/472)
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side,
benchmarks **021** / **022** still only have umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) as exact tracker
context, and benchmark **024** still has no exact current pg-toolbelt issue
or PR.

## 2) Open / resolved pgschema delta on 2026-09-30

The current open pgschema watch list is unchanged:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597), and
  [#598](https://github.com/pgplex/pgschema/issues/598)
- open PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622)

Current verdicts remain unchanged:

- open issues **#49**, **#52**, **#84**, **#559**, and **#597** remain
  **not parity work for pg-delta**
- open issue **#598** remains **covered** in current pg-delta via
  invalid-index extraction and `tests/index-invalid-repair.test.ts`
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- closed issues **#599**, **#600**, **#601**, **#602**, **#603**, and
  **#606** remain **covered**
- closed issues **#596** and **#607** remain **not parity work**
- there is currently **no open uncovered parity candidate**

No benchmark item changed status in this refresh, and no duplicate local
tracker issue exists in this repository.

## 3) What changed in this refresh

- advance the checked-in/live `repos/pg-toolbelt` submodule pointer to
  `524c04f3c1cbd4290630e0a5ed87c15ca86663b2`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-30 latest-state snapshot
- append 2026-09-30 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` fingerprints for the open pgschema
  watch list, the three active benchmarked issues, and the recent resolved
  watch-list issues against the new pg-delta head
- add this report as the 2026-09-30 latest-state sweep

No benchmark file changed verdict, no new benchmark file was needed, and no
new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct submodule head checks:
  - `git -C repos/pg-toolbelt rev-parse HEAD origin/main`
  - `git -C repos/pgschema rev-parse HEAD origin/main`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-29'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-29'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-29'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-29'`
  - `gh issue view 332 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 497 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 502 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 501 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,baseRefName,headRefName,mergeStateStatus`
  - `gh pr view 503 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,baseRefName,headRefName,mergeStateStatus`
  - `gh pr view 504 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,baseRefName,headRefName,mergeStateStatus`
  - `gh pr view 506 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,baseRefName,headRefName,mergeStateStatus`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url`
- repo Python validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
