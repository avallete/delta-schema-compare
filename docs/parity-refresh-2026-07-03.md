# Parity refresh report - 2026-07-03

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `20e272b2364a0d79ba400f35f2fb59aa1fbf7714`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

There is no benchmark-matrix parity delta versus the 2026-07-02 refresh.

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

## 2) Upstream delta on 2026-07-03

This refresh **did** have an upstream code-head delta:

- `git submodule update --remote --merge` advanced `pgschema` from
  `c281905f82d91a9bcf6c764ac4b1792cdf42ba04` to
  `20e272b2364a0d79ba400f35f2fb59aa1fbf7714`
- `git submodule update --remote --merge` kept `pg-delta` at
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`

Targeted GitHub reads after `2026-07-02T07:00:33Z` found three new
partitioning-related pgschema updates:

- [#495](https://github.com/pgplex/pgschema/issues/495), closed by merged
  [#497](https://github.com/pgplex/pgschema/pull/497)
- [#496](https://github.com/pgplex/pgschema/issues/496), still open with
  in-flight [#498](https://github.com/pgplex/pgschema/pull/498)
- [#499](https://github.com/pgplex/pgschema/issues/499), an open low-impact
  follow-up on child-specific column elements for `PARTITION OF`

On the pg-toolbelt side, there was no material exact-match tracker delta in
this window:

- no new issues created
- no new PRs created
- no issues closed
- no PRs merged

That means the current exact parity trackers remain unchanged:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pgschema PR [#479](https://github.com/pgplex/pgschema/pull/479) trigger
  enabled / disabled state ->
  [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)

## 3) Newly screened partitioning items

### pgschema #495 — covered

pgschema issue [#495](https://github.com/pgplex/pgschema/issues/495) reports
that pgschema `apply` created partition-child PK / UNIQUE constraints as local
instead of inherited clones, causing perpetual no-op churn on the next plan.

Current pg-delta already models the convergent behavior:

- `table.model.ts` marks partition-cloned constraints using `coninhcount > 0`
- `table.diff.ts` skips clone/local churn when the constraint name and
  definition already match

Focused local runtime evidence from a direct `diffTables(...)` probe:

```json
{
  "issue495_change_count": 0,
  "issue495_change_types": []
}
```

Verdict: **covered**. No new benchmark file or pg-toolbelt tracker is needed.

### pgschema #496 — covered

pgschema issue [#496](https://github.com/pgplex/pgschema/issues/496) reports
that pgschema created partition children as detached standalone tables instead
of `PARTITION OF ... FOR VALUES ...`.

Current pg-delta already covers the base attach path:

- `table.model.ts` extracts `parent_schema`, `parent_name`, and
  `partition_bound`
- `table.create.ts` emits `CREATE TABLE ... PARTITION OF ... FOR VALUES ...`
- existing roundtrip coverage remains in
  `packages/pg-delta/tests/integration/table-operations.test.ts`

Focused local runtime evidence from a direct `CreateTable` probe:

```json
{
  "issue496_sql": "CREATE TABLE test_schema.events_2025 PARTITION OF test_schema.events FOR VALUES IN (2025)"
}
```

Verdict: **covered**. No duplicate tracker should be drafted while pgschema
works through [#498](https://github.com/pgplex/pgschema/pull/498).

### pgschema #499 — not covered

pgschema issue [#499](https://github.com/pgplex/pgschema/issues/499) is the
follow-up to #496 / #498: after the base `PARTITION OF` create path is fixed,
pgschema still needs child-specific column `WITH OPTIONS` elements such as
per-child defaults or `NOT NULL` overrides.

Current pg-delta still drops that child-specific slice:

- `table.create.ts` returns early for partition children and serializes only
  the bare `PARTITION OF ... FOR VALUES ...` form
- the created-table branch in `table.diff.ts` does not add follow-up column
  alters to recover the missing child-specific metadata

Focused local runtime evidence from a direct `CreateTable` probe:

```json
{
  "issue499_sql": "CREATE TABLE test_schema.measurements_2024 PARTITION OF test_schema.measurements FOR VALUES IN (2024)"
}
```

The child-column override was omitted entirely.

Verdict: **not covered**. No exact pg-toolbelt issue or PR exists yet, so the
draft-only tracker text is now saved in
[`docs/parity-issue-drafts-2026-07-03.md`](./parity-issue-drafts-2026-07-03.md).

## 4) Existing tracked and draft-only items

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still closed upstream
  - still no exact pg-toolbelt issue or PR found
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - still closed upstream
  - related pg-toolbelt work exists in
    [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
    [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
    [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
    [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open)
  - there is still no exact tracker
- pgschema PR [#479](https://github.com/pgplex/pgschema/pull/479):
  trigger comments, trigger enabled/disabled state, and sequence comments
  - still **partially covered** in current pg-delta
  - the remaining trigger enabled / disabled state slice is still **tracked
    in-flight** by open
    [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
- pgschema [#499](https://github.com/pgplex/pgschema/issues/499):
  child-specific column elements on `PARTITION OF` create
  - new **draft-only** open parity finding in this refresh
  - no exact pg-toolbelt issue / PR exists yet

## 5) What changed in this refresh

This refresh is a latest-state reconciliation pass with one new draft-only
open parity finding:

- advance the checked-in `repos/pgschema` submodule pointer to
  `20e272b2364a0d79ba400f35f2fb59aa1fbf7714`
- update `benchmark/README.md` to the 2026-07-03 snapshot date and add the
  new partitioning screening outcomes
- refresh the July note in
  `benchmark/020-unique-constraint-nulls-not-distinct.md`
- refresh `reviewed_at` / fingerprints for the active
  `benchmark/review-memory.json` entries and add new entries for
  `#495`, `#496`, and `#499`
- add this dated report
- add the new draft-only tracker note at
  `docs/parity-issue-drafts-2026-07-03.md`

The benchmark matrix itself does **not** change in this refresh: benchmark 020
remains the only active resolved-issue gap.

## 6) Validation notes

This refresh validated the state using:

- `python3 -m pip install -r requirements.txt`
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- `cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && bun install --frozen-lockfile`
- focused pg-delta unit coverage:

```bash
cd repos/pg-toolbelt
export PATH="$HOME/.bun/bin:$PATH"
bun test \
  packages/pg-delta/src/core/objects/table/changes/table.create.test.ts \
  packages/pg-delta/src/core/objects/table/table.diff.test.ts
```

Result: **29 pass / 0 fail**.

- focused local pg-delta probes (no Docker required) covering:
  - partition child `PARTITION OF` create serialization
  - partition child local-vs-clone UNIQUE constraint convergence
  - child-specific `PARTITION OF` column-element omission
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

This runner does not currently have Docker binaries available (`docker: command
not found`), so container-backed pg-delta integration tests were not runnable
in this pass. The focused serializer / diff probes above provide the
highest-signal executed evidence for the new partitioning findings without
requiring Docker.
