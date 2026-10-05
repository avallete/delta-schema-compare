# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-05)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `6845a0beb646cec0bcbf894cec99cbcae2567fc6`
- checked-in/live `repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`

> The 2026-10-05 refresh keeps both checked-in/live heads unchanged from the
> 2026-10-04 snapshot:
> - `repos/pg-toolbelt` remains
>   `6845a0beb646cec0bcbf894cec99cbcae2567fc6`, which still comes from merged
>   PR [#508](https://github.com/supabase/pg-toolbelt/pull/508) while open
>   release PR [#509](https://github.com/supabase/pg-toolbelt/pull/509)
>   remains unmerged
> - `repos/pgschema` remains
>   `580f4040d0f3c1bfad1497918200c9c1f638a020`
>
> - `gh search issues --repo pgplex/pgschema --updated '>=2026-10-04'`
>   returned `[]`, and the matching `--include-prs` query also returned `[]`
> - open pgschema PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
>   [#622](https://github.com/pgplex/pgschema/pull/622) remain in flight
>   without new updates since 2026-09-20 / 2026-09-24
> - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-04'`
>   surfaced open issue
>   [#510](https://github.com/supabase/pg-toolbelt/issues/510), closed PR
>   [#511](https://github.com/supabase/pg-toolbelt/pull/511), and open PR
>   [#512](https://github.com/supabase/pg-toolbelt/pull/512)
> - direct inspection shows #510 / #511 are trigger `WHEN` row-comparison
>   convergence work and #512 is grouped-export column-grant ordering; none
>   touches the active benchmark paths
> - open pg-toolbelt umbrella issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332), adjacent
>   partition follow-up
>   [#502](https://github.com/supabase/pg-toolbelt/issues/502), and release PR
>   [#509](https://github.com/supabase/pg-toolbelt/pull/509) remain unchanged
>   since 2026-09-29 / 2026-09-29 / 2026-10-02
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
>   returned `[]`
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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470), [#480](https://github.com/supabase/pg-toolbelt/pull/480), and [#488](https://github.com/supabase/pg-toolbelt/pull/488) (merged), [#501](https://github.com/supabase/pg-toolbelt/pull/501) (merged partition-key retype), and [#504](https://github.com/supabase/pg-toolbelt/pull/504) (merged dependency-edge repair) | **Tracked (umbrella thread only)** |
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
    merged PR [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    merged stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    and merged PR [#504](https://github.com/supabase/pg-toolbelt/pull/504)
    sharpen nearby partition-key / dependency-edge behavior, but PR #504's own
    deferrals still call out unmodeled partition-level default overrides
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - the 2026-10-02 pg-delta delta only touches license, README, and package
    metadata; none of those changes preserves generated kind, so umbrella
    issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains
    the only tracker context
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
  - merged PR [#508](https://github.com/supabase/pg-toolbelt/pull/508) and
    open release PR [#509](https://github.com/supabase/pg-toolbelt/pull/509)
    stay outside PG18 table-column nullability modeling, and there is still
    no exact current pg-toolbelt issue or PR for this benchmark

Because today's refresh kept both checked-in/live heads unchanged from the
2026-10-04 refresh, source rechecks on the current head still find
`a.attislocal` in `relations.ts`, generated-column kind still collapsed to
expression presence plus a hard-coded `... STORED` renderer, and PG18 table
`contype = 'n'` rows still kept out of diff-visible facts. The only newly
updated pg-toolbelt items since 2026-10-04 are issue
[#510](https://github.com/supabase/pg-toolbelt/issues/510), closed PR
[#511](https://github.com/supabase/pg-toolbelt/pull/511), and open PR
[#512](https://github.com/supabase/pg-toolbelt/pull/512), which stay in
trigger convergence and grouped-export grant ordering rather than the active
gap paths. Exact duplicate searches for `pgschema#499`, `pgschema#501`, and
`pgschema#564` still return no dedicated pg-toolbelt issue or PR; keyword
searches for `"PARTITION OF"` still only surface issues
[#332](https://github.com/supabase/pg-toolbelt/issues/332) and
[#502](https://github.com/supabase/pg-toolbelt/issues/502), `"VIRTUAL"
generated` still only surfaces issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332), and `"NOT NULL"
"NOT VALID"` still returns `[]`. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) therefore still
only covers benchmarks **021** / **022**, benchmark **024** still has no exact
current pg-toolbelt issue or PR, the focused 2026-08-14 runtime observations
for benchmarks **021** / **022** remain the latest direct runtime evidence,
and benchmark **024** remains source-level not covered on the unchanged
current heads.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598), and
[#623](https://github.com/pgplex/pgschema/issues/623).

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
- **#623** publish release checksums - **not parity work for pg-delta**;
  release-asset verification is outside pg-delta's schema-diff scope

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
exact tracker context, benchmark **024** still has no exact current
pg-toolbelt issue or PR, and the current pg-toolbelt head still reflects
merged PR [#508](https://github.com/supabase/pg-toolbelt/pull/508) plus open
release PR [#509](https://github.com/supabase/pg-toolbelt/pull/509), neither
of which touches the active source paths. This repository still has no local
tracker issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-04'` and the
  matching `--include-prs` query both returned `[]`; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain open without new
  updates
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-04'`
  surfaced open issue
  [#510](https://github.com/supabase/pg-toolbelt/issues/510), closed PR
  [#511](https://github.com/supabase/pg-toolbelt/pull/511), and open PR
  [#512](https://github.com/supabase/pg-toolbelt/pull/512)
- direct inspection showed #510 / #511 are trigger `WHEN` row-comparison
  convergence work and #512 is grouped-export column-grant ordering rather
  than duplicates of benchmarks **021**, **022**, or **024**;
  open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332), open
  issue [#502](https://github.com/supabase/pg-toolbelt/issues/502), and open
  release PR [#509](https://github.com/supabase/pg-toolbelt/pull/509) remain
  the only benchmark-adjacent pg-toolbelt tracker context
- exact duplicate searches for `pgschema#499`, `pgschema#501`, and
  `pgschema#564` still returned `[]`; keyword searches for `"PARTITION OF"`,
  `"VIRTUAL" generated`, and `"NOT NULL" "NOT VALID"` likewise surfaced no new
  exact tracker candidates
- the checked-in/live pg-toolbelt head stayed on
  `6845a0beb646cec0bcbf894cec99cbcae2567fc6`, so the active gap source paths
  stayed unchanged
- previously screened pgschema verdicts remain unchanged: open issue
  [#598](https://github.com/pgplex/pgschema/issues/598) remains **covered**,
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597), and
  [#623](https://github.com/pgplex/pgschema/issues/623) remain **not parity**,
  closed issues [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602),
  [#603](https://github.com/pgplex/pgschema/issues/603), and
  [#606](https://github.com/pgplex/pgschema/issues/606) remain **covered**, and
  closed issues [#596](https://github.com/pgplex/pgschema/issues/596) and
  [#607](https://github.com/pgplex/pgschema/issues/607) remain
  **not parity work**
- **#564** safer `NOT NULL` additions / PG18 native validation workflow remains
  **not covered** in current pg-delta as benchmark **024**
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`
- there are still no local tracker issues in this repository

## Upstream watch list

- checked-in/live `pgschema` remains at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`; the updated-since issue and PR
  queries both returned `[]`, and open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain in flight without
  new updates since 2026-09-20 / 2026-09-24
- checked-in/live `pg-toolbelt` remains at
  `6845a0beb646cec0bcbf894cec99cbcae2567fc6`, which still comes from merged PR
  [#508](https://github.com/supabase/pg-toolbelt/pull/508); the updated-since
  query for `>=2026-10-04` surfaced issue
  [#510](https://github.com/supabase/pg-toolbelt/issues/510), closed PR
  [#511](https://github.com/supabase/pg-toolbelt/pull/511), and open PR
  [#512](https://github.com/supabase/pg-toolbelt/pull/512), but none of those
  tickets touches the active benchmark source paths; open release PR
  [#509](https://github.com/supabase/pg-toolbelt/pull/509) still tracks
  `@supabase/pg-delta@1.0.0-alpha.57`
- the nearby benchmark-relevant pg-toolbelt issue/PR landscape remains
  unchanged, and so does the parity mapping:
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**; exact searches for
    `pgschema#499` and `pgschema#501` still return no dedicated issue or PR
  - open issue [#502](https://github.com/supabase/pg-toolbelt/issues/502)
    remains the over-destructive partition-tree follow-up for benchmark
    **021**, and keyword `"PARTITION OF"` searches still only surface issues
    [#502](https://github.com/supabase/pg-toolbelt/issues/502) and
    [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  - historical PR [#174](https://github.com/supabase/pg-toolbelt/pull/174)
    remains legacy-engine-only context for benchmark **024**; exact
    `pgschema#564` and keyword `"NOT NULL" "NOT VALID"` searches still return
    no current pg-toolbelt issue or PR for that workflow
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
