# Parity refresh report - 2026-07-27

This report records the 2026-07-27 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`b732ce6b45eb9f3344ba3fc531ee28822730362e`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-26.md`](./parity-refresh-2026-07-26.md).

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

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
- pgschema [#506](https://github.com/pgplex/pgschema/issues/506):
  new-table FK ordered before a standalone unique index on the referenced table
  - benchmark file:
    [`benchmark/023-fk-before-standalone-unique-index.md`](../benchmark/023-fk-before-standalone-unique-index.md)
  - no matching pg-toolbelt issue or PR was found through this refresh

## 2) Upstream delta on 2026-07-27

This refresh found **no new upstream code-head or issue-state delta** relative
to the 2026-07-26 sweep:

- `pgschema` `main` still remains `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still remains `b732ce6b45eb9f3344ba3fc531ee28822730362e`
- the current open pgschema issue set remains
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#493](https://github.com/pgplex/pgschema/issues/493) remains open
  and still **not parity work** for pg-delta; merged
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514) only extends
  dump-side same-schema type qualification under `--qualify-schema`, and the
  remaining function / procedure signature slices are still upstream-only work
- pgschema [#518](https://github.com/pgplex/pgschema/issues/518) remains
  **not parity work** for pg-delta; the reported false diff depends on
  pgschema's temp comparison database resolving extension-owned types under a
  different schema than the real target, while pg-delta diffs live catalogs
  directly, can emit `ALTER EXTENSION ... SET SCHEMA`, and already roundtrips
  non-public pgvector types in
  `packages/pg-delta/tests/integration/extension-operations.test.ts`
- pgschema [#519](https://github.com/pgplex/pgschema/issues/519) remains
  **not parity work** for pg-delta; the repeated diff depends on pgschema's
  desired-state temp schema plus qualifier normalization, while pg-delta
  extracts live view definitions via `pg_get_viewdef(...)`, isolates
  `search_path`, and does not diff against a temporary planning schema
- no pgschema issues closed upstream since the 2026-07-26 refresh
- no pgschema PRs merged upstream since the 2026-07-26 refresh
- no pg-toolbelt issues or PRs updated since the 2026-07-26 refresh
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- the standing live `pg-toolbelt/main` delta still consists of the privilege
  diff fix in merged [#357](https://github.com/supabase/pg-toolbelt/pull/357),
  adjacent pg-topo ordering work in merged
  [#361](https://github.com/supabase/pg-toolbelt/pull/361), and release commit
  [#363](https://github.com/supabase/pg-toolbelt/pull/363); that delta remains
  adjacent to benchmarks **020** through **023** rather than fixing them
- direct duplicate probes still found no exact pg-toolbelt issue or PR for
  benchmarks **020** through **023**, the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), or open pgschema issue
  [#519](https://github.com/pgplex/pgschema/issues/519)

## 3) What changed in this refresh

The benchmark matrix itself did not move. The 2026-07-27 delta is just
state-rollforward with unchanged conclusions:

- add this report as the 2026-07-27 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot now records the
  unchanged 2026-07-27 state rather than the previous 2026-07-26 delta wording
- refresh `benchmark/review-memory.json` review timestamps for the rechecked
  open issues, exact tracked parity issues, active benchmark gaps, and older
  draft-only uncovered findings that were compared against current pg-delta
- leave the benchmark matrix unchanged because benchmarks **020** through
  **023** still have no exact pg-toolbelt issue or PR, and open pgschema issues
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519) do not change current
  parity conclusions
- leave the checked-in `repos/pg-toolbelt` submodule pointer unchanged at
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`; the standing live `main` delta is
  unchanged from 2026-07-26 and remains adjacent privilege / topo work rather
  than a fix for benchmarks **020** through **023** or the exact parity
  trackers [#218](https://github.com/supabase/pg-toolbelt/issues/218) /
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git -C repos/pgschema fetch origin main`
- `git -C repos/pg-toolbelt fetch origin main`
- direct GitHub issue / PR checks for:
  - the unchanged open pgschema issue set
  - closed pgschema issues updated since 2026-07-26 (**none**)
  - merged pgschema PRs since 2026-07-26 (**none**)
  - pg-toolbelt issues and PRs updated since 2026-07-26 (**none**)
  - the exact open pg-toolbelt parity trackers
    [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
    [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- exact-reference / keyword duplicate probes on pg-toolbelt for:
  - benchmarks **020** through **023**
  - older draft-only gaps **#439** / **#444**
  - open pgschema issue **#519**
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
  returned **0 issues found**
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  returned **0 resolved issues found**
- those dry-run script results remain expected because the parity-relevant
  pgschema items are still mostly missing the upstream `Bug` / `Feature`
  labels that the automation filters on, including open issues
  [#518](https://github.com/pgplex/pgschema/issues/518) and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- `git diff --check`
