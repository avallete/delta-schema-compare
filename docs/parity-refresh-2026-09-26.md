# Parity refresh report - 2026-09-26

This report records the 2026-09-26 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live heads unchanged from the 2026-09-25
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
  - open PR [#488](https://github.com/supabase/pg-toolbelt/pull/488) remains
    test-only partitioned-parent corpus coverage, and new issue
    [#497](https://github.com/supabase/pg-toolbelt/issues/497) is only
    adjacent partition-key retype context rather than a fix for child-local
    partition overrides
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
  - open PR [#484](https://github.com/supabase/pg-toolbelt/pull/484) remains
    adjacent domain `NOT NULL` work only
  - open PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) still
    touches the same PG18 `contype = 'n'` catalog family, but its summary
    explicitly says the change is diagnostics-only and leaves the fact base,
    content hashes, and resulting plans unchanged
  - benchmark **024** therefore still has no exact current pg-toolbelt issue
    or PR; the only direct historical duplicate-search hit remains merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174), which landed on
    the pre-clean-room engine

### Adjacent upstream movement that does not change benchmark status

- new open pg-toolbelt issue
  [#497](https://github.com/supabase/pg-toolbelt/issues/497) reports
  partition-key column retypes failing with PostgreSQL's
  `cannot alter column ... because it is part of the partition key` error
  - partition-key / type-change searches on `pgplex/pgschema` only surfaced
    older closed partitioning issues
    [#496](https://github.com/pgplex/pgschema/issues/496) and
    [#606](https://github.com/pgplex/pgschema/issues/606) plus covered
    type-change issues [#537](https://github.com/pgplex/pgschema/issues/537)
    and [#190](https://github.com/pgplex/pgschema/issues/190)
  - this remains adjacent pg-toolbelt-side context rather than a benchmark
    duplicate
- updated open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) still reports
  event-trigger-driven RLS state being diffed away
  - this remains adjacent trigger / RLS context rather than a duplicate of
    benchmark **018**
- new open pg-toolbelt issue
  [#491](https://github.com/supabase/pg-toolbelt/issues/491) plus stacked
  open PR [#496](https://github.com/supabase/pg-toolbelt/pull/496) track
  same-role column grants being wiped by object-level `REVOKE ALL`
  - broad grant / privilege searches across `pgplex/pgschema` still do not
    surface an exact current parity tracker
  - this remains adjacent pg-toolbelt-side context rather than a new
    benchmark item
- open pg-toolbelt PR
  [#494](https://github.com/supabase/pg-toolbelt/pull/494) adds view /
  materialized-view column-grant extraction and references the earlier closed
  duplicate report [#359](https://github.com/supabase/pg-toolbelt/issues/359)
  - broad grant / privilege searches on `pgplex/pgschema` still do not
    surface an exact current parity tracker
  - this remains adjacent context rather than a new benchmark item
- open pg-toolbelt PR
  [#490](https://github.com/supabase/pg-toolbelt/pull/490) closes adjacent
  issue [#487](https://github.com/supabase/pg-toolbelt/issues/487) by routing
  differently named enum-to-enum retypes through `::text`
  - benchmark **005** remains solved on the exact pgschema
    [#190](https://github.com/pgplex/pgschema/issues/190) `text -> enum` +
    default path
- open pg-toolbelt PR
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) (owner capability
  diagnostics), open PR
  [#492](https://github.com/supabase/pg-toolbelt/pull/492)
  (concurrent catalog-drop extraction retries), and open PR
  [#495](https://github.com/supabase/pg-toolbelt/pull/495)
  (control-file-pinned extension schema export) are still pg-delta-side fixes
  without exact current pgschema parity trackers

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-26

There is no new pgschema issue or PR delta since the 2026-09-25 refresh:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-25'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-25'`
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
- refresh `benchmark/README.md` to the 2026-09-26 latest-state snapshot
- add an explicit refresh note to benchmark
  [005](../benchmark/005-alter-column-type-using-clause.md) for adjacent
  issue [#487](https://github.com/supabase/pg-toolbelt/issues/487) / PR
  [#490](https://github.com/supabase/pg-toolbelt/pull/490)
- add this report as the 2026-09-26 latest-state sweep
- no benchmark status changed, no new benchmark files were needed, and no
  `benchmark/review-memory.json` fingerprint updates were required

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-25'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-25'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-25'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-25'`
  - `gh issue view 497 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 491 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 451 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 490 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,files,commits,headRefName,baseRefName`
  - `gh pr view 492 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,files,commits,headRefName,baseRefName`
  - `gh pr view 493 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,files,commits,headRefName,baseRefName`
  - `gh pr view 494 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,files,commits,headRefName,baseRefName`
  - `gh pr view 495 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,files,commits,headRefName,baseRefName`
  - `gh pr view 496 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,files,commits,headRefName,baseRefName`
  - `gh issue list -R pgplex/pgschema --state all --search 'partition key'`
  - `gh issue list -R pgplex/pgschema --state all --search 'grant OR grants OR privilege OR privileges'`
  - `gh issue list -R pgplex/pgschema --state all --search 'enum alter column cast'`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url`
- repo Python validation:
  - `python3 -m pip install --user -r requirements.txt` when needed for
    missing dependencies
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
