# Parity refresh report - 2026-07-01

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `c281905f82d91a9bcf6c764ac4b1792cdf42ba04`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-06-30 refresh.

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

## 2) Upstream delta on 2026-07-01

There is no upstream code-head delta versus the 2026-06-30 refresh:

- `git submodule update --remote --merge` kept `pgschema` at
  `c281905f82d91a9bcf6c764ac4b1792cdf42ba04`
- `git submodule update --remote --merge` kept `pg-delta` at
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`

Targeted GitHub reads for updates after `2026-06-30T07:16:01Z` found no newer
pgschema issue or PR activity. On the pg-toolbelt side, the only newer PR
activity is open
[#307](https://github.com/supabase/pg-toolbelt/pull/307)
(`feat(pg-delta-next): orderless declarative apply, grouped export,
formatting, redaction`), updated at `2026-06-30T18:43:06Z`. That is adjacent
next-engine work rather than an exact duplicate of any current benchmark or
draft-only parity item.

## 3) Existing tracked and draft-only items

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - latest check: still `OPEN`, last updated `2026-06-18T20:04:11Z`
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - latest check: still `OPEN`, last updated `2026-04-22T17:38:52Z`
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
  - latest check: PR #285 is still `OPEN`, `mergeStateStatus=BEHIND`, updated
    `2026-06-17T07:51:30Z`
  - no new pg-toolbelt tracker should be drafted while #285 remains open

## 4) What changed in this refresh

This is a latest-state reconciliation pass rather than a parity-state change:

- advance `benchmark/README.md` to the 2026-07-01 snapshot date
- refresh the July note in
  `benchmark/020-unique-constraint-nulls-not-distinct.md`
- refresh `reviewed_at` for the active `benchmark/review-memory.json` entries:
  `#49`, `#52`, `#84`, `#450`, `#493`, `#366`, `#404`, `#412`, `#439`, `#444`
- add this dated report

No verdicts changed in this refresh.

## 5) Validation notes

This refresh validated the state using:

- `python3 -m pip install -r requirements.txt`
- `cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && bun install --frozen-lockfile`
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
- `compare_issues.py` dry-run returned **0 issues**
- `compare_resolved.py` dry-run returned **0 resolved issues**

As in prior refreshes, the two dry-run scripts still report zero because they
filter on upstream `Bug` / `Feature` labels while the parity-relevant pgschema
items remain mostly unlabeled. The manual unlabeled-issue sweep remains
necessary.
