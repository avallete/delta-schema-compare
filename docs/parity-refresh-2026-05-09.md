# Parity refresh report — 2026-05-09

This report summarizes the latest manual parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `102ef99ae5aabb29510d48b39fbb8ecee34f5458`)

## 1) Benchmark refresh

The benchmark snapshot checked into the repo was stale relative to the current
submodule SHAs. This refresh updates the benchmark matrix and the historical
writeups that had drifted away from current pg-delta behavior.

### Newly confirmed as solved in current pg-delta

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) — `ALTER COLUMN TYPE ... USING`
- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) — function signature replacement
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) — serial / identity transitions
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) — trigger `UPDATE OF <columns>`
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) — unique index `NULLS NOT DISTINCT`
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) — temporal `WITHOUT OVERLAPS` / `PERIOD`
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) — column-less `CHECK (FALSE) NO INHERIT`

### Newly benchmarked unresolved historical gap

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412) — table-level
  `UNIQUE NULLS NOT DISTINCT` constraints
  - Recorded as benchmark item
    [`020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - Distinct from the already-solved **index** case in benchmark item 016
  - No matching pg-toolbelt issue or PR was found during this refresh

## 2) Open pgschema issue screening

### Already tracked in pg-toolbelt (do not duplicate)

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) — tracked by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) — tracked by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Covered in current pg-delta (no duplicate tracker drafted)

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362) — numeric precision changes
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401) — `RETURNS SETOF <table>` dependency ordering
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408) — quoted or reserved type names in emitted SQL
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415) — materialized-view drop relkind mismatch
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416) — custom aggregates missing from dump
- pgschema [#427](https://github.com/pgplex/pgschema/issues/427) — schema-qualified functions in RLS policy expressions

### Watch items / not yet drafted

- pgschema [#414](https://github.com/pgplex/pgschema/issues/414) — new-column
  plus view ordering
  - pgschema fix PR [#417](https://github.com/pgplex/pgschema/pull/417) is
    still open
  - did not draft a duplicate pg-toolbelt issue during this refresh
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420) —
  `varchar(n)[]` length modifier dump bug
  - no duplicate pg-toolbelt issue drafted yet
  - needs a pg-delta-specific failing repro before it is worth tracking

### Not parity work for pg-delta

- pgschema [#418](https://github.com/pgplex/pgschema/issues/418) —
  `CREATE INDEX CONCURRENTLY` on partitioned parents
  - specific to pgschema's online-DDL rewrite behavior
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421) — quoted
  mixed-case FK columns in temp-schema roundtrip
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422) — quoted
  mixed-case custom types in temp-schema roundtrip
- pgschema [#406](https://github.com/pgplex/pgschema/issues/406),
  [#407](https://github.com/pgplex/pgschema/issues/407),
  [#409](https://github.com/pgplex/pgschema/issues/409) — `.pgschemaignore`
  follow-ups

## 3) Closed-issue notes outside the benchmark matrix

- pgschema [#410](https://github.com/pgplex/pgschema/issues/410) — covered in
  current pg-delta via `format_type(...)`-backed type extraction
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423) — covered in
  current pg-delta via table persistence support (`UNLOGGED`)

## 4) Duplicate-avoidance summary

- No duplicate pg-toolbelt issue was drafted for pgschema #404 or #366 because
  they are already tracked by pg-toolbelt #218 and #219.
- pgschema #412 was **not** treated as a duplicate of benchmark item 016,
  because #412 is about the **table-constraint** form and 016 is about the
  **index** form.
- pgschema #414 was left as a watch item rather than drafted immediately while
  the upstream pgschema fix PR remains open.

## 5) Automation note

The current automation scripts still filter pgschema issues by `Bug` / `Feature`
labels. Several parity-relevant issues in this refresh are unlabeled, so a
manual GitHub issue and PR sweep remains necessary.
