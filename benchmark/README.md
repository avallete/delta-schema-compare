# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-10)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
- checked-in/live `repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`

> The 2026-10-10 refresh advances checked-in/live `repos/pg-toolbelt` from
> `3c60914eae50ff9d28084a8a1ce4e110b9c3d55d` to
> `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4` through merged PRs
> [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
> [#527](https://github.com/supabase/pg-toolbelt/pull/527), while
> checked-in/live `repos/pgschema` remains
> `580f4040d0f3c1bfad1497918200c9c1f638a020`
>
> - `gh issue list --repo pgplex/pgschema --state open --search 'updated:>=2026-10-09'`
>   surfaced open issues
>   [#623](https://github.com/pgplex/pgschema/issues/623),
>   [#627](https://github.com/pgplex/pgschema/issues/627),
>   [#628](https://github.com/pgplex/pgschema/issues/628),
>   [#629](https://github.com/pgplex/pgschema/issues/629),
>   [#630](https://github.com/pgplex/pgschema/issues/630),
>   [#631](https://github.com/pgplex/pgschema/issues/631),
>   [#632](https://github.com/pgplex/pgschema/issues/632),
>   [#633](https://github.com/pgplex/pgschema/issues/633),
>   [#634](https://github.com/pgplex/pgschema/issues/634),
>   [#635](https://github.com/pgplex/pgschema/issues/635),
>   [#636](https://github.com/pgplex/pgschema/issues/636),
>   [#638](https://github.com/pgplex/pgschema/issues/638),
>   [#639](https://github.com/pgplex/pgschema/issues/639),
>   [#640](https://github.com/pgplex/pgschema/issues/640), and
>   [#641](https://github.com/pgplex/pgschema/issues/641)
> - `gh pr list --repo pgplex/pgschema --state all --search 'updated:>=2026-10-09'`
>   surfaced open PR [#637](https://github.com/pgplex/pgschema/pull/637)
> - the new pgschema global-state cluster rooted at
>   [#627](https://github.com/pgplex/pgschema/issues/627) plus PR
>   [#637](https://github.com/pgplex/pgschema/pull/637) does not add a new
>   benchmark parity item in this repo; the schema-diff issues
>   [#638](https://github.com/pgplex/pgschema/issues/638),
>   [#639](https://github.com/pgplex/pgschema/issues/639),
>   [#640](https://github.com/pgplex/pgschema/issues/640), and
>   [#641](https://github.com/pgplex/pgschema/issues/641) are already covered
>   or avoided in current pg-delta
> - `gh issue list --repo supabase/pg-toolbelt --state all --search 'updated:>=2026-10-09'`
>   plus `gh pr list --repo supabase/pg-toolbelt --state all --search
>   'updated:>=2026-10-09'` surfaced merged PRs
>   [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
>   [#527](https://github.com/supabase/pg-toolbelt/pull/527), open PRs
>   [#471](https://github.com/supabase/pg-toolbelt/pull/471),
>   [#522](https://github.com/supabase/pg-toolbelt/pull/522),
>   [#532](https://github.com/supabase/pg-toolbelt/pull/532),
>   [#534](https://github.com/supabase/pg-toolbelt/pull/534),
>   [#536](https://github.com/supabase/pg-toolbelt/pull/536), and
>   [#537](https://github.com/supabase/pg-toolbelt/pull/537), open issues
>   [#533](https://github.com/supabase/pg-toolbelt/issues/533) and
>   [#535](https://github.com/supabase/pg-toolbelt/issues/535), plus closed
>   issues [#510](https://github.com/supabase/pg-toolbelt/issues/510) and
>   [#521](https://github.com/supabase/pg-toolbelt/issues/521)
> - direct inspection of those updated pg-toolbelt items plus
>   `git -C repos/pg-toolbelt diff --name-only
>   3c60914eae50ff9d28084a8a1ce4e110b9c3d55d..7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4 -- packages/pg-delta/src/extract/relations.ts
>   packages/pg-delta/src/extract/dependencies.ts
>   packages/pg-delta/src/plan/rules/tables.ts
>   packages/pg-delta/src/plan/rules/helpers.ts
>   packages/pg-delta/src/plan/rules/types.ts`
>   shows the active benchmark paths are unchanged; the merged code lands in
>   `src/extract/routines.ts`, `src/extract/scoped-read.ts`, frontends/export /
>   settle paths, `src/policy/policy.ts`, and related tests
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
>   still returned `[]`
>
> The active benchmarked gap set therefore remains **021**, **022**, and
> **024**, and there is still **no open uncovered parity candidate** on the
> pgschema side.

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed), replacement [#231](https://github.com/supabase/pg-toolbelt/pull/231) (merged) | **Solved in pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |
| 020 | [UNIQUE constraint NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | none found | none found | **Solved in pg-delta** |
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread), adjacent [#530](https://github.com/supabase/pg-toolbelt/issues/530) (open rewrite-risk follow-up) | adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470), [#480](https://github.com/supabase/pg-toolbelt/pull/480), and [#488](https://github.com/supabase/pg-toolbelt/pull/488) (merged), [#501](https://github.com/supabase/pg-toolbelt/pull/501) (merged partition-key retype), and [#504](https://github.com/supabase/pg-toolbelt/pull/504) (merged dependency-edge repair) | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | historical [#174](https://github.com/supabase/pg-toolbelt/pull/174) (merged, legacy engine only), adjacent [#484](https://github.com/supabase/pg-toolbelt/pull/484) and [#485](https://github.com/supabase/pg-toolbelt/pull/485) (merged) | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Three resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    keeps inherited child columns gated by `a.attislocal`, so child-local
    overrides on inherited partition columns do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` now has
    merged `_partitionKey` / `replaceRoot` logic from PR
    [#501](https://github.com/supabase/pg-toolbelt/pull/501) and merged
    dependency-edge repairs from PR
    [#504](https://github.com/supabase/pg-toolbelt/pull/504), but the
    partition-child create path still emits bare
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list
  - closed issue [#497](https://github.com/supabase/pg-toolbelt/issues/497),
    open follow-up issue [#502](https://github.com/supabase/pg-toolbelt/issues/502),
    adjacent rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    merged PR [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    merged stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    and merged PR [#504](https://github.com/supabase/pg-toolbelt/pull/504)
    sharpen nearby partition-key / dependency-edge behavior; issue #530 tracks
    rewrite-risk declarations for inherited / partition children, but PR #504's
    own deferrals still call out the separate unmodeled partition-level default
    override problem tracked here
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - the 2026-10-10 pg-delta delta only touches `extract/routines.ts`,
    `extract/scoped-read.ts`, frontends/export / settle paths,
    `src/policy/policy.ts`, and related tests; none of those changes preserves
    generated kind, so umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only live tracker context
  - current pg-delta already covers resolved pgschema issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s
    generated-expression-change family, so the active gap remains only the
    generated kind distinction
- **024** - PostgreSQL 18 native `NOT NULL ... NOT VALID` state and pending
  validation visibility
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models nullability through `a.attnotnull`; PG18 `contype = 'n'` rows still
    only survive long enough to emit `table_not_null_comment_skipped`
    diagnostics for commented rows, not to become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - the 2026-10-10 pg-delta delta only touches `extract/routines.ts`,
    `extract/scoped-read.ts`, frontends/export / settle paths,
    `src/policy/policy.ts`, and related tests; there is still no exact current
    pg-toolbelt issue or PR for this benchmark

Because today's refresh advances checked-in/live `pg-toolbelt` through merged
PRs [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
[#527](https://github.com/supabase/pg-toolbelt/pull/527) while leaving the
active benchmark source paths untouched, source rechecks on the current head
still find `a.attislocal` in `relations.ts`, generated-column kind still
collapsed to expression presence plus a hard-coded `... STORED` renderer, and
PG18 table `contype = 'n'` rows still kept out of diff-visible facts. Exact
duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
`pgschema#627`, `pgschema#638`, `pgschema#639`, `pgschema#640`, and
`pgschema#641` still return no dedicated pg-toolbelt issue or PR; keyword
`"PARTITION OF"` searches now also surface open settle-definition issues
[#526](https://github.com/supabase/pg-toolbelt/issues/526) and
[#535](https://github.com/supabase/pg-toolbelt/issues/535) alongside umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332), adjacent
follow-up [#502](https://github.com/supabase/pg-toolbelt/issues/502),
rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
and merged partition PRs
[#501](https://github.com/supabase/pg-toolbelt/pull/501),
[#503](https://github.com/supabase/pg-toolbelt/pull/503),
[#504](https://github.com/supabase/pg-toolbelt/pull/504), and
[#514](https://github.com/supabase/pg-toolbelt/pull/514); `"VIRTUAL"
generated` still only surfaces live umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus historical
merged PRs [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
[#299](https://github.com/supabase/pg-toolbelt/pull/299); and
`"NOT NULL" "NOT VALID"` still surfaces only adjacent merged PRs
[#484](https://github.com/supabase/pg-toolbelt/pull/484) and
[#485](https://github.com/supabase/pg-toolbelt/pull/485) plus umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332). New open pgschema
issues [#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639),
[#640](https://github.com/pgplex/pgschema/issues/640), and
[#641](https://github.com/pgplex/pgschema/issues/641) are already covered or
avoided by current pg-delta, while the broader global-state cluster rooted at
[#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
[#637](https://github.com/pgplex/pgschema/pull/637) does not produce a new
benchmark parity item in this repo. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) therefore still only
covers benchmarks **021** / **022**, benchmark **024** still has no exact
current pg-toolbelt issue or PR, and there is still **no open uncovered parity
candidate**.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#623](https://github.com/pgplex/pgschema/issues/623),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#628](https://github.com/pgplex/pgschema/issues/628),
[#629](https://github.com/pgplex/pgschema/issues/629),
[#630](https://github.com/pgplex/pgschema/issues/630),
[#631](https://github.com/pgplex/pgschema/issues/631),
[#632](https://github.com/pgplex/pgschema/issues/632),
[#633](https://github.com/pgplex/pgschema/issues/633),
[#634](https://github.com/pgplex/pgschema/issues/634),
[#635](https://github.com/pgplex/pgschema/issues/635),
[#636](https://github.com/pgplex/pgschema/issues/636),
[#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639),
[#640](https://github.com/pgplex/pgschema/issues/640), and
[#641](https://github.com/pgplex/pgschema/issues/641).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity work for
  pg-delta**
- **#52** explicit before / after SQL file execution in plan output - **not
  parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work for
  pg-delta**
- **#559** config-table data evolution / reference-data management - **not
  parity work for pg-delta**
- **#597** broad multi-schema complexity / auto-ignore feedback - **not parity
  work for pg-delta**
- **#598** interrupted `CREATE INDEX CONCURRENTLY` leaves an invalid index
  behind - **covered** in current pg-delta:
  - `src/extract/relations.ts` captures regular-index `indisvalid` as semantic
    `valid`
  - `src/plan/rules/indexes.ts` diffs `valid` with the `"replace"` strategy
  - `tests/index-invalid-repair.test.ts` covers the invalid-index repair path
- **#623** publish release checksums - **not parity work for pg-delta**
- **#624** SQL function created before `ADD COLUMN` it depends on - **covered**
  in current pg-delta via the routine-plan `check_function_bodies = off`
  preamble plus existing SQL-body forward-reference coverage
- **#625** existing composite-type attribute changes are silently skipped -
  **covered** in current pg-delta via composite `typeAttribute` facts and
  `ALTER TYPE ... ADD ATTRIBUTE ... CASCADE` planning
- **#626** composite type creation runs before its required table - **covered**
  in current pg-delta via dependency extraction that resolves composite row-type
  edges back onto the owning table fact
- **#627 - #636** opt-in global-state roles / ownership cluster (plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637)) - **not added as new
  benchmark parity items in this repo**. These issues describe pgschema's new
  separate global-manifest surface; adjacent pg-delta role / owner work exists
  in open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) plus merged
  membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
  [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
  [#461](https://github.com/supabase/pg-toolbelt/pull/461), but exact duplicate
  search `pgschema#627` still returns no dedicated pg-toolbelt issue or PR
- **#638** mixed column-privilege rendering (`GRANT INSERT, UPDATE (cols)`) -
  **covered** in current pg-delta:
  - `renderGrantSql()` renders column privileges as `PRIV (col), PRIV (col)`
  - `tests/column-grant-fidelity.test.ts` covers extracted table column grants
  - `src/frontends/sql-format/format-grant.test.ts` explicitly pins
    `GRANT SELECT (col), UPDATE (col) ...`
- **#639** partition bounds / attachment drift - **covered** in current
  pg-delta:
  - extracted table facts preserve `partitionBound` and `parentTable`
  - `src/plan/rules/tables.ts` treats both attributes as `"replace"`
  - corpuses `table-ops--attach-partition` and `table-ops--detach-partition`
    cover attach / detach state changes
- **#640** privileges on partitioned tables are omitted - **covered** in
  current pg-delta:
  - relation extraction already includes partitioned tables in the table ACL
    path (`c.relkind IN ('r', 'p')`)
  - column ACL extraction likewise includes `relkind 'p'`
- **#641** schema-unqualified wait query after `CREATE INDEX CONCURRENTLY` -
  **covered / not a pg-delta gap**:
  - pg-delta apply executes action SQL directly via `client.query(action.sql)`
    instead of a separate name-based wait loop
  - invalid concurrent-index residue is already modeled through `indisvalid`
    and covered by `tests/index-invalid-repair.test.ts`

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
exact tracker context, benchmark **024** still has no exact current
pg-toolbelt issue or PR, and the current pg-toolbelt head now reflects merged
PRs [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
[#527](https://github.com/supabase/pg-toolbelt/pull/527). This repository
still has no local tracker issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh issue list --repo pgplex/pgschema --state open --search
  'updated:>=2026-10-09'` surfaced open issues
  [#623](https://github.com/pgplex/pgschema/issues/623) and
  [#627](https://github.com/pgplex/pgschema/issues/627) through
  [#641](https://github.com/pgplex/pgschema/issues/641); the matching PR query
  surfaced open PR [#637](https://github.com/pgplex/pgschema/pull/637)
- the new pgschema global-state cluster rooted at
  [#627](https://github.com/pgplex/pgschema/issues/627) /
  [#637](https://github.com/pgplex/pgschema/pull/637) is not being promoted
  into new benchmark gap docs in this repo, and the new schema-diff issues
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641) are already covered or
  avoided in current pg-delta
- `gh issue list --repo supabase/pg-toolbelt --state all --search
  'updated:>=2026-10-09'` plus `gh pr list --repo supabase/pg-toolbelt --state
  all --search 'updated:>=2026-10-09'` surfaced merged PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
  [#527](https://github.com/supabase/pg-toolbelt/pull/527), open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#522](https://github.com/supabase/pg-toolbelt/pull/522),
  [#532](https://github.com/supabase/pg-toolbelt/pull/532),
  [#534](https://github.com/supabase/pg-toolbelt/pull/534),
  [#536](https://github.com/supabase/pg-toolbelt/pull/536), and
  [#537](https://github.com/supabase/pg-toolbelt/pull/537), open issues
  [#533](https://github.com/supabase/pg-toolbelt/issues/533) and
  [#535](https://github.com/supabase/pg-toolbelt/issues/535), plus closed
  issues [#510](https://github.com/supabase/pg-toolbelt/issues/510) and
  [#521](https://github.com/supabase/pg-toolbelt/issues/521)
- direct inspection of updated pg-toolbelt work plus
  `git -C repos/pg-toolbelt diff --name-only 3c60914eae50ff9d28084a8a1ce4e110b9c3d55d..7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
  showed only `src/extract/routines.ts`, `src/extract/scoped-read.ts`,
  frontends/export / settle paths, `src/policy/policy.ts`, and related tests
  changed; the active benchmark paths `src/extract/relations.ts`,
  `src/extract/dependencies.ts`, `src/plan/rules/tables.ts`,
  `src/plan/rules/helpers.ts`, and `src/plan/rules/types.ts` stayed unchanged
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#627`, `pgschema#638`, `pgschema#639`, `pgschema#640`, and
  `pgschema#641` still returned `[]`; keyword searches for `"PARTITION OF"`
  now also surface open issues
  [#526](https://github.com/supabase/pg-toolbelt/issues/526) and
  [#535](https://github.com/supabase/pg-toolbelt/issues/535) alongside the
  existing umbrella / adjacent partition context, while `"VIRTUAL" generated`
  and `"NOT NULL" "NOT VALID"` still only surface the historical / umbrella
  context already recorded in active benchmarks **022** and **024**
- previously screened pgschema verdicts remain unchanged: open issue
  [#598](https://github.com/pgplex/pgschema/issues/598) remains **covered**,
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597), and
  [#623](https://github.com/pgplex/pgschema/issues/623) remain **not parity**,
  open issues [#624](https://github.com/pgplex/pgschema/issues/624),
  [#625](https://github.com/pgplex/pgschema/issues/625),
  [#626](https://github.com/pgplex/pgschema/issues/626),
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641) remain **covered**,
  the new global-state cluster [#627](https://github.com/pgplex/pgschema/issues/627)
  through [#636](https://github.com/pgplex/pgschema/issues/636) is still
  treated as **not added as a benchmark parity gap in this repo**, and active
  resolved benchmarks [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501), and
  [#564](https://github.com/pgplex/pgschema/issues/564) remain **tracked** /
  **tracked** / **not covered** respectively
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

## Upstream watch list

- checked-in/live `pgschema` remains at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`; the updated-since issue query
  surfaced open issues [#623](https://github.com/pgplex/pgschema/issues/623)
  and [#627](https://github.com/pgplex/pgschema/issues/627) through
  [#641](https://github.com/pgplex/pgschema/issues/641), while the matching PR
  query surfaced open PR [#637](https://github.com/pgplex/pgschema/pull/637)
  as the upstream implementation branch for the new global-state surface
- checked-in/live `pg-toolbelt` now sits at
  `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`, which comes from merged PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
  [#527](https://github.com/supabase/pg-toolbelt/pull/527); the updated-since
  queries for `>=2026-10-09` surfaced open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#522](https://github.com/supabase/pg-toolbelt/pull/522),
  [#532](https://github.com/supabase/pg-toolbelt/pull/532),
  [#534](https://github.com/supabase/pg-toolbelt/pull/534),
  [#536](https://github.com/supabase/pg-toolbelt/pull/536), and
  [#537](https://github.com/supabase/pg-toolbelt/pull/537), open issues
  [#533](https://github.com/supabase/pg-toolbelt/issues/533) and
  [#535](https://github.com/supabase/pg-toolbelt/issues/535), plus closed
  issues [#510](https://github.com/supabase/pg-toolbelt/issues/510) and
  [#521](https://github.com/supabase/pg-toolbelt/issues/521), but the only new
  merged code lands in `extract/routines.ts`, `extract/scoped-read.ts`,
  frontends/export / settle paths, `policy/policy.ts`, and related tests
  rather than the active benchmark source paths
- the nearby benchmark-relevant pg-toolbelt issue/PR landscape remains
  unchanged at the exact-gap level, and so does the parity mapping:
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**; exact searches for
    `pgschema#499` and `pgschema#501` still return no dedicated issue or PR
  - open issues [#502](https://github.com/supabase/pg-toolbelt/issues/502)
    and [#530](https://github.com/supabase/pg-toolbelt/issues/530) remain the
    adjacent partition follow-up / rewrite-risk context for benchmark **021**;
    keyword `"PARTITION OF"` searches now also surface older settle issue
    [#526](https://github.com/supabase/pg-toolbelt/issues/526), newer settle
    issue [#535](https://github.com/supabase/pg-toolbelt/issues/535), and
    merged PRs [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    [#504](https://github.com/supabase/pg-toolbelt/pull/504), and
    [#514](https://github.com/supabase/pg-toolbelt/pull/514); those are still
    adjacent settle / replace-root work rather than exact child-local override
    fixes
  - historical PR [#174](https://github.com/supabase/pg-toolbelt/pull/174)
    remains legacy-engine-only context for benchmark **024**; exact
    `pgschema#564` searches still return no current pg-toolbelt issue or PR,
    while keyword `"NOT NULL" "NOT VALID"` still surfaces merged PRs
    [#484](https://github.com/supabase/pg-toolbelt/pull/484) and
    [#485](https://github.com/supabase/pg-toolbelt/pull/485) plus umbrella
    issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
    adjacent context rather than an exact tracker for that workflow
  - new open pgschema issues
    [#638](https://github.com/pgplex/pgschema/issues/638),
    [#639](https://github.com/pgplex/pgschema/issues/639),
    [#640](https://github.com/pgplex/pgschema/issues/640), and
    [#641](https://github.com/pgplex/pgschema/issues/641) have no dedicated
    pg-toolbelt issue or PR because current pg-delta already renders column
    grants correctly, models partition attachment / bounds, includes
    partitioned tables in ACL extraction, and executes concurrent-index SQL
    directly without a name-based wait loop
  - the broader global-state cluster rooted at
    [#627](https://github.com/pgplex/pgschema/issues/627) plus PR
    [#637](https://github.com/pgplex/pgschema/pull/637) is not being promoted
    into new benchmark gap docs in this repo; adjacent pg-delta owner / role
    work exists in open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471)
    and [#493](https://github.com/supabase/pg-toolbelt/pull/493) plus merged
    role / membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
    [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
    [#461](https://github.com/supabase/pg-toolbelt/pull/461)
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
