# Parity refresh report - 2026-08-14

This report records the 2026-08-14 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `551e88b42977db673a7a9d74f7b7876c2a5e5377`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-13.md`](./parity-refresh-2026-08-13.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

### Focused runtime results on the new pg-delta head

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - focused 2026-08-14 pg17 probe still emitted only
    `CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')`
    plus owner reassignment
  - child-local `priority DEFAULT 10` and `notes NOT NULL` overrides were still
    omitted
  - the current proof loop still returned `proofOk: true` with zero drift, so
    the engine still does not surface those lost child-local overrides as
    diff-visible state end-to-end
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - focused 2026-08-14 pg18 probe still emitted
    `ALTER TABLE "test_schema"."users" ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED`
  - PostgreSQL 18 `VIRTUAL` is still collapsed to `STORED`
  - the current proof loop still returned `proofOk: true` with zero drift, so
    the model still collapses the generated-column kind strongly enough that
    proof cannot see the mismatch yet

## 2) Upstream delta on 2026-08-14

The important upstream change since the 2026-08-13 refresh is again on the
pg-delta side:

- checked-in/live `pg-delta` advanced from
  `17bfd13b49e94d4e073154921df738707fd03d87` to
  `551e88b42977db673a7a9d74f7b7876c2a5e5377`
- the new head is dominated by schema-first / plan-artifact work
  (not the benchmarked parity surfaces)
- checked-in/live `pgschema` remained
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`

Current open pgschema issue set relevant to this repo remains:

- [#49](https://github.com/pgplex/pgschema/issues/49)
- [#52](https://github.com/pgplex/pgschema/issues/52)
- [#84](https://github.com/pgplex/pgschema/issues/84)
- [#450](https://github.com/pgplex/pgschema/issues/450)
- [#493](https://github.com/pgplex/pgschema/issues/493)
- [#518](https://github.com/pgplex/pgschema/issues/518)
- [#519](https://github.com/pgplex/pgschema/issues/519)
- [#534](https://github.com/pgplex/pgschema/issues/534)
- [#535](https://github.com/pgplex/pgschema/issues/535)
- [#536](https://github.com/pgplex/pgschema/issues/536)
- [#537](https://github.com/pgplex/pgschema/issues/537)

### Open-issue findings rechecked on the new head

- [#534](https://github.com/pgplex/pgschema/issues/534) remains **covered**:
  focused 2026-08-14 pg17 probe emitted `CREATE UNIQUE INDEX` before the
  self-referencing FK `ADD CONSTRAINT`, proved cleanly, and left zero drift
- [#535](https://github.com/pgplex/pgschema/issues/535) remains **covered**:
  focused 2026-08-14 pg17 probe emitted
  `CREATE TABLE "public"."x" ()` before `CREATE DOMAIN "public"."y" AS public.x`,
  proved cleanly, and left zero drift
- [#536](https://github.com/pgplex/pgschema/issues/536) remains **covered**:
  focused 2026-08-14 pg17 probe emitted
  `DROP CONSTRAINT` -> `DROP COLUMN` -> `DROP TABLE`, proved cleanly, and left
  zero drift
- [#537](https://github.com/pgplex/pgschema/issues/537) remains **covered**:
  focused 2026-08-14 pg17 probe emitted
  `ALTER COLUMN "arfcn_dl" TYPE integer USING "arfcn_dl"::integer`,
  proved cleanly, and matches the solved benchmark family in
  [005](../benchmark/005-alter-column-type-using-clause.md)

### New upstream PR context

- open pgschema PR
  [#539](https://github.com/pgplex/pgschema/pull/539) now carries the upstream
  fix path for issue [#535](https://github.com/pgplex/pgschema/issues/535)
- open pgschema PRs
  [#517](https://github.com/pgplex/pgschema/pull/517) and
  [#520](https://github.com/pgplex/pgschema/pull/520) remain outside pg-delta
  parity scope

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
  relevant tracker context for active benchmarks **021** / **022**
- recent open pg-toolbelt PRs
  [#399](https://github.com/supabase/pg-toolbelt/pull/399),
  [#400](https://github.com/supabase/pg-toolbelt/pull/400),
  [#401](https://github.com/supabase/pg-toolbelt/pull/401),
  [#415](https://github.com/supabase/pg-toolbelt/pull/415), and
  [#418](https://github.com/supabase/pg-toolbelt/pull/418) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022** or open pgschema issues **#534** / **#535** / **#536** / **#537**
- there is still **no dedicated exact open pg-toolbelt issue or PR** for
  benchmark **021**, benchmark **022**, or the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

The 2026-08-14 delta is:

- advance the checked-in pg-delta submodule pointer to
  `551e88b42977db673a7a9d74f7b7876c2a5e5377`
- refresh `benchmark/README.md` to:
  - record the newer checked-in/live pg-delta head
  - keep the active gap set at **021** / **022**
  - note that open pgschema issue **#535** now has upstream PR
    [#539](https://github.com/pgplex/pgschema/pull/539)
  - extend the open pg-toolbelt PR watch list through
    [#418](https://github.com/supabase/pg-toolbelt/pull/418)
- refresh benchmark files
  [005](../benchmark/005-alter-column-type-using-clause.md),
  [021](../benchmark/021-partition-child-column-overrides.md), and
  [022](../benchmark/022-virtual-generated-columns.md)
- refresh `benchmark/review-memory.json` for:
  - the current open pgschema watch-list issue set on the new head
  - benchmark **021** / pgschema **#499** -> still `tracked`
  - benchmark **022** / pgschema **#501** -> still `tracked`
  - open covered issues **#534** / **#535** / **#536** / **#537**
- add this report as the 2026-08-14 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set including
    [#534](https://github.com/pgplex/pgschema/issues/534),
    [#535](https://github.com/pgplex/pgschema/issues/535),
    [#536](https://github.com/pgplex/pgschema/issues/536), and
    [#537](https://github.com/pgplex/pgschema/issues/537)
  - still-open pgschema PRs
    [#517](https://github.com/pgplex/pgschema/pull/517),
    [#520](https://github.com/pgplex/pgschema/pull/520), and
    [#539](https://github.com/pgplex/pgschema/pull/539)
  - open umbrella tracker
    [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  - current open pg-toolbelt PRs
    [#399](https://github.com/supabase/pg-toolbelt/pull/399),
    [#400](https://github.com/supabase/pg-toolbelt/pull/400),
    [#401](https://github.com/supabase/pg-toolbelt/pull/401),
    [#415](https://github.com/supabase/pg-toolbelt/pull/415), and
    [#418](https://github.com/supabase/pg-toolbelt/pull/418)
- duplicate-search review against the current open pg-toolbelt issue / PR lists
- focused Docker-backed pg17/pg18 pg-delta probes showing:
  - benchmark **021** / pgschema **#499** -> still behaviorally uncovered
  - benchmark **022** / pgschema **#501** -> still behaviorally uncovered
  - pgschema **#534** -> covered
  - pgschema **#535** -> covered
  - pgschema **#536** -> covered
  - pgschema **#537** -> covered
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `DRY_RUN=true python3 scripts/compare_issues.py`
- `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- those dry-run script runs still return **0** parity items because the
  parity-relevant pgschema issues are still mostly missing the upstream
  `Bug` / `Feature` labels that the automation filters on, including open
  issues **#518**, **#519**, **#534**, **#535**, **#536**, and **#537**
- `git diff --check`
