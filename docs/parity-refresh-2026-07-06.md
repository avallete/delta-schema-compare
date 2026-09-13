# Parity refresh report - 2026-07-06

This report records the 2026-07-06 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `d2410fc47267a5c623e62ad4f78edeeee0106e71`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark issue status refresh

This refresh **does** change the benchmark matrix versus 2026-07-05.

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

Benchmark 022 is new in this refresh because pgschema #501 is now closed
upstream, while current pg-delta still collapses the generated-column kind and
serializes the PostgreSQL 18 case as `... STORED`.

## 2) Upstream delta on 2026-07-06

This refresh had a pgschema code-head delta but no pg-delta head delta:

- `git submodule update --remote --merge` advanced `pgschema` from
  `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2` to
  `d2410fc47267a5c623e62ad4f78edeeee0106e71`
- `git submodule update --remote --merge` kept `pg-delta` at
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`

Targeted GitHub reads showed:

- [#501](https://github.com/pgplex/pgschema/issues/501) is now **closed** by
  merged [#503](https://github.com/pgplex/pgschema/pull/503) and remains
  **not covered** in current pg-delta, so it is now benchmarked as **022**
- [#502](https://github.com/pgplex/pgschema/issues/502) remains **open** and
  remains **not parity work for pg-delta**
- the highest live pgschema issue number is still **#502**; no newer issue
  numbers exist yet

On the pg-toolbelt side, no exact tracker-state delta was found in this window:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  remains open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  remains open
- no exact pg-toolbelt issue / PR exists yet for benchmark **020**,
  benchmark **021**, benchmark **022**, resolved pgschema
  [#439](https://github.com/pgplex/pgschema/issues/439), or resolved pgschema
  [#444](https://github.com/pgplex/pgschema/issues/444)

## 3) Executed pg-delta evidence for the active gaps

Focused local source-level probes against the checked-in pg-delta head produced:

```json
{
  "issue020_change_count": 0,
  "issue020_sql": [],
  "issue021_sql": "CREATE TABLE test_schema.orders_us PARTITION OF test_schema.orders FOR VALUES IN ('us')",
  "issue022_create_sql": "CREATE TABLE test_schema.users (first_name text, last_name text, full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED)",
  "issue022_alter_sql": [
    "ALTER TABLE test_schema.users ADD COLUMN full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED"
  ]
}
```

Interpretation:

- **#412 / benchmark 020** still diffs to **zero changes**, confirming that the
  table-constraint `NULLS NOT DISTINCT` modifier is still ignored
- **#499 / benchmark 021** still serializes only the bare
  `PARTITION OF ... FOR VALUES ...` statement, confirming that child-specific
  column overrides are still dropped
- **#501 / benchmark 022** still serializes generated columns as
  `... STORED` in both create and add-column paths, confirming that pg-delta
  does not yet preserve PostgreSQL 18 `VIRTUAL` generated-column semantics

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
- pgschema [#502](https://github.com/pgplex/pgschema/issues/502):
  `COMMENT ON COLUMN` misresolved when a table shares the target schema name
  - still **open**
  - still **not parity work for pg-delta**

## 5) What changed in this refresh

This refresh is a latest-state reconciliation pass with one new benchmarked
resolved gap:

- fast-forward this working branch from stale `master` to the existing
  2026-07-05 parity baseline from
  `origin/avallete-ia/schema-comparison-benchmark-fbe7`
- advance the checked-in `repos/pgschema` submodule pointer to
  `d2410fc47267a5c623e62ad4f78edeeee0106e71`
- update `benchmark/README.md` to the 2026-07-06 snapshot date and refresh the
  open / resolved screening narrative
- refresh the active notes in
  `benchmark/020-unique-constraint-nulls-not-distinct.md` and
  `benchmark/021-partition-child-column-overrides.md`
- add new benchmark file
  `benchmark/022-virtual-generated-columns.md`
- move `#501` from `review-memory.open` to `review-memory.resolved` and refresh
  the currently reviewed open / resolved entries touched by this pass to the new
  `pgschema` SHA
- keep the July 4 draft note for #501 as historical pre-promotion context in
  `docs/parity-issue-drafts-2026-07-04.md`
- add this dated report

## 6) Validation notes

This refresh validated the state using:

- dependency setup:

```bash
python3 -m pip install -r requirements.txt
export PATH="$HOME/.bun/bin:$PATH"
bun install --frozen-lockfile --cwd repos/pg-toolbelt
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
  - benchmark 022 PostgreSQL 18 `VIRTUAL` generated columns

- repository-local validation:

```bash
python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark
python3 -m json.tool benchmark/review-memory.json >/dev/null
TOKEN="$(python3 - <<'PY'
import subprocess, urllib.parse
url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
print(urllib.parse.urlsplit(url).password or '')
PY
)"
GITHUB_TOKEN="$TOKEN" DRY_RUN=true python3 scripts/compare_issues.py
GITHUB_TOKEN="$TOKEN" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py
git diff --check
```

Results:

- `tests.test_review_memory` + `tests.test_compare_resolved_benchmark`:
  **9 tests passed**
- `benchmark/review-memory.json` parsed cleanly
- `compare_issues.py` dry-run returned **0 issues**
- `compare_resolved.py` dry-run returned **0 resolved issues**
- `git diff --check` returned cleanly

As in prior refreshes, the two dry-run scripts still report zero because they
filter on upstream `Bug` / `Feature` labels while the parity-relevant pgschema
items remain mostly unlabeled. The manual unlabeled-issue sweep remains
necessary.
