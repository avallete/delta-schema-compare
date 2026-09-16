# Parity refresh report - 2026-09-16

This report records the 2026-09-16 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `11678c582923fc1a27ed2edf37f3503d1fc466a8`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `94de18e34e9758e36cd0c18f7ffadeb2291bb446`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`bb393ff61f5cd9ba95aee2824045f737afbe013b` (post-alpha.51 main) to
`94de18e34e9758e36cd0c18f7ffadeb2291bb446`
(`@supabase/pg-delta@1.0.0-alpha.52`) through merged release PR
[#479](https://github.com/supabase/pg-toolbelt/pull/479), while
checked-in/live `pgschema` remains at
`11678c582923fc1a27ed2edf37f3503d1fc466a8`.

The benchmark matrix itself remains unchanged versus
[`docs/parity-refresh-2026-09-15.md`](./parity-refresh-2026-09-15.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - today's pg-delta delta is release metadata only:
    `packages/pg-delta/CHANGELOG.md` and
    `packages/pg-delta/package.json`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - no source files in the generated-column extract / plan path changed in
    alpha.52
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - no source files in the PG18 nullability extract / plan path changed in
    alpha.52
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

The target repo still has no local tracker issues. Current pg-toolbelt open
issue/PR lists still show only umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) for benchmarks
**021** / **022**, while benchmark **024** still has no exact pg-toolbelt
issue or PR. Open pg-toolbelt issue
[#476](https://github.com/supabase/pg-toolbelt/issues/476) plus issue
[#477](https://github.com/supabase/pg-toolbelt/issues/477) / PR
[#478](https://github.com/supabase/pg-toolbelt/pull/478) are adjacent
cluster-global role / identity-sequence privilege work rather than duplicates
of the active benchmarks.

## 2) Open / resolved pgschema delta on 2026-09-16

There is no upstream issue or PR delta on the pgschema side since the
2026-09-15 refresh:

- no new open pgschema issues
- no newly closed pgschema issues
- no newly merged pgschema PRs

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#588](https://github.com/pgplex/pgschema/issues/588),
  [#594](https://github.com/pgplex/pgschema/issues/594),
  [#596](https://github.com/pgplex/pgschema/issues/596), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain
  **not parity work for pg-delta**
- open issues [#593](https://github.com/pgplex/pgschema/issues/593),
  [#598](https://github.com/pgplex/pgschema/issues/598),
  [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602), and
  [#603](https://github.com/pgplex/pgschema/issues/603) remain **covered** in
  current pg-delta
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### pg-toolbelt open work check

- open pg-toolbelt issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) still carries the
  only umbrella tracker context for benchmarks **021** / **022**
- benchmark **024** still has no exact pg-toolbelt issue or PR
- merged pg-toolbelt PR
  [#479](https://github.com/supabase/pg-toolbelt/pull/479) is the only new
  upstream pg-delta change and is release-only
- open pg-toolbelt issue
  [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus issue
  [#477](https://github.com/supabase/pg-toolbelt/issues/477) and open PR
  [#478](https://github.com/supabase/pg-toolbelt/pull/478) remain adjacent
  cluster-global role / identity-sequence privilege work, not exact matches
  for any current pgschema parity gap
- open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472), and
  [#473](https://github.com/supabase/pg-toolbelt/pull/473) remain unrelated to
  the active benchmark set

## 3) What changed in this refresh

- advance the checked-in `repos/pg-toolbelt` submodule pointer to
  `94de18e34e9758e36cd0c18f7ffadeb2291bb446`
- refresh `benchmark/README.md` and `benchmark/review-memory.json` to the
  2026-09-16 latest-state snapshot
- add fresh 2026-09-16 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- add this report as the 2026-09-16 latest-state sweep
- no new benchmark files or draft-only uncovered issue docs were added

## 4) Validation notes

This refresh was validated with:

- `git reset --hard origin/avallete/schema-comparison-benchmark-7d48`
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `git -C repos/pg-toolbelt log --oneline bb393ff61f5cd9ba95aee2824045f737afbe013b..HEAD`
- `git -C repos/pg-toolbelt diff --stat bb393ff61f5cd9ba95aee2824045f737afbe013b..HEAD -- packages/pg-delta`
- `git -C repos/pgschema log --oneline 11678c582923fc1a27ed2edf37f3503d1fc466a8..HEAD`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 50 --json number,title,updatedAt,url`
  - `gh issue list -R pgplex/pgschema --state closed --search 'closed:>=2026-09-15' --limit 50 --json number,title,updatedAt,url`
  - `gh pr list -R pgplex/pgschema --state merged --search 'merged:>=2026-09-15' --limit 50 --json number,title,mergedAt,url`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 80 --json number,title,updatedAt,url`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 80 --json number,title,updatedAt,url`
  - `gh pr list -R supabase/pg-toolbelt --state merged --search 'merged:>=2026-09-15' --limit 50 --json number,title,mergedAt,url`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 80 --json number,title,state,updatedAt,url`
- repo Python validation after installing `requirements.txt`:
  - `python3 -m pip install -r requirements.txt`
  - `DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
    (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
    (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were necessary in this environment because
  today's upstream delta is limited to release metadata rather than active
  extract / plan codepaths
