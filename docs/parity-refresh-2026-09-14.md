# Parity refresh report - 2026-09-14

This report records the 2026-09-14 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `9fac5a973a0fddac0618314164331633606b5126`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) to
`9fac5a973a0fddac0618314164331633606b5126`
(`@supabase/pg-delta@1.0.0-alpha.51`) through merged PR
[#470](https://github.com/supabase/pg-toolbelt/pull/470) and release
[#474](https://github.com/supabase/pg-toolbelt/pull/474), while keeping
`pgschema` unchanged at `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`.

The benchmark matrix itself remains unchanged versus
[`docs/parity-refresh-2026-09-13.md`](./parity-refresh-2026-09-13.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

The current pg-delta head changed, but the new alpha.51 work is still adjacent
rather than gap-closing for the benchmark set:

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list for local `DEFAULT` / `NOT NULL` overrides
  - merged pg-toolbelt PR
    [#470](https://github.com/supabase/pg-toolbelt/pull/470) adds replace-path
    dependent rebuild, publication-membership restoration, and attached
    partition-index convergence, but it still does not add the missing
    child-override model
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - current pg-delta already covered issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-
    expression-change family before upstream merged its fix, via
    `packages/pg-delta/corpus/alter-table--generated-column` and
    `generatedExpr: "replace"` in
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - the active benchmark **022** gap remains the missing `VIRTUAL` versus
    `STORED` kind: `relations.ts` still collapses `attgenerated` to generated
    expression presence, and `helpers.ts` still hard-codes
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

Direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
`pgschema#564`, `pgschema#593`, `pgschema#594`, and `pgschema#595` still
return no dedicated pg-toolbelt issue or PR, and the target repo still has no
existing tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-14

The new upstream delta since the 2026-09-13 refresh is on the pgschema open-
issue side:

- new open issues
  [#596](https://github.com/pgplex/pgschema/issues/596) through
  [#603](https://github.com/pgplex/pgschema/issues/603)
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
- open issue [#593](https://github.com/pgplex/pgschema/issues/593) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    explicit non-default column collations from `a.attcollation`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` replays
    that state as `COLLATE ...` in `columnClause()`
- open issue [#595](https://github.com/pgplex/pgschema/issues/595) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` and
    `repos/pg-toolbelt/packages/pg-delta/src/extract/routines.ts` tag
    extension-owned relations and routines with `memberOfExtension`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/view.ts` keeps extension
    members reference-only in the managed view, and the export/load frontends
    already avoid recreating them directly
- new open issue [#598](https://github.com/pgplex/pgschema/issues/598) is
  already **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` captures
    regular-index `indisvalid` as semantic `valid`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/indexes.ts` diffs
    `valid` with the `"replace"` strategy
  - `repos/pg-toolbelt/packages/pg-delta/tests/index-invalid-repair.test.ts`
    covers the invalid-index repair path directly
- new open issue [#599](https://github.com/pgplex/pgschema/issues/599) is
  **source-level covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` captures
    `pg_trigger.tgenabled` as `enabled`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` maps the
    `O` / `D` / `R` / `A` trigger states to the corresponding `ALTER TABLE`
    phrases
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/triggers.ts` emits the
    corresponding `ENABLE REPLICA` / `ENABLE ALWAYS` trigger alters
- new open issue [#600](https://github.com/pgplex/pgschema/issues/600) is
  already **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/types.ts` marks
    `ALTER TYPE ... ADD VALUE` with
    `transactionality: "commitBoundaryAfter"`
  - `repos/pg-toolbelt/packages/pg-delta/src/apply/commit-boundary.test.ts`
    plus the `type-ops--enum-add-value-used-in-*` corpus pin the required
    commit boundary and the 55P04-safe apply path
- new open issue [#601](https://github.com/pgplex/pgschema/issues/601) is
  **source-level covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
    attributes a view's `_RETURN` dependencies to the view fact itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/routines.ts` treats
    `returnType` as `"replace"` and marks routines `rebuildable`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/views.ts` marks views
    `rebuildable`, so a dependent view is rebuilt around a demolished function
- new open issue [#602](https://github.com/pgplex/pgschema/issues/602) is
  already **covered** in current pg-delta:
  - ownership is modeled as owner edges and emitted as `ALTER ... OWNER TO`
  - `repos/pg-toolbelt/packages/pg-delta/tests/owner-edge.test.ts` covers
    owner roundtrip and owner-change flows
  - `ownerAlterPrefix` is implemented across tables, views, sequences, and
    routines
- new open issue [#603](https://github.com/pgplex/pgschema/issues/603) is
  already **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/roles.ts` keeps
    `defaclnamespace = 0` rows as global default-privilege facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` omits
    `IN SCHEMA` when a default-privilege fact has `schema: null`
  - `repos/pg-toolbelt/packages/pg-delta/tests/default-privileges-owner-self-revoke.test.ts`
    and `src/plan/rules/default-privilege.test.ts` cover the global
    extract/render path
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### pg-toolbelt open work check

- open pg-toolbelt issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) still carries the
  only umbrella tracker context for benchmarks **021** / **022**
- benchmark **024** still has no exact pg-toolbelt issue or PR
- nearby pg-toolbelt PRs are now merged
  [#470](https://github.com/supabase/pg-toolbelt/pull/470) plus open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472),
  [#473](https://github.com/supabase/pg-toolbelt/pull/473), and
  [#475](https://github.com/supabase/pg-toolbelt/pull/475)
- only merged PR **#470** is adjacent to the benchmark set, and it still does
  not close benchmark **021**'s child-local column-override gap
- PRs **#471**, **#472**, **#473**, and **#475** remain unrelated to
  benchmarks **021**, **022**, and **024**

## 3) What changed in this refresh

- advance the checked-in `repos/pg-toolbelt` submodule pointer to
  `9fac5a973a0fddac0618314164331633606b5126`
  (`@supabase/pg-delta@1.0.0-alpha.51`)
- refresh `benchmark/README.md` and `benchmark/review-memory.json` to the
  2026-09-14 latest-state snapshot
- add fresh 2026-09-14 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- add this report as the 2026-09-14 latest-state sweep
- no new benchmark files or draft-only uncovered issue docs were added:
  today's new open pgschema issues were either already covered by current
  pg-delta or outside the parity scope, so the active benchmark set stayed
  unchanged

## 4) Validation notes

This refresh was validated with:

- `git reset --hard origin/avallete/schema-comparison-benchmark-427e`
- `git submodule update --init --recursive`
- `git -C repos/pgschema fetch origin`
- `git -C repos/pg-toolbelt fetch origin`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 30 --json number,title,updatedAt,url`
  - `gh issue list -R pgplex/pgschema --state closed --search 'closed:>=2026-09-13'`
  - `gh pr list -R pgplex/pgschema --state merged --search 'merged:>=2026-09-13'`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 50 --json number,title,updatedAt,url`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 50 --json number,title,updatedAt,url`
- GitHub CLI issue / PR context checks for:
  - pgschema issues **#596** / **#597** / **#598** / **#599** / **#600** /
    **#601** / **#602** / **#603**
  - pg-toolbelt PR **#470**
  - target-repo issue list (`gh issue list -R avallete/delta-schema-compare --state all`)
- exact duplicate issue / PR searches across `supabase/pg-toolbelt` and
  `avallete/delta-schema-compare` for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, `pgschema#593`, `pgschema#594`, `pgschema#595`,
  `pgschema#439`, and `pgschema#444`
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/routines.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/roles.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/indexes.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/triggers.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/routines.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/index-invalid-repair.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/owner-edge.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/default-privileges-owner-self-revoke.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/default-privilege.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/apply/commit-boundary.test.ts`
- Bun-backed pg-delta runtime probes were not re-run in this environment
  because Bun and Docker are unavailable in the pod; source inspection and
  checked-in tests were used instead
