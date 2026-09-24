# Parity refresh report - 2026-08-08

This report records the 2026-08-08 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`)
- checked-in `pg-delta` (`repos/pg-toolbelt` @ `2929e83981fee139772cc1c60255f1b2592a6f3a`)
- live `pg-delta/main` (`repos/pg-toolbelt` remote head @
  `2929e83981fee139772cc1c60255f1b2592a6f3a`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-08-07.md`](./parity-refresh-2026-08-07.md).

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, and **023** remain solved in current pg-delta

### Active resolved-issue benchmark gaps

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#499](https://github.com/pgplex/pgschema/issues/499):
  child-specific column overrides in `PARTITION OF` create path
  - benchmark file:
    [`benchmark/021-partition-child-column-overrides.md`](../benchmark/021-partition-child-column-overrides.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
- pgschema [#501](https://github.com/pgplex/pgschema/issues/501):
  PostgreSQL 18 `VIRTUAL` generated columns
  - benchmark file:
    [`benchmark/022-virtual-generated-columns.md`](../benchmark/022-virtual-generated-columns.md)
  - no matching pg-toolbelt issue or PR was found through this refresh

## 2) Upstream delta on 2026-08-08

This refresh found **one new open upstream issue without changing either the
checked-in code heads or the active benchmark matrix**:

- the checked-in `pg-delta` pointer still matches live `pg-toolbelt/main` at
  `2929e83981fee139772cc1c60255f1b2592a6f3a`
- checked-in/live `pgschema` also remain
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`
- new open pgschema issue
  [#534](https://github.com/pgplex/pgschema/issues/534)
  ("Self-referencing FK to a non-PK UNIQUE constraint is always inlined in
  `CREATE TABLE`") is already **covered** in current pg-delta:
  - pg-delta never inlines table FKs into `CREATE TABLE`; it creates the table
    first and adds constraints later
  - a focused 2026-08-08 pg17 runtime probe emitted the dependency-safe order:
    `CREATE TABLE` ->
    `ALTER TABLE ... ADD CONSTRAINT parent_orgs_pkey PRIMARY KEY` ->
    `CREATE UNIQUE INDEX parent_orgs_external_key_key` ->
    `ALTER TABLE ... ADD CONSTRAINT fk_self_migrated_from FOREIGN KEY`
  - the generated plan applied cleanly and left zero remaining changes
  - there is still no exact pg-toolbelt issue or PR to update because the
    current default-branch engine already converges on the scenario
- the open pgschema issue set is now
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518),
  [#519](https://github.com/pgplex/pgschema/issues/519), and
  [#534](https://github.com/pgplex/pgschema/issues/534)
- open pgschema parity-relevant PRs remain
  [#517](https://github.com/pgplex/pgschema/pull/517) and
  [#520](https://github.com/pgplex/pgschema/pull/520)
- exact open pg-toolbelt parity trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- adjacent pg-toolbelt work remains unchanged in parity terms:
  open [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains the
  `feat/pg-delta-next` cutover PR, while merged
  [#379](https://github.com/supabase/pg-toolbelt/pull/379),
  [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
  [#381](https://github.com/supabase/pg-toolbelt/pull/381) remain on
  `feat/pg-delta-next`, not on the current default-branch engine

Direct duplicate-search probes still found **no exact pg-toolbelt issue or PR**
for:

- active benchmarks **020**, **021**, and **022**
- the older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444)
- the new covered open issue
  [#534](https://github.com/pgplex/pgschema/issues/534)
- the earlier closed ordering issues
  [#530](https://github.com/pgplex/pgschema/issues/530) and
  [#532](https://github.com/pgplex/pgschema/issues/532)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-08-08 delta is:

- refresh `benchmark/README.md` so the source-of-truth snapshot records the new
  open covered issue [#534](https://github.com/pgplex/pgschema/issues/534)
  while keeping the active gaps unchanged
- refresh `benchmark/review-memory.json` for the expanded open issue set,
  including the new covered issue
  [#534](https://github.com/pgplex/pgschema/issues/534)
- add this report as the 2026-08-08 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set including
    [#534](https://github.com/pgplex/pgschema/issues/534)
  - still-open pgschema PRs
    [#517](https://github.com/pgplex/pgschema/pull/517) and
    [#520](https://github.com/pgplex/pgschema/pull/520)
  - the exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - adjacent pg-toolbelt work
    [#285](https://github.com/supabase/pg-toolbelt/pull/285),
    [#299](https://github.com/supabase/pg-toolbelt/pull/299),
    [#379](https://github.com/supabase/pg-toolbelt/pull/379),
    [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
    [#381](https://github.com/supabase/pg-toolbelt/pull/381)
- duplicate-search queries for benchmarks **020** through **022**, the
  draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), and the new open
  issue [#534](https://github.com/pgplex/pgschema/issues/534)
- a focused Docker-backed pg-delta probe showing pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534) is already covered:
  the pg17 plan emitted `CREATE UNIQUE INDEX parent_orgs_external_key_key`
  before `ADD CONSTRAINT fk_self_migrated_from FOREIGN KEY`, applied cleanly,
  and left zero remaining changes
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- those dry-run script runs still remain expected to return **0** parity items
  because the parity-relevant pgschema issues are still mostly missing the
  upstream `Bug` / `Feature` labels that the automation filters on, including
  open issues [#518](https://github.com/pgplex/pgschema/issues/518),
  [#519](https://github.com/pgplex/pgschema/issues/519), and
  [#534](https://github.com/pgplex/pgschema/issues/534)
- `git diff --check`
