# Parity refresh report - 2026-08-13

This report records the 2026-08-13 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `17bfd13b49e94d4e073154921df738707fd03d87`)

## 1) Benchmark status refresh

This refresh found **no behavioral benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-11.md`](./parity-refresh-2026-08-11.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- the active resolved-issue benchmark gaps remain **021** and **022**

What *did* change is the pg-toolbelt issue mapping for those active gaps:

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499) is still behaviorally
  uncovered, but the current open umbrella fidelity tracker
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
  explicitly lists inherited-column local overrides on declarative partitions
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501) is still behaviorally
  uncovered, but the same open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
  explicitly lists PostgreSQL 17/18 virtual generated columns

### Focused runtime results on the new pg-delta head

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - focused 2026-08-13 pg17 probe still emitted only
    `CREATE TABLE "test_schema"."orders_us" PARTITION OF "test_schema"."orders" FOR VALUES IN ('us')`
    plus owner reassignment
  - child-local `priority DEFAULT 10` and `notes NOT NULL` overrides were still
    omitted
  - the current proof loop still returned `proofOk: true` with zero drift, so
    the engine is still not surfacing the lost child-local overrides as
    diff-visible state
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - focused 2026-08-13 pg18 probe still emitted
    `ALTER TABLE "test_schema"."users" ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED`
  - PostgreSQL 18 `VIRTUAL` is still collapsed to `STORED`
  - the current proof loop still returned `proofOk: true` with zero drift, so
    the model still collapses the generated-column kind strongly enough that
    proof cannot see the mismatch yet

## 2) Upstream delta on 2026-08-13

The important upstream change since the 2026-08-11 refresh is on the pg-delta
side:

- checked-in/live `pg-delta` advanced from
  `2247de05849455b358fae71bbe514273cae4faba` to
  `17bfd13b49e94d4e073154921df738707fd03d87`
- checked-in/live `pgschema` remained
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`

Current open pgschema issue set relevant to this repo:

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

### Newly screened open-issue finding

- new open pgschema issue
  [#537](https://github.com/pgplex/pgschema/issues/537)
  (`ALTER COLUMN TYPE` without `USING` for built-in text-like → numeric/boolean
  targets) is already **covered** in current pg-delta:
  - focused 2026-08-13 pg17 probe emitted
    `ALTER TABLE "public"."nokia_cell_info" ALTER COLUMN "arfcn_dl" TYPE integer USING "arfcn_dl"::integer`
  - the plan proved cleanly with zero drift
  - this matches the already-solved benchmark family in
    [005](../benchmark/005-alter-column-type-using-clause.md)

### Still-open covered pgschema issues re-checked on the new head

- [#534](https://github.com/pgplex/pgschema/issues/534) remains **covered**:
  focused 2026-08-13 pg17 probe emitted
  `CREATE TABLE` -> `CREATE UNIQUE INDEX` -> `ADD self FK`, proved cleanly, and
  left zero drift
- [#535](https://github.com/pgplex/pgschema/issues/535) remains **covered**:
  focused 2026-08-13 pg17 probe emitted
  `CREATE TABLE "public"."x" ()` before `CREATE DOMAIN "public"."y" AS public.x`,
  proved cleanly, and left zero drift
- [#536](https://github.com/pgplex/pgschema/issues/536) remains **covered**:
  focused 2026-08-13 pg17 probe emitted
  `DROP CONSTRAINT` -> `DROP COLUMN` -> `DROP TABLE`, proved cleanly, and left
  zero drift

### Current pg-toolbelt tracker / duplicate state

- open umbrella issue
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
  is now the relevant tracker context for active benchmarks **021** / **022**
- open pg-toolbelt issues
  [#330](https://github.com/supabase/pg-toolbelt/issues/330),
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#339](https://github.com/supabase/pg-toolbelt/issues/339),
  [#340](https://github.com/supabase/pg-toolbelt/issues/340), and
  [#344](https://github.com/supabase/pg-toolbelt/issues/344) remain useful
  current context, but none except the umbrella **#332** is even adjacent to
  the active benchmarks
- open pg-toolbelt PRs
  [#399](https://github.com/supabase/pg-toolbelt/pull/399),
  [#400](https://github.com/supabase/pg-toolbelt/pull/400), and
  [#401](https://github.com/supabase/pg-toolbelt/pull/401) are unrelated to the
  active benchmark gaps
- there is still **no dedicated exact open pg-toolbelt issue or PR** for
  benchmark **021**, benchmark **022**, or the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

The 2026-08-13 delta is:

- advance the checked-in pg-delta submodule pointer to
  `17bfd13b49e94d4e073154921df738707fd03d87`
- refresh `benchmark/README.md` to:
  - record the newer checked-in/live pg-delta head
  - add new open covered issue
    [#537](https://github.com/pgplex/pgschema/issues/537)
  - map active benchmarks **021** / **022** to open umbrella tracker
    [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
- refresh benchmark files
  [005](../benchmark/005-alter-column-type-using-clause.md),
  [021](../benchmark/021-partition-child-column-overrides.md), and
  [022](../benchmark/022-virtual-generated-columns.md)
- refresh `benchmark/review-memory.json` for:
  - the current open pgschema issue set, including new issue **#537**
  - benchmark **021** / pgschema **#499** -> now `tracked`
  - benchmark **022** / pgschema **#501** -> now `tracked`
  - open covered issues **#534** / **#535** / **#536** / **#537**
- add this report as the 2026-08-13 latest-state sweep

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
    [#517](https://github.com/pgplex/pgschema/pull/517) and
    [#520](https://github.com/pgplex/pgschema/pull/520)
  - open pg-toolbelt umbrella tracker
    [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  - current open pg-toolbelt PRs
    [#399](https://github.com/supabase/pg-toolbelt/pull/399),
    [#400](https://github.com/supabase/pg-toolbelt/pull/400), and
    [#401](https://github.com/supabase/pg-toolbelt/pull/401)
- duplicate-search review against the current open pg-toolbelt issue / PR lists
- focused Docker-backed pg-delta probes showing:
  - pgschema **#499** / benchmark **021** -> still behaviorally uncovered
  - pgschema **#501** / benchmark **022** -> still behaviorally uncovered
  - pgschema **#534** -> covered
  - pgschema **#535** -> covered
  - pgschema **#536** -> covered
  - pgschema **#537** -> covered
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- `git diff --check`
