# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-08-13)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `17bfd13b49e94d4e073154921df738707fd03d87`
- checked-in/live `repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`

> The 2026-08-13 refresh keeps the **active behavioral gap set** unchanged, but
> it **updates the benchmark issue mapping**.
>
> - the active benchmarked gap set remains **021** and **022**
> - both active benchmarks now map to the open umbrella fidelity tracker
>   [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332),
>   whose current body explicitly carries both inherited-column local overrides
>   on declarative partitions and PostgreSQL 17/18 virtual generated columns
> - open pgschema issues
>   [#534](https://github.com/pgplex/pgschema/issues/534),
>   [#535](https://github.com/pgplex/pgschema/issues/535),
>   [#536](https://github.com/pgplex/pgschema/issues/536), and new
>   [#537](https://github.com/pgplex/pgschema/issues/537) are already
>   **covered** in current pg-delta
> - exact closed coverage trackers
>   [#218](https://github.com/supabase/pg-toolbelt/issues/218) /
>   [#219](https://github.com/supabase/pg-toolbelt/issues/219) remain solved
>   historical context for pgschema
>   [#404](https://github.com/pgplex/pgschema/issues/404) /
>   [#366](https://github.com/pgplex/pgschema/issues/366)
> - direct duplicate searches still find **no dedicated exact pg-toolbelt issue
>   or PR** for the active benchmarks **021** / **022** or the older draft-only
>   gaps
>   [#439](https://github.com/pgplex/pgschema/issues/439) /
>   [#444](https://github.com/pgplex/pgschema/issues/444); **#332** is the
>   current umbrella tracker, not a dedicated one-to-one issue

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella) | none found | **Tracked (umbrella fidelity tracker)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella) | none found | **Tracked (umbrella fidelity tracker)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Two resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
- **022** - PostgreSQL 18 `VIRTUAL` generated columns

Focused 2026-08-13 runtime probes on current heads show:

- benchmark **021** still emits only
  `CREATE TABLE ... PARTITION OF ... FOR VALUES ...`, omitting the
  child-local `priority DEFAULT 10` and `notes NOT NULL` overrides
- benchmark **022** still emits
  `ALTER TABLE ... ADD COLUMN ... GENERATED ALWAYS AS (...) STORED`
  for a PostgreSQL 18 `VIRTUAL` generated column
- both scenarios still produced `proofOk: true`, which means the current
  engine is not surfacing those missing semantics as end-to-end drift on
  the current fact model / proof path yet
- open umbrella tracker
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
  now explicitly lists both fidelity gaps, so these benchmarks are
  behaviorally unresolved but no longer untracked

## Open pgschema issue screening (current state)

The current open pgschema issue set is:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#450](https://github.com/pgplex/pgschema/issues/450),
[#493](https://github.com/pgplex/pgschema/issues/493),
[#518](https://github.com/pgplex/pgschema/issues/518),
[#519](https://github.com/pgplex/pgschema/issues/519),
[#534](https://github.com/pgplex/pgschema/issues/534),
[#535](https://github.com/pgplex/pgschema/issues/535),
[#536](https://github.com/pgplex/pgschema/issues/536), and
[#537](https://github.com/pgplex/pgschema/issues/537).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity
  work for pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work
  for pg-delta**
- **#450** missing role blocks plan/apply - **not parity work for
  pg-delta**; this remains specific to pgschema's desired-state temp
  schema workflow, while pg-delta diffs live catalogs directly
- **#493** `--qualify-schema` type-reference follow-up work - **not parity
  work for pg-delta**
- **#518** extension-owned type schema mismatch in pgschema's temp
  comparison database - **not parity work for pg-delta**; open
  [pgschema#517](https://github.com/pgplex/pgschema/pull/517) stays on
  the pgschema-specific side of the fence
- **#519** view normalization through the temporary plan schema - **not
  parity work for pg-delta**; open
  [pgschema#520](https://github.com/pgplex/pgschema/pull/520) remains a
  pgschema temp-schema normalization fix rather than a live-catalog diff
  gap
- **#534** self-referencing FK to a non-PK standalone unique index on the
  same table - **covered** in current pg-delta; the focused 2026-08-13
  probe emitted `CREATE UNIQUE INDEX parent_orgs_external_key_key`
  immediately before `ADD CONSTRAINT fk_self_migrated_from FOREIGN KEY`,
  proved cleanly, and left zero drift
- **#535** domain created over a table row type - **covered** in current
  pg-delta; the focused 2026-08-13 probe emitted `CREATE TABLE public.x ()`
  before `CREATE DOMAIN public.y AS public.x`, proved cleanly, and left
  zero drift
- **#536** dropping a foreign-keyed table/column in the wrong order -
  **covered** in current pg-delta; the focused 2026-08-13 probe emitted
  `DROP CONSTRAINT` -> `DROP COLUMN` -> `DROP TABLE`, proved cleanly, and
  left zero drift
- **#537** built-in `ALTER COLUMN TYPE` without a `USING` clause -
  **covered** in current pg-delta; the focused 2026-08-13 probe emitted
  `ALTER COLUMN "arfcn_dl" TYPE integer USING "arfcn_dl"::integer`,
  proved cleanly, and matches the solved benchmark family in
  [005](005-alter-column-type-using-clause.md)

There is currently **no dedicated exact open pg-toolbelt parity tracker** for
the covered open issues above or for the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444). The remaining active
benchmarks **021** / **022** are now tracked under the open umbrella fidelity
issue [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332),
whose body explicitly lists both gaps, but there is still no dedicated issue or
PR for either benchmark.

## Recent closed-issue / tracker updates

- **#404** deferrable unique constraints - **covered** in current
  pg-delta; exact tracker
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#366** enum-arg function privilege signatures - **covered** in
  current pg-delta; exact tracker
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#412** `UNIQUE NULLS NOT DISTINCT` on table constraints - now
  **covered** in current pg-delta; benchmark [020](020-unique-constraint-nulls-not-distinct.md)
  is retained as a historical record
- **#499** child-specific column elements on `PARTITION OF` create -
  still **not covered in current behavior**, but now tracked under the open
  umbrella fidelity issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [021](021-partition-child-column-overrides.md)
- **#501** PostgreSQL 18 `VIRTUAL` generated columns - still **not covered in
  current behavior**, but now tracked under the open umbrella fidelity issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [022](022-virtual-generated-columns.md)
- **#506** new-table FK before standalone unique index - **covered** in
  current pg-delta; benchmark [023](023-fk-before-standalone-unique-index.md)
  is retained as a historical record
- draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444) still have no
  exact pg-toolbelt issue or PR

## Upstream watch list

- pgschema PRs [#517](https://github.com/pgplex/pgschema/pull/517) and
  [#520](https://github.com/pgplex/pgschema/pull/520) remain open, and
  both still stay in the **not parity work for pg-delta** bucket
- pg-toolbelt `main` now advances beyond the 2026-08-11 clean-room baseline to
  `17bfd13b49e94d4e073154921df738707fd03d87`; focused probes on that newer head
  did not change the active behavioral gap set
- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) is now the
  important tracker context for benchmarks **021** / **022**
- recent open pg-toolbelt PRs
  [#399](https://github.com/supabase/pg-toolbelt/pull/399),
  [#400](https://github.com/supabase/pg-toolbelt/pull/400), and
  [#401](https://github.com/supabase/pg-toolbelt/pull/401) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022** or open pgschema issues **#534** / **#535** / **#536** / **#537**

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by
  the automation scripts.
