# Parity refresh report - 2026-09-15

This report records the 2026-09-15 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `11678c582923fc1a27ed2edf37f3503d1fc466a8`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `bb393ff61f5cd9ba95aee2824045f737afbe013b`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`9fac5a973a0fddac0618314164331633606b5126`
(`@supabase/pg-delta@1.0.0-alpha.51`) to post-alpha.51 main
`bb393ff61f5cd9ba95aee2824045f737afbe013b` through merged PR
[#475](https://github.com/supabase/pg-toolbelt/pull/475), and advances
checked-in/live `pgschema` from `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`
to `11678c582923fc1a27ed2edf37f3503d1fc466a8` through merged PR
[#604](https://github.com/pgplex/pgschema/pull/604).

The benchmark matrix itself remains unchanged versus
[`docs/parity-refresh-2026-09-14.md`](./parity-refresh-2026-09-14.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - the pg-delta delta between the two heads only touches assumed default
    grants, export/policy paths, and tests; `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
    still keeps relation columns gated by `a.attislocal`, so child-local
    overrides on inherited partition columns never surface as diff-visible
    facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
  - pgschema PR [#604](https://github.com/pgplex/pgschema/pull/604) closes
    [#595](https://github.com/pgplex/pgschema/issues/595) and adds adjacent
    application-partition coverage when the parent is extension-owned, which
    reinforces that pgschema currently covers a broader slice of the same
    column-override family than pg-delta does
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - PR [#475](https://github.com/supabase/pg-toolbelt/pull/475) and pgschema
    PR [#604](https://github.com/pgplex/pgschema/pull/604) are unrelated to
    generated-kind preservation
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - PR [#475](https://github.com/supabase/pg-toolbelt/pull/475) and pgschema
    PR [#604](https://github.com/pgplex/pgschema/pull/604) are unrelated to
    this PG18 native not-null workflow gap

The target repo still has no local tracker issues. Current pg-toolbelt open
issue/PR lists still show only umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) for benchmarks
**021** / **022**, while benchmark **024** still has no exact pg-toolbelt
issue or PR. New pg-toolbelt issue
[#477](https://github.com/supabase/pg-toolbelt/issues/477) and open PR
[#478](https://github.com/supabase/pg-toolbelt/pull/478) are identity-sequence
privilege follow-ups rather than duplicates of the active benchmarks.

## 2) Open / resolved pgschema delta on 2026-09-15

The new upstream delta since the 2026-09-14 refresh is on the merged/closed
side:

- no new open pgschema issues
- closed issue [#595](https://github.com/pgplex/pgschema/issues/595)
- merged PR [#604](https://github.com/pgplex/pgschema/pull/604)

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#588](https://github.com/pgplex/pgschema/issues/588),
  [#594](https://github.com/pgplex/pgschema/issues/594),
  [#596](https://github.com/pgplex/pgschema/issues/596), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain
  **not parity work for pg-delta**
- open issue [#593](https://github.com/pgplex/pgschema/issues/593) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    explicit non-default column collations from `a.attcollation`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` replays
    that state as `COLLATE ...`
- open issues [#598](https://github.com/pgplex/pgschema/issues/598),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#602](https://github.com/pgplex/pgschema/issues/602), and
  [#603](https://github.com/pgplex/pgschema/issues/603) remain **covered** in
  current pg-delta, while [#599](https://github.com/pgplex/pgschema/issues/599)
  and [#601](https://github.com/pgplex/pgschema/issues/601) remain
  **source-level covered** by the current trigger/routine/view rules
- closed issue [#595](https://github.com/pgplex/pgschema/issues/595) now sits
  on the historical side and remains **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` and
    `repos/pg-toolbelt/packages/pg-delta/src/extract/routines.ts` tag
    extension-owned relations and routines with `memberOfExtension`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/view.ts` keeps extension
    members reference-only in the managed view
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
    and `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
    avoid recreating extension members directly and rely on
    `CREATE EXTENSION` to materialize them
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### pg-toolbelt open work check

- open pg-toolbelt issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) still carries the
  only umbrella tracker context for benchmarks **021** / **022**
- benchmark **024** still has no exact pg-toolbelt issue or PR
- merged pg-toolbelt PR [#475](https://github.com/supabase/pg-toolbelt/pull/475)
  is now the checked-in/live head delta and remains unrelated to benchmarks
  **021**, **022**, and **024**
- open pg-toolbelt issue
  [#477](https://github.com/supabase/pg-toolbelt/issues/477) and open PR
  [#478](https://github.com/supabase/pg-toolbelt/pull/478) are adjacent
  identity-sequence privilege work, not exact matches for any current
  pgschema parity gap
- open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472),
  [#473](https://github.com/supabase/pg-toolbelt/pull/473), and
  [#479](https://github.com/supabase/pg-toolbelt/pull/479) remain unrelated to
  the active benchmark set

## 3) What changed in this refresh

- advance the checked-in `repos/pg-toolbelt` submodule pointer to
  `bb393ff61f5cd9ba95aee2824045f737afbe013b`
- advance the checked-in `repos/pgschema` submodule pointer to
  `11678c582923fc1a27ed2edf37f3503d1fc466a8`
- refresh `benchmark/README.md` and `benchmark/review-memory.json` to the
  2026-09-15 latest-state snapshot
- add fresh 2026-09-15 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- add this report as the 2026-09-15 latest-state sweep
- no new benchmark files or draft-only uncovered issue docs were added

## 4) Validation notes

This refresh was validated with:

- `git reset --hard origin/avallete/schema-comparison-benchmark-3262`
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `git -C repos/pgschema log --oneline 319b88c83d62b2c9a62eff7a09ec6563954bcf4b..HEAD`
- `git -C repos/pg-toolbelt log --oneline 9fac5a973a0fddac0618314164331633606b5126..HEAD`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 40 --json number,title,updatedAt,url`
  - `gh issue list -R pgplex/pgschema --state closed --search 'closed:>=2026-09-14' --limit 40 --json number,title,updatedAt,url`
  - `gh pr list -R pgplex/pgschema --state merged --search 'merged:>=2026-09-14' --limit 40 --json number,title,mergedAt,url`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 60 --json number,title,updatedAt,url`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 60 --json number,title,updatedAt,url`
- GitHub CLI issue / PR context checks for:
  - pgschema issue **#595** and PR **#604**
  - pg-toolbelt issue **#332**
  - pg-toolbelt PR **#475**
  - pg-toolbelt issues **#476** / **#477**
  - pg-toolbelt PR **#478**
  - target-repo issue list (`gh issue list -R avallete/delta-schema-compare --state all`)
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/routines.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/roles.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/view.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/indexes.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/triggers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/routines.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/index-invalid-repair.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/owner-edge.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/default-privileges-owner-self-revoke.test.ts`
- direct codepath diff checks:
  - `git -C repos/pg-toolbelt diff --stat 9fac5a973a0fddac0618314164331633606b5126..bb393ff61f5cd9ba95aee2824045f737afbe013b -- packages/pg-delta/src/extract/relations.ts packages/pg-delta/src/plan/rules/helpers.ts packages/pg-delta/src/plan/rules/tables.ts packages/pg-delta/src/plan/rules/constraints.ts packages/pg-delta/tests`
  - `git -C repos/pgschema diff --stat 319b88c83d62b2c9a62eff7a09ec6563954bcf4b..11678c582923fc1a27ed2edf37f3503d1fc466a8 -- internal/diff/table.go cmd/dump/extension_integration_test.go ir/queries/extension_members_test.go ir/queries/queries.sql cmd/plan/plan.go`
- repo Python validation after installing `requirements.txt`:
  - `python3 -m pip install -r requirements.txt`
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- Bun-backed pg-delta runtime probes were not re-run in this environment
  because Bun is not installed in the pod and Docker is unavailable; source
  inspection and checked-in tests were used instead
