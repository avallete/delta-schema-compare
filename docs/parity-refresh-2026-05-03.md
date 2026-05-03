# Parity refresh report - 2026-05-03

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`)

## 1) Benchmark refresh

The benchmark snapshot is now aligned to the latest submodule state.

### Solved historical benchmark scenarios

All previously tracked benchmark entries from the earlier refresh are now
solved in current pg-delta:

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) -> pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130), merged PR [#231](https://github.com/supabase/pg-toolbelt/pull/231)
- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) -> pg-toolbelt issue [#132](https://github.com/supabase/pg-toolbelt/issues/132), merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214)
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) -> pg-toolbelt issue [#133](https://github.com/supabase/pg-toolbelt/issues/133), merged PR [#149](https://github.com/supabase/pg-toolbelt/pull/149)
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) -> pg-toolbelt issue [#138](https://github.com/supabase/pg-toolbelt/issues/138), merged PR [#154](https://github.com/supabase/pg-toolbelt/pull/154)
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) -> pg-toolbelt issue [#140](https://github.com/supabase/pg-toolbelt/issues/140), merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200)
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) -> pg-toolbelt issue [#183](https://github.com/supabase/pg-toolbelt/issues/183), merged PR [#185](https://github.com/supabase/pg-toolbelt/pull/185)
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) -> pg-toolbelt issue [#182](https://github.com/supabase/pg-toolbelt/issues/182), merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213)
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) -> pg-toolbelt issue [#184](https://github.com/supabase/pg-toolbelt/issues/184), merged PR [#187](https://github.com/supabase/pg-toolbelt/pull/187)
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) -> pg-toolbelt issue [#198](https://github.com/supabase/pg-toolbelt/issues/198), merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212)

### New benchmark entry

A new historical gap has been added:

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412) - table-level
  `UNIQUE NULLS NOT DISTINCT` constraints. This is now benchmarked as
  [020](../benchmark/020-unique-constraint-nulls-not-distinct.md).

This gap is distinct from benchmark 016: standalone unique indexes with
`NULLS NOT DISTINCT` are solved in pg-delta, but the table-constraint form
still lacks dedicated diff coverage.

## 2) Open pgschema issue sweep

### Already tracked in pg-toolbelt (do not duplicate)

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Covered or not parity work (no duplicate tracker drafted)

- **Covered in current pg-delta:** #362, #401, #408, #414, #415, #416,
  #418, #420, #421, #422
- **Not parity work for pg-delta:** #406, #407, #409, #419 (`.pgschemaignore`
  surface area only)

## 3) Recent closed-issue sweep

- **#410** built-in `name` type dumped as `char[]` - no duplicate pg-toolbelt
  issue drafted; pg-delta uses `format_type(a.atttypid, a.atttypmod)` and
  serializes `data_type_str` directly.
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` - confirmed unresolved in
  pg-delta and added to the benchmark as entry 020.
- **#423** `UNLOGGED` dropped from table definitions - no duplicate
  pg-toolbelt issue drafted; pg-delta tracks `relpersistence`, serializes
  `CREATE UNLOGGED TABLE`, and diffs `LOGGED <-> UNLOGGED`.
- **#396** table-level CHECK constraints omitted from dump - covered by the
  current pg-delta constraint model and benchmark 019's focused tests.
- **#399** qualified references inside function bodies - not a pg-delta
  parity gap; specific to pgschema's temp-schema rewrite path.
- **#403** table row-type composite parameters in function validation - not
  a pg-delta parity gap; specific to pgschema's validation architecture.

## 4) Draft issue text for the unresolved gap

Draft tracker issue content for pgschema #412 is saved in:

- [`docs/parity-issue-drafts-2026-05-03.md`](./parity-issue-drafts-2026-05-03.md)

No pg-toolbelt issue or PR for the table-constraint variant was found during
this refresh.

## 5) Notes

- Benchmark 005 was the main status change from the previous refresh:
  pg-toolbelt issue #130 is now closed and the real fix landed in merged PR
  #231, while the earlier draft PR #146 was closed unmerged.
- Manual unlabeled-issue sweeps remain necessary. pgschema issues often ship
  without `Bug` / `Feature` labels, so the automation scripts can miss
  relevant parity work in dry-run unless the benchmark and screening notes
  are kept current.
