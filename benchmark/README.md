# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-09-12)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `85e8946a79b0a5b149fe9a772fef882c14cb9567`
- checked-in/live `repos/pgschema` @ `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`

> The 2026-09-12 refresh keeps the active benchmarked gap set unchanged at
> **021**, **022**, and **024**:
>
> - there is no upstream code delta since the 2026-09-11 refresh; both
>   checked-in submodules already match the latest `origin/main` heads
> - the only new upstream issue is
>   [#594](https://github.com/pgplex/pgschema/issues/594)
>   (`ignore views seems broken`), which remains **not parity work for
>   pg-delta** because it is a `.pgschemaignore` view-ignore configuration
>   issue rather than pg-delta diff/apply behavior
> - benchmark **021** remains unresolved because child-local partition column
>   overrides are still not extracted or rendered
> - benchmark **022** remains unresolved because pg-delta still collapses the
>   generated-column kind and rewrites PostgreSQL 18 `VIRTUAL` to `STORED`
> - benchmark **024** remains unresolved because pg-delta still does not model
>   PostgreSQL 18 native `NOT NULL ... NOT VALID` / `VALIDATE CONSTRAINT`
>   state
> - exact duplicate searches for `pgschema#499`, `#501`, `#564`, `#593`, and
>   `#594` still return no dedicated pg-toolbelt issue or PR, and this
>   repository still has no local tracker issues

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | [#470](https://github.com/supabase/pg-toolbelt/pull/470) (open, adjacent only) | **Tracked (umbrella thread only)** |
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
  - open PR [#470](https://github.com/supabase/pg-toolbelt/pull/470) remains
    adjacent only, and umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only tracker context
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

Because the checked-in/live heads are unchanged from the 2026-09-11 refresh,
the focused 2026-08-14 runtime observations for benchmarks **021** / **022**
and the source-level validation for benchmark **024** remain the latest direct
evidence on current pg-delta.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#588](https://github.com/pgplex/pgschema/issues/588),
[#593](https://github.com/pgplex/pgschema/issues/593), and
[#594](https://github.com/pgplex/pgschema/issues/594).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity work for
  pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work for
  pg-delta**
- **#588** data-feature design feedback - **not parity work for pg-delta**;
  current pg-delta remains a schema-diff tool and deliberately leaves row-level
  data comparison out of scope
- **#593** explicit non-default column collations - **covered** in current
  pg-delta's extract/render model:
  - `src/extract/relations.ts` preserves explicit non-default `attcollation`
    on column facts
  - `src/plan/rules/helpers.ts` replays that state as `COLLATE ...`
- **#594** view-ignore behavior in `.pgschemaignore` - **not parity work for
  pg-delta**; it is an upstream dump/filter configuration issue rather than a
  pg-delta live-catalog diff/apply gap

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
adjacent tracker context, benchmark **024** still has no exact pg-toolbelt
issue or PR, and exact duplicate searches for the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444) still return no dedicated
pg-toolbelt issue or PR.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most recent benchmark-
relevant closed items remain:

- **#591** generated-column expression changes on existing columns - closed on
  2026-09-10 by [pgschema#592](https://github.com/pgplex/pgschema/pull/592)
  and remains **covered** in current pg-delta via the existing
  `packages/pg-delta/corpus/alter-table--generated-column` scenario plus the
  `generatedExpr: "replace"` diff path
- **#589** `ON DELETE SET NULL` / `SET DEFAULT` column lists on foreign keys -
  closed on 2026-09-09 by [pgschema#590](https://github.com/pgplex/pgschema/pull/590)
  and remains **covered** because pg-delta keys and replays foreign-key
  definitions from canonical `pg_get_constraintdef(...)` text
- **#564** safer `NOT NULL` additions / PG18 native validation workflow -
  closed on 2026-09-08 by
  [pgschema#566](https://github.com/pgplex/pgschema/pull/566) and
  [pgschema#587](https://github.com/pgplex/pgschema/pull/587), and remains
  **not covered** in current pg-delta as benchmark **024**
- **#571**, **#573**, **#574**, **#576**, **#579**, and **#580** remain
  **covered** in current pg-delta and do not change the active benchmark set

## Upstream watch list

- checked-in/live `pgschema` remains at
  `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`
- checked-in/live `pg-toolbelt` remains at
  `85e8946a79b0a5b149fe9a772fef882c14cb9567`
- there are no merged pgschema PRs or newly closed pgschema issues since the
  2026-09-11 refresh
- recent pg-toolbelt activity since 2026-09-11 remains open PRs
  [#470](https://github.com/supabase/pg-toolbelt/pull/470),
  [#471](https://github.com/supabase/pg-toolbelt/pull/471), and
  [#472](https://github.com/supabase/pg-toolbelt/pull/472)
  - only PR **#470** is adjacent to the benchmark set, and it still does not
    close benchmark **021**'s child-local column-override gap
  - PRs **#471** and **#472** remain unrelated to benchmarks **021**, **022**,
    and **024**
- no target-repo issue in `avallete/delta-schema-compare` currently matches
  pgschema issues **#499**, **#501**, **#564**, **#593**, **#594**, **#439**,
  or **#444**

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
