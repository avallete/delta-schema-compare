# PostgreSQL 18 `VIRTUAL` generated columns

> pgschema issue [#501](https://github.com/pgplex/pgschema/issues/501) (closed), fixed by [pgschema#503](https://github.com/pgplex/pgschema/pull/503)

## Context

## Refresh note (2026-10-08)

This recheck advances checked-in/live `pg-delta` from
`5e7c43674ab55f297702d18830489ac0008c019d` to `8a62438b03300c1922cb04b292d2140fcc694b25` through merged PRs
[#515](https://github.com/supabase/pg-toolbelt/pull/515) and
[#520](https://github.com/supabase/pg-toolbelt/pull/520), while checked-in/live
`pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream activity still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-07'` and the
  matching `--include-prs` query both surfaced only open issue
  [#624](https://github.com/pgplex/pgschema/issues/624), whose updated body now
  explicitly calls out the same `check_function_bodies=off` workaround that
  current pg-delta already applies; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain unchanged since
  2026-09-20 / 2026-09-24
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
  [#526](https://github.com/supabase/pg-toolbelt/issues/526), plus closed issue
  [#517](https://github.com/supabase/pg-toolbelt/issues/517)
- `git -C repos/pg-toolbelt diff --name-only
  5e7c43674ab55f297702d18830489ac0008c019d..8a62438b03300c1922cb04b292d2140fcc694b25 -- packages/pg-delta/src/extract/relations.ts
  packages/pg-delta/src/plan/rules/helpers.ts
  packages/pg-delta/src/plan/rules/tables.ts` returned no paths; the new
  merged code lands in declarative-e2e infrastructure plus declarative public-
  schema revoke export, not the active generated-kind extract / render path
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated`, but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- direct exact searches for `pgschema#501` still return no dedicated
  pg-toolbelt issue or PR. Keyword `"VIRTUAL" generated --include-prs`
  searches still surface live umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus historical
  merged PRs [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
  [#299](https://github.com/supabase/pg-toolbelt/pull/299), but there is still
  no exact current tracker for the generated-kind distinction itself

The focused 2026-08-14 runtime observation therefore still stands: pg-delta
serializes the generated column as `... STORED`, collapses away the
PostgreSQL 18 `VIRTUAL` keyword, and still lets the proof loop return
`proofOk: true` with zero drift afterward. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

pgschema issue #501 reports that PostgreSQL 18 `VIRTUAL` generated columns
were being rewritten into invalid non-generated SQL during pgschema's plan
output. pg-delta does not share that exact desired-state SQL rewrite path,
but the user-visible parity gap still exists: current pg-delta does not
preserve the generated-column kind and collapses PostgreSQL's
`VIRTUAL` versus `STORED` distinction away.

That means pg-delta can still lose the distinction between `VIRTUAL` and
`STORED` generated columns even though it avoids the precise upstream bug
mechanism. This benchmark tracks the now-resolved upstream scenario after
pgschema merged its fix on `main`, while current pg-delta still lacks exact
coverage.

## Refresh note (2026-10-02)

This recheck advances checked-in/live `pg-delta` from
`8154463671f8637d5a7a9b65134526fa3eb06b84` to
`6845a0beb646cec0bcbf894cec99cbcae2567fc6` through merged PR
[#508](https://github.com/supabase/pg-toolbelt/pull/508), while checked-in/live
`pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream delta still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-01'`
  and
  `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-01'`
  both returned `[]`, so there is no new pgschema-side generated-column delta;
  open PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain in flight
  unchanged since 2026-09-20 / 2026-09-24
- `git -C repos/pg-toolbelt diff --name-only
  8154463671f8637d5a7a9b65134526fa3eb06b84..6845a0beb646cec0bcbf894cec99cbcae2567fc6`
  only touches `LICENSE`, `README.md`, and package metadata; none of
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` or
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` changed on
  the new checked-in/live head
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only tracker context; there is still no exact current
  pg-toolbelt issue or PR for this scenario

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Benchmark 022 therefore remains **behaviorally uncovered** with only
**umbrella-thread tracker context**.

## Refresh note (2026-10-01)

This recheck advances checked-in/live `pg-delta` from
`524c04f3c1cbd4290630e0a5ed87c15ca86663b2` to
`8154463671f8637d5a7a9b65134526fa3eb06b84` through merged PRs
[#500](https://github.com/supabase/pg-toolbelt/pull/500),
[#501](https://github.com/supabase/pg-toolbelt/pull/501),
[#504](https://github.com/supabase/pg-toolbelt/pull/504), and release PR
[#507](https://github.com/supabase/pg-toolbelt/pull/507), while checked-in/live
`pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream delta still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-09-30'`
  surfaced only open issue
  [#623](https://github.com/pgplex/pgschema/issues/623), which is a release
  checksums request unrelated to generated columns, and no pgschema PRs were
  updated in that window
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- the 2026-10-01 pg-delta delta lands in partition-key replacement,
  dependency-edge resolution, pg-topo range-type support, and release
  packaging; none of those changes preserves generated kind
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only tracker context; there is still no exact current
  pg-toolbelt issue or PR for this scenario

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, so benchmark 022 remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-30)

This recheck advances checked-in/live `pg-delta` from
`e17c45925c3ddbf660dfb13c51029b605bcee448` to
`524c04f3c1cbd4290630e0a5ed87c15ca86663b2` through merged PRs
[#496](https://github.com/supabase/pg-toolbelt/pull/496),
[#495](https://github.com/supabase/pg-toolbelt/pull/495),
[#478](https://github.com/supabase/pg-toolbelt/pull/478),
[#473](https://github.com/supabase/pg-toolbelt/pull/473), and release PR
[#505](https://github.com/supabase/pg-toolbelt/pull/505), while checked-in/live
`pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream delta still stays outside the active generated-kind gap:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-29'`
  and
  `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-29'`
  both returned `[]`, so there is still no new pgschema-side generated-column
  delta
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- the new mainline pg-delta delta lands in column/object grant preservation,
  pinned-extension schema export, identity-sequence privileges, and
  PK-redundant UNIQUE folding; none of those changes preserves generated kind
- the new nearby partition follow-up issue
  [#502](https://github.com/supabase/pg-toolbelt/issues/502) plus open PR
  [#504](https://github.com/supabase/pg-toolbelt/pull/504) are unrelated
  partition work rather than duplicates of the generated-kind gap
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only tracker context; there is still no exact current
  pg-toolbelt issue or PR for this scenario

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, so benchmark 022 remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-29)

This recheck advances checked-in/live `pg-delta` from
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` to
`e17c45925c3ddbf660dfb13c51029b605bcee448` through merged PRs
[#490](https://github.com/supabase/pg-toolbelt/pull/490),
[#488](https://github.com/supabase/pg-toolbelt/pull/488),
[#494](https://github.com/supabase/pg-toolbelt/pull/494),
[#484](https://github.com/supabase/pg-toolbelt/pull/484),
[#485](https://github.com/supabase/pg-toolbelt/pull/485),
[#492](https://github.com/supabase/pg-toolbelt/pull/492), and
[#499](https://github.com/supabase/pg-toolbelt/pull/499), while checked-in/live
`pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream delta still stays outside the active generated-kind gap:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  and
  `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  both returned `[]`, so there is no new pgschema-side generated-column delta
- the 2026-09-29 pg-delta delta lands in enum-retype casts, concurrent-drop
  retries, view/materialized-view column grants, and PG18 NOT NULL
  diagnostics; none of those changes preserves generated kind
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but collapses it to generated-expression presence instead of
  preserving the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only open tracker context; there is still no exact pg-toolbelt
  issue or PR for the generated-kind gap itself

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-23)

This recheck keeps checked-in/live `pg-delta` at
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` and keeps checked-in/live
`pgschema` at `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream delta still stays outside the active generated-kind gap:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-22'`
  and
  `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-22'`
  both returned `[]`, so there is no new pgschema-side issue or PR delta
  since the 2026-09-22 sweep
- there is no new merged `pg-toolbelt/main` code on top of the current
  checked-in/live head, so the active extract / render files remain unchanged
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only open tracker context for this benchmark, while open issue
  [#483](https://github.com/supabase/pg-toolbelt/issues/483), open PR
  [#484](https://github.com/supabase/pg-toolbelt/pull/484), open PR
  [#485](https://github.com/supabase/pg-toolbelt/pull/485), issue
  [#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
  [#477](https://github.com/supabase/pg-toolbelt/issues/477), PR
  [#478](https://github.com/supabase/pg-toolbelt/pull/478), and merged PRs
  [#480](https://github.com/supabase/pg-toolbelt/pull/480) and
  [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
  work rather than duplicates

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-22)

This recheck advances checked-in/live `pg-delta` from
`0882fc4cb6b792b79b599a414b434e4e048b6672` to
`c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` through merged release PR
[#481](https://github.com/supabase/pg-toolbelt/pull/481), while
checked-in/live `pgschema` remains
`580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream delta still stays outside the active generated-kind gap:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-21'`
  and
  `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-21'`
  both returned `[]`, so there is no new pgschema-side issue or PR delta
  beyond the 2026-09-21 sweep
- merged release PR [#481](https://github.com/supabase/pg-toolbelt/pull/481)
  only bumps `packages/pg-delta/CHANGELOG.md` and
  `packages/pg-delta/package.json`; none of
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` or
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` changed on
  the new checked-in/live head
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only open tracker context for this benchmark, while open issues
  [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  [#477](https://github.com/supabase/pg-toolbelt/issues/477),
  [#482](https://github.com/supabase/pg-toolbelt/issues/482), and
  [#483](https://github.com/supabase/pg-toolbelt/issues/483), open PR
  [#478](https://github.com/supabase/pg-toolbelt/pull/478), and merged PRs
  [#480](https://github.com/supabase/pg-toolbelt/pull/480) and
  [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
  work rather than duplicates

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-21)

This recheck keeps checked-in/live `pg-delta` at
`0882fc4cb6b792b79b599a414b434e4e048b6672` and advances checked-in/live
`pgschema` to `580f4040d0f3c1bfad1497918200c9c1f638a020` through merged PRs
[#616](https://github.com/pgplex/pgschema/pull/616),
[#617](https://github.com/pgplex/pgschema/pull/617),
[#618](https://github.com/pgplex/pgschema/pull/618),
[#619](https://github.com/pgplex/pgschema/pull/619),
[#620](https://github.com/pgplex/pgschema/pull/620),
[#621](https://github.com/pgplex/pgschema/pull/621), and
[#608](https://github.com/pgplex/pgschema/pull/608).

Today's upstream movement still stays outside the active generated-kind gap:

- merged PR [#616](https://github.com/pgplex/pgschema/pull/616) is the
  follow-up on already-upstream-only issue
  [#596](https://github.com/pgplex/pgschema/issues/596) and remains in
  pgschema's temp-schema / SQL-function batching path
- merged PRs [#617](https://github.com/pgplex/pgschema/pull/617),
  [#618](https://github.com/pgplex/pgschema/pull/618),
  [#619](https://github.com/pgplex/pgschema/pull/619),
  [#620](https://github.com/pgplex/pgschema/pull/620),
  [#621](https://github.com/pgplex/pgschema/pull/621), and
  [#608](https://github.com/pgplex/pgschema/pull/608) close already-screened
  covered or upstream-only issues
  [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602),
  [#603](https://github.com/pgplex/pgschema/issues/603), and
  [#607](https://github.com/pgplex/pgschema/issues/607); none of those touch
  generated-column kind extraction or rendering
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  open issue [#477](https://github.com/supabase/pg-toolbelt/issues/477), open
  PR [#478](https://github.com/supabase/pg-toolbelt/pull/478), merged PR
  [#480](https://github.com/supabase/pg-toolbelt/pull/480), and open release
  PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
  work rather than duplicates, and umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
  open tracker context for this benchmark

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-20)

This recheck keeps checked-in/live `pg-delta` at
`0882fc4cb6b792b79b599a414b434e4e048b6672` and advances checked-in/live
`pgschema` to `b8e7e26a9db221ea01cdd64f4cfb8ca96923c536` through merged PRs
[#610](https://github.com/pgplex/pgschema/pull/610),
[#612](https://github.com/pgplex/pgschema/pull/612),
[#613](https://github.com/pgplex/pgschema/pull/613),
[#614](https://github.com/pgplex/pgschema/pull/614), and
[#615](https://github.com/pgplex/pgschema/pull/615).

Today's upstream pgschema movement stays outside the active generated-kind gap:

- merged PR [#610](https://github.com/pgplex/pgschema/pull/610) closes covered
  issue [#606](https://github.com/pgplex/pgschema/issues/606), while merged
  PRs [#613](https://github.com/pgplex/pgschema/pull/613),
  [#614](https://github.com/pgplex/pgschema/pull/614), and
  [#615](https://github.com/pgplex/pgschema/pull/615) plus open follow-up PR
  [#616](https://github.com/pgplex/pgschema/pull/616) land in other fidelity
  or temp-schema families rather than generated-column kind extraction
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  open issue [#477](https://github.com/supabase/pg-toolbelt/issues/477), open
  PR [#478](https://github.com/supabase/pg-toolbelt/pull/478), and open
  release PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain
  adjacent work rather than duplicates, and umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
  open tracker context for this benchmark

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-19)

This recheck keeps checked-in/live `pg-delta` at
`0882fc4cb6b792b79b599a414b434e4e048b6672` and keeps checked-in/live
`pgschema` at `11678c582923fc1a27ed2edf37f3503d1fc466a8`.

There is no new pg-delta code or tracker delta since the 2026-09-18 refresh,
and the new pgschema activity does not change this generated-kind benchmark:

- open pgschema PR [#610](https://github.com/pgplex/pgschema/pull/610) is the
  upstream fix path for issue [#606](https://github.com/pgplex/pgschema/issues/606),
  which current pg-delta already covers and which is unrelated to generated
  column kind extraction or rendering
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  open issue [#477](https://github.com/supabase/pg-toolbelt/issues/477),
  open PR [#478](https://github.com/supabase/pg-toolbelt/pull/478), and open
  release PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain
  adjacent work rather than duplicates, and umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
  open tracker context for this benchmark

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-18)

This recheck advances checked-in/live `pg-delta` from
`94de18e34e9758e36cd0c18f7ffadeb2291bb446`
(`@supabase/pg-delta@1.0.0-alpha.52`) to post-alpha.52 main
`0882fc4cb6b792b79b599a414b434e4e048b6672` through merged PR
[#480](https://github.com/supabase/pg-toolbelt/pull/480), while
checked-in/live `pgschema` remains
`11678c582923fc1a27ed2edf37f3503d1fc466a8`.

The new upstream movement is still adjacent rather than gap-closing for this
generated-kind benchmark:

- the pg-delta delta between those heads only touches
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/indexes.ts`,
  `repos/pg-toolbelt/packages/pg-delta/src/plan/partition-index-attach.test.ts`,
  and the `partitioned-table-operations--drop-family-with-indexes` corpus;
  none of `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`,
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`, or
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` changed
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- merged PR [#480](https://github.com/supabase/pg-toolbelt/pull/480),
  open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  open issue [#477](https://github.com/supabase/pg-toolbelt/issues/477),
  and open PR [#478](https://github.com/supabase/pg-toolbelt/pull/478)
  remain adjacent work rather than duplicates, and umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
  open tracker context for this benchmark

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-17)

This recheck keeps checked-in/live `pg-delta` at
`94de18e34e9758e36cd0c18f7ffadeb2291bb446`
(`@supabase/pg-delta@1.0.0-alpha.52`) and keeps checked-in/live
`pgschema` at `11678c582923fc1a27ed2edf37f3503d1fc466a8`.

There is no upstream code or issue delta on either side since the
2026-09-16 refresh, so the same generated-kind gap remains:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  remains the only open tracker context for this benchmark, while issue
  [#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
  [#477](https://github.com/supabase/pg-toolbelt/issues/477), and PR
  [#478](https://github.com/supabase/pg-toolbelt/pull/478) remain adjacent
  role / identity-sequence privilege work rather than duplicates

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-16)

This recheck advances checked-in/live `pg-delta` from
`bb393ff61f5cd9ba95aee2824045f737afbe013b` (post-alpha.51 main) to
`94de18e34e9758e36cd0c18f7ffadeb2291bb446`
(`@supabase/pg-delta@1.0.0-alpha.52`) through merged release PR
[#479](https://github.com/supabase/pg-toolbelt/pull/479), while
checked-in/live `pgschema` remains
`11678c582923fc1a27ed2edf37f3503d1fc466a8`.

The new upstream movement is still release-only rather than gap-closing for
this generated-kind benchmark:

- the pg-delta delta between those heads only touches
  `packages/pg-delta/CHANGELOG.md` and
  `packages/pg-delta/package.json`; none of
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`,
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`, or
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` changed
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- open pg-toolbelt issue [#476](https://github.com/supabase/pg-toolbelt/issues/476)
  plus issue [#477](https://github.com/supabase/pg-toolbelt/issues/477) /
  PR [#478](https://github.com/supabase/pg-toolbelt/pull/478) remain adjacent
  role / identity-sequence privilege work rather than duplicates, and umbrella
  issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  only open tracker context for this benchmark

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
Benchmark 022 therefore remains **behaviorally uncovered**, while resolved
pgschema issue **#591** itself remains **covered** in current pg-delta.

## Refresh note (2026-09-15)

This recheck advances checked-in/live `pg-delta` from
`9fac5a973a0fddac0618314164331633606b5126`
(`@supabase/pg-delta@1.0.0-alpha.51`) to post-alpha.51 main
`bb393ff61f5cd9ba95aee2824045f737afbe013b` through merged PR
[#475](https://github.com/supabase/pg-toolbelt/pull/475), and advances
checked-in/live `pgschema` from `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`
to `11678c582923fc1a27ed2edf37f3503d1fc466a8` through merged PR
[#604](https://github.com/pgplex/pgschema/pull/604).

The new upstream movement does not touch this generated-kind gap:

- the pg-delta delta between those heads only touches assumed default grants,
  export/policy paths, and their tests; `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  still collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- pgschema PR [#604](https://github.com/pgplex/pgschema/pull/604) closes
  issue [#595](https://github.com/pgplex/pgschema/issues/595), but its
  extension-member filtering is unrelated to PostgreSQL 18 generated-column
  kind preservation
- new pg-toolbelt issue [#477](https://github.com/supabase/pg-toolbelt/issues/477)
  and open PR [#478](https://github.com/supabase/pg-toolbelt/pull/478) are
  adjacent identity-sequence privilege work rather than duplicates of this
  benchmark

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
remains the only open tracker context for this benchmark. Benchmark 022
therefore remains **behaviorally uncovered**, while resolved pgschema issue
**#591** itself is already **covered** in current pg-delta.

## Refresh note (2026-09-14)

This recheck advances checked-in/live `pg-delta` from
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) to
`9fac5a973a0fddac0618314164331633606b5126`
(`@supabase/pg-delta@1.0.0-alpha.51`) through merged PR
[#470](https://github.com/supabase/pg-toolbelt/pull/470) and release
[#474](https://github.com/supabase/pg-toolbelt/pull/474), and keeps
checked-in/live `pgschema` at `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`.

The new open pgschema issues [#596](https://github.com/pgplex/pgschema/issues/596)
through [#603](https://github.com/pgplex/pgschema/issues/603) do not change
this benchmark's active uncovered slice, and the alpha.51 pg-delta delta does
not touch the generated-kind path:

- current pg-delta already covered issue
  [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-expression
  change family before upstream merged its fix, via
  `packages/pg-delta/corpus/alter-table--generated-column` and the
  `generatedExpr: "replace"` path in
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`.
- benchmark **022** remains about the missing `VIRTUAL` versus `STORED` kind:
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.
- merged PR [#470](https://github.com/supabase/pg-toolbelt/pull/470) and open
  PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472),
  [#473](https://github.com/supabase/pg-toolbelt/pull/473), and
  [#475](https://github.com/supabase/pg-toolbelt/pull/475) remain adjacent or
  unrelated; none closes the generated-kind gap.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#593`, `pgschema#594`, and
`pgschema#595` still return no dedicated pg-toolbelt issue or PR. Umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
only adjacent tracker context. Benchmark 022 therefore remains
**behaviorally uncovered**, while resolved pgschema issue **#591** itself is
already **covered** in current pg-delta.

## Refresh note (2026-09-13)

This recheck keeps checked-in/live `pg-delta` at
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) and keeps checked-in/live
`pgschema` at `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`.

There is no upstream code delta on either side since the 2026-09-12 refresh.
The only new pgschema activity is open issue
[#595](https://github.com/pgplex/pgschema/issues/595)
(`dump takes some extension objects`), which current pg-delta already covers
through extension-member reference-only / export handling and therefore stays
outside this generated-column benchmark. The active generated-kind gap is
unchanged:

- current pg-delta already covered issue
  [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-expression
  change family before upstream merged its fix, via
  `packages/pg-delta/corpus/alter-table--generated-column` and the
  `generatedExpr: "replace"` path in
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`.
- benchmark **022** remains about the missing `VIRTUAL` versus `STORED` kind:
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.
- open PRs [#470](https://github.com/supabase/pg-toolbelt/pull/470),
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472), and
  [#473](https://github.com/supabase/pg-toolbelt/pull/473) remain adjacent or
  unrelated; none closes the generated-kind gap.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#593`, `pgschema#594`, and
`pgschema#595` still return no dedicated pg-toolbelt issue or PR. Umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
only adjacent tracker context. Benchmark 022 therefore remains
**behaviorally uncovered**, while resolved pgschema issue **#591** itself is
already **covered** in current pg-delta.

## Refresh note (2026-09-12)

This recheck keeps checked-in/live `pg-delta` at
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) and keeps checked-in/live
`pgschema` at `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`.

There is no upstream code delta on either side since the 2026-09-11 refresh.
The only new pgschema activity is open issue
[#594](https://github.com/pgplex/pgschema/issues/594), which is a
`.pgschemaignore` view-filtering report and remains outside this generated-
column benchmark. The active generated-kind gap is therefore unchanged:

- current pg-delta already covered issue
  [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-expression
  change family before upstream merged its fix, via
  `packages/pg-delta/corpus/alter-table--generated-column` and the
  `generatedExpr: "replace"` path in
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`.
- benchmark **022** remains about the missing `VIRTUAL` versus `STORED` kind:
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.
- open PRs [#470](https://github.com/supabase/pg-toolbelt/pull/470),
  [#471](https://github.com/supabase/pg-toolbelt/pull/471), and
  [#472](https://github.com/supabase/pg-toolbelt/pull/472) remain adjacent or
  unrelated; none closes the generated-kind gap.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#593`, and `pgschema#594`
still return no dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains **behaviorally
uncovered**, while resolved pgschema issue **#591** itself is already
**covered** in current pg-delta.

## Refresh note (2026-09-11)

This recheck advances checked-in/live `pg-delta` from
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) to
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) and advances checked-in/live
`pgschema` from `738a3bb40cf6b062928eeb564e3a98ec7f3c6989` to
`319b88c83d62b2c9a62eff7a09ec6563954bcf4b` through merged PR
[#592](https://github.com/pgplex/pgschema/pull/592), which closes
[#591](https://github.com/pgplex/pgschema/issues/591).

The new upstream generated-column fix still does not change this benchmark's
active uncovered slice:

- `git diff` between the two pg-delta heads is empty for the active files
  `src/extract/relations.ts`, `src/plan/rules/helpers.ts`,
  `src/plan/rules/tables.ts`, and the generated-column corpus, so the latest
  runtime evidence for this benchmark is still representative on alpha.50.
- current pg-delta already covered issue
  [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-expression
  change scenario before the upstream fix landed: the existing
  `packages/pg-delta/corpus/alter-table--generated-column` case exercises a
  `+` -> `*` expression change, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still diffs
  `generatedExpr` with `"replace"` semantics.
- benchmark **022** remains about the missing `VIRTUAL` versus `STORED` kind:
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.
- open pgschema issue [#593](https://github.com/pgplex/pgschema/issues/593)
  remains a separate covered column-collation case and does not touch the
  generated-column kind path.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#591`, and `pgschema#593`
still return no dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains **behaviorally
uncovered**, while resolved pgschema issue **#591** itself is already
**covered** in current pg-delta.

## Refresh note (2026-09-10)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main`
still at `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, and keeps
checked-in/live `pgschema` at `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`.

New open pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591)
and open PR [#592](https://github.com/pgplex/pgschema/pull/592) widen the
upstream generated-column family, but they do not change this benchmark's
active uncovered slice:

- current pg-delta already covers generated-expression changes on existing
  columns through `packages/pg-delta/corpus/alter-table--generated-column` and
  the `generatedExpr: "replace"` attribute path in
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`, so
  `pgschema#591` is not a new pg-delta parity gap
- benchmark **022** remains about the missing `VIRTUAL` versus `STORED` kind:
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
  collapses `attgenerated` to generated-expression presence, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`
- open pgschema issue [#593](https://github.com/pgplex/pgschema/issues/593) is
  a separate covered column-collation case and does not touch the generated-
  column kind path

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501` and `pgschema#591` still return no
dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains **behaviorally
uncovered**, while open pgschema issue **#591** itself is already **covered**
in current pg-delta.

## Refresh note (2026-09-09)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main` at
`ce61f01c24962fe21b9d02b319d8c26be0b5fd13` through merged PRs
[#460](https://github.com/supabase/pg-toolbelt/pull/460),
[#461](https://github.com/supabase/pg-toolbelt/pull/461),
[#462](https://github.com/supabase/pg-toolbelt/pull/462),
[#464](https://github.com/supabase/pg-toolbelt/pull/464),
[#467](https://github.com/supabase/pg-toolbelt/pull/467), and
[#469](https://github.com/supabase/pg-toolbelt/pull/469), and advances
checked-in/live `pgschema` from
`b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd` to
`738a3bb40cf6b062928eeb564e3a98ec7f3c6989` through merged PRs
[#585](https://github.com/pgplex/pgschema/pull/585),
[#586](https://github.com/pgplex/pgschema/pull/586),
[#587](https://github.com/pgplex/pgschema/pull/587), and
[#590](https://github.com/pgplex/pgschema/pull/590).

Today's upstream delta reshapes the watch list and promotes resolved
pgschema issue [#564](https://github.com/pgplex/pgschema/issues/564) into new
benchmark [024](024-pg18-not-null-validation.md), but it still does not touch
the active generated-column extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#564`, and `pgschema#589`
still return no dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-08)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main` at
`a982dfab6a87fa97f47130a1754dbd48d69446ce` through merged PR
[#458](https://github.com/supabase/pg-toolbelt/pull/458), and advances
checked-in/live `pgschema` from `fe7c64bfa410e7f9e8235eae3b912eb163b255f4` to
`b25a9e9c7312d0ddc1be17207bc4b3d61f4140cd` through merged PRs
[#582](https://github.com/pgplex/pgschema/pull/582) and
[#583](https://github.com/pgplex/pgschema/pull/583).

The new live pg-delta delta is adjacent rather than gap-closing: PR #458 only
guards checked-out clients from connection errors in apply/extract/load
callers, so the active generated-column extract / plan path is still
unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

Today's pgschema delta is also outside the active generated-column path.
Merged PR [#582](https://github.com/pgplex/pgschema/pull/582) broadens the
already-covered multi-file ordering family around
[#580](https://github.com/pgplex/pgschema/issues/580), merged PR
[#583](https://github.com/pgplex/pgschema/pull/583) closes
[#559](https://github.com/pgplex/pgschema/issues/559) as config-data work
outside pg-delta's schema-diff scope, and new issue
[#584](https://github.com/pgplex/pgschema/issues/584) plus open PR
[#585](https://github.com/pgplex/pgschema/pull/585) remain embedded-plan
ergonomics rather than this benchmark.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#564`, and `pgschema#584`
still return no dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-07)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `c6ed06f6fd5f1e36a00787b7034e35bda025e86b` to
`fe7c64bfa410e7f9e8235eae3b912eb163b255f4` through merged PR
[#581](https://github.com/pgplex/pgschema/pull/581).

Today's upstream delta is still outside the active generated-column path.
pgschema issues [#579](https://github.com/pgplex/pgschema/issues/579) and
[#580](https://github.com/pgplex/pgschema/issues/580) closed on 2026-09-07,
and follow-up PR [#582](https://github.com/pgplex/pgschema/pull/582) remains
open, but current pg-delta's generated-column extract / plan path is unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
direct exact searches for `pgschema#501`, `pgschema#579`, and `pgschema#580`
still return no dedicated pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-06)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and keeps checked-in/live `pgschema` at
`c6ed06f6fd5f1e36a00787b7034e35bda025e86b`.

No upstream code, issue, or PR delta landed since the 2026-09-05 refresh:
`gh issue list` / `gh pr list` updated-since checks returned empty arrays for
both `pgplex/pgschema` and `supabase/pg-toolbelt`, so the active generated-
column extract / plan path remains unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
exact duplicate searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
adjacent tracker context. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-09-05)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `89265906bd4d1a5c65971529989a81eb8b159d96` to
`c6ed06f6fd5f1e36a00787b7034e35bda025e86b` through merged PR
[#578](https://github.com/pgplex/pgschema/pull/578).

The upstream delta since the 2026-09-04 refresh is still on the pgschema side
only. It is the ownership-only follow-up in the already-resolved
[#573](https://github.com/pgplex/pgschema/issues/573) sequence family and does
not touch the active generated-column extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, while keyword duplicate searches for `VIRTUAL
generated` still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Benchmark 022
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-09-04)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` to
`89265906bd4d1a5c65971529989a81eb8b159d96` through merged PR
[#577](https://github.com/pgplex/pgschema/pull/577).

The upstream delta since the 2026-09-03 refresh is on the pgschema side only.
It fixes sequence ownership / SERIAL collapsing for issues
[#573](https://github.com/pgplex/pgschema/issues/573),
[#574](https://github.com/pgplex/pgschema/issues/574), and
[#576](https://github.com/pgplex/pgschema/issues/576), and does not touch the
active generated-column extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, while keyword duplicate searches for `VIRTUAL
generated` still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Benchmark 022
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-09-03)

This recheck advances checked-in/live `pg-delta` from
`107ac3df4b889c527215d1f6a37df64b33154c16`
(`@supabase/pg-delta@1.0.0-alpha.48`) to
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) through merged PR
[#455](https://github.com/supabase/pg-toolbelt/pull/455) and release
[#457](https://github.com/supabase/pg-toolbelt/pull/457), and advances
checked-in/live `pgschema` from
`97d8d60dd72a46704cc63b71b63aab2784847658`
(`v1.12.5`) to `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` through merged PR
[#572](https://github.com/pgplex/pgschema/pull/572).

The new pg-delta delta only touches `packages/pg-delta/src/plan/internal.ts`
plus enum/default ordering tests and corpus fixtures, while the new pgschema
delta only touches quoted-identifier dependency detection for issue
[#571](https://github.com/pgplex/pgschema/issues/571). The active generated-
column extract / plan path is unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, while keyword duplicate searches for `VIRTUAL
generated` still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Benchmark 022
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-10-07)

This recheck advances checked-in/live `pg-delta` from
`55d20b026f4208a21d24034c1714d9daa9daf9ee` to
`5e7c43674ab55f297702d18830489ac0008c019d` through merged PR
[#513](https://github.com/supabase/pg-toolbelt/pull/513) and release PR
[#516](https://github.com/supabase/pg-toolbelt/pull/516), while
checked-in/live `pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream activity still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-06'` and the
  matching `--include-prs` query surfaced only open issue
  [#624](https://github.com/pgplex/pgschema/issues/624), which is the SQL-
  function-body ordering family and is covered separately in current pg-delta
  via its `check_function_bodies = off` routine-plan preamble; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain unchanged since
  2026-09-20 / 2026-09-24
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-06'`
  surfaced merged PRs [#513](https://github.com/supabase/pg-toolbelt/pull/513)
  and [#516](https://github.com/supabase/pg-toolbelt/pull/516), merged release
  PR [#509](https://github.com/supabase/pg-toolbelt/pull/509), open PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514),
  [#515](https://github.com/supabase/pg-toolbelt/pull/515), and
  [#520](https://github.com/supabase/pg-toolbelt/pull/520), plus open issues
  [#510](https://github.com/supabase/pg-toolbelt/issues/510),
  [#517](https://github.com/supabase/pg-toolbelt/issues/517),
  [#518](https://github.com/supabase/pg-toolbelt/issues/518), and
  [#519](https://github.com/supabase/pg-toolbelt/issues/519)
- `git -C repos/pg-toolbelt diff --name-only
  55d20b026f4208a21d24034c1714d9daa9daf9ee..5e7c43674ab55f297702d18830489ac0008c019d`
  only touches `src/extract/dependencies.ts`,
  `src/frontends/schema-plan.ts`, `src/frontends/seed-assumed-schemas.ts`,
  `src/policy/*.ts`, `tests/orioledb-shadow.test.ts`, and release metadata;
  none touch the active generated-column extract / render path
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated`, but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`

Direct exact searches for `pgschema#501` still return no dedicated pg-toolbelt
issue or PR on 2026-10-07. Keyword `"VIRTUAL" generated"` searches continue to
surface live umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
plus historical merged PRs
[#378](https://github.com/supabase/pg-toolbelt/pull/378) and
[#299](https://github.com/supabase/pg-toolbelt/pull/299), but there is still
no exact current tracker for the generated-kind distinction itself. Resolved
pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591) remains
covered separately in current pg-delta.

The focused 2026-08-14 runtime observation therefore still stands: pg-delta
serializes the generated column as `... STORED`, collapses away the
PostgreSQL 18 `VIRTUAL` keyword, and still lets the proof loop return
`proofOk: true` with zero drift afterward. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-10-06)

This recheck advances checked-in/live `pg-delta` from
`6845a0beb646cec0bcbf894cec99cbcae2567fc6` to
`55d20b026f4208a21d24034c1714d9daa9daf9ee` through merged PR
[#512](https://github.com/supabase/pg-toolbelt/pull/512), while
checked-in/live `pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

Today's upstream activity still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-05'` and the
  matching `--include-prs` query both returned `[]`, so there is still no new
  pgschema-side generated-column delta; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain unchanged since
  2026-09-20 / 2026-09-24
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-05'`
  surfaced merged PR [#512](https://github.com/supabase/pg-toolbelt/pull/512)
  and open release PR [#509](https://github.com/supabase/pg-toolbelt/pull/509)
- `git -C repos/pg-toolbelt diff --name-only
  6845a0beb646cec0bcbf894cec99cbcae2567fc6..55d20b026f4208a21d24034c1714d9daa9daf9ee`
  only touches `.changeset/grouped-export-column-grants.md`,
  `packages/pg-delta/src/frontends/export-sql-files.ts`, and
  `packages/pg-delta/tests/export-grouped.test.ts`; none touch the active
  generated-column extract / render path
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated`, but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`

Direct exact searches for `pgschema#501` still return no dedicated pg-toolbelt
issue or PR on 2026-10-06. Keyword `"VIRTUAL" generated"` searches continue to
surface live umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
plus historical merged PRs
[#378](https://github.com/supabase/pg-toolbelt/pull/378) and
[#299](https://github.com/supabase/pg-toolbelt/pull/299), but there is still
no exact current tracker for the generated-kind distinction itself. Resolved
pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591) remains
covered separately in current pg-delta.

The focused 2026-08-14 runtime observation therefore still stands: pg-delta
serializes the generated column as `... STORED`, collapses away the
PostgreSQL 18 `VIRTUAL` keyword, and still lets the proof loop return
`proofOk: true` with zero drift afterward. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-10-05)

This recheck keeps checked-in/live `pg-delta` at
`6845a0beb646cec0bcbf894cec99cbcae2567fc6` and checked-in/live `pgschema` at
`580f4040d0f3c1bfad1497918200c9c1f638a020`; neither head moved since the
2026-10-04 refresh.

Today's upstream activity still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-04'` and the
  matching `--include-prs` query both returned `[]`, so there is still no new
  pgschema-side generated-column delta; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain unchanged since
  2026-09-20 / 2026-09-24
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-04'`
  surfaced open issue [#510](https://github.com/supabase/pg-toolbelt/issues/510),
  closed PR [#511](https://github.com/supabase/pg-toolbelt/pull/511), and
  open PR [#512](https://github.com/supabase/pg-toolbelt/pull/512); direct
  inspection shows #510 / #511 are trigger `WHEN` row-comparison convergence
  work and #512 is grouped-export column-grant ordering rather than generated-
  column kind tracking
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated`, but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`

Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR on 2026-10-05. Keyword `"VIRTUAL" generated`
searches still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Resolved
pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591)
remains covered separately in current pg-delta, so the active parity gap
is still only the missing generated-kind distinction itself.

The focused 2026-08-14 runtime observation therefore still stands: pg-delta
serializes the generated column as `... STORED`, collapses away the
PostgreSQL 18 `VIRTUAL` keyword, and still lets the proof loop return
`proofOk: true` with zero drift afterward. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-10-04)

This recheck keeps checked-in/live `pg-delta` at
`6845a0beb646cec0bcbf894cec99cbcae2567fc6` and checked-in/live `pgschema` at
`580f4040d0f3c1bfad1497918200c9c1f638a020`; neither head moved since the
2026-10-03 refresh.

Today's upstream activity still stays outside the active generated-kind gap:

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-03'` and the
  matching `--include-prs` query both returned `[]`, so there is still no new
  pgschema-side generated-column delta; open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain unchanged since
  2026-09-20 / 2026-09-24
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-03'`
  surfaced open issue [#510](https://github.com/supabase/pg-toolbelt/issues/510),
  closed issue [#491](https://github.com/supabase/pg-toolbelt/issues/491), and
  updated open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476);
  direct inspection showed they are trigger/ACL/role-scope work rather than
  generated-column kind tracking
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated`, but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`

Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR on 2026-10-04. Keyword `"VIRTUAL" generated`
searches still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Resolved
pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591)
remains covered separately in current pg-delta, so the active parity gap
is still only the missing generated-kind distinction itself.

The focused 2026-08-14 runtime observation therefore still stands: pg-delta
serializes the generated column as `... STORED`, collapses away the
PostgreSQL 18 `VIRTUAL` keyword, and still lets the proof loop return
`proofOk: true` with zero drift afterward. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-10-03)

This recheck keeps checked-in/live `pg-delta` at
`6845a0beb646cec0bcbf894cec99cbcae2567fc6` and checked-in/live `pgschema` at
`580f4040d0f3c1bfad1497918200c9c1f638a020`; neither head moved since the
2026-10-02 refresh.

A source recheck on the current pg-delta head still finds the same uncovered
path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated`, but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

Direct exact searches for `pgschema#501` still return no dedicated pg-toolbelt
issue or PR on 2026-10-03. Keyword `"VIRTUAL" generated` searches still only
surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Resolved pgschema
issue [#591](https://github.com/pgplex/pgschema/issues/591) remains covered
separately in current pg-delta, so the active parity gap is still only the
missing generated-kind distinction itself.

The focused 2026-08-14 runtime observation therefore still stands: pg-delta
serializes the generated column as `... STORED`, collapses away the PostgreSQL
18 `VIRTUAL` keyword, and still lets the proof loop return `proofOk: true`
with zero drift afterward. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Refresh note (2026-08-31)

This recheck keeps checked-in/live `pg-delta` at
`107ac3df4b889c527215d1f6a37df64b33154c16`
(`@supabase/pg-delta@1.0.0-alpha.48`) and advances checked-in/live
`pgschema` to `97d8d60dd72a46704cc63b71b63aab2784847658`
(`v1.12.5`) through merged PRs
[#565](https://github.com/pgplex/pgschema/pull/565),
[#566](https://github.com/pgplex/pgschema/pull/566),
[#567](https://github.com/pgplex/pgschema/pull/567), and
[#568](https://github.com/pgplex/pgschema/pull/568).

A source recheck on the current pg-delta head still finds the same uncovered
path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The upstream delta since the 2026-08-30 refresh is on the pgschema side rather
than the pg-delta side. Those new pgschema changes land in online rewrite,
constraint-validation, docs, and release surfaces, while the active
`relations.ts` / `helpers.ts` codepaths above remain unchanged, so the last
focused 2026-08-14 runtime observation still stands and serialized the
generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
The same proof still returned `proofOk: true` with zero drift, which means
the current extract/model path is also collapsing the kind strongly enough
that the proof loop cannot see the mismatch yet.

There is still no dedicated exact pg-toolbelt issue or PR for this scenario on
2026-08-31. Direct exact searches for `pgschema#501` still return nothing, and
keyword duplicate searches for `VIRTUAL generated` still only surface umbrella
fidelity tracker [#332](https://github.com/supabase/pg-toolbelt/issues/332).
Comments on that issue thread (not the original issue body) still carry the
PG17/18 virtual-generated-column note. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
    first_name text,
    last_name text
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.users
  ADD COLUMN full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL;
```

**Expected:** pg-delta preserves the PostgreSQL 18 `VIRTUAL` generated-
column kind when diffing and serializing the migration plan.

**Actual on current pg-delta:** current pg-delta emits `... STORED`
instead. The focused 2026-08-14 proof also reported zero drift afterward,
which means the current extract/model path is not preserving the
`VIRTUAL` / `STORED` distinction as diff-visible state yet.

## How pgschema handled it

pgschema fixed the issue in PR #503 by preserving the generated-column kind
through inspection and diff planning instead of collapsing it to a single
generated/not-generated state.

The merged fix added regression data under:

- `repos/pgschema/testdata/diff/create_table/issue_501_virtual_generated_column/`

That fixture now records `GENERATED ALWAYS AS (...) VIRTUAL` in the
expected plan output, confirming that upstream keeps the PostgreSQL 18
keyword intact in the resolved scenario.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Extract reads generated columns at all | Partially - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` reads `attgenerated`, but only uses it to decide whether `default_expr` should be treated as a generated expression |
| Extract / IR preserves `VIRTUAL` vs `STORED` kind | No - the current payload stores `generatedExpr` but not the actual generated kind |
| SQL emission preserves `VIRTUAL` | No - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` hard-codes `... STORED` in `columnClause()` |
| Focused proof on the exact PG18 scenario | No user-visible fidelity - the focused 2026-08-14 probe emitted `... STORED` yet still proved cleanly because the current model collapses the kind |
| Existing exact pg-toolbelt issue / PR | No dedicated exact tracker or PR yet; keyword duplicate searches only surface umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332), and comments on that issue thread now carry the PG17/18 virtual-generated-column note |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog / IR representation** | Preserves generated-column kind through the resolved fix | Collapses `attgenerated` down to generated-expression presence |
| **Plan / SQL emission** | Emits `VIRTUAL` when the schema requires it | Emits `GENERATED ALWAYS AS (...) STORED` |
| **Current parity state** | Fixed | Only umbrella-thread context under [#332](https://github.com/supabase/pg-toolbelt/issues/332); still behaviorally uncovered |

## Plan to handle it in pg-delta

1. Preserve the actual PostgreSQL generated-column kind from
   `attgenerated` in the extracted facts instead of collapsing it to
   generated-expression presence.
2. Update the diff path so `VIRTUAL` versus `STORED` is treated as a
   meaningful change.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
   (and any related create/alter rule helpers) so generated-column SQL
   preserves the correct PostgreSQL 18 keyword.
4. Add a focused pg18 regression under `packages/pg-delta/tests/` for the
   exact `VIRTUAL` scenario above, and make sure the proof loop fails until
   the kind is preserved end-to-end.
