# Parity refresh report - 2026-09-10

This report records the 2026-09-10 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`)

## 1) Benchmark status refresh

This refresh keeps the benchmark matrix unchanged versus
[`docs/parity-refresh-2026-09-09.md`](./parity-refresh-2026-09-09.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps
- checked-in `pg-delta` remains `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`)
- live `pg-delta/main` remains `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`; no new merged pg-toolbelt
  delta landed since the 2026-09-09 refresh, but open PRs
  [#470](https://github.com/supabase/pg-toolbelt/pull/470),
  [#471](https://github.com/supabase/pg-toolbelt/pull/471), and
  [#472](https://github.com/supabase/pg-toolbelt/pull/472) appeared
- checked-in/live `pgschema` remains `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`; no new merged pgschema
  delta landed since the 2026-09-09 refresh, but open issue
  [#591](https://github.com/pgplex/pgschema/issues/591), open PR
  [#592](https://github.com/pgplex/pgschema/pull/592), and open issue
  [#593](https://github.com/pgplex/pgschema/issues/593) appeared

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - current pg-delta still keeps `COLUMNS_SQL` gated by `a.attislocal` in
    `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`, so
    child-local overrides on inherited partition columns never surface as
    diff-visible facts
  - open pg-toolbelt PR [#470](https://github.com/supabase/pg-toolbelt/pull/470)
    changes attached partition-index extraction and `PARTITION OF` ordering,
    but its `tables.ts` branch still emits bare
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column-
    element list for local `DEFAULT` / `NOT NULL` overrides
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - current pg-delta already covers generated-expression changes on existing
    columns through `packages/pg-delta/corpus/alter-table--generated-column`
    and the `generatedExpr: "replace"` attribute path in
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`, so new
    pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591) is
    not a new pg-delta parity gap
  - the active benchmark **022** gap remains the missing `VIRTUAL` versus
    `STORED` generated-column kind: `relations.ts` still collapses
    `attgenerated` to generated-expression presence, and
    `helpers.ts` still hard-codes `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, `pgschema#591`, and `pgschema#593` still return no dedicated
  pg-toolbelt issue or PR
- the target repo still has no existing tracker issues

## 2) Open / resolved pgschema delta on 2026-09-10

Today's upstream delta is on the open-issue side only:

- pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591) opened
  on 2026-09-09, and open PR
  [#592](https://github.com/pgplex/pgschema/pull/592) implements the upstream
  fix
- pgschema issue [#593](https://github.com/pgplex/pgschema/issues/593) opened
  on 2026-09-09
- pgschema issue [#588](https://github.com/pgplex/pgschema/issues/588)
  received another update on 2026-09-09
- no new pgschema issue closures or merged pg-toolbelt PRs landed after the
  2026-09-09 refresh

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84), and
  [#588](https://github.com/pgplex/pgschema/issues/588) remain
  **not parity work for pg-delta**
- open issue [#591](https://github.com/pgplex/pgschema/issues/591) appears
  **covered** in current pg-delta:
  - `packages/pg-delta/corpus/alter-table--generated-column` already covers an
    existing generated-expression change (`a + b` -> `a * b`) and a new
    generated-column add
  - `generatedExpr` is a diff-visible attribute with `"replace"` semantics in
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`, so the
    change is not invisible even though pg-delta uses drop/add rather than
    pgschema's version-gated `SET EXPRESSION AS`
  - no dedicated exact pg-toolbelt issue or PR exists; only umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) is adjacent
- open issue [#593](https://github.com/pgplex/pgschema/issues/593) appears
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    explicit non-default column collations from `a.attcollation`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` replays
    that state as `COLLATE ...` in `columnClause()`
  - no dedicated exact pg-toolbelt issue or PR exists
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### pg-toolbelt open work check

- open PR [#470](https://github.com/supabase/pg-toolbelt/pull/470) is adjacent
  but not exact: it improves partition replacement/index attach handling, yet
  leaves benchmark **021**'s child-local column override path unresolved
- open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#472](https://github.com/supabase/pg-toolbelt/pull/472) are not related to
  the active benchmarks or the new pgschema issues

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-09-10 latest-state snapshot,
  folding in open issues **#591** / **#593** and pg-toolbelt PR **#470**'s
  adjacent-but-non-fixing state
- refresh `benchmark/review-memory.json` review timestamps and open-issue
  fingerprints, add open issues **#591** and **#593**, and update issue
  **#588**'s latest fingerprint
- add fresh 2026-09-10 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- add this report as the 2026-09-10 latest-state sweep
- leave the checked-in `pg-delta` pointer at `08219f1a8832f86e7287e50bab793a498129db7a` while
  recording a live-head recheck against `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, because there is still
  no merged pg-delta delta that changes the active parity conclusions

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-since queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-09 sort:updated-desc'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-09 sort:updated-desc'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-09 sort:updated-desc'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-09 sort:updated-desc'`
- GitHub CLI state checks for the current open pgschema watch-list items
  **#49**, **#52**, **#84**, **#588**, **#591**, and **#593**
- GitHub CLI PR context checks for pgschema PR **#592** and pg-toolbelt PRs
  **#470**, **#471**, and **#472**
- GitHub CLI exact duplicate searches around benchmarks **021** / **022** /
  **024**, the new open issues **#591** / **#593**, and
  `gh issue list -R avallete/delta-schema-compare`, which is still empty
- dry-run compare scripts:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - both still return **0** labeled parity items, so manual unlabeled sweeps
    remain required
- repo Python regression tests:
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - **9 tests passed**
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/corpus/alter-table--generated-column/`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `git diff --check`
