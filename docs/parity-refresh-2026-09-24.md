# Parity refresh report - 2026-09-24

This report records the 2026-09-24 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live heads unchanged from the 2026-09-23
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
    remains the only open tracker context; open issues
    [#486](https://github.com/supabase/pg-toolbelt/issues/486) /
    [#487](https://github.com/supabase/pg-toolbelt/issues/487) are unrelated
    adjacent work
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

### Adjacent upstream movement that does not change benchmark status

- open pg-toolbelt issue
  [#487](https://github.com/supabase/pg-toolbelt/issues/487) reports a
  differently named enum-to-enum retype path that still emits
  `USING col::new_enum` instead of `USING col::text::new_enum`
  - that is adjacent to benchmark **005**, but it does **not** reopen the
    exact pgschema [#190](https://github.com/pgplex/pgschema/issues/190)
    `text -> enum` + default sequence already covered by
    `tests/integration/alter-table-operations.test.ts`
  - benchmark **005** therefore remains solved while the broader enum-cast
    family regains an adjacent open pg-toolbelt bug
- open pgschema PR [#622](https://github.com/pgplex/pgschema/pull/622) is a
  follow-up to covered issue [#601](https://github.com/pgplex/pgschema/issues/601)
  that broadens upstream function-recreate handling to non-view dependents
  - current pg-delta already has generic replacement expansion in
    `src/plan/phases/replacement-expansion.ts`, and the relevant dependent
    kinds (`default`, `constraint`, `index`, `policy`, `trigger`, `table`)
    remain marked `rebuildable` in the rule table
  - because this is an open follow-up PR rather than a new merged pgschema
    issue, and because it does not change the existing benchmark evidence,
    it stays watch-list context rather than becoming a new benchmark item
- open pg-toolbelt issue
  [#486](https://github.com/supabase/pg-toolbelt/issues/486) is a shadow
  non-superuser event-trigger loading failure and is adjacent tooling behavior
  rather than a pgschema parity benchmark

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-24

There is no new pgschema **issue** delta since the 2026-09-23 refresh:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-23'`
  returned `[]`

There is one new pgschema **PR** delta since the 2026-09-23 refresh:

- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-23'`
  returned open PR [#622](https://github.com/pgplex/pgschema/pull/622) only

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
- open PR [#622](https://github.com/pgplex/pgschema/pull/622) is follow-up
  context for already-covered issue [#601](https://github.com/pgplex/pgschema/issues/601)
- unrelated security-update PR
  [#605](https://github.com/pgplex/pgschema/pull/605) remains open
- there is currently **no open uncovered parity candidate** on the pgschema
  side

## 3) What changed in this refresh

- keep the checked-in/live `repos/pg-toolbelt` submodule pointer at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-24 latest-state snapshot
- add an explicit adjacent-follow-up note to benchmark
  [005](../benchmark/005-alter-column-type-using-clause.md) for open
  pg-toolbelt issue [#487](https://github.com/supabase/pg-toolbelt/issues/487)
- add this report as the 2026-09-24 latest-state sweep
- no new benchmark files and no new draft-only uncovered issue docs were
  needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-23'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-23'`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 200 --json number,title,updatedAt,url,labels`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 200 --json number,title,updatedAt,url,headRefName,baseRefName,isDraft`
  - `gh issue view 486 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 487 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 483 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 484 -R supabase/pg-toolbelt --json number,title,body,state,isDraft,updatedAt,url,baseRefName,headRefName`
  - `gh pr view 485 -R supabase/pg-toolbelt --json number,title,body,state,isDraft,updatedAt,url,baseRefName,headRefName`
  - `gh pr view 622 -R pgplex/pgschema --json number,title,body,state,isDraft,updatedAt,url,baseRefName,headRefName`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 120 --json number,title,state,updatedAt,url` (**returned `[]`**)
- repo Python validation:
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this refresh because the
  checked-in/live heads are unchanged from the 2026-09-23 refresh and the new
  upstream movement is adjacent issue / PR bookkeeping rather than merged code
