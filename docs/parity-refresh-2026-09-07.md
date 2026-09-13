# Parity refresh report - 2026-09-07

This report records the 2026-09-07 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `fe7c64bfa410e7f9e8235eae3b912eb163b255f4`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-09-06.md`](./parity-refresh-2026-09-06.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**
- checked-in/live `pg-delta` remains
  `08219f1a8832f86e7287e50bab793a498129db7a`
  (`@supabase/pg-delta@1.0.0-alpha.49`)
- checked-in/live `pgschema` advances from
  `c6ed06f6fd5f1e36a00787b7034e35bda025e86b` to
  `fe7c64bfa410e7f9e8235eae3b912eb163b255f4` through merged PR
  [#581](https://github.com/pgplex/pgschema/pull/581)
- no pg-toolbelt code, issue, or PR delta landed since 2026-09-06:
  - `git submodule update --remote --merge` left `repos/pg-toolbelt`
    unchanged at `08219f1a8832f86e7287e50bab793a498129db7a`
  - `gh issue list` / `gh pr list` updated-since queries returned empty arrays
    for `supabase/pg-toolbelt`

### Current evidence on the current heads

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
- direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, `pgschema#579`, and `pgschema#580` returned no dedicated
  pg-toolbelt issue or PR

## 2) Open / resolved pgschema delta on 2026-09-07

Today's upstream delta is entirely on the pgschema side:

- issues [#579](https://github.com/pgplex/pgschema/issues/579) and
  [#580](https://github.com/pgplex/pgschema/issues/580) closed on 2026-09-07
- merged PR [#581](https://github.com/pgplex/pgschema/pull/581) advanced
  `pgschema/main`
- open PR [#582](https://github.com/pgplex/pgschema/pull/582) remains a
  follow-up for the broader #580 family
- the open pgschema watch list is otherwise unchanged:
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#564](https://github.com/pgplex/pgschema/issues/564)

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#559](https://github.com/pgplex/pgschema/issues/559) remain
  **not parity work for pg-delta**
- open issue [#564](https://github.com/pgplex/pgschema/issues/564) remains the
  one **open not-covered parity candidate** from the current watch list; the
  existing draft-only tracker body remains in
  [`docs/parity-issue-drafts-2026-08-31.md`](./parity-issue-drafts-2026-08-31.md)

### Newly closed pgschema issues

- resolved issue [#579](https://github.com/pgplex/pgschema/issues/579) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts` maps
    relation row types through `pg_type.typrelid` back to the owning
    table/view facts
  - `repos/pg-toolbelt/packages/pg-delta/corpus/table-fn-dep--setof-function/`
    exercises `RETURNS SETOF test_schema.users`
  - `repos/pg-toolbelt/packages/pg-delta/tests/composite-order-roundtrip.test.ts`
    keeps a `RETURNS SETOF` export/load chain round-trippable
- resolved issue [#580](https://github.com/pgplex/pgschema/issues/580) also
  remains **covered** in current pg-delta's supported export/load path:
  - `exportSqlFiles()` preserves plan order across files in the default
    `by-object` layout
  - `layout: "ordered"` prefixes filenames in dependency order for single-pass
    reloads
  - `tests/export.test.ts` and
    `repos/pg-toolbelt/packages/pg-delta/tests/export-fidelity.test.ts`
    gate `load(export(fb)) ≡ fb`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts` proves
    out-of-order files still converge through dependency-aware retry rounds
  - no dedicated exact pg-toolbelt issue or PR was found
- open pgschema PR [#582](https://github.com/pgplex/pgschema/pull/582)
  remains adjacent upstream context only for now. Because it is not merged into
  `pgschema/main` yet and has no dedicated companion pgschema issue, it does
  not change today's benchmark matrix or require a new benchmark file.

There is still **no dedicated exact open pg-toolbelt parity tracker** for the
active benchmarks **021** / **022**, the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444), or the one open
not-covered parity candidate [#564](https://github.com/pgplex/pgschema/issues/564).
Current open pg-toolbelt issue
[#451](https://github.com/supabase/pg-toolbelt/issues/451) and open PRs
[#432](https://github.com/supabase/pg-toolbelt/pull/432),
[#303](https://github.com/supabase/pg-toolbelt/pull/303), and
[#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
adjacent context, but none is an exact duplicate of the active benchmarks or
the open #564 watch-list item. The target repository
`avallete/delta-schema-compare` still has no existing issues, so there were no
repo-local tracker issues to update.

## 3) What changed in this refresh

- advance the checked-in `pgschema` submodule pointer to
  `fe7c64bfa410e7f9e8235eae3b912eb163b255f4`
- refresh `benchmark/README.md` to the 2026-09-07 latest-state snapshot
- refresh `benchmark/review-memory.json` review timestamps/fingerprints for the
  current open watch-list items, active benchmark issues **#499** / **#501**,
  and the newly closed issues **#579** / **#580**
- add a fresh 2026-09-07 refresh note to benchmark files
  [021](../benchmark/021-partition-child-column-overrides.md) and
  [022](../benchmark/022-virtual-generated-columns.md)
- add this report as the 2026-09-07 latest-state sweep
- no benchmark row status changed, no new benchmark file was added, and no new
  draft-only tracker markdown was needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-since queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-06 sort:updated-desc'`
  - `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-06 sort:updated-desc'`
  - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-06 sort:updated-desc'`
  - `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-06 sort:updated-desc'`
- GitHub CLI state checks for current open pgschema issues
  **#49**, **#52**, **#84**, **#450**, **#559**, and **#564**
- GitHub CLI state checks for resolved pgschema issues
  **#499**, **#501**, **#579**, and **#580**
- GitHub CLI state checks for current pg-toolbelt issue / PR context:
  **#332**, **#451**, **#432**, **#303**, and **#288**
- GitHub CLI exact duplicate queries around the active benchmarks, the current
  watch-list items, and today's newly closed pgschema issues, plus
  `gh issue list -R avallete/delta-schema-compare`, which is still empty
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-fidelity.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/composite-order-roundtrip.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/corpus/table-fn-dep--setof-function/`

The dry-run compare scripts still need to be executed on top of this refreshed
snapshot because the parity-relevant pgschema watch-list issues remain
unlabeled and manual review is still required even when the labeled sweeps
return zero items.
