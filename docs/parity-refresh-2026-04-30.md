# Parity refresh report - 2026-04-30

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `67029213ea0e6e734849abfef4f051f8c3e02a5b`)

## 1) Benchmark issue status refresh

The historical benchmark now tracks ten parity scenarios.

### Solved in pg-delta

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) -> pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130), PR [#231](https://github.com/supabase/pg-toolbelt/pull/231) merged
- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) -> pg-toolbelt issue [#132](https://github.com/supabase/pg-toolbelt/issues/132), PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) merged
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) -> pg-toolbelt issue [#133](https://github.com/supabase/pg-toolbelt/issues/133), PR [#149](https://github.com/supabase/pg-toolbelt/pull/149) merged
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) -> pg-toolbelt issue [#138](https://github.com/supabase/pg-toolbelt/issues/138), PR [#154](https://github.com/supabase/pg-toolbelt/pull/154) merged
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) -> pg-toolbelt issue [#140](https://github.com/supabase/pg-toolbelt/issues/140), PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) merged
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) -> pg-toolbelt issue [#183](https://github.com/supabase/pg-toolbelt/issues/183), PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) merged
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) -> pg-toolbelt issue [#182](https://github.com/supabase/pg-toolbelt/issues/182), PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) merged
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) -> pg-toolbelt issue [#184](https://github.com/supabase/pg-toolbelt/issues/184), PR [#187](https://github.com/supabase/pg-toolbelt/pull/187) merged
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) -> pg-toolbelt issue [#198](https://github.com/supabase/pg-toolbelt/issues/198), PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) merged

### Still tracked upstream

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Not covered yet

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412): table-level `UNIQUE NULLS NOT DISTINCT` constraints
  - Added as [benchmark 020](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - Drafted for future issue filing in
    [`docs/parity-issue-drafts-2026-04-30.md`](./parity-issue-drafts-2026-04-30.md)

## 2) Newly screened open pgschema issues

### Covered in pg-delta or no duplicate needed

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric precision changes
  - Evidence: `alter-table-operations.test.ts` covers numeric type changes.
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom / reserved type names in plan output
  - Evidence: pg-delta uses `format_type(...)`-backed extraction and preserves quoted type names.
- pgschema [#414](https://github.com/pgplex/pgschema/issues/414): views ordered before newly added columns
  - Evidence: `view-operations.test.ts` covers select-`*` view replacement, and `mixed-objects.test.ts` covers mixed add-column / replace-view ordering.
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415): materialized-view refactor emits `DROP VIEW`
  - Evidence: `materialized-view-operations.test.ts` covers drop / recreate of materialized views with dependent objects and uses `DROP MATERIALIZED VIEW`.
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416): custom aggregates missing from dump
  - Evidence: `aggregate-operations.test.ts` covers aggregate creation, drop, comments, and privileges.
- pgschema [#418](https://github.com/pgplex/pgschema/issues/418): `CREATE INDEX CONCURRENTLY` on partitioned parents
  - Evidence: pg-delta serializes partitioned-parent indexes without `CONCURRENTLY` and has partitioned-table index coverage.
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420): `varchar(n)[]` length modifier silently dropped in dump
  - Evidence: table-column extraction uses `format_type(a.atttypid, a.atttypmod)`.
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421): quoted mixed-case FK columns cannot be round-tripped
  - Not filed as a duplicate: this is specific to pgschema's dump + temp-schema roundtrip architecture.
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422): quoted mixed-case custom types cannot be round-tripped
  - Not filed as a duplicate: same temp-schema roundtrip architecture difference as #421.

### Already tracked upstream

- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): enum-arg function privileges -> tracked by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- pgschema [#404](https://github.com/pgplex/pgschema/issues/404): deferrable unique constraints -> tracked by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)

## 3) Recently closed pgschema issues

- pgschema [#410](https://github.com/pgplex/pgschema/issues/410): built-in `name` type dumped as `char[]`
  - Covered in pg-delta by `format_type(...)`-backed extraction.
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412): table-level `UNIQUE NULLS NOT DISTINCT`
  - Not covered in pg-delta today; benchmark 020 tracks the gap.
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED` tables dropped from definitions
  - Covered in pg-delta by table persistence support (`CREATE UNLOGGED TABLE`, `ALTER TABLE ... SET UNLOGGED`, `ALTER TABLE ... SET LOGGED`).

## 4) Notes

- Benchmark files 005, 007, 013, 015, 016, 017, and 019 were refreshed so
  their body text now matches the current pg-delta snapshot instead of the
  older pre-fix state.
- Benchmark 016 remains solved for standalone unique indexes; benchmark 020
  is intentionally separate because it covers the table-constraint path.
- The old draft PR for issue #130 ([pg-toolbelt#146](https://github.com/supabase/pg-toolbelt/pull/146)) was closed after the real merged fix landed in [pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231).
