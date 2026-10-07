# Parity refresh report - 2026-10-07

This report records the 2026-10-07 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `5e7c43674ab55f297702d18830489ac0008c019d`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`55d20b026f4208a21d24034c1714d9daa9daf9ee` to
`5e7c43674ab55f297702d18830489ac0008c019d` through merged PR
[#513](https://github.com/supabase/pg-toolbelt/pull/513) and release PR
[#516](https://github.com/supabase/pg-toolbelt/pull/516), while
checked-in/live `pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

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
    pg-toolbelt issue or PR; keyword `"PARTITION OF"` searches still surface
    umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332),
    adjacent follow-up
    [#502](https://github.com/supabase/pg-toolbelt/issues/502), and merged
    partition PRs [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    [#503](https://github.com/supabase/pg-toolbelt/pull/503), and
    [#504](https://github.com/supabase/pg-toolbelt/pull/504)
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - exact duplicate search `pgschema#501` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"VIRTUAL" generated` still surfaces live
    umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    plus historical merged PRs
    [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
    [#299](https://github.com/supabase/pg-toolbelt/pull/299)
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows still do not become diff-visible facts and only
    survive long enough to emit `table_not_null_comment_skipped` diagnostics
    for commented rows
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - exact duplicate search `pgschema#564` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"NOT NULL" "NOT VALID"` still surfaces
    merged domain-only PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484), which remains
    adjacent rather than an exact table-column PG18 validation tracker

### Upstream movement since 2026-10-06

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-06'`
  surfaced open issue [#624](https://github.com/pgplex/pgschema/issues/624)
- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-06'`
  returned the same single issue; open pgschema PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain open without new
  updates since 2026-09-20 / 2026-09-24
- issue [#624](https://github.com/pgplex/pgschema/issues/624) is covered in
  current pg-delta because routine-touching plans deliberately emit
  `SET check_function_bodies = off;`
  (`src/plan/preamble.ts`, `src/plan/preamble.test.ts`,
  `src/plan/render-sql.test.ts`), and the existing
  `corpus/function-ops--sql-body-cross-reference` coverage already exercises
  forward-referencing SQL-language function bodies
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-06'`
  surfaced merged PRs [#513](https://github.com/supabase/pg-toolbelt/pull/513)
  and [#516](https://github.com/supabase/pg-toolbelt/pull/516), merged release
  PR [#509](https://github.com/supabase/pg-toolbelt/pull/509), open PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514),
  [#515](https://github.com/supabase/pg-toolbelt/pull/515), and
  [#520](https://github.com/supabase/pg-toolbelt/pull/520), plus open issues
  [#510](https://github.com/supabase/pg-toolbelt/issues/510),
  [#517](https://github.com/supabase/pg-toolbelt/issues/517),
  [#518](https://github.com/supabase/pg-toolbelt/issues/518), and
  [#519](https://github.com/supabase/pg-toolbelt/issues/519)
- direct inspection plus
  `git -C repos/pg-toolbelt diff --name-only 55d20b026f4208a21d24034c1714d9daa9daf9ee..5e7c43674ab55f297702d18830489ac0008c019d`
  show the only merged pg-delta code lands in OrioleDB assumed-extension
  seeding / dependency resolution / Supabase policy plus release metadata
  rather than the active benchmark source paths
- open pg-toolbelt issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  and open issue [#502](https://github.com/supabase/pg-toolbelt/issues/502)
  remain the only benchmark-adjacent pg-toolbelt tracker context
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-07

The current open pgschema watch list is now:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597),
  [#598](https://github.com/pgplex/pgschema/issues/598),
  [#623](https://github.com/pgplex/pgschema/issues/623), and
  [#624](https://github.com/pgplex/pgschema/issues/624)
- open PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622)

Current verdicts remain:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, and **#623**
  remain **not parity work for pg-delta**
- open issue **#598** remains **covered** in current pg-delta via
  invalid-index extraction and `tests/index-invalid-repair.test.ts`
- open issue **#624** is **covered** in current pg-delta via the existing
  routine-plan `check_function_bodies = off` behavior plus forward-reference
  corpus coverage
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- closed issues **#599**, **#600**, **#601**, **#602**, **#603**, and
  **#606** remain **covered**
- closed issues **#596** and **#607** remain **not parity work**
- there is currently **no open uncovered parity candidate**

No benchmark item changed status in this refresh, and no duplicate local
tracker issue exists in this repository.

## 3) What changed in this refresh

- move the checked-in/live `repos/pg-toolbelt` submodule pointer to
  `5e7c43674ab55f297702d18830489ac0008c019d`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-10-07 latest-state snapshot
- append 2026-10-07 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` review timestamps and fingerprints for
  the current open-watch list, active benchmark issues, and the current
  recently-screened closed-issue set
- add this report as the 2026-10-07 latest-state sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct submodule head checks:
  - `git -C repos/pgschema rev-parse HEAD`
  - `git -C repos/pg-toolbelt rev-parse HEAD`
  - `git -C repos/pg-toolbelt diff --name-only 55d20b026f4208a21d24034c1714d9daa9daf9ee..5e7c43674ab55f297702d18830489ac0008c019d`
- GitHub CLI updated-state and duplicate checks:
  - `gh search issues --repo pgplex/pgschema --updated '>=2026-10-06' --json number,title,state,updatedAt,url`
  - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-06' --json number,title,state,updatedAt,url`
  - `gh issue view 624 -R pgplex/pgschema --json number,title,body,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-06' --json number,title,state,updatedAt,url`
  - `gh pr view 514 -R supabase/pg-toolbelt --json number,title,state,updatedAt,url,files`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#499' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#501' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#564' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#624' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt '"PARTITION OF"' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt '"VIRTUAL" generated' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt '"NOT NULL" "NOT VALID"' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'check_function_bodies' --json number,title,state,updatedAt,url`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
- repo validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
