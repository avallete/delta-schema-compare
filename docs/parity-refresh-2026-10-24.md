# Parity refresh report - 2026-10-24

This report records the 2026-10-24 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `6b82eff84dba925a176f0c6a78e5a16843885366`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`265af521e462577886ea6fdbb5777e1a23811cce` to
`6b82eff84dba925a176f0c6a78e5a16843885366` through merged PR
[#559](https://github.com/supabase/pg-toolbelt/pull/559), while checked-in/live
`pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. The only file
in that range is `.github/CODEOWNERS`. `packages/pg-delta` is unchanged.
There is **no benchmark-status reclassification today**:

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, **023**, and **025** stay solved in current
  pg-delta
- benchmarks **021**, **022**, and **024** remain the active unresolved parity
  set
- there is still **no open uncovered parity candidate** on the pgschema side

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    inherited child columns gated by `a.attislocal` (line 189)
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` (line 52) with no child
    column elements for local `DEFAULT` / `NOT NULL` overrides
  - the parent-index consume path (lines 94-100) is unchanged, so the covered
    inherited-index ordering for pgschema
    [#653](https://github.com/pgplex/pgschema/issues/653) stays in place
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` and stores only generated-expression presence as
    `generatedExpr` (lines 211 and 261)
  - `columnClause()` in `src/plan/rules/tables.ts` still hard-codes
    `GENERATED ALWAYS AS (...) STORED` (line 712)
  - a `VIRTUAL` search under `packages/pg-delta` still returns no matches
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull` (line 121); PG18
    `contype = 'n'` rows remain outside diff-visible facts and only emit
    `table_not_null_comment_skipped` (lines 361-396)
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` (line 449)
  - today's `265af521...6b82eff8` delta still lands no exact current
    pg-toolbelt issue or PR for this benchmark
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - stays solved. Merged PR
    [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains in the
    checked-in/live history
  - `src/plan/internal.ts` still refuses an export constraint fold when a
    same-table column or same-table dependent is emitted after `CREATE TABLE`
    (lines 779-793)

### Upstream movement since 2026-10-23

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-23'`
  returned `[]`
- `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-23'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-23'`
  surfaced open PR [#645](https://github.com/pgplex/pgschema/pull/645)
  (`updatedAt` `2026-10-23T10:28:25Z`)
- `gh search prs --repo pgplex/pgschema --merged --updated '>=2026-10-23'`
  returned `[]`
- a direct open-issue listing still shows only
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
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639), and
  [#653](https://github.com/pgplex/pgschema/issues/653)
- open PR [#645](https://github.com/pgplex/pgschema/pull/645) moved because of
  a comment ("it would be nice to have it asap"). Its latest commit is still
  `6a620735` from 2026-10-16. It remains the implementation thread for covered
  issue [#653](https://github.com/pgplex/pgschema/issues/653)
- older open PR [#662](https://github.com/pgplex/pgschema/pull/662)
  (`updatedAt` `2026-10-17T15:35:33Z`) remains watch-only `MATCH FULL`
  context: exact duplicate searches for `"MATCH FULL"` and `confmatchtype`
  still found no pg-toolbelt issue or PR, while current pg-delta still
  preserves the clause via verbatim `pg_get_constraintdef(con.oid)`
  extraction plus verbatim `def` replay. The current tree still lacks a
  dedicated scenario test
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-23'`
  returned `[]`
- `gh search issues --repo supabase/pg-toolbelt --state closed --updated '>=2026-10-23'`
  returned `[]`
- `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-23'`
  returned `[]`
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-23'`
  surfaced merged PR [#559](https://github.com/supabase/pg-toolbelt/pull/559)
  (`mergedAt` `2026-10-23T10:29:06Z`)
- direct views keep these previously watched items open, with no update in
  today's date window: issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  (`updatedAt` `2026-09-29T15:57:49Z`),
  [#518](https://github.com/supabase/pg-toolbelt/issues/518)
  (`updatedAt` `2026-10-20T13:17:30Z`), and
  [#554](https://github.com/supabase/pg-toolbelt/issues/554)
  (`updatedAt` `2026-10-21T15:42:52Z`), plus open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#493](https://github.com/supabase/pg-toolbelt/pull/493),
  [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#555](https://github.com/supabase/pg-toolbelt/pull/555), and
  [#558](https://github.com/supabase/pg-toolbelt/pull/558)
- merged PR [#559](https://github.com/supabase/pg-toolbelt/pull/559) sets
  `@supabase/cli` as code owners. Schema diff output is unchanged
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) stays
  open for the user-function `DEFAULT` order case. pgschema searches for
  `generated expression column order` returned `[]`
- open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554) stays
  the unmatched zero-argument `IMMUTABLE` generated-column apply failure.
  pgschema searches for `zero-arg` returned `[]`
- open PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) still
  settles deparsed spelling before rename and owner checks and is not in the
  checked-in/live head. pgschema searches for `settle spelling` returned `[]`
- open PRs [#506](https://github.com/supabase/pg-toolbelt/pull/506) and
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) remain unmatched
  policy-withheld and adjacent global-state / role-setting context. Open PR
  [#558](https://github.com/supabase/pg-toolbelt/pull/558) remains CI sharding
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#534`, and `pgschema#653` still returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 50`
  still returned `[]`

## 2) Duplicate and scope checks

No new tracking issue is drafted. The refreshed heads do not reveal a new
uncovered pgschema scenario, and the three active gaps already have recorded
benchmark files:

- benchmarks **021** and **022** stay on umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332)
- benchmark **024** still has no exact current pg-toolbelt issue or PR
- benchmark **025** stays solved through closed issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) and merged PR
  [#546](https://github.com/supabase/pg-toolbelt/pull/546)
- open pgschema PR [#645](https://github.com/pgplex/pgschema/pull/645) stays
  attached to covered issue
  [#653](https://github.com/pgplex/pgschema/issues/653)

`benchmark/review-memory.json` fingerprints for the open watch list and
resolved benchmarks **#499**, **#501**, **#534**, and **#564** were refreshed
to the new pg-delta SHA. Verdicts are unchanged.
