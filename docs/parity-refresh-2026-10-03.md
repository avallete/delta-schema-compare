# Parity refresh report - 2026-10-03

This report records the 2026-10-03 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `6845a0beb646cec0bcbf894cec99cbcae2567fc6`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live heads unchanged from the 2026-10-02
snapshot.

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
    pg-toolbelt issue or PR; keyword `"PARTITION OF"` searches still only
    surface issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    plus adjacent follow-up
    [#502](https://github.com/supabase/pg-toolbelt/issues/502)
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - exact duplicate search `pgschema#501` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"VIRTUAL" generated` still only surfaces
    issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows still do not become diff-visible facts and only
    survive long enough to emit `table_not_null_comment_skipped` diagnostics
    for commented rows
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - exact duplicate search `pgschema#564` and keyword
    `"NOT NULL" "NOT VALID"` both still return no current pg-toolbelt issue
    or PR

### Upstream movement since 2026-10-02

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-03'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-03'`
  returned `[]`
- open pgschema PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain open without new
  updates since 2026-09-20 / 2026-09-24
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-03'`
  returned `[]`
- open pg-toolbelt issue [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  open pg-toolbelt issue [#502](https://github.com/supabase/pg-toolbelt/issues/502),
  and open release PR [#509](https://github.com/supabase/pg-toolbelt/pull/509)
  remain unchanged since 2026-09-29 / 2026-09-29 / 2026-10-02
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-03

The current open pgschema watch list remains:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597),
  [#598](https://github.com/pgplex/pgschema/issues/598), and
  [#623](https://github.com/pgplex/pgschema/issues/623)
- open PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622)

Current verdicts remain unchanged:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, and **#623**
  remain **not parity work for pg-delta**
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

- keep the checked-in/live `repos/pg-toolbelt` submodule pointer at
  `6845a0beb646cec0bcbf894cec99cbcae2567fc6`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-10-03 latest-state snapshot
- append 2026-10-03 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` review timestamps for the current
  watch-list and active benchmark issues
- add this report as the 2026-10-03 latest-state sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct submodule head checks:
  - `git -C repos/pg-toolbelt rev-parse HEAD origin/main`
  - `git -C repos/pgschema rev-parse HEAD origin/main`
- GitHub CLI updated-state and duplicate checks:
  - `gh search issues --repo pgplex/pgschema --updated '>=2026-10-03' --limit 50 --json number,title,state,updatedAt,url`
  - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-03' --limit 50 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh pr list -R pgplex/pgschema --state open --limit 20 --json number,title,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-03' --limit 100 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh issue view 332 -R supabase/pg-toolbelt --json number,title,state,updatedAt,url,body`
  - `gh issue view 502 -R supabase/pg-toolbelt --json number,title,state,updatedAt,url,body`
  - `gh pr view 509 -R supabase/pg-toolbelt --json number,title,state,updatedAt,url,body`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#499' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#501' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#564' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt '\"PARTITION OF\"' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt '\"VIRTUAL\" generated' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt '\"NOT NULL\" \"NOT VALID\"' --limit 20 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url`
- repo validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
