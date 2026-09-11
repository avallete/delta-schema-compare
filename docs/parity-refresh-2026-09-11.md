# Parity refresh report - 2026-09-11

This report records the 2026-09-11 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `85e8946a79b0a5b149fe9a772fef882c14cb9567`)

## 1) Benchmark status refresh

This refresh keeps the benchmark matrix unchanged versus
[`docs/parity-refresh-2026-09-10.md`](./parity-refresh-2026-09-10.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps
- checked-in/live `pg-delta` advances from
  `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`) to
  `85e8946a79b0a5b149fe9a772fef882c14cb9567`
  (`@supabase/pg-delta@1.0.0-alpha.50`)
- checked-in/live `pgschema` advances from
  `738a3bb40cf6b062928eeb564e3a98ec7f3c6989` to
  `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    `COLUMNS_SQL` gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list for local `DEFAULT` / `NOT NULL` overrides
  - open pg-toolbelt PR
    [#470](https://github.com/supabase/pg-toolbelt/pull/470) remains adjacent
    only; it improves partition replacement/index-attach handling but does not
    add the missing child override model
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - current pg-delta already covered pgschema issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-
    expression change family before upstream merged its fix, via
    `packages/pg-delta/corpus/alter-table--generated-column` and
    `generatedExpr: "replace"` in
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - the active benchmark **022** gap remains the missing `VIRTUAL` versus
    `STORED` kind: `relations.ts` still collapses `attgenerated` to expression
    presence and `helpers.ts` still hard-codes
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
- `git -C repos/pg-toolbelt diff --stat
  08219f1a8832f86e7287e50bab793a498129db7a..85e8946a79b0a5b149fe9a772fef882c14cb9567
  -- packages/pg-delta/src/extract/relations.ts
  packages/pg-delta/src/plan/rules/helpers.ts
  packages/pg-delta/src/plan/rules/tables.ts
  packages/pg-delta/corpus/alter-table--generated-column`
  returns no output, so the active gap paths are unchanged across the
  alpha.49 -> alpha.50 bump
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, and `pgschema#593` still return no dedicated pg-toolbelt
  issue or PR
- the target repo still has no existing tracker issues

## 2) Open / resolved pgschema delta on 2026-09-11

Today's upstream delta is the pgschema side only:

- pgschema PR
  [#592](https://github.com/pgplex/pgschema/pull/592) merged on 2026-09-10
  and closed issue [#591](https://github.com/pgplex/pgschema/issues/591)
- there are no new pg-toolbelt issues, and the new pg-toolbelt activity since
  the last refresh is open PR
  [#473](https://github.com/supabase/pg-toolbelt/pull/473), which is unrelated
  to the active benchmarks

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84), and
  [#588](https://github.com/pgplex/pgschema/issues/588) remain
  **not parity work for pg-delta**
- open issue [#593](https://github.com/pgplex/pgschema/issues/593) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    explicit non-default column collations from `a.attcollation`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` replays
    that state as `COLLATE ...` in `columnClause()`
- resolved issue [#591](https://github.com/pgplex/pgschema/issues/591) also
  remains **covered** in current pg-delta:
  - `packages/pg-delta/corpus/alter-table--generated-column` already exercises
    a generated-expression change on an existing column
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still diffs
    `generatedExpr` with `"replace"` semantics
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### pg-toolbelt open work check

- open PR [#470](https://github.com/supabase/pg-toolbelt/pull/470) is still
  adjacent but not exact: it improves partition replacement/index attach
  handling, yet leaves benchmark **021**'s child-local column override path
  unresolved
- open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472), and
  [#473](https://github.com/supabase/pg-toolbelt/pull/473) are not related to
  benchmarks **021**, **022**, or **024**
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  still carries the only adjacent tracker context for benchmarks **021** /
  **022**; benchmark **024** still has no exact pg-toolbelt issue or PR

## 3) What changed in this refresh

- bump checked-in submodules to the latest upstream heads for `repos/pgschema`
  and `repos/pg-toolbelt`
- refresh `benchmark/README.md` to the 2026-09-11 latest-state snapshot
- refresh `benchmark/review-memory.json` review fingerprints/timestamps for the
  live watch-list items and active benchmarked issues, and move issue **#591**
  from `open` to `resolved`
- add fresh 2026-09-11 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- add this report as the 2026-09-11 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-since queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-10 sort:updated-desc'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-10 sort:updated-desc'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-10 sort:updated-desc'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-10 sort:updated-desc'`
- GitHub CLI state checks for current open watch-list items **#49**, **#52**,
  **#84**, **#588**, and **#593**
- GitHub CLI PR context checks for pgschema PR **#592** and pg-toolbelt PRs
  **#470** and **#473**
- GitHub CLI exact duplicate searches around benchmarks **021** / **022** /
  **024**, issue **#593**, and `gh issue list -R avallete/delta-schema-compare`
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/corpus/alter-table--generated-column/`
  - `repos/pgschema/internal/diff/column.go`
  - `repos/pgschema/internal/diff/generated_column_test.go`
- repo Python validation after installing `requirements.txt`:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- Bun-backed pg-delta runtime probes were not re-run in this environment
  because Bun is not currently installed in the pod; the active gap paths were
  instead revalidated by source inspection plus the no-diff check across the
  alpha.49 -> alpha.50 bump
