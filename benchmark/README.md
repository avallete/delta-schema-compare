# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-08)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `8a62438b03300c1922cb04b292d2140fcc694b25`
- checked-in/live `repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`

> The 2026-10-08 refresh advances checked-in/live `repos/pg-toolbelt` from
> `5e7c43674ab55f297702d18830489ac0008c019d` to `8a62438b03300c1922cb04b292d2140fcc694b25` through merged PRs
> [#515](https://github.com/supabase/pg-toolbelt/pull/515) and
> [#520](https://github.com/supabase/pg-toolbelt/pull/520), while
> checked-in/live `repos/pgschema` remains
> `580f4040d0f3c1bfad1497918200c9c1f638a020`
>
> - `gh search issues --repo pgplex/pgschema --updated '>=2026-10-07'`
>   surfaced open issue
>   [#624](https://github.com/pgplex/pgschema/issues/624)
> - the matching `--include-prs` query returned the same single issue, and
>   open pgschema PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
>   [#622](https://github.com/pgplex/pgschema/pull/622) remain unchanged since
>   2026-09-20 / 2026-09-24
> - pgschema issue [#624](https://github.com/pgplex/pgschema/issues/624)
>   remains **covered** in current pg-delta: routine-touching plans still emit
>   `SET check_function_bodies = off;`
>   (`src/plan/preamble.ts`, `src/plan/preamble.test.ts`,
>   `src/plan/render-sql.test.ts`), and the updated issue body now explicitly
>   calls out the same workaround; exact duplicate search `pgschema#624` still
>   returned no pg-toolbelt issue or PR
> - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-07'`
>   surfaced merged PRs
>   [#515](https://github.com/supabase/pg-toolbelt/pull/515) and
>   [#520](https://github.com/supabase/pg-toolbelt/pull/520), open PRs
>   [#514](https://github.com/supabase/pg-toolbelt/pull/514),
>   [#522](https://github.com/supabase/pg-toolbelt/pull/522),
>   [#527](https://github.com/supabase/pg-toolbelt/pull/527), and
>   [#528](https://github.com/supabase/pg-toolbelt/pull/528), open issues
>   [#510](https://github.com/supabase/pg-toolbelt/issues/510),
>   [#521](https://github.com/supabase/pg-toolbelt/issues/521),
>   [#523](https://github.com/supabase/pg-toolbelt/issues/523),
>   [#524](https://github.com/supabase/pg-toolbelt/issues/524),
>   [#525](https://github.com/supabase/pg-toolbelt/issues/525), and
>   [#526](https://github.com/supabase/pg-toolbelt/issues/526), plus closed
>   issue [#517](https://github.com/supabase/pg-toolbelt/issues/517)
> - direct inspection of those updated pg-toolbelt items plus
>   `git -C repos/pg-toolbelt diff --name-only
>   5e7c43674ab55f297702d18830489ac0008c019d..8a62438b03300c1922cb04b292d2140fcc694b25 -- packages/pg-delta/src/extract/relations.ts
>   packages/pg-delta/src/plan/rules/tables.ts
>   packages/pg-delta/src/plan/rules/helpers.ts`
>   shows the active benchmark paths are unchanged; the merged code lands in
>   declarative-e2e infrastructure plus declarative public-schema revoke
>   export, and the open work is separate declarative settle / export / test
>   coverage rather than benchmark duplicates
> - open pg-toolbelt umbrella issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332) and adjacent
>   partition follow-up
>   [#502](https://github.com/supabase/pg-toolbelt/issues/502) remain the only
>   benchmark-adjacent tracker context
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
  - the 2026-10-07 pg-delta delta only touches OrioleDB assumed-extension
    seeding / dependency resolution, Supabase policy handling, and release
    metadata; none of those changes preserves generated kind, so umbrella issue
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
  - the 2026-10-07 pg-delta delta only touches OrioleDB assumed-extension
    seeding / dependency resolution, Supabase policy handling, and release
    metadata; there is still no exact current pg-toolbelt issue or PR for this
    benchmark

Because today's refresh advances checked-in/live `pg-toolbelt` through merged
PRs [#515](https://github.com/supabase/pg-toolbelt/pull/515) and
[#520](https://github.com/supabase/pg-toolbelt/pull/520) while leaving the
active benchmark source paths untouched, source rechecks on the current head
still find `a.attislocal` in `relations.ts`, generated-column kind still
collapsed to expression presence plus a hard-coded `... STORED` renderer, and
PG18 table `contype = 'n'` rows still kept out of diff-visible facts. Exact
duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`, and
`pgschema#624` still return no dedicated pg-toolbelt issue or PR; keyword
searches for `"PARTITION OF"` still surface umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332), adjacent follow-up
[#502](https://github.com/supabase/pg-toolbelt/issues/502), merged partition
PRs [#501](https://github.com/supabase/pg-toolbelt/pull/501),
[#503](https://github.com/supabase/pg-toolbelt/pull/503), and
[#504](https://github.com/supabase/pg-toolbelt/pull/504), plus declarative
settling PR [#514](https://github.com/supabase/pg-toolbelt/pull/514) as
separate context; `"VIRTUAL" generated` still surfaces live umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) plus historical
merged PRs [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
[#299](https://github.com/supabase/pg-toolbelt/pull/299); and
`"NOT NULL" "NOT VALID"` with `--include-prs` still surfaces merged
domain-only PR [#484](https://github.com/supabase/pg-toolbelt/pull/484)
rather than an exact table-column PG18 validation tracker. Open pg-toolbelt
issues [#523](https://github.com/supabase/pg-toolbelt/issues/523),
[#524](https://github.com/supabase/pg-toolbelt/issues/524),
[#525](https://github.com/supabase/pg-toolbelt/issues/525), and
[#526](https://github.com/supabase/pg-toolbelt/issues/526) plus open PRs
[#514](https://github.com/supabase/pg-toolbelt/pull/514),
[#527](https://github.com/supabase/pg-toolbelt/pull/527), and
[#528](https://github.com/supabase/pg-toolbelt/pull/528) are separate
declarative settle / export / test work, while open pgschema issue
[#624](https://github.com/pgplex/pgschema/issues/624) remains covered through
the existing routine-plan `check_function_bodies = off` behavior. Umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) therefore
still only covers benchmarks **021** / **022**, benchmark **024** still has
no exact current pg-toolbelt issue or PR, the focused 2026-08-14 runtime
observations for benchmarks **021** / **022** remain the latest direct runtime
evidence, and benchmark **024** remains source-level not covered on the new
current head.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#623](https://github.com/pgplex/pgschema/issues/623), and
[#624](https://github.com/pgplex/pgschema/issues/624).

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
- **#624** SQL function created before `ADD COLUMN` it depends on -
  **covered** in current pg-delta:
  - `src/plan/preamble.ts` deliberately keeps `check_function_bodies = off`
    for routine-touching plans because quoted SQL/plpgsql bodies do not record
    body-dependency edges
  - `src/plan/preamble.test.ts` and `src/plan/render-sql.test.ts` assert that
    routine plans retain and emit that preamble
  - `corpus/function-ops--sql-body-cross-reference/b.sql` already covers the
    same forward-referencing SQL-language function-body pattern
  - exact duplicate search `pgschema#624` still returns no dedicated
    pg-toolbelt issue or PR, so no new tracker issue is needed

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
exact tracker context, benchmark **024** still has no exact current
pg-toolbelt issue or PR, and the current pg-toolbelt head now reflects merged
PRs [#515](https://github.com/supabase/pg-toolbelt/pull/515) and
[#520](https://github.com/supabase/pg-toolbelt/pull/520). Direct inspection of
the new open pg-toolbelt issues
[#523](https://github.com/supabase/pg-toolbelt/issues/523),
[#524](https://github.com/supabase/pg-toolbelt/issues/524),
[#525](https://github.com/supabase/pg-toolbelt/issues/525), and
[#526](https://github.com/supabase/pg-toolbelt/issues/526) plus open PRs
[#514](https://github.com/supabase/pg-toolbelt/pull/514),
[#527](https://github.com/supabase/pg-toolbelt/pull/527), and
[#528](https://github.com/supabase/pg-toolbelt/pull/528) shows declarative
settle / export / test work rather than new parity coverage or duplicates.
Open pgschema issue [#624](https://github.com/pgplex/pgschema/issues/624)
remains covered through the existing routine-plan preamble behavior rather
than a new tracker gap. This repository still has no local tracker issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-07'`
  surfaced only open issue [#624](https://github.com/pgplex/pgschema/issues/624);
  the matching `--include-prs` query returned the same single issue; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain open without new
  updates
- issue [#624](https://github.com/pgplex/pgschema/issues/624) remains covered
  by current pg-delta's routine-plan preamble strategy
  (`check_function_bodies = off`), the updated issue body now explicitly notes
  the same workaround, and exact duplicate search `pgschema#624` still
  returned `[]`
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-07'`
  surfaced merged PRs [#515](https://github.com/supabase/pg-toolbelt/pull/515)
  and [#520](https://github.com/supabase/pg-toolbelt/pull/520), open PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514),
  [#522](https://github.com/supabase/pg-toolbelt/pull/522),
  [#527](https://github.com/supabase/pg-toolbelt/pull/527), and
  [#528](https://github.com/supabase/pg-toolbelt/pull/528), open issues
  [#510](https://github.com/supabase/pg-toolbelt/issues/510),
  [#521](https://github.com/supabase/pg-toolbelt/issues/521),
  [#523](https://github.com/supabase/pg-toolbelt/issues/523),
  [#524](https://github.com/supabase/pg-toolbelt/issues/524),
  [#525](https://github.com/supabase/pg-toolbelt/issues/525), and
  [#526](https://github.com/supabase/pg-toolbelt/issues/526), plus closed
  issue [#517](https://github.com/supabase/pg-toolbelt/issues/517)
- direct inspection of updated pg-toolbelt work plus
  `git -C repos/pg-toolbelt diff --name-only 5e7c43674ab55f297702d18830489ac0008c019d..8a62438b03300c1922cb04b292d2140fcc694b25`
  showed only declarative-e2e infrastructure,
  `src/frontends/export-sql-files.ts`, `src/frontends/schema-export.ts`,
  `src/policy/policy.ts`, and related tests changed; the active benchmark
  paths `src/extract/relations.ts`, `src/plan/rules/tables.ts`, and
  `src/plan/rules/helpers.ts` stayed unchanged
- exact duplicate searches for `pgschema#499`, `pgschema#501`, and
  `pgschema#564` still returned `[]`; `pgschema#624` also returned `[]`;
  keyword searches for `"PARTITION OF"` and `"VIRTUAL" generated` still
  surfaced only existing umbrella / adjacent context, while
  `"NOT NULL" "NOT VALID" --include-prs` still only surfaced historical
  domain-only PR [#484](https://github.com/supabase/pg-toolbelt/pull/484)
- the checked-in/live pg-toolbelt head advanced to
  `8a62438b03300c1922cb04b292d2140fcc694b25`, but the active gap source paths stayed unchanged
- previously screened pgschema verdicts remain unchanged: open issue
  [#598](https://github.com/pgplex/pgschema/issues/598) remains **covered**,
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597), and
  [#623](https://github.com/pgplex/pgschema/issues/623) remain **not parity**,
  open issue [#624](https://github.com/pgplex/pgschema/issues/624) remains
  **covered**, closed issues
  [#599](https://github.com/pgplex/pgschema/issues/599),
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
  `580f4040d0f3c1bfad1497918200c9c1f638a020`; the updated-since issue query
  surfaced open issue [#624](https://github.com/pgplex/pgschema/issues/624),
  the matching `--include-prs` query returned the same single issue, and open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain in flight without
  new updates since 2026-09-20 / 2026-09-24
- checked-in/live `pg-toolbelt` now sits at
  `8a62438b03300c1922cb04b292d2140fcc694b25`, which comes from merged PRs
  [#515](https://github.com/supabase/pg-toolbelt/pull/515) and
  [#520](https://github.com/supabase/pg-toolbelt/pull/520); the updated-since
  query for `>=2026-10-07` surfaced merged PRs
  [#515](https://github.com/supabase/pg-toolbelt/pull/515) and
  [#520](https://github.com/supabase/pg-toolbelt/pull/520), open PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514),
  [#522](https://github.com/supabase/pg-toolbelt/pull/522),
  [#527](https://github.com/supabase/pg-toolbelt/pull/527), and
  [#528](https://github.com/supabase/pg-toolbelt/pull/528), open issues
  [#510](https://github.com/supabase/pg-toolbelt/issues/510),
  [#521](https://github.com/supabase/pg-toolbelt/issues/521),
  [#523](https://github.com/supabase/pg-toolbelt/issues/523),
  [#524](https://github.com/supabase/pg-toolbelt/issues/524),
  [#525](https://github.com/supabase/pg-toolbelt/issues/525), and
  [#526](https://github.com/supabase/pg-toolbelt/issues/526), plus closed
  issue [#517](https://github.com/supabase/pg-toolbelt/issues/517), but the
  only new merged code lands in declarative-e2e infrastructure plus
  declarative public-schema revoke export rather than the active benchmark
  source paths
- the nearby benchmark-relevant pg-toolbelt issue/PR landscape remains
  unchanged, and so does the parity mapping:
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**; exact searches for
    `pgschema#499` and `pgschema#501` still return no dedicated issue or PR
  - open issue [#502](https://github.com/supabase/pg-toolbelt/issues/502)
    remains the over-destructive partition-tree follow-up for benchmark
    **021**, and keyword `"PARTITION OF" --include-prs` searches still surface
    issue [#502](https://github.com/supabase/pg-toolbelt/issues/502), issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332), open PR
    [#514](https://github.com/supabase/pg-toolbelt/pull/514), and merged
    partition PRs [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    [#503](https://github.com/supabase/pg-toolbelt/pull/503), and
    [#504](https://github.com/supabase/pg-toolbelt/pull/504)
  - historical PR [#174](https://github.com/supabase/pg-toolbelt/pull/174)
    remains legacy-engine-only context for benchmark **024**; exact
    `pgschema#564` searches still return no current pg-toolbelt issue or PR,
    while keyword `"NOT NULL" "NOT VALID" --include-prs` still surfaces
    merged domain-only PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484) as adjacent
    historical context rather than an exact tracker for that workflow
  - open pgschema issue
    [#624](https://github.com/pgplex/pgschema/issues/624) has no dedicated
    pg-toolbelt issue or PR because current routine plans already disable
    function-body validation through `check_function_bodies = off`
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
