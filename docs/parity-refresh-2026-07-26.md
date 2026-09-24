# Parity refresh report - 2026-07-26

This report records the 2026-07-26 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`b732ce6b45eb9f3344ba3fc531ee28822730362e`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-25.md`](./parity-refresh-2026-07-25.md).

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

## 2) Upstream delta on 2026-07-26

This refresh found **no new upstream code-head delta** relative to the
2026-07-25 sweep:

- `pgschema` `main` still remains `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, and live `pg-toolbelt` `main`
  still remains `b732ce6b45eb9f3344ba3fc531ee28822730362e`
- the current open pgschema issue set now includes
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- pgschema [#519](https://github.com/pgplex/pgschema/issues/519) is the net-new
  upstream item in this sweep. It remains **not parity work** for pg-delta:
  the repeated diff depends on pgschema's temporary desired-state schema and its
  qualifier-normalization path, while pg-delta extracts live view definitions
  via `pg_get_viewdef(...)`, isolates `search_path`, and does not diff against a
  temporary planning schema
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- direct issue / PR rechecks confirm pg-toolbelt
  [#308](https://github.com/supabase/pg-toolbelt/issues/308) remains closed by
  merged [#357](https://github.com/supabase/pg-toolbelt/pull/357), merged
  [#358](https://github.com/supabase/pg-toolbelt/pull/358) stays adjacent, and
  open [#310](https://github.com/supabase/pg-toolbelt/pull/310) still does not
  replace parity tracker [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- direct duplicate probes still found no exact pg-toolbelt issue or PR for
  benchmarks **020** through **023**, the older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) /
  [#444](https://github.com/pgplex/pgschema/issues/444), or the new open
  pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519)
- the closest adjacent regular-definition work is still
  [pg-toolbelt#301](https://github.com/supabase/pg-toolbelt/issues/301) /
  [#305](https://github.com/supabase/pg-toolbelt/pull/305), but that scope is
  materialized-view definition stability under differing `search_path` values,
  not regular-view normalization through pgschema's temporary desired-state
  schema

## 3) What changed in this refresh

The benchmark matrix itself did not move. The real 2026-07-26 delta is
state-reconciliation around the new upstream open issue:

- add this report as the 2026-07-26 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot records the new
  unlabeled open pgschema issue [#519](https://github.com/pgplex/pgschema/issues/519),
  the unchanged checked-in/live pg-delta split, and the unchanged exact
  pg-toolbelt tracker set
- add an open-issue review-memory entry for pgschema
  [#519](https://github.com/pgplex/pgschema/issues/519) with a `not_parity`
  verdict so future refreshes do not rediscover it as a net-new candidate
- leave the benchmark matrix unchanged because benchmarks **020** through
  **023** still have no exact pg-toolbelt issue or PR and the new open issue
  [#519](https://github.com/pgplex/pgschema/issues/519) does not change current
  parity conclusions
- leave the checked-in `repos/pg-toolbelt` submodule pointer unchanged at
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`; the standing live `main` delta is
  unchanged from 2026-07-25 and remains adjacent privilege / topo work rather
  than a fix for benchmarks **020** through **023** or the exact parity
  trackers [#218](https://github.com/supabase/pg-toolbelt/issues/218) /
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set, including new issue
    [#519](https://github.com/pgplex/pgschema/issues/519)
  - recent merged pgschema PRs
  - pg-toolbelt issues **#218**, **#219**, **#263**, **#286**, **#301**,
    **#304**, **#308**, **#311**, **#332**, **#333**, **#339**, **#340**,
    **#344**, and **#346**
  - pg-toolbelt PRs **#273**, **#285**, **#288**, **#299**, **#305**,
    **#307**, **#310**, **#313**, **#314**, **#315**, **#316**, **#350**,
    **#354**, **#355**, **#356**, **#357**, and **#358**
- exact-reference / keyword duplicate probes on pg-toolbelt for:
  - benchmarks **020** through **023**
  - older draft-only gaps **#439** / **#444**
  - new pgschema issue **#519**
- `sudo docker info`
- focused live pg-delta probe on `pg-toolbelt/main` with Docker-backed pg17 and
  `PGDELTA_SKIP_DUMMY_SECLABEL_BUILD=1`:

  ```bash
  cd repos/pg-toolbelt/packages/pg-delta/tests
  export PATH="$HOME/.bun/bin:$PATH"
  sudo -E env "PATH=$PATH" PGDELTA_SKIP_DUMMY_SECLABEL_BUILD=1 bun -e 'import { withDb } from "./utils.ts"; import { roundtripFidelityTest } from "./integration/roundtrip.ts"; await withDb(17, async (db) => { await roundtripFidelityTest({ mainSession: db.main, branchSession: db.branch, initialSetup: "CREATE EXTENSION IF NOT EXISTS ltree; CREATE TABLE public.categories (id integer, path ltree);", testSql: "CREATE VIEW public.categories_valid AS SELECT id FROM public.categories WHERE public.nlevel(path) = 8;" }); console.log("probe_issue_519:pass"); })();'
  ```

  Result: **`probe_issue_519:pass`**.

- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
  returned **0 issues found**
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  returned **0 resolved issues found**
- those dry-run script results remain expected because the parity-relevant
  pgschema items are still mostly missing the upstream `Bug` / `Feature`
  labels that the automation filters on, including new open issue
  [#519](https://github.com/pgplex/pgschema/issues/519)
- `git diff --check`
