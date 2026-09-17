# Parity refresh report - 2026-06-29

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `c0e697343afc6116a393df68f14e9a4aee773365`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-28 refresh.

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

## 2) No new upstream issue / PR activity

There is also no upstream code-head delta versus the 2026-06-28 refresh:

- `pgschema` remains at `c0e697343afc6116a393df68f14e9a4aee773365`
- `pg-delta` remains at `9284412d71635308ebb0c1537e0b0183d2cfa4da`

GitHub issue / PR searches for `updated:>=2026-06-28` returned no new results
for:

- pgschema issues
- pgschema PRs
- pg-toolbelt issues
- pg-toolbelt PRs

This refresh is therefore a pure state-reconciliation pass rather than a new
upstream-code snapshot.

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
  - related pg-toolbelt work exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - current pg-delta coverage is still only exact for the
    `ALTER COLUMN TYPE` + dependent-view ordering case, not this destructive
    `DROP COLUMN` ordering case
  - there is still no exact tracker, so the saved draft remains active context
    in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479):
  trigger comments, trigger enabled/disabled state, and sequence comments
  - still **partially covered** in current pg-delta
  - trigger comments and sequence comments remain covered on current `main`
  - the remaining trigger enabled / disabled state slice is now **tracked
    in-flight** by open
    [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
  - PR #285 now contains explicit trigger-state regressions plus
    `ALTER TABLE ... DISABLE TRIGGER ...` implementation work, so no new
    pg-toolbelt tracker should be drafted while it remains open
  - the older draft in
    [`docs/parity-issue-drafts-2026-06-19.md`](./parity-issue-drafts-2026-06-19.md)
    is retained as historical review context only

## 4) What changed in this refresh

The benchmark matrix itself did not move. The real June 29 delta was issue
classification hygiene:

- keep benchmark 020 / pgschema #412 as the only active resolved-issue gap
- keep pgschema #404 and #366 mapped to existing pg-toolbelt issues #218 / #219
- keep pgschema #439 and #444 as still-untracked draft-only candidates
- reclassify the remaining trigger enabled-state slice from pgschema PR #479 as
  **tracked by open pg-toolbelt PR #285**, instead of an untracked draft-only
  candidate

## 5) Validation notes

This refresh validated the state using:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `env -u GITHUB_TOKEN gh issue list -R pgplex/pgschema --state all --limit 30 --search 'updated:>=2026-06-28 sort:updated-desc' --json number,title,state,updatedAt,url`
- `env -u GITHUB_TOKEN gh pr list -R pgplex/pgschema --state all --limit 30 --search 'updated:>=2026-06-28 sort:updated-desc' --json number,title,state,updatedAt,url`
- `env -u GITHUB_TOKEN gh issue list -R supabase/pg-toolbelt --state open --limit 40 --search 'updated:>=2026-06-28 sort:updated-desc' --json number,title,updatedAt,url`
- `env -u GITHUB_TOKEN gh pr list -R supabase/pg-toolbelt --state all --limit 50 --search 'updated:>=2026-06-28 sort:updated-desc' --json number,title,state,updatedAt,url`
- targeted `gh issue view` / `gh pr view` reads for pgschema #444, pgschema PR #479,
  pg-toolbelt #218, #219, #263, and pg-toolbelt PRs #273, #285, #291, and #315
- repository-local source/test searches confirming:
  - benchmark 020 still has no exact table-constraint integration coverage
  - current pg-delta mainline coverage is exact for the `ALTER COLUMN TYPE`
    dependent-view case, but not for the destructive `DROP COLUMN` case from
    pgschema #444
  - the trigger enabled-state slice from pgschema PR #479 is now represented by
    direct in-flight work in open pg-toolbelt PR #285
