# Parity refresh report - 2026-09-28

This report records the 2026-09-28 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live heads unchanged from the 2026-09-27
snapshot:

- `pg-delta` remains at `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- `pgschema` remains at `580f4040d0f3c1bfad1497918200c9c1f638a020`

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain the only active unresolved
  gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
  - updated issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
    still covers partition-key column retypes only, so it remains adjacent
    context rather than a duplicate of the child-local override gap
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
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - benchmark **024** still has no exact current pg-toolbelt issue or PR; open
    PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) remains
    diagnostics-only and does not change extraction or planning

### One upstream movement since 2026-09-27

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
  returned `[]`
- `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
  returned updated issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
- `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
  returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`
- `git -C repos/pg-toolbelt rev-parse HEAD origin/main` returned the same SHA
  for both refs
- `git -C repos/pgschema rev-parse HEAD origin/main` returned the same SHA for
  both refs

The active benchmark set therefore remains **021**, **022**, and **024**.
Issue [#497](https://github.com/supabase/pg-toolbelt/issues/497) is still
useful adjacent context, but it does not change the benchmark mapping:
benchmarks **021** / **022** still only have umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) as exact tracker
context, benchmark **024** still has no exact current pg-toolbelt issue or PR,
and there is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-09-28

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

- keep the checked-in/live `repos/pg-toolbelt` submodule pointer at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-09-28 latest-state snapshot
- add this report as the 2026-09-28 latest-state sweep
- no benchmark file changed status, no new benchmark file was needed, no
  `benchmark/review-memory.json` fingerprint update was required, and no new
  tracker issue draft was needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct submodule head checks:
  - `git -C repos/pg-toolbelt rev-parse HEAD origin/main`
  - `git -C repos/pgschema rev-parse HEAD origin/main`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
  - `gh issue view 497 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh issue view 332 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,labels`
  - `gh pr view 488 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh pr view 485 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url,isDraft,baseRefName,headRefName`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200 --json number,title,state,updatedAt,url`
- repo Python validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
