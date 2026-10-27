# Parity refresh report - 2026-10-27

This report records the 2026-10-27 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `8703c276c3ee4bab6d4e30b14e6e8982ace14b89`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `6b82eff84dba925a176f0c6a78e5a16843885366`)

## 1) Benchmark status refresh

`pg-toolbelt` `main` did not move. `git ls-remote` still returns
`6b82eff84dba925a176f0c6a78e5a16843885366`. `pgschema` `main` advanced from
`24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca` to
`8703c276c3ee4bab6d4e30b14e6e8982ace14b89` (v1.13.4). `packages/pg-delta` is
unchanged. There is **no benchmark-status reclassification today**:

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
  - merged pgschema PR [#663](https://github.com/pgplex/pgschema/pull/663)
    adds `issue_653_partition_default_function_chain`, which emits
    `PARTITION OF ... (payload DEFAULT count_events_text())`. That default is
    this same gap. The parent-index consume path (lines 94-100) is unchanged
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` and stores only generated-expression presence as
    `generatedExpr` (lines 211 and 261)
  - `columnClause()` in `src/plan/rules/tables.ts` still hard-codes
    `GENERATED ALWAYS AS (...) STORED` (line 712)
  - a `VIRTUAL` search under `packages/pg-delta/src` still returns no matches
  - the new pgschema commits do not touch generated-column kind
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull` (line 121); PG18
    `contype = 'n'` rows remain outside diff-visible facts and only emit
    `table_not_null_comment_skipped` (lines 361-396)
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` (line 449)
  - today's pgschema delta still lands no exact current pg-toolbelt issue or
    PR for this benchmark
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - stays solved. Merged PR
    [#546](https://github.com/supabase/pg-toolbelt/pull/546) remains in the
    checked-in/live history
  - `src/plan/internal.ts` still refuses an export constraint fold when a
    same-table column or same-table dependent is emitted after `CREATE TABLE`
    (lines 779-793)

### Upstream movement since 2026-10-26

pgschema commits:

- `e3672a98` — [#662](https://github.com/pgplex/pgschema/pull/662) preserve
  `MATCH FULL` (`pg_constraint.confmatchtype = 'f'`). pg-delta already stores
  `pg_get_constraintdef(con.oid)` verbatim (`relations.ts`) and replays that
  `def` in `src/plan/rules/constraints.ts`. Exact searches for `"MATCH FULL"`
  and `confmatchtype` returned no pg-toolbelt issue or PR. There is still no
  dedicated scenario test, so this stays watch-only and is not a new benchmark
- `a18e2b98` — [#661](https://github.com/pgplex/pgschema/pull/661) closes
  [#638](https://github.com/pgplex/pgschema/issues/638). The bug was rendering
  several column privileges as `GRANT INSERT, UPDATE (cols)`, which grants
  `INSERT` on the whole table. `renderGrantSql()` (`helpers.ts` lines 182-197)
  qualifies every privilege on a column acl, so the plan emits
  `GRANT INSERT ("col"), UPDATE ("col")`. Verdict stays **covered**. The
  review-memory entry moves from `open` to `resolved`
- `906a0f7a` — [#663](https://github.com/pgplex/pgschema/pull/663) closes
  [#653](https://github.com/pgplex/pgschema/issues/653). Inherited
  primary-key / unique indexes keep their catalog names by adding constraints
  with `ALTER TABLE ONLY` after partitions exist, instead of letting
  `PARTITION OF` autoname them into a collision with a standalone index.
  pg-delta excludes constraint-backed indexes (`relations.ts` lines 466-469)
  and makes partition creation consume parent indexes plus parent primary-key
  and unique constraints (`tables.ts` lines 94-100), so the colliding index
  exists first and Postgres autonames the inherited primary key. Verdict stays
  **covered / avoided**. The review-memory entry moves from `open` to
  `resolved`. The partition-column `DEFAULT` fixture in the same PR is
  benchmark **021**, still open
- `8703c276` — [#664](https://github.com/pgplex/pgschema/pull/664) version
  bump only

Closed without merge:

- [#645](https://github.com/pgplex/pgschema/pull/645) (`closedAt`
  `2026-10-27T05:41:38Z`, head still `6a620735`). Superseded by
  [#663](https://github.com/pgplex/pgschema/pull/663)
- [#660](https://github.com/pgplex/pgschema/pull/660) (`closedAt`
  `2026-10-27T03:35:30Z`). Issue
  [#639](https://github.com/pgplex/pgschema/issues/639) stays open and stays
  **covered** in pg-delta
- [#637](https://github.com/pgplex/pgschema/pull/637) (`closedAt`
  `2026-10-27T02:32:47Z`). Umbrella
  [#627](https://github.com/pgplex/pgschema/issues/627) stays open and stays
  outside the benchmark matrix

The live open pgschema issue set is now
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627), and
[#639](https://github.com/pgplex/pgschema/issues/639).

pg-toolbelt:

- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-26'`
  surfaced only [#518](https://github.com/supabase/pg-toolbelt/issues/518).
  The timeline event is an unassignment at `2026-10-26T15:10:58Z`. The last
  comment is still the 2026-10-18 planner note. The user-function `DEFAULT`
  order case stays open, with partial coverage from merged PR
  [#553](https://github.com/supabase/pg-toolbelt/pull/553). pgschema searches
  for `generated expression column order` returned `[]`
- `gh search issues --repo supabase/pg-toolbelt --state closed --updated '>=2026-10-26'`
  returned `[]`
- `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-26'`
  surfaced [#506](https://github.com/supabase/pg-toolbelt/pull/506) and
  [#560](https://github.com/supabase/pg-toolbelt/pull/560)
- [#506](https://github.com/supabase/pg-toolbelt/pull/506) gained a 2026-10-26
  comment that questions the skip-machinery approach. The latest commit is
  still `c284eb4` from 2026-10-22. It stays unmatched policy-withheld context
- [#560](https://github.com/supabase/pg-toolbelt/pull/560) is a draft
  `@supabase/pg-checks` spike. It does not change `packages/pg-delta` schema
  diff behavior
- `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-26'`
  returned `[]`
- direct views keep issues
  [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  (`updatedAt` `2026-09-29T15:57:49Z`) and
  [#554](https://github.com/supabase/pg-toolbelt/issues/554)
  (`updatedAt` `2026-10-21T15:42:52Z`) open, and keep PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#493](https://github.com/supabase/pg-toolbelt/pull/493),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#555](https://github.com/supabase/pg-toolbelt/pull/555)
  (`updatedAt` `2026-10-25T10:00:47Z`, head `a638ed1`), and
  [#558](https://github.com/supabase/pg-toolbelt/pull/558) at their prior
  timestamps
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#534`, `pgschema#653`, and `pgschema#638` still returned `[]`
- `benchmark/review-memory.json` now uses pgschema SHA
  `8703c276c3ee4bab6d4e30b14e6e8982ace14b89` on the revalidated open watch
  list and on benchmarks **021** / **022** / **024** / **025**. Issues
  **#638** and **#653** moved from `open` to `resolved` with their new
  `updated_at` values. Verdicts are unchanged

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
- closed pgschema issues **#638** and **#653** stay covered in current
  pg-delta, so they do not become new benchmark files
- merged `MATCH FULL` support stays watch-only because verbatim constraint
  definitions already carry the clause
- open pg-toolbelt PR [#555](https://github.com/supabase/pg-toolbelt/pull/555)
  stays unmatched rename/respell work
- open pg-toolbelt PR [#560](https://github.com/supabase/pg-toolbelt/pull/560)
  stays outside schema-diff parity

No solved benchmark moved back to an open gap, and no active gap gained a
merged fix.
