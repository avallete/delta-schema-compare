# Parity refresh report - 2026-06-30

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `c281905f82d91a9bcf6c764ac4b1792cdf42ba04`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-29 refresh.

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

## 2) Upstream delta on 2026-06-30

The only upstream code-head movement in this refresh came from pgschema:

- pgschema [#492](https://github.com/pgplex/pgschema/pull/492) merged:
  `dump --qualify-schema` for
  [#321](https://github.com/pgplex/pgschema/issues/321)
- pgschema [#494](https://github.com/pgplex/pgschema/pull/494) merged:
  docs for the same `--qualify-schema` feature

That means:

- pgschema [#321](https://github.com/pgplex/pgschema/issues/321) moved from the
  still-open reviewed set to **resolved / not_parity**
- new pgschema
  [#493](https://github.com/pgplex/pgschema/issues/493) opened as a follow-up on
  preserving schema identity for type references under `--qualify-schema`

Issue #493 was screened as **not parity work for pg-delta**. It is a follow-up
on pgschema's dump-only qualification mode, not a live-catalog diff or
migration-planning gap. Duplicate checks against current pg-toolbelt issues and
PRs found no exact pg-toolbelt tracker for #493, and none is needed because the
scenario does not map to pg-delta parity work.

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
  - the remaining trigger enabled / disabled state slice is still **tracked
    in-flight** by open
    [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
  - no new pg-toolbelt tracker should be drafted while #285 remains open

## 4) What changed in this refresh

The benchmark matrix itself did not move. The real June 30 delta was state
reconciliation around the pgschema dump-qualification work:

- advance the checked-in `repos/pgschema` submodule from
  `c0e697343afc6116a393df68f14e9a4aee773365` to
  `c281905f82d91a9bcf6c764ac4b1792cdf42ba04`
- move pgschema #321 from `review-memory.open` to `review-memory.resolved` with
  verdict `not_parity`
- add new open pgschema issue #493 to `review-memory.open` with verdict
  `not_parity`
- refresh the current-review fingerprints for the still-open screened issues
  (#49, #52, #84, #450) and the still-relevant tracked / not-covered resolved
  items (#366, #404, #412, #439, #444)
- keep benchmark 020 / pgschema #412 as the only active resolved-issue gap

## 5) Validation notes

This refresh validated the state using:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `python3 -m pip install -r requirements.txt`
- `cd repos/pg-toolbelt && bun install --frozen-lockfile`
- targeted GitHub reads for:
  - pgschema issues #321 and #493
  - pg-toolbelt issues #218 and #219
  - pg-toolbelt PRs #285 and #291
  - updated-since-2026-06-29 issue/PR scans on both upstream repos
- focused pg-delta unit coverage:

```bash
cd repos/pg-toolbelt
export PATH="$HOME/.bun/bin:$PATH"
bun test \
  packages/pg-delta/src/core/objects/index/index.diff.test.ts \
  packages/pg-delta/src/core/objects/rls-policy/changes/rls-policy.alter.test.ts \
  packages/pg-delta/src/core/objects/trigger/changes/trigger.alter.test.ts \
  packages/pg-delta/src/core/objects/table/table.diff.test.ts \
  packages/pg-delta/src/core/plan/sql-format/format-trigger-quoted-name.test.ts
```

Result: **41 pass / 0 fail**.

- repository-local validation:

```bash
python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark
python3 -m json.tool benchmark/review-memory.json >/dev/null
TOKEN="$(env -u GITHUB_TOKEN gh auth token)"
GITHUB_TOKEN="$TOKEN" DRY_RUN=true python3 scripts/compare_issues.py
GITHUB_TOKEN="$TOKEN" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py
```

Results:

- `tests.test_review_memory` + `tests.test_compare_resolved_benchmark`:
  **9 tests passed**
- `benchmark/review-memory.json` parsed cleanly
- both dry-run compare scripts still returned **0 issues**, which remains
  expected because the scripts filter on upstream `Bug` / `Feature` labels and
  the parity-relevant pgschema items are still mostly unlabeled

I did **not** rerun the older containerized benchmark-020 diff probe in this
refresh. `pg-delta` itself did not change, and the new pgschema head only adds
`--qualify-schema` dump behavior plus docs. The latest exact runtime evidence
for benchmark 020 therefore remains the 2026-06-24 focused probe already cited
in the benchmark file, which still returned a zero-change diff for `UNIQUE`
table constraints toggled to `UNIQUE NULLS NOT DISTINCT`.
