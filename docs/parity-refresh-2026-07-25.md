# Parity refresh report - 2026-07-25

This report records the 2026-07-25 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`)
- checked-in `pg-delta` baseline (`repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`)
- live `pg-toolbelt` `main` (`b732ce6b45eb9f3344ba3fc531ee28822730362e`)

## 1) Benchmark status refresh

This refresh found **no benchmark-matrix delta** versus
[`docs/parity-refresh-2026-07-24.md`](./parity-refresh-2026-07-24.md).

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

## 2) Upstream delta on 2026-07-25

- `pgschema` `main` still remains `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- checked-in `pg-delta` remains
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, but live `pg-toolbelt` `main`
  advanced to `b732ce6b45eb9f3344ba3fc531ee28822730362e`
- the current open pgschema issue set now includes
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493), and
  [#518](https://github.com/pgplex/pgschema/issues/518)
- pgschema [#493](https://github.com/pgplex/pgschema/issues/493) remains
  **open** and still **not parity work** for pg-delta. Merged
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514) remains the most
  recent upstream code change here, but it only extends dump-side
  `--qualify-schema` handling for same-schema type references; the remaining
  function / procedure parameter and return-type slices are still outstanding
  upstream and still do not change current pg-delta parity classification
- new open pgschema
  [#518](https://github.com/pgplex/pgschema/issues/518) is **not parity work**
  for pg-delta. The reported false diff depends on pgschema's temp comparison
  database resolving extension-owned types under a different schema than the
  real target, while pg-delta diffs live catalogs directly, already roundtrips
  extension-owned types in non-public schemas, and can model real extension
  schema moves via `ALTER EXTENSION ... SET SCHEMA`
- exact open pg-toolbelt trackers still remain only
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pg-toolbelt [#308](https://github.com/supabase/pg-toolbelt/issues/308) is
  now **closed** by merged
  [#357](https://github.com/supabase/pg-toolbelt/pull/357), and merged
  [#358](https://github.com/supabase/pg-toolbelt/pull/358) plus still-open
  [#310](https://github.com/supabase/pg-toolbelt/pull/310) remain useful
  adjacent function-privilege work without replacing
  [#219](https://github.com/supabase/pg-toolbelt/issues/219); their scope is
  `REVOKE EXECUTE ... FROM PUBLIC`, not the enum-typed function signature drift
  from pgschema [#366](https://github.com/pgplex/pgschema/issues/366)
- direct issue / PR rechecks confirm
  [#286](https://github.com/supabase/pg-toolbelt/issues/286),
  [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#333](https://github.com/supabase/pg-toolbelt/issues/333),
  [#339](https://github.com/supabase/pg-toolbelt/issues/339),
  [#340](https://github.com/supabase/pg-toolbelt/issues/340),
  [#344](https://github.com/supabase/pg-toolbelt/issues/344),
  [#346](https://github.com/supabase/pg-toolbelt/issues/346), and open PRs
  [#299](https://github.com/supabase/pg-toolbelt/pull/299),
  [#305](https://github.com/supabase/pg-toolbelt/pull/305),
  [#313](https://github.com/supabase/pg-toolbelt/pull/313),
  [#314](https://github.com/supabase/pg-toolbelt/pull/314), and
  [#316](https://github.com/supabase/pg-toolbelt/pull/316) remain adjacent
  rather than exact duplicates for benchmarks **020** through **023** or the
  older draft-only gaps
  [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) What changed in this refresh

- add this report as the 2026-07-25 latest-state sweep
- refresh `benchmark/README.md` so the source-of-truth snapshot records the new
  open pgschema issue [#518](https://github.com/pgplex/pgschema/issues/518),
  the live `pg-toolbelt/main` advance to `b732ce6b45eb9f3344ba3fc531ee28822730362e`,
  and the updated pg-toolbelt [#308](https://github.com/supabase/pg-toolbelt/issues/308) /
  [#357](https://github.com/supabase/pg-toolbelt/pull/357) /
  [#358](https://github.com/supabase/pg-toolbelt/pull/358) /
  [#310](https://github.com/supabase/pg-toolbelt/pull/310) state
- add an open-issue review-memory entry for pgschema
  [#518](https://github.com/pgplex/pgschema/issues/518) with a `not_parity`
  verdict so future refreshes do not rediscover it as a net-new candidate
- leave the benchmark matrix unchanged because benchmarks **020** through
  **023** still have no exact pg-toolbelt issue or PR and none of the new live
  pg-delta commits target those scenarios
- leave the checked-in `repos/pg-toolbelt` submodule pointer unchanged at
  `c0decd173d191bc470bf7b8c8dd3e862f08ae398`; the live `main` delta in this
  refresh is adjacent privilege / topo work rather than a fix for benchmarks
  **020** through **023** or the exact parity trackers
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) /
  [#219](https://github.com/supabase/pg-toolbelt/issues/219)

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct GitHub issue / PR checks for:
  - the current open pgschema issue set, including
    [#518](https://github.com/pgplex/pgschema/issues/518)
  - recent merged pgschema PRs
  - pg-toolbelt issues **#218**, **#219**, **#286**, **#308**, **#332**,
    **#333**, **#339**, **#340**, **#344**, and **#346**
  - pg-toolbelt PRs **#299**, **#305**, **#310**, **#313**, **#314**,
    **#316**, **#357**, and **#358**
- direct submodule-head checks confirming:
  - checked-in `repos/pgschema` == live `origin/main`
  - checked-in `repos/pg-toolbelt` != live `origin/main`
    (`c0decd173d191bc470bf7b8c8dd3e862f08ae398` vs
    `b732ce6b45eb9f3344ba3fc531ee28822730362e`)
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  (**9 tests**, pass)
- `cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && bun install --frozen-lockfile`
- `cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && bun test packages/pg-delta/src/core/objects/procedure/procedure.diff.test.ts packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  (**39 tests**, pass)
- `cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && sudo -E env "PATH=$PATH" bun test --timeout 30000 packages/pg-delta/tests/integration/revoke-execute-from-public.test.ts`
  (**12 tests**, pass)
- `cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && sudo -E env "PATH=$PATH" bun test packages/pg-delta/tests/integration/extension-operations.test.ts`
  (**6 tests**, pass)
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true python3 scripts/compare_issues.py`
  returned **0 issues found**
- `GITHUB_TOKEN="<remote-token>" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  returned **0 resolved issues found**
- those dry-run script results remain expected because the parity-relevant
  pgschema items are still mostly missing the upstream `Bug` / `Feature`
  labels that the automation filters on, including new open issue
  [#518](https://github.com/pgplex/pgschema/issues/518)
- `git diff --check`
