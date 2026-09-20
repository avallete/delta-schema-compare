# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-09-20)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `0882fc4cb6b792b79b599a414b434e4e048b6672`
- checked-in/live `repos/pgschema` @ `b8e7e26a9db221ea01cdd64f4cfb8ca96923c536`

> The 2026-09-20 refresh advances checked-in/live `pgschema` from
> `11678c582923fc1a27ed2edf37f3503d1fc466a8` to
> `b8e7e26a9db221ea01cdd64f4cfb8ca96923c536` through merged PRs
> [#610](https://github.com/pgplex/pgschema/pull/610),
> [#612](https://github.com/pgplex/pgschema/pull/612),
> [#613](https://github.com/pgplex/pgschema/pull/613),
> [#614](https://github.com/pgplex/pgschema/pull/614), and
> [#615](https://github.com/pgplex/pgschema/pull/615), while checked-in/live
> `pg-toolbelt` remains `0882fc4cb6b792b79b599a414b434e4e048b6672`
>
> - merged pgschema PR [#610](https://github.com/pgplex/pgschema/pull/610)
>   closes already-covered issue
>   [#606](https://github.com/pgplex/pgschema/issues/606)
> - merged pgschema PR [#613](https://github.com/pgplex/pgschema/pull/613)
>   closes already-covered issue
>   [#593](https://github.com/pgplex/pgschema/issues/593)
> - merged pgschema PR [#614](https://github.com/pgplex/pgschema/pull/614)
>   closes upstream-only issue
>   [#594](https://github.com/pgplex/pgschema/issues/594)
> - merged pgschema PR [#615](https://github.com/pgplex/pgschema/pull/615)
>   closes upstream-only issue
>   [#596](https://github.com/pgplex/pgschema/issues/596), while open
>   follow-up PR [#616](https://github.com/pgplex/pgschema/pull/616)
>   continues the same temp-schema / SQL-function ordering family
> - merged pgschema PR [#612](https://github.com/pgplex/pgschema/pull/612)
>   reopens config-data request
>   [#559](https://github.com/pgplex/pgschema/issues/559) after removing
>   data-management work from `main`; that request remains outside pg-delta's
>   schema-diff parity scope
> - open pgschema PR [#611](https://github.com/pgplex/pgschema/pull/611) is
>   the upstream fix path for already-covered issue
>   [#598](https://github.com/pgplex/pgschema/issues/598), and open pgschema
>   PR [#608](https://github.com/pgplex/pgschema/pull/608) remains the
>   upstream fix path for upstream-only issue
>   [#607](https://github.com/pgplex/pgschema/issues/607)
> - the open pg-toolbelt umbrella issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332) still covers
>   only benchmarks **021** / **022**, while the adjacent issue / PR cluster
>   [#476](https://github.com/supabase/pg-toolbelt/issues/476),
>   [#477](https://github.com/supabase/pg-toolbelt/issues/477),
>   [#478](https://github.com/supabase/pg-toolbelt/pull/478),
>   [#480](https://github.com/supabase/pg-toolbelt/pull/480), and
>   [#481](https://github.com/supabase/pg-toolbelt/pull/481) still does not
>   close any active benchmark gap
> - the active benchmarked gap set therefore remains **021**, **022**, and
>   **024**
> - there is still **no open uncovered parity candidate** on the pgschema
>   side

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470) and [#480](https://github.com/supabase/pg-toolbelt/pull/480) (merged) | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | none found | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Three resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    keeps relation columns gated by `a.attislocal`, so child-local overrides
    on inherited partition columns do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed
    child column-element list
  - merged PR [#470](https://github.com/supabase/pg-toolbelt/pull/470)
    (alpha.51) and merged PR
    [#480](https://github.com/supabase/pg-toolbelt/pull/480) remain adjacent
    only: they rebuild replace-path dependents and keep attached child indexes
    on a partition drop root, but still do not add child-local override
    extraction or rendering; umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only open tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - current pg-delta already covers resolved pgschema issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s
    generated-expression-change family, so the active gap remains only the
    generated kind distinction
- **024** - PostgreSQL 18 native `NOT NULL ... NOT VALID` state and pending
  validation visibility
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models nullability through `a.attnotnull` and filters extracted table
    constraints to `con.contype IN ('p', 'u', 'f', 'c', 'x')`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - there is still no exact pg-toolbelt issue or PR for this benchmark

Because `pg-toolbelt` did not move in this refresh and the new pgschema delta
is confined to other covered or upstream-only issue families, the focused
2026-08-14 runtime observations for benchmarks **021** / **022** remain the
latest direct runtime evidence, and benchmark **024** remains source-level not
covered on the same current heads.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#599](https://github.com/pgplex/pgschema/issues/599),
[#600](https://github.com/pgplex/pgschema/issues/600),
[#601](https://github.com/pgplex/pgschema/issues/601),
[#602](https://github.com/pgplex/pgschema/issues/602),
[#603](https://github.com/pgplex/pgschema/issues/603), and
[#607](https://github.com/pgplex/pgschema/issues/607).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity work for
  pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work for
  pg-delta**
- **#559** config-table data evolution / reference-data management -
  **not parity work for pg-delta**; merged pgschema PR
  [#612](https://github.com/pgplex/pgschema/pull/612) reverted that feature
  out of `main`, but row-data synchronization remains outside pg-delta's
  schema-diff scope
- **#597** broad multi-schema complexity / auto-ignore feedback - **not parity
  work for pg-delta**; it is general product feedback rather than a concrete
  pg-delta parity scenario
- **#598** interrupted `CREATE INDEX CONCURRENTLY` leaves an invalid index
  behind - **covered** in current pg-delta:
  - `src/extract/relations.ts` captures regular-index `indisvalid` as semantic
    `valid`
  - `src/plan/rules/indexes.ts` diffs `valid` with the `"replace"` strategy
  - `tests/index-invalid-repair.test.ts` covers the invalid-index repair path
  - open pgschema PR [#611](https://github.com/pgplex/pgschema/pull/611) is
    the upstream fix path on the pgschema side
- **#599** trigger `ENABLE REPLICA` / `ENABLE ALWAYS` states - **covered** in
  current pg-delta's trigger model:
  - `src/extract/relations.ts` captures `pg_trigger.tgenabled` as `enabled`
  - `src/plan/rules/helpers.ts` maps `O/D/R/A` to `ENABLE`, `DISABLE`,
    `ENABLE REPLICA`, and `ENABLE ALWAYS`
  - `src/plan/rules/triggers.ts` emits the corresponding
    `ALTER TABLE ... TRIGGER` clauses
- **#600** enum `ADD VALUE` plus same-plan default use - **covered** in current
  pg-delta:
  - `src/plan/rules/types.ts` marks `ALTER TYPE ... ADD VALUE` actions as
    `transactionality: "commitBoundaryAfter"`
  - `src/apply/commit-boundary.test.ts` and the
    `type-ops--enum-add-value-used-in-*` corpus pin the required commit
    boundary
- **#601** function return-type change with a dependent view - **covered** by
  current pg-delta's generic replace-path dependent rebuild:
  - `src/extract/dependencies.ts` resolves a view's `_RETURN` rule
    dependencies onto the view fact itself
  - `src/plan/rules/routines.ts` treats `returnType` as `"replace"` and marks
    routines `rebuildable`
  - `src/plan/rules/views.ts` marks views `rebuildable`, so dependent views are
    dropped and recreated around a demolished function
- **#602** schema-level `OWNER TO` changes - **covered** in current pg-delta:
  - ownership is modeled as owner edges and emitted as `ALTER ... OWNER TO`
  - `tests/owner-edge.test.ts` covers owner roundtrip and owner-change flows
  - `ownerAlterPrefix` is implemented for tables, views, sequences, and
    routines
- **#603** global `ALTER DEFAULT PRIVILEGES` (no `IN SCHEMA`) - **covered** in
  current pg-delta:
  - `src/extract/roles.ts` keeps `defaclnamespace = 0` rows as global
    default-privilege facts
  - `src/plan/rules/helpers.ts` omits `IN SCHEMA` when the default-privilege
    fact carries `schema: null`
  - `tests/default-privileges-owner-self-revoke.test.ts` and
    `src/plan/rules/default-privilege.test.ts` cover the global
    extract/render shapes
- **#607** extension-owned types in the external plan/temp-schema path -
  **not parity work for pg-delta**; it remains the same upstream temp-schema /
  `search_path` resolution class as closed issue
  [#518](https://github.com/pgplex/pgschema/issues/518):
  - pg-delta diffs live catalogs instead of applying desired-state SQL to a
    temporary comparison schema
  - `src/extract/scope.ts` pins extraction `search_path` to `pg_catalog`,
    while `src/extract/relations.ts` preserves type text via `format_type(...)`
  - `tests/supabase-integration.test.ts` covers non-public `pgvector`
    type usage, and open pgschema PR
    [#608](https://github.com/pgplex/pgschema/pull/608) is the upstream fix
    path

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
adjacent tracker context, benchmark **024** still has no exact pg-toolbelt
issue or PR, open pg-toolbelt issue
[#476](https://github.com/supabase/pg-toolbelt/issues/476) plus issue
[#477](https://github.com/supabase/pg-toolbelt/issues/477) / PR
[#478](https://github.com/supabase/pg-toolbelt/pull/478), merged PR
[#480](https://github.com/supabase/pg-toolbelt/pull/480), and open release PR
[#481](https://github.com/supabase/pg-toolbelt/pull/481) are adjacent
cluster-global role / identity-sequence privilege / partition-index / release
work rather than duplicates, and this repository still has no local tracker
issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- closed pgschema issue
  [#588](https://github.com/pgplex/pgschema/issues/588) is still **not parity
  work** for pg-delta; the related config-data request
  [#559](https://github.com/pgplex/pgschema/issues/559) is open again after
  merged revert PR [#612](https://github.com/pgplex/pgschema/pull/612)
- closed pgschema issue
  [#593](https://github.com/pgplex/pgschema/issues/593) remains **covered** in
  current pg-delta; merged PR
  [#613](https://github.com/pgplex/pgschema/pull/613) is the upstream fix
- closed pgschema issue
  [#594](https://github.com/pgplex/pgschema/issues/594) remains **not parity
  work** for pg-delta; merged PR
  [#614](https://github.com/pgplex/pgschema/pull/614) only hardens
  `.pgschemaignore` parsing by rejecting unknown keys
- closed pgschema issue
  [#596](https://github.com/pgplex/pgschema/issues/596) remains **not parity
  work** for pg-delta; merged PR
  [#615](https://github.com/pgplex/pgschema/pull/615) and open follow-up PR
  [#616](https://github.com/pgplex/pgschema/pull/616) both land in
  pgschema's temp-schema / SQL-function body / batch-ordering path
- closed pgschema issue
  [#606](https://github.com/pgplex/pgschema/issues/606) remains **covered** in
  current pg-delta; merged PR
  [#610](https://github.com/pgplex/pgschema/pull/610) preserves partitioned-
  table primary-key order upstream
- open pgschema PR
  [#611](https://github.com/pgplex/pgschema/pull/611) is the upstream fix path
  for covered issue [#598](https://github.com/pgplex/pgschema/issues/598)
- open pgschema PR
  [#608](https://github.com/pgplex/pgschema/pull/608) remains the upstream fix
  path for upstream-only issue
  [#607](https://github.com/pgplex/pgschema/issues/607)
- **#564** safer `NOT NULL` additions / PG18 native validation workflow remains
  **not covered** in current pg-delta as benchmark **024**
- there are still no local tracker issues in this repository

## Upstream watch list

- checked-in/live `pgschema` advances to
  `b8e7e26a9db221ea01cdd64f4cfb8ca96923c536`; merged PRs
  [#610](https://github.com/pgplex/pgschema/pull/610),
  [#612](https://github.com/pgplex/pgschema/pull/612),
  [#613](https://github.com/pgplex/pgschema/pull/613),
  [#614](https://github.com/pgplex/pgschema/pull/614), and
  [#615](https://github.com/pgplex/pgschema/pull/615) landed since the
  2026-09-19 refresh, while open PRs
  [#608](https://github.com/pgplex/pgschema/pull/608),
  [#611](https://github.com/pgplex/pgschema/pull/611), and
  [#616](https://github.com/pgplex/pgschema/pull/616) remain in flight
- checked-in/live `pg-toolbelt` remains at
  `0882fc4cb6b792b79b599a414b434e4e048b6672`; no new pg-toolbelt issue or PR
  landed since the 2026-09-19 refresh that changes any benchmark verdict
- the nearby pg-toolbelt issue/PR landscape is:
  - open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476)
  - open issue [#477](https://github.com/supabase/pg-toolbelt/issues/477)
  - open PR [#478](https://github.com/supabase/pg-toolbelt/pull/478)
  - merged PR [#480](https://github.com/supabase/pg-toolbelt/pull/480)
  - open release PR [#481](https://github.com/supabase/pg-toolbelt/pull/481)
  - older open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
    [#472](https://github.com/supabase/pg-toolbelt/pull/472), and
    [#473](https://github.com/supabase/pg-toolbelt/pull/473)
  - only umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**, and benchmark **024**
    still has no exact pg-toolbelt issue or PR
  - issue **#476**, issue **#477**, PR **#478**, PR **#480**, and PR **#481**
    are adjacent cluster-global role / identity-sequence privilege /
    partition-index / release work rather than duplicates of the active
    benchmark set
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
