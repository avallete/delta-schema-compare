# Parity refresh report - 2026-08-31

This report records the 2026-08-31 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `97d8d60dd72a46704cc63b71b63aab2784847658`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `107ac3df4b889c527215d1f6a37df64b33154c16`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-30.md`](./parity-refresh-2026-08-30.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Current evidence on the current heads

- checked-in/live `pg-delta` remains
  `107ac3df4b889c527215d1f6a37df64b33154c16`
  (`@supabase/pg-delta@1.0.0-alpha.48`)
- checked-in/live `pgschema` advances to
  `97d8d60dd72a46704cc63b71b63aab2784847658`
  (`v1.12.5`) through merged PRs
  [#565](https://github.com/pgplex/pgschema/pull/565),
  [#566](https://github.com/pgplex/pgschema/pull/566),
  [#567](https://github.com/pgplex/pgschema/pull/567), and
  [#568](https://github.com/pgplex/pgschema/pull/568)
- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
    relation columns with `a.attislocal`, so child-local overrides on inherited
    partition columns never become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child-element
    list
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence as
    `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes `GENERATED ALWAYS AS (...) STORED`
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for both active benchmarks, and today's upstream delta is on the
  pgschema side rather than the pg-delta side
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#439`, `pgschema#444`, `pgschema#559`, `pgschema#564`,
  `pgschema#561`, `pgschema#569`, and `pgschema#571` returned no dedicated
  pg-toolbelt issue or PR
- keyword searches for `VIRTUAL generated` still only surface open umbrella
  issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
- keyword searches for `PARTITION OF` still surface umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus unrelated
  open issue [#451](https://github.com/supabase/pg-toolbelt/issues/451)
- keyword searches for `ADD COLUMN NOT NULL`, `ALTER COLUMN SET NOT NULL`, and
  `NOT NULL NOT VALID` surfaced only umbrella / backlog context
  ([#332](https://github.com/supabase/pg-toolbelt/issues/332) and closed
  [#333](https://github.com/supabase/pg-toolbelt/issues/333)), not an exact
  tracker for the new open pgschema #564 parity candidate

## 2) Upstream delta on 2026-08-31

- checked-in/live `pgschema` advances from
  `00db700e74b2b255e1e570495ae59fda6af38ed7` to
  `97d8d60dd72a46704cc63b71b63aab2784847658`
  (`v1.12.5`)
- the new pgschema code arrived through:
  - [#565](https://github.com/pgplex/pgschema/pull/565) - run
    `VALIDATE CONSTRAINT` in its own transaction for online rewrites
  - [#566](https://github.com/pgplex/pgschema/pull/566) - use native
    PostgreSQL 18 `NOT NULL ... NOT VALID` constraints on PG18+ targets
  - [#567](https://github.com/pgplex/pgschema/pull/567) - release to v1.12.5
  - [#568](https://github.com/pgplex/pgschema/pull/568) - bump embedded
    PostgreSQL 18 to 18.3.0
- open pgschema issue
  [#563](https://github.com/pgplex/pgschema/issues/563) closed on 2026-08-31
  after pgschema documented the manual data-migration / plan-edit workflow; it
  remains **not parity work for pg-delta**
- new current open pgschema watch-list items are now
  [#564](https://github.com/pgplex/pgschema/issues/564),
  [#569](https://github.com/pgplex/pgschema/issues/569), and
  [#571](https://github.com/pgplex/pgschema/issues/571)
- current open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) and open PRs
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  [#303](https://github.com/supabase/pg-toolbelt/pull/303), and
  [#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
  upstream context, but none is an exact duplicate of the active benchmarks,
  the older draft-only gaps, or the new open #564 parity candidate

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#559](https://github.com/pgplex/pgschema/issues/559) remain
  **not parity work for pg-delta**
- open issue [#564](https://github.com/pgplex/pgschema/issues/564) is the one
  **new open parity candidate** in this refresh: related pgschema PR
  [#566](https://github.com/pgplex/pgschema/pull/566) now plans PostgreSQL 18
  `ADD CONSTRAINT ... NOT NULL <col> NOT VALID` +
  `VALIDATE CONSTRAINT`, while current pg-delta still emits direct
  `ADD COLUMN ... NOT NULL` / `ALTER COLUMN ... SET NOT NULL` forms and has no
  exact tracker
- open issue [#569](https://github.com/pgplex/pgschema/issues/569) appears
  **covered** in current pg-delta's declarative `schema apply` flow; the
  shadow-loader path already splits and AST-reorders wrong-order SQL through
  `src/frontends/sql-order.ts` and retries bounded rounds in
  `src/frontends/load-sql-files.ts`
- open issue [#571](https://github.com/pgplex/pgschema/issues/571) appears
  **covered** in current pg-delta's dependency model; current pg-delta uses
  AST-based `@supabase/pg-topo` for shadow ordering and PostgreSQL's own
  `pg_depend` in `src/extract/dependencies.ts`, not a
  `functionCallRegex`-style text heuristic

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-08-31 latest-state snapshot
- refresh `benchmark/review-memory.json`:
  - move **#563** from `open` to `resolved`
  - refresh the open watch-list entries **#49**, **#52**, **#84**, **#450**,
    **#559**, **#564**, **#569**, and **#571**
  - refresh the rechecked resolved entries **#439**, **#444**, **#499**,
    **#501**, **#557**, **#561**, and **#563**
- refresh benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md) to the current upstream
  pgschema head
- add a new draft-only tracker body for the open #564 parity candidate in
  [`docs/parity-issue-drafts-2026-08-31.md`](./parity-issue-drafts-2026-08-31.md)
- add this report as the 2026-08-31 latest-state sweep
- advance checked-in/live `pgschema` to
  `97d8d60dd72a46704cc63b71b63aab2784847658`; checked-in/live `pg-delta`
  remains `107ac3df4b889c527215d1f6a37df64b33154c16`

## 4) Validation notes

This refresh was validated with:

- GitHub CLI state checks for current pgschema issues
  **#49**, **#52**, **#84**, **#439**, **#444**, **#450**, **#499**, **#501**,
  **#557**, **#559**, **#561**, **#563**, **#564**, **#569**, and **#571**
- GitHub CLI state checks for merged pgschema PRs
  **#565**, **#566**, **#567**, and **#568**
- GitHub CLI state checks for current pg-toolbelt issues / PRs and duplicate
  queries around the active benchmarks and new open watch-list items
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/sql-order.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/reorder-shadow.test.ts`
  - `repos/pg-toolbelt/packages/pg-topo/README.md`
  - `repos/pg-toolbelt/packages/pg-topo/test/object-ref-normalization.test.ts`
- `python3 -m pip install -r requirements.txt`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`

The dry-run script runs are still expected to return **0** parity items because
the manually tracked current open pgschema issues **#49**, **#52**, **#84**,
**#450**, **#559**, **#564**, **#569**, and **#571** do not carry the upstream
`Bug` / `Feature` labels that the automation currently filters on.

No fresh Docker-backed pg-delta runtime recheck was needed for benchmarks
**021** / **022** because the current head change is upstream-only on the
pgschema side, not the active pg-delta codepaths. The new #564 / #569 / #571
judgments therefore rest on current source-path inspection, current committed
tests around shadow loading / ordering, and live GitHub state checks.
