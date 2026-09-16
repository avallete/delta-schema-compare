# Parity refresh report - 2026-08-11

This report records the 2026-08-11 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`)
- checked-in/live `pg-delta` (`repos/pg-toolbelt` @ `2247de05849455b358fae71bbe514273cae4faba`)

## 1) Benchmark status refresh

This refresh **changes** the benchmark matrix versus
[`docs/parity-refresh-2026-08-09.md`](./parity-refresh-2026-08-09.md).

### Newly solved in pg-delta

- benchmark **020** / pgschema
  [#412](https://github.com/pgplex/pgschema/issues/412) now converges on
  current pg-delta
  - the focused 2026-08-11 pg17 proof emitted:
    - `DROP CONSTRAINT pgschema_repro_nulls_uniq`
    - `ADD CONSTRAINT pgschema_repro_nulls_uniq UNIQUE NULLS NOT DISTINCT (a, b)`
  - the plan proved cleanly with zero drift
  - benchmark [020](../benchmark/020-unique-constraint-nulls-not-distinct.md)
    moves to **Solved in pg-delta**

### Active resolved-issue benchmark gaps

- pgschema [#499](https://github.com/pgplex/pgschema/issues/499):
  child-specific column overrides in `PARTITION OF` create path
  - benchmark file:
    [021](../benchmark/021-partition-child-column-overrides.md)
  - the focused 2026-08-11 pg17 probe still emitted only
    `CREATE TABLE ... PARTITION OF ... FOR VALUES ...`
  - the child-local `priority DEFAULT 10` and `notes NOT NULL` overrides
    were still omitted
  - the current proof loop still returned `proofOk: true`, so the missing
    overrides are not being surfaced as end-to-end drift yet
- pgschema [#501](https://github.com/pgplex/pgschema/issues/501):
  PostgreSQL 18 `VIRTUAL` generated columns
  - benchmark file:
    [022](../benchmark/022-virtual-generated-columns.md)
  - the focused 2026-08-11 pg18 probe still emitted
    `GENERATED ALWAYS AS (...) STORED`
  - the current proof loop still returned `proofOk: true`, so the engine is
    also collapsing the `VIRTUAL` / `STORED` distinction away in its
    current fact/proof path

## 2) Upstream delta on 2026-08-11

The important upstream change since the 2026-08-09 refresh is on the
pg-delta side:

- checked-in/live `pg-delta` advanced from
  `2929e83981fee139772cc1c60255f1b2592a6f3a` to
  `2247de05849455b358fae71bbe514273cae4faba`
- that new default-branch head includes merged
  [pg-toolbelt#299](https://github.com/supabase/pg-toolbelt/pull/299)
  plus the 2026-08-09 alpha release
  [pg-toolbelt#397](https://github.com/supabase/pg-toolbelt/pull/397)
- checked-in/live `pgschema` remained
  `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`

Current open pgschema issue set:

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

Newly changed open-issue findings:

- new open pgschema issue
  [#536](https://github.com/pgplex/pgschema/issues/536)
  (foreign-key drop ordering) is already **covered** in current pg-delta:
  the focused 2026-08-11 pg17 probe emitted
  `DROP CONSTRAINT` -> `DROP COLUMN` -> `DROP TABLE`, proved cleanly, and
  left zero drift
- earlier open issues
  [#534](https://github.com/pgplex/pgschema/issues/534) and
  [#535](https://github.com/pgplex/pgschema/issues/535) remain **covered**
  in current pg-delta on the new default-branch engine
- exact pg-toolbelt parity trackers
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219) are now both
  **closed**; their exact scenarios
  [#404](https://github.com/pgplex/pgschema/issues/404) and
  [#366](https://github.com/pgplex/pgschema/issues/366) also converge on
  current pg-delta
- there is currently **no exact open pg-toolbelt issue or PR** for the
  remaining active benchmarks **021** / **022**, the draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), or the covered
  open issues **#534** / **#535** / **#536**
- open pgschema PRs
  [#517](https://github.com/pgplex/pgschema/pull/517) and
  [#520](https://github.com/pgplex/pgschema/pull/520) remain **not parity
  work for pg-delta**

## 3) What changed in this refresh

The 2026-08-11 delta is:

- advance the checked-in pg-delta submodule pointer to the new default-
  branch engine at `2247de05849455b358fae71bbe514273cae4faba`
- refresh `benchmark/README.md` to record benchmark **020** as solved,
  keep **021** / **022** active, add open covered issue **#536**, and drop
  the stale `#218` / `#219` tracker language
- refresh benchmark files [020](../benchmark/020-unique-constraint-nulls-not-distinct.md),
  [021](../benchmark/021-partition-child-column-overrides.md), and
  [022](../benchmark/022-virtual-generated-columns.md) so their current
  pg-delta status sections match the new clean-room engine rather than the
  pre-rewrite architecture
- refresh `benchmark/review-memory.json` for:
  - benchmark **020** -> `covered`
  - benchmarks **021** / **022** -> still `not_covered` on the new head
  - resolved coverage trackers **#404** / **#366** -> now `covered`
  - open covered issues **#534** / **#535** refreshed to the new head
  - new open covered issue **#536** added
- add this report as the 2026-08-11 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set including
    [#534](https://github.com/pgplex/pgschema/issues/534),
    [#535](https://github.com/pgplex/pgschema/issues/535), and
    [#536](https://github.com/pgplex/pgschema/issues/536)
  - the still-open pgschema PRs
    [#517](https://github.com/pgplex/pgschema/pull/517) and
    [#520](https://github.com/pgplex/pgschema/pull/520)
  - the now-closed pg-toolbelt trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - the merged pg-toolbelt clean-room rewrite
    [#299](https://github.com/supabase/pg-toolbelt/pull/299) and release
    [#397](https://github.com/supabase/pg-toolbelt/pull/397)
- duplicate-search queries for the remaining active benchmarks **021** /
  **022**, the draft-only gaps **#439** / **#444**, and the covered open
  issues **#534** / **#535** / **#536**
- a focused Docker-backed pg17/pg18 pg-delta probe script covering:
  - benchmark **020** / pgschema **#412** -> now covered
  - benchmark **021** / pgschema **#499** -> still uncovered
  - benchmark **022** / pgschema **#501** -> still uncovered
  - pgschema **#404** -> covered (`DEFERRABLE INITIALLY DEFERRED` preserved)
  - pgschema **#366** -> covered (enum-arg function privilege signatures stay stable, no temp-schema leak)
  - pgschema **#534** -> covered (safe unique-index-before-FK order)
  - pgschema **#535** -> covered (safe table-before-domain order)
  - pgschema **#536** -> covered (safe drop ordering)
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
- those dry-run script runs still remain expected to return **0** parity
  items because the parity-relevant pgschema issues are still mostly
  missing the upstream `Bug` / `Feature` labels that the automation filters
  on, including open issues **#518**, **#519**, **#534**, **#535**, and
  **#536**
- `git diff --check`
