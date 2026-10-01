# Parity refresh report - 2026-10-01

This report records the 2026-10-01 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `8154463671f8637d5a7a9b65134526fa3eb06b84`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`524c04f3c1cbd4290630e0a5ed87c15ca86663b2` to
`8154463671f8637d5a7a9b65134526fa3eb06b84` through merged PRs
[#500](https://github.com/supabase/pg-toolbelt/pull/500),
[#501](https://github.com/supabase/pg-toolbelt/pull/501),
[#504](https://github.com/supabase/pg-toolbelt/pull/504), and release PR
[#507](https://github.com/supabase/pg-toolbelt/pull/507), while
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
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` now
    carries merged `_partitionKey` / `replaceRoot` logic from PR
    [#501](https://github.com/supabase/pg-toolbelt/pull/501) and merged
    dependency-edge repairs from PR
    [#504](https://github.com/supabase/pg-toolbelt/pull/504), but the
    partition-child create path still emits bare
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list
  - closed issue [#497](https://github.com/supabase/pg-toolbelt/issues/497),
    open follow-up issue [#502](https://github.com/supabase/pg-toolbelt/issues/502),
    merged PR [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    merged stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    and merged PR [#504](https://github.com/supabase/pg-toolbelt/pull/504)
    remain adjacent rather than exact duplicates; #504's own deferrals still
    call out unmodeled partition-level default overrides
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
  - the 2026-10-01 pg-delta delta lands in partition-key replacement,
    dependency-edge resolution, pg-topo range-type support, and release
    packaging; none of those changes preserves generated kind
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
  - merged PRs [#500](https://github.com/supabase/pg-toolbelt/pull/500),
    [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    [#504](https://github.com/supabase/pg-toolbelt/pull/504), and release PR
    [#507](https://github.com/supabase/pg-toolbelt/pull/507) stay outside PG18
    table-column nullability modeling
  - benchmark **024** still has no exact current pg-toolbelt issue or PR; the
    only historical exact hit remains merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which targets
    the pre-clean-room engine only

### Upstream movement since 2026-09-30

- `gh search issues --repo pgplex/pgschema --updated '>=2026-09-30'`
  surfaced only open issue
  [#623](https://github.com/pgplex/pgschema/issues/623)
- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-09-30'`
  surfaced no pgschema PR updates
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-09-30'`
  surfaced merged PRs
  [#500](https://github.com/supabase/pg-toolbelt/pull/500),
  [#501](https://github.com/supabase/pg-toolbelt/pull/501),
  [#504](https://github.com/supabase/pg-toolbelt/pull/504), and
  [#507](https://github.com/supabase/pg-toolbelt/pull/507), open PRs
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) and
  [#506](https://github.com/supabase/pg-toolbelt/pull/506), and closed issues
  [#282](https://github.com/supabase/pg-toolbelt/issues/282) and
  [#497](https://github.com/supabase/pg-toolbelt/issues/497)
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side,
benchmarks **021** / **022** still only have umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) as exact tracker
context, and benchmark **024** still has no exact current pg-toolbelt issue
or PR.

## 2) Open / resolved pgschema delta on 2026-10-01

The current open pgschema watch list is now:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597),
  [#598](https://github.com/pgplex/pgschema/issues/598), and
  [#623](https://github.com/pgplex/pgschema/issues/623)
- open PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622)

Current verdicts remain unchanged except for the new non-parity watch item:

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

- advance the checked-in/live `repos/pg-toolbelt` submodule pointer to
  `8154463671f8637d5a7a9b65134526fa3eb06b84`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-10-01 latest-state snapshot
- append 2026-10-01 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` fingerprints for the open pgschema
  watch list, the three active benchmarked issues, and the recent resolved
  watch-list issues against the new pg-delta head
- add this report as the 2026-10-01 latest-state sweep

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
  - `gh search issues --repo pgplex/pgschema --updated '>=2026-09-30' --limit 50 --json number,title,state,updatedAt,url`
  - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-09-30' --limit 50 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-09-30' --limit 100 --json number,title,state,updatedAt,url,isPullRequest`
  - `gh issue view 332 -R supabase/pg-toolbelt`
  - `gh issue view 497 -R supabase/pg-toolbelt`
  - `gh issue view 502 -R supabase/pg-toolbelt`
  - `gh pr view 501 -R supabase/pg-toolbelt`
  - `gh pr view 504 -R supabase/pg-toolbelt`
  - `gh pr view 493 -R supabase/pg-toolbelt --json number,title,state,updatedAt,url`
  - `gh pr view 506 -R supabase/pg-toolbelt --json number,title,state,updatedAt,url`
  - `gh pr list -R pgplex/pgschema --state open --limit 20`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url`
- repo Python validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
