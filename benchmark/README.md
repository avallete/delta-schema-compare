# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-09-10)

Refreshed against:

- checked-in `repos/pg-toolbelt` @ `08219f1a8832f86e7287e50bab793a498129db7a`
- live `repos/pg-toolbelt/main` @ `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`
- checked-in/live `repos/pgschema` @ `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`

> The 2026-09-10 refresh keeps the active benchmarked gap set at **021**,
> **022**, and **024** while screening two new open pgschema issues:
>
> - [#591](https://github.com/pgplex/pgschema/issues/591)
>   (`GENERATED ALWAYS AS` expression changes) is **covered** in current
>   pg-delta via the existing `alter-table--generated-column` corpus scenario
>   and `generatedExpr: "replace"` diff path
> - [#593](https://github.com/pgplex/pgschema/issues/593)
>   (non-default column collations omitted from dump) appears **covered** in
>   current pg-delta because column extraction preserves explicit
>   `attcollation` and SQL emission replays `COLLATE ...`
> - checked-in `repos/pg-toolbelt` remains
>   `08219f1a8832f86e7287e50bab793a498129db7a` (`@supabase/pg-delta@1.0.0-alpha.49`)
> - live `pg-toolbelt/main` remains `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`; new open PRs
>   [#470](https://github.com/supabase/pg-toolbelt/pull/470),
>   [#471](https://github.com/supabase/pg-toolbelt/pull/471), and
>   [#472](https://github.com/supabase/pg-toolbelt/pull/472) are adjacent only
> - checked-in/live `pgschema` remains `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`; new issue
>   [#591](https://github.com/pgplex/pgschema/issues/591), open PR
>   [#592](https://github.com/pgplex/pgschema/pull/592), and new issue
>   [#593](https://github.com/pgplex/pgschema/issues/593) widen upstream
>   generated-column and column-collation coverage
> - benchmark **021** remains unresolved because child-local partition
>   overrides are still not modeled, while benchmarks **022** and **024**
>   remain unresolved for the previously documented `VIRTUAL`-kind and PG18
>   native `NOT NULL` reasons
> - exact duplicate searches for `pgschema#499`, `#501`, `#564`, `#591`, and
>   `#593` still return no dedicated pg-toolbelt issue or PR, and this
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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | none found | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Three resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
- **024** - PostgreSQL 18 native `NOT NULL ... NOT VALID` state and pending
  validation visibility

The checked-in `pg-delta` head remains
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), live `pg-toolbelt/main` remains
`ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, and checked-in/live `pgschema` remains
`738a3bb40cf6b062928eeb564e3a98ec7f3c6989`.

Today's upstream delta does not change the active gap set, but it adds adjacent
context:

- benchmark **021** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  child-inherited columns with `a.attislocal`, and open PR
  [#470](https://github.com/supabase/pg-toolbelt/pull/470) still leaves the
  bare `CREATE TABLE ... PARTITION OF ... ${bound}` child-create path without a
  typed column-element list for local `DEFAULT` / `NOT NULL` overrides
- benchmark **022** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still collapses
  `attgenerated` to generated-expression presence and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still renders
  generated columns as `... STORED`; new pgschema issue
  [#591](https://github.com/pgplex/pgschema/issues/591) is already covered in
  current pg-delta and does not change this benchmark verdict
- benchmark **024** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still tracks
  nullability via `a.attnotnull` and filters extracted table constraints to
  `con.contype IN ('p', 'u', 'f', 'c', 'x')`, while
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits a
  plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
- new pgschema issue [#593](https://github.com/pgplex/pgschema/issues/593)
  appears covered in current pg-delta's extract/render path, so there is still
  no open uncovered parity candidate on the pgschema side
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for benchmarks **021** / **022**, while benchmark **024** remains
  source-validated from its 2026-09-09 promotion note
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  still carries the only adjacent tracker context for benchmarks **021** /
  **022**; benchmark **024** still has no exact pg-toolbelt issue or PR

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#588](https://github.com/pgplex/pgschema/issues/588),
[#591](https://github.com/pgplex/pgschema/issues/591),
and [#593](https://github.com/pgplex/pgschema/issues/593).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity
  work for pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work
  for pg-delta**
- **#588** data-feature design feedback - **not parity work for pg-delta**;
  it discusses pgschema's config/data dump workflow, while current pg-delta
  remains a schema-diff tool and explicitly leaves row-level data comparison
  out of scope
- **#591** generated-column expression changes on existing columns -
  **covered** in current pg-delta; `packages/pg-delta/corpus/alter-table--generated-column`
  already exercises an existing generated-expression change and
  `tableRules.column.generatedExpr` is diffed with `"replace"` semantics, so
  the change is not invisible even though pg-delta uses replacement rather than
  pgschema's version-gated `SET EXPRESSION AS`
- **#593** explicit non-default column collations - **covered** in current
  pg-delta's extract/render model; `src/extract/relations.ts` preserves
  explicit non-default `attcollation` on column facts and
  `src/plan/rules/helpers.ts` replays that state as `COLLATE ...` in column
  definitions

There is currently **no open uncovered parity candidate** on the pgschema side.
There is also **no dedicated exact open pg-toolbelt parity tracker** for the
active benchmarks above or the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444). The remaining active
benchmarks **021** / **022** are only adjacently tracked under the open
umbrella fidelity issue
[pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332),
benchmark **024** still has no exact pg-toolbelt issue or PR, and open PR
[#470](https://github.com/supabase/pg-toolbelt/pull/470) is still adjacent
rather than a direct fix for benchmark **021**'s child-local column-override
path. Exact duplicate searches for current open watch-list issues
[#588](https://github.com/pgplex/pgschema/issues/588),
[#591](https://github.com/pgplex/pgschema/issues/591),
[#593](https://github.com/pgplex/pgschema/issues/593), and the already-
benchmarked resolved issue [#564](https://github.com/pgplex/pgschema/issues/564)
also return no dedicated pg-toolbelt issue or PR.

## Recent closed-issue / tracker updates

- **#571** quoted identifiers in dependency detection - closed on 2026-09-03
  by [pgschema#572](https://github.com/pgplex/pgschema/pull/572) and remains
  **covered** in current pg-delta; pg-delta resolves dependencies from
  PostgreSQL catalog edges rather than a regex-limited function-call matcher

- **#573** sequence definitions omitted from dump while sequence grants remain
  - closed on 2026-09-03 by
  [pgschema#577](https://github.com/pgplex/pgschema/pull/577), then followed by
  ownership-only fix [pgschema#578](https://github.com/pgplex/pgschema/pull/578)
  on 2026-09-04, and remains
  **covered** in current pg-delta:
  - user sequences are extracted as first-class `sequence` facts, and
    `tests/extract.test.ts` keeps the `default -> sequence` dependency edge
  - `tests/export-serial-owned-by.test.ts` confirms export emits real
    `CREATE SEQUENCE` plus grants while keeping `OWNED BY` with the owning
    table file
  - `tests/export.test.ts` round-trips an explicit `CREATE SEQUENCE` plus
    `DEFAULT nextval(...)` pair
  - `tests/load-sql-files-statement-fallback.test.ts` confirms the split
    sequence/table file model still converges
  - `src/plan/rules/sequences.ts` still renders explicit `CREATE SEQUENCE`
    statements instead of inventing `<table>_<column>_seq` names
  - `sequenceOwnedBySpecs()` in `src/plan/rules/helpers.ts` already emits both
    `ALTER SEQUENCE ... OWNED BY ...` and `OWNED BY NONE`, and
    `src/plan/rules/sequences.ts` wires that helper on both create and alter
    paths, so the new upstream ownership-only follow-up also remains covered

- **#574** shared-sequence defaults rewritten as guessed `BIGSERIAL` / wrong
  per-table sequence names and **#576** extra sequences for custom-named
  defaults - both closed on 2026-09-03 as duplicates folded into the now-
  resolved root-cause issue
  [#573](https://github.com/pgplex/pgschema/issues/573); current pg-delta
  remains **covered** because it preserves explicit sequences plus
  `DEFAULT nextval(...)` edges rather than rewriting them into guessed
  `<table>_<column>_seq` sequences

- **#579** `type does not exist` for an unusual
  `RETURNS SETOF <relation>` multi-file dump case - closed on 2026-09-07 and
  remains **covered** in current pg-delta:
  - `src/extract/dependencies.ts` maps relation row types through
    `pg_type.typrelid` back to the owning table/view facts
  - `corpus/table-fn-dep--setof-function` exercises
    `RETURNS SETOF test_schema.users`
  - `tests/composite-order-roundtrip.test.ts` keeps a `RETURNS SETOF`
    export/load chain round-trippable

- **#580** multi-file include ordering by dependency - closed on 2026-09-07 by
  [pgschema#581](https://github.com/pgplex/pgschema/pull/581), then broadened
  on 2026-09-07 by merged follow-up
  [pgschema#582](https://github.com/pgplex/pgschema/pull/582), and current
  pg-delta still appears **covered**:
  - `exportSqlFiles()` preserves plan order across files in the default
    `by-object` layout and offers filename-stable dependency order through
    `layout: "ordered"`
  - `tests/export.test.ts` and `tests/export-fidelity.test.ts` gate
    `load(export(fb)) ≡ fb` across layouts
  - `tests/load-sql-files.test.ts` proves out-of-order SQL files still
    converge through dependency-aware retry rounds
  - `src/frontends/load-sql-files.ts` and `src/plan/preamble.ts` both set
    `check_function_bodies = off`, so forward-referencing SQL function bodies
    remain replayable in the load/apply path
  - `src/extract/dependencies.ts` maps relation row types through
    `pg_type.typrelid` back to the owning table/view facts and resolves
    `pg_proc` aggregates (`prokind = 'a'`) as first-class dependency endpoints,
    so aggregates over view row types still sort after the view
  - no dedicated exact pg-toolbelt issue or PR was found

- **#589** `ON DELETE SET NULL` / `SET DEFAULT` column lists on foreign keys -
  closed on 2026-09-09 by
  [pgschema#590](https://github.com/pgplex/pgschema/pull/590) and appears
  **covered** in current pg-delta:
  - `TABLE_CONSTRAINTS_SQL` in
    `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    canonical `pg_get_constraintdef(con.oid)` text as the constraint `def`
  - current diff keys table constraints on that `def`, and
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts`
    replays foreign-key definitions verbatim through
    `ADD CONSTRAINT ... ${def}`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extract.test.ts` already asserts
    canonical constraint-definition extraction

- **#564** safer `NOT NULL` additions / PG18 native validation workflow -
  closed on 2026-09-08 after merged PRs
  [#566](https://github.com/pgplex/pgschema/pull/566) and
  [#587](https://github.com/pgplex/pgschema/pull/587), and remains
  **not covered** in current pg-delta; benchmarked as
  [024](024-pg18-not-null-validation.md):
  - current pg-delta still tracks column nullability only via
    `a.attnotnull`
  - constraint extraction still filters out PG18 `contype = 'n'` rows
  - `src/plan/rules/tables.ts` still emits plain
    `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

- **#450** missing role blocks plan/apply - closed on 2026-09-08 by
  [pgschema#586](https://github.com/pgplex/pgschema/pull/586) and remains
  **not parity work for pg-delta**; the fix stubs referenced roles into
  pgschema's embedded/external plan database, while pg-delta diffs live
  catalogs directly and already extracts roles as first-class facts

- **#584** global items / extensions / roles - closed on 2026-09-08 by
  [pgschema#585](https://github.com/pgplex/pgschema/pull/585) and remains
  **not parity work for pg-delta**; the fix mirrors target extensions into
  pgschema's embedded plan database and treats the roles half as a duplicate of
  [#450](https://github.com/pgplex/pgschema/issues/450), while current
  pg-delta does not depend on an embedded plan database

- **#559** support config data evolution - closed on 2026-09-08 by
  [pgschema#583](https://github.com/pgplex/pgschema/pull/583) and remains
  **not parity work for pg-delta** because current pg-delta still explicitly
  stops at schema diffing and documents in
  `src/frontends/load-sql-files.ts` plus
  `packages/pg-delta/tests/load-sql-files.test.ts` that it deliberately never
  compares data

- benchmark [024](024-pg18-not-null-validation.md) is new on 2026-09-09;
  checked-in `pg-delta` remains
  `08219f1a8832f86e7287e50bab793a498129db7a`, live
  `pg-toolbelt/main` advances to
  `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, checked-in/live `pgschema`
  advances to `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`, and the active
  benchmark set expands from **021** / **022** to **021** / **022** / **024**

- **#569** `dump and plan uses wrong order` - closed on 2026-09-02 after the
  already-merged pgschema fix
  [#570](https://github.com/pgplex/pgschema/pull/570) and remains
  **covered** in current pg-delta; `src/frontends/sql-order.ts` can split and
  topo-order statements for shadow loading, `src/frontends/load-sql-files.ts`
  still retries file-granular dependency rounds, and
  `tests/reorder-shadow.test.ts` plus `tests/load-sql-files.test.ts` already
  pin out-of-order shadow-load cases

- **#563** dealing with migrations that impact existing data - closed on
  2026-08-31 after pgschema documented the manual plan-edit workflow; this
  remains **not parity work for pg-delta** because current pg-delta still
  explicitly stops at schema diffing and documents in
  `src/frontends/load-sql-files.ts` plus
  `packages/pg-delta/tests/load-sql-files.test.ts` that it deliberately never
  compares data

- **#557** lock timeout and retries - closed by
  [pgschema#560](https://github.com/pgplex/pgschema/pull/560) and remains
  **not parity work for pg-delta**; current pg-delta already exposes
  `lockTimeoutMs` through `src/apply/apply-preamble.ts` and
  `src/cli/commands/schema.ts`, while the pgschema fix adds apply retry
  ergonomics rather than changing schema-diff fidelity

- **#561** index `NULLS FIRST` / `NULLS LAST` ordering - closed by
  [pgschema#562](https://github.com/pgplex/pgschema/pull/562) and appears
  **covered** in current pg-delta; `src/extract/relations.ts` stores exact
  `pg_get_indexdef(i.indexrelid)` output in standalone index facts, the diff
  keys indexes on exact `def`, and `src/plan/rules/indexes.ts` replays that
  definition unchanged apart from optional `CONCURRENTLY` insertion, so
  non-default null-ordering clauses should survive extraction, diff, and plan
  generation even though there is no dedicated exact regression test yet

- **#493** `--qualify-schema` type-reference follow-up - closed on
  2026-08-21 and remains **not parity work for pg-delta**; the issue is still
  about pgschema's desired-schema render / IR fidelity rather than pg-delta's
  live-catalog diff surface
- **#404** deferrable unique constraints - **covered** in current
  pg-delta; exact tracker
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#366** enum-arg function privilege signatures - **covered** in
  current pg-delta; exact tracker
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#551** removing an explicit RLS `WITH CHECK` clause - closed by
  [pgschema#554](https://github.com/pgplex/pgschema/pull/554) and remains
  **covered** in current pg-delta;
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/policies.ts` still
  rebuilds policies when `usingExpr` / `checkExpr` changes, and
  `src/plan/policy-clause-removal.test.ts` still pins the clause-removal path
- **#552** cross-schema partition child planning with an external plan database
  - closed by [pgschema#555](https://github.com/pgplex/pgschema/pull/555) and
  remains **not parity work for pg-delta**; the merged fix adds cross-schema
  partition-parent stubs in `repos/pgschema/cmd/plan/partition_stubs.go`,
  while pg-delta still diffs live catalogs directly and its active partition
  benchmark remains the separate child-override gap
  [021](021-partition-child-column-overrides.md)
- **#553** external plan database rejects `ALTER DEFAULT PRIVILEGES` in
  Supabase-style plans - closed by
  [pgschema#556](https://github.com/pgplex/pgschema/pull/556) and remains
  **not parity work for pg-delta**; the merged fix adds temporary role stubs
  for pgschema's external plan database, while current pg-delta already
  exercises default-privilege planning in Supabase-style contexts through
  `src/plan/rules/default-privilege.test.ts` and
  `src/policy/supabase-default-privileges.test.ts`
- **#412** `UNIQUE NULLS NOT DISTINCT` on table constraints - now
  **covered** in current pg-delta; benchmark [020](020-unique-constraint-nulls-not-distinct.md)
  is retained as a historical record
- **#518** extension-owned type schema mismatch - closed by
  [pgschema#544](https://github.com/pgplex/pgschema/pull/544) and still
  **not parity work for pg-delta**
- **#519** view normalization through the temporary plan schema - closed by
  [pgschema#520](https://github.com/pgplex/pgschema/pull/520) and still
  **not parity work for pg-delta**
- **#534** self-referencing FK to a non-PK standalone unique index on the same
  table - closed by [pgschema#540](https://github.com/pgplex/pgschema/pull/540)
  and remains **covered** in current pg-delta
- **#535** domain created over a table row type - closed by
  [pgschema#539](https://github.com/pgplex/pgschema/pull/539) and remains
  **covered** in current pg-delta
- **#536** dropping a foreign-keyed table/column in the wrong order - closed
  upstream and remains **covered** in current pg-delta
- **#537** built-in `ALTER COLUMN TYPE` without a `USING` clause - closed by
  [pgschema#541](https://github.com/pgplex/pgschema/pull/541), remains
  **covered** in current pg-delta, and matches the solved benchmark family in
  [005](005-alter-column-type-using-clause.md)
- **#538** dropping a table with a trigger - closed upstream; current pg-delta
  already has trigger-drop-before-function-drop coverage (historical tracker
  [pg-toolbelt#137](https://github.com/supabase/pg-toolbelt/issues/137) plus
  the `trigger-operations--trigger-drop-before-function-drop` corpus scenario)
- **#545** function signature depends on a deferred table row type - closed by
  [pgschema#546](https://github.com/pgplex/pgschema/pull/546); current
  pg-delta already resolves routine signature dependencies on relation row
  types through `pg_depend` in
  `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`, so no new
  benchmark file or duplicate tracker is needed
- **#548** cross-schema FK to `auth.users` when the `auth` schema is
  intentionally excluded from a pgschema dump - closed by
  [pgschema#549](https://github.com/pgplex/pgschema/pull/549) and remains
  **not parity work for pg-delta**; pg-delta diffs live catalogs directly and
  already carries `auth`-schema fixtures, so no benchmark or duplicate tracker
  change is needed
- **#499** child-specific column elements on `PARTITION OF` create -
  still **not covered in current behavior**, with only umbrella-thread context
  from [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [021](021-partition-child-column-overrides.md)
- **#501** PostgreSQL 18 `VIRTUAL` generated columns - still **not covered in
  current behavior**, with only umbrella-thread context from
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [022](022-virtual-generated-columns.md)
- **#564** PostgreSQL 18 native `NOT NULL` validation workflow -
  still **not covered in current behavior** and benchmarked as
  [024](024-pg18-not-null-validation.md)
- **#506** new-table FK before standalone unique index - **covered** in
  current pg-delta; benchmark [023](023-fk-before-standalone-unique-index.md)
  is retained as a historical record
- draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444) still have no
  exact pg-toolbelt issue or PR

## Upstream watch list

- the current open pgschema watch scope is
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  and [#588](https://github.com/pgplex/pgschema/issues/588)
- checked-in `pg-toolbelt` now sits at
  `08219f1a8832f86e7287e50bab793a498129db7a`
- live `pg-toolbelt/main` now sits at
  `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`
- checked-in/live `pgschema` now sits at
  `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`
- merged pgschema PR
  [#590](https://github.com/pgplex/pgschema/pull/590) is the current latest
  upstream change on `main`; it closes issue
  [#589](https://github.com/pgplex/pgschema/issues/589), which current
  pg-delta appears to cover structurally through canonical constraint-
  definition extraction
- merged pgschema PR
  [#587](https://github.com/pgplex/pgschema/pull/587) is the immediately
  previous benchmark-relevant `main` change; it closes the remaining
  visibility gap in the broader
  [#564](https://github.com/pgplex/pgschema/issues/564) NOT NULL workflow
  after the initial PostgreSQL 18-native implementation in
  [#566](https://github.com/pgplex/pgschema/pull/566)
- merged pgschema PR [#586](https://github.com/pgplex/pgschema/pull/586)
  closes [#450](https://github.com/pgplex/pgschema/issues/450) and merged PR
  [#585](https://github.com/pgplex/pgschema/pull/585) closes
  [#584](https://github.com/pgplex/pgschema/issues/584); both remain not-parity
  plan-database ergonomics for pg-delta
- open pgschema issue [#588](https://github.com/pgplex/pgschema/issues/588)
  is the current adjacent watch-list context, but it remains outside the
  schema-diff matrix because it is feedback on pgschema's data/config design
- open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) tracks event-
  trigger-driven RLS state drift on identical SQL inputs; it is useful current
  pg-delta context, but it does not map to an open pgschema issue or the active
  benchmarked gaps
- recent merged pg-toolbelt PRs between checked-in alpha.49 and live `main`
  are [#460](https://github.com/supabase/pg-toolbelt/pull/460),
  [#461](https://github.com/supabase/pg-toolbelt/pull/461),
  [#462](https://github.com/supabase/pg-toolbelt/pull/462),
  [#464](https://github.com/supabase/pg-toolbelt/pull/464),
  [#467](https://github.com/supabase/pg-toolbelt/pull/467), and
  [#469](https://github.com/supabase/pg-toolbelt/pull/469); none is a
  dedicated tracker or fix for benchmarks **021** / **022** / **024**
- comments on open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remain the
  closest tracker context for benchmarks **021** / **022**
- no exact pg-toolbelt issue or PR was found for benchmark **024** or the
  older draft-only gaps **#439** / **#444**

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by
  the automation scripts.
