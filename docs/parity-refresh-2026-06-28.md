# Parity refresh report - 2026-06-28

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `c0e697343afc6116a393df68f14e9a4aee773365`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-26 refresh.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Still active in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR was found through this refresh
  - benchmark 020 remains the only active resolved-issue gap

## 2) Open-issue screening refresh

No newly-filed or newly-updated open pgschema issues landed after the
2026-06-26 refresh.

### Still-open reviewed pgschema issues

- pgschema [#49](https://github.com/pgplex/pgschema/issues/49):
  explicit rename / refactor workflow proposal
  - **not parity work** for pg-delta
- pgschema [#52](https://github.com/pgplex/pgschema/issues/52):
  explicit before / after SQL file execution in plan output
  - **not parity work** for pg-delta
- pgschema [#84](https://github.com/pgplex/pgschema/issues/84):
  feedback / testimonial collection thread
  - **not parity work** for pg-delta
- pgschema [#321](https://github.com/pgplex/pgschema/issues/321):
  dump without schema-qualifier shortening
  - **not parity work** for pg-delta
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450):
  missing role blocks plan/apply
  - **not parity work** for pg-delta

Because there was no upstream issue-state movement, `benchmark/review-memory.json`
was intentionally left unchanged in this pass.

## 3) Existing tracked and draft-only items

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - still resolved upstream
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - still closed upstream as `not_planned`
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - adjacent pg-toolbelt issue / PR
    [#308](https://github.com/supabase/pg-toolbelt/issues/308) /
    [#310](https://github.com/supabase/pg-toolbelt/pull/310) remain
    **non-duplicates**; they cover `REVOKE EXECUTE ... FROM PUBLIC`, not the
    enum-typed signature drift from pgschema #366
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still closed upstream
  - still no exact pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - still closed upstream
  - related but non-exact pg-toolbelt work still exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - there is still no exact tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  trigger comments, trigger enabled/disabled state, and sequence comments
  - still **partially covered** in current pg-delta
  - trigger comments and sequence comments remain covered
  - trigger enabled / disabled state still lacks an exact pg-delta tracker
  - the draft-only pg-delta issue body remains in
    [`docs/parity-issue-drafts-2026-06-19.md`](./parity-issue-drafts-2026-06-19.md)

## 4) Fresh pg-toolbelt activity checked for duplicate avoidance

The only upstream movement since the 2026-06-26 refresh was fresh pg-toolbelt
PR activity. These PRs were checked and do **not** change the parity matrix:

- [#301](https://github.com/supabase/pg-toolbelt/issues/301) /
  [#305](https://github.com/supabase/pg-toolbelt/pull/305) now cover
  materialized-view definition stability under differing `search_path` values.
  This is adjacent to historical materialized-view parity work, but it is not
  an exact duplicate of benchmark 008, benchmark 020, or the current draft-only
  candidates
- [#304](https://github.com/supabase/pg-toolbelt/issues/304) /
  [#313](https://github.com/supabase/pg-toolbelt/pull/313) cover leading enum
  value insert ordering. No matching pgschema benchmark or screened issue
  currently maps to this exact scenario
- [#311](https://github.com/supabase/pg-toolbelt/issues/311) /
  [#314](https://github.com/supabase/pg-toolbelt/pull/314) cover mutual inline
  foreign-key cycles in declarative apply. This is useful adjacent dependency
  work, but it is not an exact duplicate of benchmark 020 or the current
  draft-only items #439 / #444 / #479
- [#315](https://github.com/supabase/pg-toolbelt/pull/315) is the RED,
  pg-delta-next test companion to
  [#307](https://github.com/supabase/pg-toolbelt/pull/307); it does not affect
  the current-engine parity benchmark state

## 5) Validation notes

- live upstream head checks on 2026-06-28 confirmed there is **no code-head
  delta** versus the 2026-06-26 refresh; both repos remain at the same SHAs
- `bun test packages/pg-delta/src/core/objects/index/index.diff.test.ts packages/pg-delta/src/core/objects/rls-policy/changes/rls-policy.alter.test.ts packages/pg-delta/src/core/objects/trigger/changes/trigger.alter.test.ts packages/pg-delta/src/core/objects/table/table.diff.test.ts packages/pg-delta/src/core/plan/sql-format/format-trigger-quoted-name.test.ts`
  passed (`41 pass`, `0 fail`)
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  passed (`9` tests)
- `python3 -m json.tool benchmark/review-memory.json >/dev/null` succeeded
- `GITHUB_TOKEN="$(env -u GITHUB_TOKEN gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py`
  returned zero items
- `GITHUB_TOKEN="$(env -u GITHUB_TOKEN gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  returned zero items
- both dry-run scripts still filter on upstream `Bug` / `Feature` labels, so
  the manual unlabeled-issue sweep remains necessary for this repository
