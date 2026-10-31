# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-31)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`
- checked-in/live `repos/pgschema` @ `9de190efdf78cd422850a3bc3db13ee84a11462d`

> `git ls-remote` confirms both `main` branches are still those SHAs. Neither
> head moved since the 2026-10-30 refresh, so no benchmark verdict changed.
> Full notes are in
> [`docs/parity-refresh-2026-10-31.md`](../docs/parity-refresh-2026-10-31.md).
> The 2026-10-30 record remains in
> [`docs/parity-refresh-2026-10-30.md`](../docs/parity-refresh-2026-10-30.md).
>
> The only upstream item newer than that refresh is open pgschema PR
> [#679](https://github.com/pgplex/pgschema/pull/679) (`16b7d85e`, updated
> `2026-10-30T09:11:22Z`, not merged). It shortens the `_pgschema_new`
> candidate for a 63-byte index name and would close
> [#670](https://github.com/pgplex/pgschema/issues/670). That mechanism is
> still **not parity** for pg-delta: a `_pgschema_new` search under
> `packages/pg-delta` returns no matches, and pg-delta builds concurrent
> indexes under the final name. #670 stays open (`updatedAt`
> `2026-10-27T21:05:08Z`). No tracker was opened.
>
> Active gaps remain **021**, **022**, **024**, and **026**. Benchmark
> **025** stays solved. The same-table fold guard is still
> `src/plan/internal.ts` lines 783-797. Direct source rechecks on the
> unchanged pg-delta head keep the previous citations: `relations.ts` line
> 189 (`a.attislocal`), `tables.ts` line 52 (bare `PARTITION OF`),
> `relations.ts` lines 211 and 261 (`generatedExpr`), `tables.ts` line 712
> (hard-coded `STORED`), `relations.ts` line 121 (`a.attnotnull`),
> `relations.ts` lines 361-396 (PG18 `contype = 'n'` skipped except the
> comment diagnostic), `tables.ts` line 449 (plain `SET NOT NULL`), and
> `tables.ts` lines 246-247 (`partitionBound` / `parentTable` replace).
> A `VIRTUAL` search and a `DETACH PARTITION` search under
> `packages/pg-delta` TypeScript still return no matches.
>
> Exact duplicate searches for `pgschema#499`, `pgschema#501`,
> `pgschema#564`, `pgschema#534`, `pgschema#639`, `pgschema#670`,
> `pgschema#673`, `pgschema#674`, and `pgschema#677` still returned no
> dedicated pg-toolbelt issue or PR. Umbrella issue
> [#332](https://github.com/supabase/pg-toolbelt/issues/332) is still
> `updatedAt` `2026-09-29T15:57:49Z`. Issue
> [#554](https://github.com/supabase/pg-toolbelt/issues/554) is still
> `updatedAt` `2026-10-28T11:36:22Z`. Open pgschema PR
> [#676](https://github.com/pgplex/pgschema/pull/676) is still unmerged, so
> [#673](https://github.com/pgplex/pgschema/issues/673) stays **covered**
> here and open upstream. [#674](https://github.com/pgplex/pgschema/issues/674)
> stays the open `not_covered` candidate; the draft remains
> [`docs/parity-issue-drafts-2026-10-30.md`](../docs/parity-issue-drafts-2026-10-30.md)
> and was not opened. No new numbered benchmark.
>
> `benchmark/review-memory.json` is unchanged. Both submodule SHAs and the
> watched issue `updated_at` values are the same as the 2026-10-30
> fingerprints. This repository still has no local tracker issues.
>
> Previous snapshot (2026-10-30), kept below:

## Previous refresh snapshot (2026-10-30)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`
- checked-in/live `repos/pgschema` @ `9de190efdf78cd422850a3bc3db13ee84a11462d`

> `git ls-remote` confirms both `main` branches moved.
> `supabase/pg-toolbelt` advanced from
> `6b82eff84dba925a176f0c6a78e5a16843885366` to
> `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c` through merged PR
> [#555](https://github.com/supabase/pg-toolbelt/pull/555).
> `pgplex/pgschema` advanced from
> `36a38ff3c25db956ae8b5be2eee552d8bc69fb47` to
> `9de190efdf78cd422850a3bc3db13ee84a11462d`. Full notes are in
> [`docs/parity-refresh-2026-10-30.md`](../docs/parity-refresh-2026-10-30.md).
> The 2026-10-28 record remains in
> [`docs/parity-refresh-2026-10-28.md`](../docs/parity-refresh-2026-10-28.md).
>
> pgschema commits on that range:
>
> - [#678](https://github.com/pgplex/pgschema/pull/678) merged — re-emit
>   `COMMENT ON` when a function or procedure is dropped and recreated,
>   closing [#677](https://github.com/pgplex/pgschema/issues/677)
>   (`9de190ef`)
> - [#675](https://github.com/pgplex/pgschema/pull/675) merged — Alpine
>   base image bump (`f2ebe96b`). Outside schema-diff parity.
>
> [#677](https://github.com/pgplex/pgschema/issues/677) is **covered**.
> A return-type change replaces the routine, and the replace path
> recreates unchanged child facts
> (`src/plan/phases/action-emitter.ts` lines 373-389), including the
> comment satellite. No new benchmark. The same path recreates unchanged
> ACL children, so the grants follow-up noted in PR #678 is not a
> pg-delta gap. It is unfiled on the pgschema side and stays watch-only.
>
> New unlabeled open issues, screened by hand because the label-filtered
> compare scripts still return zero rows:
>
> - [#673](https://github.com/pgplex/pgschema/issues/673) `INCLUDE`
>   columns on PRIMARY KEY and UNIQUE constraints — **covered**.
>   `pg_get_constraintdef` is stored as `def` and emitted verbatim
>   (`src/extract/relations.ts` line 335,
>   `src/plan/rules/constraints.ts` lines 18-21). `def` is `"replace"`,
>   so an INCLUDE-only change replaces the constraint. Partition children
>   clone that definition through `PARTITION OF`. Open pgschema PR
>   [#676](https://github.com/pgplex/pgschema/pull/676) is the upstream
>   fix and is not merged. Exact search for `pgschema#673` returned no
>   pg-toolbelt issue or PR. No tracker was opened.
> - [#674](https://github.com/pgplex/pgschema/issues/674) comments on
>   table constraints, including distinct comments on inherited partition
>   constraints — **not covered** for the child comment. Local constraint
>   comments already round-trip. Inherited rows (`conislocal = false`)
>   are skipped (`relations.ts` line 360), so a child comment that
>   differs from the parent is never extracted. Exact search for
>   `pgschema#674` returned no pg-toolbelt issue or PR. Umbrella issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332) item 4 is
>   view column comments, not this case. The draft is
>   [`docs/parity-issue-drafts-2026-10-30.md`](../docs/parity-issue-drafts-2026-10-30.md).
>   No issue was opened. The pgschema issue is still open, so this stays
>   on the watch list as `not_covered` rather than a numbered benchmark.
>
> No benchmark verdict changed. Active gaps remain **021**, **022**,
> **024**, and **026**. Benchmark **025** stays solved. The same-table
> fold guard is now `src/plan/internal.ts` lines 783-797. It was lines
> 779-793 before PR #555 inserted a four-line rename-cycle guard at
> line 277. The check itself is unchanged.
>
> Direct source rechecks on the new pg-delta head: `relations.ts` line
> 189 still gates `a.attislocal`; `tables.ts` line 52 still emits bare
> `PARTITION OF`; `relations.ts` lines 211 and 261 still collapse
> generated kind to `generatedExpr`; `tables.ts` line 712 still
> hard-codes `STORED`; `relations.ts` line 121 still uses `a.attnotnull`;
> `relations.ts` lines 361-396 still skip PG18 `contype = 'n'` except for
> the comment diagnostic; `tables.ts` line 449 still plans plain
> `SET NOT NULL`. A `VIRTUAL` search and a `DETACH PARTITION` search
> under `packages/pg-delta` TypeScript still return no matches.
>
> The open pgschema watch list is now **#49 / #52 / #84 / #559 / #597 /
> #598 / #624 / #625 / #626 / #627 / #670 / #672 / #673 / #674**.
> **#674** is the new open `not_covered` candidate. **#673** is
> `covered`. **#677** is resolved `covered`.
>
> Previous snapshot (2026-10-28), kept below for the commit range that
> introduced benchmark **026**:

## Earlier refresh snapshot (2026-10-28)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `6b82eff84dba925a176f0c6a78e5a16843885366`
- checked-in/live `repos/pgschema` @ `36a38ff3c25db956ae8b5be2eee552d8bc69fb47`

> `git ls-remote` on 2026-10-28 confirmed `supabase/pg-toolbelt` `main` was
> still `6b82eff84dba925a176f0c6a78e5a16843885366`. `pgplex/pgschema` `main`
> had advanced from `8703c276c3ee4bab6d4e30b14e6e8982ace14b89` to
> `36a38ff3c25db956ae8b5be2eee552d8bc69fb47`. `packages/pg-delta` was
> unchanged that day, so benchmarks **021**, **022**, **024**, and **025**
> kept their previous verdicts. Full notes are in
> [`docs/parity-refresh-2026-10-28.md`](../docs/parity-refresh-2026-10-28.md).
>
> pgschema commits on that range:
>
> - [#668](https://github.com/pgplex/pgschema/pull/668) merged — detach and
>   attach partitions when their parent or bound changes, closing
>   [#639](https://github.com/pgplex/pgschema/issues/639) (`36a38ff3`)
> - [#667](https://github.com/pgplex/pgschema/pull/667) merged — disable
>   `check_function_bodies` on apply, closing
>   [#665](https://github.com/pgplex/pgschema/issues/665) (`4b3bd0f6`)
> - [#666](https://github.com/pgplex/pgschema/pull/666) merged — retry the
>   embedded PostgreSQL launch when the probed port is taken (`2a475ace`)
>
> [#639](https://github.com/pgplex/pgschema/issues/639) moves from the open
> watch list to benchmark **026**. pg-delta already detects the drift:
> `partitionBound` and `parentTable` are `"replace"` in
> `src/plan/rules/tables.ts` (line 246). The landed plan is
> `DETACH PARTITION` then `ATTACH PARTITION`. A `DETACH PARTITION` search
> under `packages/pg-delta` returns no TypeScript matches, and
> `DROP TABLE` on the partition deletes rows and fails when a foreign key
> references the parent. Exact searches for `pgschema#639` returned no
> pg-toolbelt issue or PR. The tracker draft is
> [`docs/parity-issue-drafts-2026-10-28.md`](../docs/parity-issue-drafts-2026-10-28.md);
> no issue was opened.
>
> [#665](https://github.com/pgplex/pgschema/issues/665) stays **covered**.
> pg-delta already sets `check_function_bodies = off` when a plan touches a
> routine (`src/plan/plan.ts` lines 823-831).
> [#666](https://github.com/pgplex/pgschema/pull/666) is the embedded
> launcher and is outside schema-diff parity.
>
> New unlabeled issues screened by hand:
> [#669](https://github.com/pgplex/pgschema/issues/669) closed completed
> with no source change (online-index `_pgschema_new` collision),
> [#670](https://github.com/pgplex/pgschema/issues/670) and
> [#672](https://github.com/pgplex/pgschema/issues/672) stay open on that
> same online-index mechanism, and
> [#671](https://github.com/pgplex/pgschema/issues/671) closed
> `NOT_PLANNED` (apostrophes in pgschema's desired-state qualifier).
> All four are **not parity** for pg-delta. pg-delta quotes identifiers
> with `qid()` and builds concurrent indexes under the final name.
>
> pg-toolbelt `main` gained no merged PRs and no closed issues in the
> `>=2026-10-27` window. Open PR
> [#555](https://github.com/supabase/pg-toolbelt/pull/555) gained commit
> `67793ef` in `src/frontends/settle-desired.ts` (respelled check names
> across a table rename). That commit does not touch the active gap paths.
> New issue [#561](https://github.com/supabase/pg-toolbelt/issues/561) /
> PR [#562](https://github.com/supabase/pg-toolbelt/pull/562) and issue
> [#563](https://github.com/supabase/pg-toolbelt/issues/563) / PR
> [#564](https://github.com/supabase/pg-toolbelt/pull/564) are Supabase
> profile hiding and non-superuser owner changes. PR
> [#560](https://github.com/supabase/pg-toolbelt/pull/560) remains the
> `@supabase/pg-checks` spike.
>
> The active benchmarked gap set is now **021**, **022**, **024**, and
> **026**. Benchmark **025** stays **Solved in pg-delta**. The live open
> pgschema issue set is now **#49 / #52 / #84 / #559 / #597 / #598 / #624 /
> #625 / #626 / #627 / #670 / #672**.
>
> Direct source rechecks on the unchanged pg-delta head keep the previous
> gap paths open: benchmark **021** still hinges on `a.attislocal`
> (`relations.ts` line 189) plus bare `PARTITION OF ... ${bound}` rendering
> (`tables.ts` line 52), benchmark **022** still collapses generated kind to
> `generatedExpr` (`relations.ts` lines 211 and 261) plus hard-coded
> `... STORED` in `tables.ts` `columnClause()` (line 712), and benchmark
> **024** still keeps PG18 `contype = 'n'` rows out of diff-visible facts
> (`relations.ts` lines 361-396) while planning plain `SET NOT NULL`
> (`tables.ts` line 449). A `VIRTUAL` search under `packages/pg-delta/src`
> still returns no matches. Exact duplicate searches for `pgschema#499`,
> `pgschema#501`, `pgschema#564`, `pgschema#534`, and `pgschema#639` still
> returned no dedicated pg-toolbelt issue or PR.
> `benchmark/review-memory.json` now records the new pgschema SHA on the
> revalidated watch list and on benchmarks **021** / **022** / **024** /
> **025**, moves **#639** to `resolved` as `not_covered`, and records
> **#665** as covered plus **#669** / **#670** / **#671** / **#672** as
> not parity.

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread), adjacent [#530](https://github.com/supabase/pg-toolbelt/issues/530) (closed rewrite-risk precursor) | merged [#541](https://github.com/supabase/pg-toolbelt/pull/541) (rewrite-risk declarations only), adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470), [#480](https://github.com/supabase/pg-toolbelt/pull/480), and [#488](https://github.com/supabase/pg-toolbelt/pull/488) (merged), [#501](https://github.com/supabase/pg-toolbelt/pull/501) (merged partition-key retype), and [#504](https://github.com/supabase/pg-toolbelt/pull/504) (merged dependency-edge repair) | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | adjacent [#553](https://github.com/supabase/pg-toolbelt/pull/553) (merged generated-column fold order only) and [#556](https://github.com/supabase/pg-toolbelt/pull/556) (merged helper move; `columnClause()` now lives in `tables.ts` and still hard-codes `STORED`) | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | historical [#174](https://github.com/supabase/pg-toolbelt/pull/174) (merged, legacy engine only), adjacent [#484](https://github.com/supabase/pg-toolbelt/pull/484) and [#485](https://github.com/supabase/pg-toolbelt/pull/485) (merged) | **Not covered** |
| 025 | [Self-referencing FK to non-PK UNIQUE key](025-self-referencing-fk-nonpk-unique-ordering.md) | [#534](https://github.com/pgplex/pgschema/issues/534) | [#543](https://github.com/supabase/pg-toolbelt/issues/543) (closed) | merged [#546](https://github.com/supabase/pg-toolbelt/pull/546) (exact fix) | **Solved in pg-delta** |
| 026 | [Partition rebind via DETACH / ATTACH](026-partition-rebind-detach-attach.md) | [#639](https://github.com/pgplex/pgschema/issues/639) | none found | none found; roadmap note only (`docs/roadmap/pg-delta-next-follow-ups.md`) | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Four resolved-issue benchmark scenarios remain active as unresolved behavior.
Rechecked on 2026-10-31 against the same pg-toolbelt `36ac91d3` and pgschema
`9de190ef` heads. Neither `main` moved, and no benchmark verdict changed.
Open pgschema PR [#679](https://github.com/pgplex/pgschema/pull/679) is the
only newer upstream item. It is unmerged and is not a pg-delta gap. The
2026-10-30 recheck against those same heads found that merged pg-toolbelt PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) settles renamed
check spelling before rename discovery. It does not close any of these
gaps. The benchmark **025** fold guard moved from `internal.ts` lines
779-793 to lines 783-797 because that PR inserts a rename-cycle guard;
the same-table check itself is unchanged.

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
    closed rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541),
    merged PR [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    merged stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    and merged PR [#504](https://github.com/supabase/pg-toolbelt/pull/504)
    sharpen nearby partition-key / rewrite-risk / dependency-edge behavior.
    Merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) edits
    `src/plan/rules/tables.ts` for generated-column fold hints only. Merged PR
    [#550](https://github.com/supabase/pg-toolbelt/pull/550) now restores a
    non-subpartitioned child's own index storage options after
    `PARTITION OF`, and records further `INHERITS` parents as
    `inheritsAlso`. The partition-child create path and `a.attislocal` filter
    stay as they were
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
    `columnClause()` hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`. Merged PR
    [#556](https://github.com/supabase/pg-toolbelt/pull/556) moved that helper
    out of `src/plan/rules/helpers.ts` without changing the keyword
  - merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) still
    folds generated columns into `CREATE TABLE` through the same
    `columnClause()` helper, so the hard-coded `STORED` keyword also
    appears on the inline create path. Umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only live tracker context for the kind distinction
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
  - the 2026-10-23 pg-delta delta from
    `63b3f653d99f936fa40c5a7689d771e829f09f45` to
    `265af521e462577886ea6fdbb5777e1a23811cce` changes export round-trip
    fidelity, helper placement, apply error text, and shadow-load durability.
    It still lands no exact current pg-toolbelt issue or PR for this benchmark.
    The 2026-10-24 follow-on commit `6b82eff8` edits only `.github/CODEOWNERS`
- **026** - partition parent or bound changes applied as
  `DETACH PARTITION` / `ATTACH PARTITION`
  - `src/plan/rules/tables.ts` still marks `partitionBound` and
    `parentTable` `"replace"` (line 246), so the plan is `DROP TABLE` plus
    `CREATE TABLE ... PARTITION OF`
  - a `DETACH PARTITION` search under `packages/pg-delta` returns no
    TypeScript matches. The existing attach and detach corpuses still go
    through table replace
  - exact search for `pgschema#639` still returns no dedicated pg-toolbelt
    issue or PR. The draft is
    [`docs/parity-issue-drafts-2026-10-28.md`](../docs/parity-issue-drafts-2026-10-28.md)

As of 2026-10-30, PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) is merged at
`36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c` and is on the checked-in head.
The paragraph below is the 2026-10-28 record.

The 2026-10-28 pgschema advance adds benchmark **026** and leaves **021** /
**022** / **024** in place. The active set is now **021** / **022** /
**024** / **026**. The 2026-10-27 advance did not change that older set,
which was **021** / **022** / **024**. On that day `pg-toolbelt` `main` did
not move. The
previous pg-delta advance, from
`265af521e462577886ea6fdbb5777e1a23811cce` to
`6b82eff84dba925a176f0c6a78e5a16843885366` through merged PR
[#559](https://github.com/supabase/pg-toolbelt/pull/559), still edits only
`.github/CODEOWNERS`. On 2026-10-27, pgschema `main` moved through merged PRs
[#662](https://github.com/pgplex/pgschema/pull/662),
[#661](https://github.com/pgplex/pgschema/pull/661),
[#663](https://github.com/pgplex/pgschema/pull/663), and
[#664](https://github.com/pgplex/pgschema/pull/664). Open PR
[#645](https://github.com/pgplex/pgschema/pull/645) closed without merge;
[#663](https://github.com/pgplex/pgschema/pull/663) is the landed fix for
[#653](https://github.com/pgplex/pgschema/issues/653). Open pg-toolbelt PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) gained commit
`67793ef` on 2026-10-28. That commit edits
`src/frontends/settle-desired.ts` to pair respelled check names across a
table rename. It is still unmatched rename/respell work, and it is still
absent from the checked-in head. The earlier commit `a638ed1` was a merge
of current `main`. Merged PRs
[#550](https://github.com/supabase/pg-toolbelt/pull/550) and
[#556](https://github.com/supabase/pg-toolbelt/pull/556) remain in history:
the first fixes multi-parent `INHERITS`, partition-child index storage
options, and row-type `CHECK` folding, and the second moves `columnClause()`
into `tables.ts` while still appending `STORED`. Those changes leave the
`VIRTUAL` versus `STORED` distinction, the partition-child column-element
path, and the PG18 `NOT NULL ... NOT VALID` workflow open. Benchmark **025**
stays solved from merged PR
[#546](https://github.com/supabase/pg-toolbelt/pull/546); the same-table fold
guard in `src/plan/internal.ts` is now lines 783-797 (lines 779-793 before
merged PR [#555](https://github.com/supabase/pg-toolbelt/pull/555)). PR
[#662](https://github.com/pgplex/pgschema/pull/662) is now merged. pg-delta
already preserves `MATCH FULL` through verbatim constraint-definition
extraction and replay, with no dedicated scenario test or linked tracker yet,
so the scenario stays watch-only.
Open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) stays
open after partial coverage from merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553); open follow-up
[#554](https://github.com/supabase/pg-toolbelt/issues/554) did not move.
Exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
and `pgschema#653` still return no dedicated pg-toolbelt issue or PR, so
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
still only covers benchmarks **021** / **022**. Benchmarks **024** and
**026** still have no exact current pg-toolbelt issue or PR. On 2026-10-28
the open pgschema watch list had no uncovered parity candidate; the new
uncovered case that day was closed issue
[#639](https://github.com/pgplex/pgschema/issues/639), recorded as
benchmark **026**. On 2026-10-30 the open uncovered candidate is
[#674](https://github.com/pgplex/pgschema/issues/674).

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#670](https://github.com/pgplex/pgschema/issues/670),
[#672](https://github.com/pgplex/pgschema/issues/672),
[#673](https://github.com/pgplex/pgschema/issues/673), and
[#674](https://github.com/pgplex/pgschema/issues/674).
Closed on 2026-10-30 and recorded as **covered**:
[#677](https://github.com/pgplex/pgschema/issues/677).
Closed on 2026-10-27 and already in `review-memory.resolved` as **covered**:
[#638](https://github.com/pgplex/pgschema/issues/638) and
[#653](https://github.com/pgplex/pgschema/issues/653).
Closed on 2026-10-28 and moved out of the open watch list:
[#639](https://github.com/pgplex/pgschema/issues/639) (**not covered**,
benchmark **026**),
[#665](https://github.com/pgplex/pgschema/issues/665) (**covered**),
[#669](https://github.com/pgplex/pgschema/issues/669) (**not parity**), and
[#671](https://github.com/pgplex/pgschema/issues/671) (**not parity**).

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
- **#624** SQL function created before `ADD COLUMN` it depends on - **covered**
  in current pg-delta via the routine-plan `check_function_bodies = off`
  preamble plus existing SQL-body forward-reference coverage
- **#625** existing composite-type attribute changes are silently skipped -
  **covered** in current pg-delta via composite `typeAttribute` facts and
  `ALTER TYPE ... ADD ATTRIBUTE ... CASCADE` planning
- **#626** composite type creation runs before its required table - **covered**
  in current pg-delta via dependency extraction that resolves composite row-type
  edges back onto the owning table fact
- **#627** opt-in global-state roles / ownership umbrella (PR
  [#637](https://github.com/pgplex/pgschema/pull/637) closed without merge on
  2026-10-27; it had closed child issues **#628-#636**) - **not added as a new
  benchmark parity item in this repo**. This remains pgschema's separate
  explicit global-manifest surface;
  adjacent pg-delta role / owner work exists in open PR
  [#471](https://github.com/supabase/pg-toolbelt/pull/471) and open PR
  [#564](https://github.com/supabase/pg-toolbelt/pull/564). PR
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) closed unmerged
  on 2026-10-29, as did PR
  [#548](https://github.com/supabase/pg-toolbelt/pull/548), plus merged
  membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
  [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
  [#461](https://github.com/supabase/pg-toolbelt/pull/461), but exact duplicate
  search `pgschema#627` still returns no dedicated pg-toolbelt issue or PR
- **#638** mixed column-privilege rendering (`GRANT INSERT, UPDATE (cols)`) -
  **covered** in current pg-delta, and merged PR
  [#661](https://github.com/pgplex/pgschema/pull/661) is upstream catch-up.
  The issue is now closed:
  - `renderGrantSql()` renders column privileges as `PRIV (col), PRIV (col)`
  - `tests/column-grant-fidelity.test.ts` covers extracted table column grants
  - `src/frontends/sql-format/format-grant.test.ts` explicitly pins
    `GRANT SELECT (col), UPDATE (col) ...`
- **#639** partition bounds / attachment drift - **not covered** as of
  merged PR [#668](https://github.com/pgplex/pgschema/pull/668), benchmark
  **026**. Detection was already present (`partitionBound` and
  `parentTable` are `"replace"`). The landed plan is `DETACH PARTITION`
  then `ATTACH PARTITION`, which pg-delta does not emit. PR
  [#660](https://github.com/pgplex/pgschema/pull/660) had closed without
  merge on 2026-10-27; #668 is the landed fix
- **#665** mutually recursive SQL functions while `check_function_bodies`
  is on - **covered** by the routine-plan preamble
- **#669 / #670 / #672** online index replacement candidate names
  (`_pgschema_new`) - **not parity work for pg-delta**. #669 closed
  completed with no source change; #670 and #672 stay open. Open PR
  [#679](https://github.com/pgplex/pgschema/pull/679) (created
  2026-10-30, not merged) would close #670 by shortening a 63-byte
  `_pgschema_new` candidate. pg-delta does not use that temporary name
- **#671** apostrophes in quoted identifiers during desired-state
  qualification - closed `NOT_PLANNED`. **Not parity work for pg-delta**;
  `qid()` already quotes identifiers for plan output
- **#673** `INCLUDE` columns on PRIMARY KEY and UNIQUE constraints -
  **covered** in current pg-delta. Open pgschema PR
  [#676](https://github.com/pgplex/pgschema/pull/676) is not merged.
  `pg_get_constraintdef` is the constraint `def`, and create/fold emit
  that text verbatim
- **#674** comments on inherited partition constraints - **not covered**
  for a child comment that differs from its parent. Local constraint
  comments already use `COMMENT ON CONSTRAINT`. Inherited
  `conislocal = false` rows are skipped, so the child comment is never
  extracted. Draft only:
  [`docs/parity-issue-drafts-2026-10-30.md`](../docs/parity-issue-drafts-2026-10-30.md)
- **#677** function `COMMENT` lost across `DROP` + `CREATE` - **covered**.
  Closed by pgschema PR
  [#678](https://github.com/pgplex/pgschema/pull/678). pg-delta recreates
  unchanged comment children when the routine is replaced
- **#653** inherited partition-index name collisions during dump replay -
  **covered / avoided** in current pg-delta. Merged PR
  [#663](https://github.com/pgplex/pgschema/pull/663) closed the issue;
  [#645](https://github.com/pgplex/pgschema/pull/645) closed without merge.
  The same PR's partition-default fixture remains benchmark **021**:
  - `src/plan/rules/tables.ts` makes child `PARTITION OF` creation consume
    parent indexes plus parent PRIMARY KEY / UNIQUE constraints, so the
    standalone parent index exists before the child partition is created
  - constraint-backed indexes stay excluded in `src/extract/relations.ts`, so
    pg-delta does not re-emit the autonamed child primary-key index
  - `src/plan/partition-index-attach.test.ts` already covers child
    `CREATE INDEX` + `ATTACH PARTITION` plus parent-index rename / replacement
    behavior

The open uncovered parity candidate is now
[#674](https://github.com/pgplex/pgschema/issues/674) (inherited partition
constraint comments). It is drafted and not opened. Closed issue
[#639](https://github.com/pgplex/pgschema/issues/639) is benchmark **026**
and is **not covered**. The remaining active benchmarks **021** / **022**
still only have umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) as exact tracker
context, and benchmarks **024** and **026** still have no exact current
pg-toolbelt issue or PR. Open issue
[#673](https://github.com/pgplex/pgschema/issues/673) is **covered** through
verbatim `pg_get_constraintdef` replay. Benchmark
[#534](https://github.com/pgplex/pgschema/issues/534) stays **covered**
through merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546).
Closed issue [#665](https://github.com/pgplex/pgschema/issues/665) is
**covered** by the `check_function_bodies = off` preamble. Closed issue
[#653](https://github.com/pgplex/pgschema/issues/653) stays covered / avoided
through merged PR [#663](https://github.com/pgplex/pgschema/pull/663). The
global-state umbrella [#627](https://github.com/pgplex/pgschema/issues/627)
stays open after PR [#637](https://github.com/pgplex/pgschema/pull/637)
closed without merge and is still not a benchmark gap. Open issue
[#518](https://github.com/supabase/pg-toolbelt/issues/518) stays open after
partial coverage from merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553). Open follow-up
[#554](https://github.com/supabase/pg-toolbelt/issues/554) is still open.
Its `updatedAt` moved to `2026-10-28T11:36:22Z` with no comments; the title
is still the zero-arg IMMUTABLE generated-column apply failure and does
not close benchmark **022**. PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) merged on
2026-10-29 (`36ac91d3`) and is now the checked-in head. This
repository still has no local tracker issues.

## Recent closed-issue / tracker updates

On 2026-10-28, pgschema `main` advanced to
`36a38ff3c25db956ae8b5be2eee552d8bc69fb47`. Benchmark **026** is new.
Benchmarks **021**, **022**, **024**, and **025** keep their previous
verdicts. The notes below are the 2026-10-27 record.

No benchmark verdict changed in this refresh. `pg-toolbelt` `main` stayed at
`6b82eff84dba925a176f0c6a78e5a16843885366`. `pgschema` `main` advanced to
`8703c276c3ee4bab6d4e30b14e6e8982ace14b89` through merged PRs
[#662](https://github.com/pgplex/pgschema/pull/662),
[#661](https://github.com/pgplex/pgschema/pull/661),
[#663](https://github.com/pgplex/pgschema/pull/663), and
[#664](https://github.com/pgplex/pgschema/pull/664). Issues
[#638](https://github.com/pgplex/pgschema/issues/638) and
[#653](https://github.com/pgplex/pgschema/issues/653) closed and stay covered
in pg-delta. PR [#645](https://github.com/pgplex/pgschema/pull/645) closed
without merge. Open pg-toolbelt PR
[#558](https://github.com/supabase/pg-toolbelt/pull/558) did not update and
remains CI sharding. Merged PR
[#559](https://github.com/supabase/pg-toolbelt/pull/559) is already in the
checked-in/live head and only rewrites `.github/CODEOWNERS`. Merged PRs
[#550](https://github.com/supabase/pg-toolbelt/pull/550),
[#551](https://github.com/supabase/pg-toolbelt/pull/551),
[#556](https://github.com/supabase/pg-toolbelt/pull/556), and
[#557](https://github.com/supabase/pg-toolbelt/pull/557) remain in that head
from the 2026-10-23 advance. Merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553) remains the partial
coverage for open issue
[#518](https://github.com/supabase/pg-toolbelt/issues/518) on generated-column
and same-schema-type column order. The user-function `DEFAULT` case in that
issue stays open, and pgschema still has no matching column-order benchmark.
Open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554) records
the remaining generated-column chain failure, and open PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) is unmatched
rename/respell settlement with new commits on 2026-10-22. The prior verdict
change that still stands is:

- pgschema issue [#534](https://github.com/pgplex/pgschema/issues/534) /
  merged PR [#540](https://github.com/pgplex/pgschema/pull/540) now moves
  benchmark [025](025-self-referencing-fk-nonpk-unique-ordering.md) to
  **Solved in pg-delta**:
  - closed pg-toolbelt issue
    [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
    [#546](https://github.com/supabase/pg-toolbelt/pull/546) are now in the
    checked-in/live head
  - `packages/pg-delta/src/plan/internal.ts` now blocks export-time inline
    folds when a same-table dependency is emitted after `CREATE TABLE`
  - `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` now
    round-trips the exact export-reload scenario, and
    `packages/declarative-e2e/scenarios/self-fk-on-unique-index/` now covers
    the same shape through the declarative-e2e harness
- the remaining active benchmarked pg-toolbelt trackers are unchanged at the
  verdict level:
  - open umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still covers benchmarks **021** / **022**
  - closed issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
    and merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
    remain adjacent partition rewrite-risk context for benchmark **021**, but
    they do not touch `src/extract/relations.ts` or
    `src/plan/rules/tables.ts`
  - benchmark **024** still has no exact current pg-toolbelt issue or PR
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518)
  remains open. Merged PR
  [#553](https://github.com/supabase/pg-toolbelt/pull/553) now covers its
  generated-column and same-schema-type order cases on the checked-in/live
  head, and open issue
  [#554](https://github.com/supabase/pg-toolbelt/issues/554) tracks the
  zero-argument `IMMUTABLE` follow-up. Today's pgschema searches for
  `generated expression column order` and `zero-arg` returned `[]`
- merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is now
  in the checked-in/live head. It adds an export round-trip corpus gate plus
  three export fixes (multi-parent `INHERITS`, partition-child index storage
  options, and a row-type `CHECK` fold veto). Current pgschema keyword sweeps
  for `multi-parent`, `fillfactor`, and `row type` still find no open parity
  counterpart. One deferred corpus gap remains for sub-partition index
  options, recorded in pg-toolbelt
  `docs/roadmap/pg-delta-next-follow-ups.md`
- pg-toolbelt issues [#525](https://github.com/supabase/pg-toolbelt/issues/525)
  and [#544](https://github.com/supabase/pg-toolbelt/issues/544) still have no
  matching pgschema counterpart from the current `union alias` / `?column?` and
  `BETWEEN` / `nested AND` keyword searches
- merged PR [#549](https://github.com/supabase/pg-toolbelt/pull/549) plus open
  PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issues
  [#476](https://github.com/supabase/pg-toolbelt/issues/476) /
  [#339](https://github.com/supabase/pg-toolbelt/issues/339) are adjacent role
  / user-mapping work; today's pgschema keyword sweeps still only land on
  umbrella issue [#627](https://github.com/pgplex/pgschema/issues/627), which
  this repo continues to exclude from benchmark promotion
- merged PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) is now
  in the checked-in/live head and remains unmatched apply/search_path context:
  apply stays on `search_path = pg_catalog` and explains `42883` failures
- open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
  unmatched policy-withheld-prerequisite context and does not map to a current
  pgschema benchmark item
- pgschema PR [#662](https://github.com/pgplex/pgschema/pull/662)
  (`MATCH FULL` foreign keys) is now merged. Exact duplicate searches still
  found no linked pgschema issue or pg-toolbelt issue / PR, and pg-delta
  preserves the clause through verbatim `pg_get_constraintdef` extraction
  and verbatim `def` replay. The current tree still lacks a dedicated
  scenario test, so the scenario stays watch-only
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#653`, and `pgschema#638` still returned `[]`; keyword `"PARTITION OF"`,
  `"VIRTUAL" generated`, `"NOT NULL" "NOT VALID"`, `union alias`,
  `BETWEEN`, `nested AND`, `inherited partition index`, and the export
  column-order search terms still only surface the existing active tracker
  context or unmatched watch-only notes already recorded in this repo
- label-filtered dry-run `compare_issues.py` / `compare_resolved.py` still
  returned **0 open** and **0 resolved** issues, so manual unlabeled sweeps
  remain required
- previously screened pgschema verdicts remain unchanged at the parity level:
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain **not parity**;
  open issues [#598](https://github.com/pgplex/pgschema/issues/598),
  [#624](https://github.com/pgplex/pgschema/issues/624),
  [#625](https://github.com/pgplex/pgschema/issues/625),
  [#626](https://github.com/pgplex/pgschema/issues/626) remain **covered**
  in the 2026-10-27 record. On 2026-10-28,
  [#639](https://github.com/pgplex/pgschema/issues/639) closed and is
  benchmark **026** (**not covered**);
  closed issues [#638](https://github.com/pgplex/pgschema/issues/638) and
  [#653](https://github.com/pgplex/pgschema/issues/653) stay **covered** and
  now live under `review-memory.resolved`;
  the narrowed global-state umbrella [#627](https://github.com/pgplex/pgschema/issues/627)
  plus closed child issues **#628-#636** is still treated as **not added as a
  benchmark parity gap in this repo**; active resolved benchmarks
  [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501),
  [#534](https://github.com/pgplex/pgschema/issues/534), and
  [#564](https://github.com/pgplex/pgschema/issues/564) now remain
  **tracked** / **tracked** / **covered** / **not covered** respectively
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

## Upstream watch list

- 2026-10-28: checked-in/live `pgschema` sits at
  `36a38ff3c25db956ae8b5be2eee552d8bc69fb47` after merged PRs
  [#668](https://github.com/pgplex/pgschema/pull/668),
  [#667](https://github.com/pgplex/pgschema/pull/667), and
  [#666](https://github.com/pgplex/pgschema/pull/666). Checked-in/live
  `pg-toolbelt` is still
  `6b82eff84dba925a176f0c6a78e5a16843885366`. See
  [`docs/parity-refresh-2026-10-28.md`](../docs/parity-refresh-2026-10-28.md).
  The bullets below are the 2026-10-27 record.
- checked-in/live `pgschema` now sits at
  `8703c276c3ee4bab6d4e30b14e6e8982ace14b89`. The updated-since queries for
  `>=2026-10-26` closed issues
  [#638](https://github.com/pgplex/pgschema/issues/638) and
  [#653](https://github.com/pgplex/pgschema/issues/653) and merged PRs
  [#661](https://github.com/pgplex/pgschema/pull/661),
  [#662](https://github.com/pgplex/pgschema/pull/662),
  [#663](https://github.com/pgplex/pgschema/pull/663), and
  [#664](https://github.com/pgplex/pgschema/pull/664). The open-PR query
  returned `[]`. PR [#645](https://github.com/pgplex/pgschema/pull/645)
  closed without merge; [#663](https://github.com/pgplex/pgschema/pull/663)
  is the landed fix for
  [#653](https://github.com/pgplex/pgschema/issues/653). Merged PR
  [#662](https://github.com/pgplex/pgschema/pull/662) is the `MATCH FULL`
  fix and stays watch-only on the pg-delta side. PR
  [#660](https://github.com/pgplex/pgschema/pull/660) closed without merge
  while issue [#639](https://github.com/pgplex/pgschema/issues/639) stays
  open and covered. PR [#661](https://github.com/pgplex/pgschema/pull/661)
  merged as upstream catch-up for already-covered
  [#638](https://github.com/pgplex/pgschema/issues/638)
- checked-in/live `pg-toolbelt` still sits at
  `6b82eff84dba925a176f0c6a78e5a16843885366`. The updated-since queries for
  `>=2026-10-26` surfaced open issue
  [#518](https://github.com/supabase/pg-toolbelt/issues/518) (unassigned,
  `updatedAt` `2026-10-26T15:10:58Z`, no new comment), open PR
  [#506](https://github.com/supabase/pg-toolbelt/pull/506) (design comment,
  no new commits), and new open PR
  [#560](https://github.com/supabase/pg-toolbelt/pull/560) (a
  `@supabase/pg-checks` spike, not schema-diff parity). No merged PRs and no
  closed issues landed in that window. Direct views still show open issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) and
  [#554](https://github.com/supabase/pg-toolbelt/issues/554), plus open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#493](https://github.com/supabase/pg-toolbelt/pull/493),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#555](https://github.com/supabase/pg-toolbelt/pull/555), and
  [#558](https://github.com/supabase/pg-toolbelt/pull/558) at their prior
  timestamps. PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) still have their
  latest commits from September
- the nearby benchmark-relevant pg-toolbelt issue / PR landscape therefore now
  reads:
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**; exact searches for
    `pgschema#499` and `pgschema#501` still return no dedicated issue or PR
  - open issue [#502](https://github.com/supabase/pg-toolbelt/issues/502)
    plus closed issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
    and merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
    remain adjacent partition follow-up / rewrite-risk context for benchmark
    **021**; none of them changes child-local `PARTITION OF` column-element
    modeling
  - closed issue [#543](https://github.com/supabase/pg-toolbelt/issues/543)
    plus merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546)
    now solve benchmark **025** /
    pgschema [#534](https://github.com/pgplex/pgschema/issues/534) on the
    checked-in/live head, even though an exact `pgschema#534` text search still
    returns `[]`
  - issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) remains
    open. Merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553)
    now covers the generated-column and same-schema-type slices on the
    checked-in/live head, and open issue
    [#554](https://github.com/supabase/pg-toolbelt/issues/554) tracks the
    zero-argument `IMMUTABLE` follow-up. Today's pgschema searches for
    `generated expression column order` and `zero-arg` returned `[]`. Open PR
    [#555](https://github.com/supabase/pg-toolbelt/pull/555) is unmatched
    rename/respell settlement and is not in the checked-in/live head
  - merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is now
    in the checked-in/live head as unmatched export-roundtrip fidelity work.
    Its remaining known gap is sub-partition index storage options, which
    Postgres rejects via `ALTER INDEX SET/RESET` on partitioned indexes
  - issues [#525](https://github.com/supabase/pg-toolbelt/issues/525) and
    [#544](https://github.com/supabase/pg-toolbelt/issues/544) remain
    unmatched upstream context
  - issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus open
    PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
    [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus merged PR
    [#549](https://github.com/supabase/pg-toolbelt/pull/549) are adjacent role
    / user-mapping context around explicit global-state management; current
    pgschema keyword searches still only land on
    [#627](https://github.com/pgplex/pgschema/issues/627) and do not change the
    repo's benchmark scope
  - merged PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) is now
    in the checked-in/live head and remains unmatched apply/search_path
    context
  - open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
    unmatched policy-suppression context. A 2026-10-26 comment questions the
    skip-machinery approach; the head is still `c284eb4` from 2026-10-22.
    Today's pgschema keyword sweeps still found no counterpart
  - exact `"MATCH FULL"` / `confmatchtype` duplicate searches still return no
    pg-toolbelt issue or PR. Merged pgschema PR
    [#662](https://github.com/pgplex/pgschema/pull/662) is upstream catch-up:
    current pg-delta already replays the clause from
    `pg_get_constraintdef`, and the missing dedicated scenario test keeps
    the item watch-only
  - exact `pgschema#653` and `inherited partition index` searches still return
    no pg-toolbelt issue or PR. Merged pgschema PR
    [#663](https://github.com/pgplex/pgschema/pull/663) closed the issue.
    Current pg-delta still avoids the collision through partition-index
    attach planning and child `PARTITION OF` create ordering
  - historical PR [#174](https://github.com/supabase/pg-toolbelt/pull/174)
    remains legacy-engine-only context for benchmark **024**; exact
    `pgschema#564` searches still return no current pg-toolbelt issue or PR
  - the broader global-state cluster is still centered on open umbrella issue
    [#627](https://github.com/pgplex/pgschema/issues/627) after PR
    [#637](https://github.com/pgplex/pgschema/pull/637) closed without merge
    and issues **#628-#636** stayed closed. It is still not being promoted
    into new benchmark gap docs in this repo. Adjacent pg-delta global-state
    work now also includes issue
    [#476](https://github.com/supabase/pg-toolbelt/issues/476)
    / PR [#548](https://github.com/supabase/pg-toolbelt/pull/548), issue
    [#339](https://github.com/supabase/pg-toolbelt/issues/339) / PR
    [#549](https://github.com/supabase/pg-toolbelt/pull/549), merged PR
    [#551](https://github.com/supabase/pg-toolbelt/pull/551), and older open
    PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
    [#493](https://github.com/supabase/pg-toolbelt/pull/493) alongside merged
    role / membership fixes
    [#117](https://github.com/supabase/pg-toolbelt/pull/117),
    [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
    [#461](https://github.com/supabase/pg-toolbelt/pull/461)
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
