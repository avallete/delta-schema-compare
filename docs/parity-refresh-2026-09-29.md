# Parity refresh report - 2026-09-29

This report records the 2026-09-29 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `e17c45925c3ddbf660dfb13c51029b605bcee448`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` to
`e17c45925c3ddbf660dfb13c51029b605bcee448` through merged PRs
[#490](https://github.com/supabase/pg-toolbelt/pull/490),
[#488](https://github.com/supabase/pg-toolbelt/pull/488),
[#494](https://github.com/supabase/pg-toolbelt/pull/494),
[#484](https://github.com/supabase/pg-toolbelt/pull/484),
[#485](https://github.com/supabase/pg-toolbelt/pull/485),
[#492](https://github.com/supabase/pg-toolbelt/pull/492), and
[#499](https://github.com/supabase/pg-toolbelt/pull/499), while
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
  - merged PR [#488](https://github.com/supabase/pg-toolbelt/pull/488) is
    test-only corpus coverage for a different partitioned-parent mix
  - open issue [#497](https://github.com/supabase/pg-toolbelt/issues/497) plus
    open PR [#501](https://github.com/supabase/pg-toolbelt/pull/501) remain
    partition-key retype / parent-replace context rather than the child-local
    override gap itself
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
  - the 2026-09-29 pg-delta delta lands in enum-retype casts, concurrent-drop
    retries, view/materialized-view column grants, and PG18 NOT NULL
    diagnostics; none of those changes preserves generated kind
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; there is still no exact current
    pg-toolbelt issue or PR for the generated-kind gap
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows now survive only long enough to emit
    `table_not_null_comment_skipped` diagnostics for commented rows, not to
    become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - merged PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) is
    diagnostics-only for PG18 table `contype = 'n'` rows, and merged PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484) fixes the
    domain-only half of the same root cause; neither changes the table-column
    fact base or planner
  - benchmark **024** still has no exact current pg-toolbelt issue or PR; the
    only historical hit remains merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which targets
    the pre-clean-room engine only

### Upstream movement since 2026-09-28

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  returned `[]`
- `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
  returned closed issues
  [#482](https://github.com/supabase/pg-toolbelt/issues/482),
  [#483](https://github.com/supabase/pg-toolbelt/issues/483), and
  [#487](https://github.com/supabase/pg-toolbelt/issues/487)
- `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
  returned merged PRs
  [#484](https://github.com/supabase/pg-toolbelt/pull/484),
  [#485](https://github.com/supabase/pg-toolbelt/pull/485),
  [#488](https://github.com/supabase/pg-toolbelt/pull/488),
  [#490](https://github.com/supabase/pg-toolbelt/pull/490),
  [#492](https://github.com/supabase/pg-toolbelt/pull/492),
  [#494](https://github.com/supabase/pg-toolbelt/pull/494),
  [#499](https://github.com/supabase/pg-toolbelt/pull/499), and open PRs
  [#498](https://github.com/supabase/pg-toolbelt/pull/498),
  [#500](https://github.com/supabase/pg-toolbelt/pull/500), and
  [#501](https://github.com/supabase/pg-toolbelt/pull/501)
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side,
benchmarks **021** / **022** still only have umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) as exact tracker
context, and benchmark **024** still has no exact current pg-toolbelt issue
or PR.

## 2) Open / resolved pgschema delta on 2026-09-29

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
- there is currently **no open uncovered parity candidate**

No benchmark item changed status in this refresh, and no duplicate local
tracker issue exists in this repository.

## 3) What changed in this refresh

- advance the checked-in/live `repos/pg-toolbelt` submodule pointer to
  `e17c45925c3ddbf660dfb13c51029b605bcee448`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-29 latest-state snapshot
- append 2026-09-29 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` fingerprints for the open pgschema
  watch list and the three active benchmarked issues against the new pg-delta
  head
- add this report as the 2026-09-29 latest-state sweep

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
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
  - `gh issue view 332 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 497 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 501 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh pr view 488 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh pr view 485 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh pr view 484 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh pr view 490 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh pr view 494 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url`
- repo Python validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
