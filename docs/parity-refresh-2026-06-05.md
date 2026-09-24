# Parity refresh report - 2026-06-05

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `592c19c95b06830255b45bc4d80eeacd62e7e727`)
- `pg-delta` (`repos/pg-toolbelt` @ `b9b8b157c23e08e9d8a9c7573718edcc06f603c3`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-06-04 refresh.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Still active in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR found during this refresh
  - current pg-delta still ignores this definition-only difference in the table
    constraint path (see validation note below)

## 2) Existing open pgschema issue refresh

There is no open-issue parity-state delta versus the 2026-06-04 refresh.

### Already tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Draft-only uncovered open candidates

- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - pg-delta still has related coverage and adjacent dependency-ordering work,
    but no exact `DROP COLUMN` + dependent-view regression or dedicated tracker
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

### Open items classified as not parity work

- pgschema [#449](https://github.com/pgplex/pgschema/issues/449): repeat plan
  drift for same-schema policy and CHECK expressions after apply
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450): missing role
  blocks plan and apply

No newer parity-relevant open pgschema issues appeared since the 2026-06-04
refresh.

## 3) Recently closed issue screening

No new parity-relevant pgschema closed issues or merged fix PRs landed since the
2026-06-04 refresh. The screened closed-item state remains unchanged:

- pgschema [#406](https://github.com/pgplex/pgschema/issues/406): indexes in
  `.pgschemaignore` remain not parity work for pg-delta
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom
  or reserved type names in plan output remain covered in current pg-delta
- pgschema [#410](https://github.com/pgplex/pgschema/issues/410): `name` typed
  columns remain covered in current pg-delta
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints remains not covered
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED`
  tables remain covered in current pg-delta
- pgschema [#426](https://github.com/pgplex/pgschema/issues/426): Docker Hub
  image lag remains not parity work for pg-delta
- pgschema [#445](https://github.com/pgplex/pgschema/issues/445): same-schema
  CHECK constraint qualifier drift remains not parity work for pg-delta
- pgschema [#446](https://github.com/pgplex/pgschema/issues/446): explicit
  `UNIQUE` constraints on `PRIMARY KEY` columns remain covered in current
  pg-delta

## 4) Validation notes

- `bun test packages/pg-delta/src/core/objects/table/table.diff.test.ts`
  passed on current `pg-delta@b9b8b157c23e08e9d8a9c7573718edcc06f603c3`,
  confirming the new upstream `NOT VALID` constraint diff behavior.
- A focused one-off Bun probe constructed two otherwise-identical table
  constraints whose only difference was `UNIQUE (a, b)` versus
  `UNIQUE NULLS NOT DISTINCT (a, b)`. The current diff code returned:

  ```json
  {
    "changeCount": 0,
    "sql": []
  }
  ```

  That reproduces the unresolved benchmark 020 behavior without needing a full
  Docker-backed integration environment.
- The automated `compare_issues.py` / `compare_resolved.py` dry runs still need
  to be interpreted alongside a manual unlabeled-issue sweep, because most of
  the current pgschema issues do not carry the `Bug` / `Feature` labels that
  those scripts filter on.
