# Parity refresh report - 2026-09-25

This report records the 2026-09-25 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live heads unchanged from the 2026-09-24
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
    remains the only exact tracker context
  - open PR [#488](https://github.com/supabase/pg-toolbelt/pull/488) is only
    adjacent test coverage for a partitioned-parent corpus and does not change
    extraction or planning
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
  - PR [#484](https://github.com/supabase/pg-toolbelt/pull/484) remains
    adjacent domain `NOT NULL` work only
  - PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) still touches
    the same PG18 `contype = 'n'` catalog family, but its summary explicitly
    says the change is diagnostics-only and leaves the fact base, content
    hashes, and resulting plans unchanged
  - benchmark **024** therefore still has no exact current pg-toolbelt issue
    or PR; the only direct historical duplicate-search hit remains merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which landed on
    the pre-clean-room engine

### Adjacent upstream movement that does not change benchmark status

- open pg-toolbelt issue
  [#489](https://github.com/supabase/pg-toolbelt/issues/489) reports missing
  column grants on views in declarative schema output
  - broad privilege / grant keyword searches across `pgplex/pgschema` issues
    did not surface an exact matching parity tracker
  - this remains adjacent pg-toolbelt-side context rather than a new
    benchmark duplicate
- open pg-toolbelt PR
  [#488](https://github.com/supabase/pg-toolbelt/pull/488) adds a test-only
  corpus scenario for heap-to-partitioned replacement with `ON ONLY` parent
  indexes, cross-schema partitions, and
  `publish_via_partition_root = true`
  - the PR body explicitly says it is test-only and ships no production code
  - this is adjacent context for benchmark **021**, not a fix for the active
    child-local override gap
- open pg-toolbelt issue
  [#487](https://github.com/supabase/pg-toolbelt/issues/487) still reports the
  differently named enum-to-enum retype path that emits
  `USING col::new_enum` instead of `USING col::text::new_enum`
  - that remains adjacent to benchmark **005**, but does **not** reopen the
    exact pgschema [#190](https://github.com/pgplex/pgschema/issues/190)
    `text -> enum` + default sequence already covered by current pg-delta
- open pgschema PR [#622](https://github.com/pgplex/pgschema/pull/622) is a
  follow-up to covered issue [#601](https://github.com/pgplex/pgschema/issues/601)
  that broadens upstream function-recreate handling to non-view dependents
  - current pg-delta already has generic replacement expansion in
    `src/plan/phases/replacement-expansion.ts`, and the relevant dependent
    kinds remain rebuildable
  - because this is still follow-up PR context rather than a new merged
    pgschema issue, it stays watch-list context rather than becoming a new
    benchmark item
- closed pgschema PR [#605](https://github.com/pgplex/pgschema/pull/605) is
  the unrelated security-update bump and does not affect parity

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-25

There is no new pgschema **issue** delta since the 2026-09-24 refresh:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
  returned `[]`

There is PR delta since the 2026-09-24 refresh:

- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
  returned open PR [#622](https://github.com/pgplex/pgschema/pull/622) and
  closed PR [#605](https://github.com/pgplex/pgschema/pull/605)

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
- open PR [#622](https://github.com/pgplex/pgschema/pull/622) remains
  follow-up context for already-covered issue
  [#601](https://github.com/pgplex/pgschema/issues/601)
- there is currently **no open uncovered parity candidate** on the pgschema
  side

## 3) What changed in this refresh

- keep the checked-in/live `repos/pg-toolbelt` submodule pointer at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-25 latest-state snapshot
- add an explicit refresh note to benchmark
  [021](../benchmark/021-partition-child-column-overrides.md) for open
  pg-toolbelt PR [#488](https://github.com/supabase/pg-toolbelt/pull/488)
- add this report as the 2026-09-25 latest-state sweep
- no benchmark status changed, no new benchmark files were needed, no new
  draft-only uncovered issue docs were needed, and no
  `benchmark/review-memory.json` fingerprint updates were required

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
  - `gh issue view 489 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 488 -R supabase/pg-toolbelt --json number,title,body,state,isDraft,updatedAt,url,files,commits,headRefName,baseRefName`
  - `gh issue list -R pgplex/pgschema --state all --search 'grant OR grants OR privilege OR privileges'`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url` (**returned `[]`**)
- repo Python validation:
  - `python3 -m pip install --user -r requirements.txt` (required in this pod because `openai` was missing)
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this refresh because the
  checked-in/live heads are unchanged from the 2026-09-24 refresh and the new
  upstream movement is adjacent issue / PR bookkeeping plus test-only corpus
  work rather than merged code on `main`
