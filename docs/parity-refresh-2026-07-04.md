# Parity refresh report - 2026-07-04

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

This refresh **does** change the benchmark matrix versus 2026-07-03.

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

Benchmark 021 is new in this refresh because pgschema #499 is now closed
upstream, while current pg-delta still drops the child-specific
`DEFAULT` / `NOT NULL` override slice.

## 2) Upstream delta on 2026-07-04

This refresh had a pgschema code-head delta but no pg-delta head delta:

- `git submodule update --remote --merge` advanced `pgschema` from
  `20e272b2364a0d79ba400f35f2fb59aa1fbf7714` to
  `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2`
- `git submodule update --remote --merge` kept `pg-delta` at
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`

Targeted GitHub reads showed:

- [#496](https://github.com/pgplex/pgschema/issues/496) is now **closed** by
  merged [#498](https://github.com/pgplex/pgschema/pull/498) and remains
  **covered** in current pg-delta
- [#499](https://github.com/pgplex/pgschema/issues/499) is now **closed** by
  merged [#500](https://github.com/pgplex/pgschema/pull/500) and remains
  **not covered** in current pg-delta, so it is now benchmarked as **021**
- [#501](https://github.com/pgplex/pgschema/issues/501) is newly **open** and
  appears **not covered** in current pg-delta; the finding is saved as a
  draft-only tracker in
  [`docs/parity-issue-drafts-2026-07-04.md`](./parity-issue-drafts-2026-07-04.md)
- [#502](https://github.com/pgplex/pgschema/issues/502) is newly **open** and
  remains **not parity work for pg-delta**

On the pg-toolbelt side, no exact tracker-state delta was found in this window:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  remains open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  remains open
- pgschema PR [#479](https://github.com/pgplex/pgschema/pull/479) trigger
  enabled / disabled state ->
  [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
  remains the exact in-flight tracker

## 3) Executed pg-delta evidence for the active gaps

Focused local source-level probes against the checked-in pg-delta head produced:

```json
{
  "issue020_change_count": 0,
  "issue020_sql": [],
  "issue021_sql": "CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')",
  "issue501_sql": "CREATE TABLE test_schema.users (first_name text, last_name text, full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED)"
}
```

Interpretation:

- **#412 / benchmark 020** still diffs to **zero changes**, confirming that the
  table-constraint `NULLS NOT DISTINCT` modifier is still ignored
- **#499 / benchmark 021** still serializes only the bare
  `PARTITION OF ... FOR VALUES ...` statement, confirming that child-specific
  column overrides are still dropped
- **#501** still serializes generated columns as `... STORED`, which matches the
  model-level evidence that pg-delta does not yet preserve PostgreSQL 18
  `VIRTUAL` generated-column semantics

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
- pgschema [#501](https://github.com/pgplex/pgschema/issues/501):
  PostgreSQL 18 `VIRTUAL` generated columns
  - new **draft-only** open parity finding in this refresh
  - no exact pg-toolbelt issue / PR exists yet

## 5) What changed in this refresh

This refresh is a latest-state reconciliation pass with one new benchmarked
resolved gap and one new draft-only open parity finding:

- advance the checked-in `repos/pgschema` submodule pointer to
  `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2`
- update `benchmark/README.md` to the 2026-07-04 snapshot date and refresh the
  open / resolved screening narrative
- refresh the July note in
  `benchmark/020-unique-constraint-nulls-not-distinct.md`
- add new benchmark file
  `benchmark/021-partition-child-column-overrides.md`
- move `#496` and `#499` from `review-memory.open` to
  `review-memory.resolved`, and add new open entries for `#501` / `#502`
- add the new draft-only tracker note at
  `docs/parity-issue-drafts-2026-07-04.md`
- add this dated report

## 6) Validation notes

This refresh validated the state using:

- dependency setup:

```bash
python3 -m pip install -r requirements.txt
cd repos/pg-toolbelt && export PATH="$HOME/.bun/bin:$PATH" && bun install --frozen-lockfile
```

- focused pg-delta unit coverage:

```bash
cd repos/pg-toolbelt
export PATH="$HOME/.bun/bin:$PATH"
bun test \
  packages/pg-delta/src/core/objects/table/changes/table.create.test.ts \
  packages/pg-delta/src/core/objects/table/table.diff.test.ts
```

Result: **29 pass / 0 fail**.

- focused local pg-delta probes covering:
  - benchmark 020 table-constraint `NULLS NOT DISTINCT`
  - benchmark 021 partition-child column overrides
  - draft-only #501 PostgreSQL 18 `VIRTUAL` generated columns

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

This runner still does not currently have Docker binaries available
(`docker: command not found`), so container-backed pg-delta integration tests
were not runnable in this pass. The focused table unit tests and direct
serializer / diff probes above provide the highest-signal executed evidence for
the July 4 parity changes without requiring Docker.
