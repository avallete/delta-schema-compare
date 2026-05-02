# Parity refresh report — 2026-05-02

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`)

## 1) Benchmark issue status refresh

The benchmark now tracks ten historical parity scenarios.

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

### Still tracked as open parity work

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404): `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - tracked by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function privilege signatures with enum-typed arguments
  - tracked by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### New unresolved historical benchmark gap

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412): table-level `UNIQUE NULLS NOT DISTINCT`
  - fixed in pgschema by [#413](https://github.com/pgplex/pgschema/pull/413)
  - no corresponding pg-toolbelt issue/PR found
  - benchmark entry added as `benchmark/020-unique-constraint-nulls-not-distinct.md`

## 2) Open pgschema candidate screening

### Covered in current pg-delta

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric precision changes
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401): table/function dependency ordering
- pgschema [#414](https://github.com/pgplex/pgschema/issues/414): add-column + dependent-view ordering
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415): materialized-view replacement emits wrong drop kind
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416): aggregate objects missing from dump / schema model

### Already tracked

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### No duplicate pg-toolbelt issue drafted

- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom / reserved type names in rendered DDL
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420): `varchar(n)[]` typmod preservation
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421): quoted mixed-case FK identifiers
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422): quoted mixed-case custom type names

These were not drafted because current pg-delta already relies on
`format_type(...)` and `quote_ident(...)`-backed catalog strings in the relevant
models, so the pgschema failures are not evidence of a matching pg-delta parity
gap on today's tree.

### Not parity work for pg-delta

- pgschema [#406](https://github.com/pgplex/pgschema/issues/406)
- pgschema [#407](https://github.com/pgplex/pgschema/issues/407)
- pgschema [#409](https://github.com/pgplex/pgschema/issues/409)

Those are `.pgschemaignore` feature requests / follow-ups specific to pgschema's
own schema-management surface area.

### Out of scope as a direct parity tracker

- pgschema [#418](https://github.com/pgplex/pgschema/issues/418): `CREATE INDEX CONCURRENTLY` on partitioned parents

This is a pgschema-specific rewrite / online-DDL policy issue rather than a
clear pg-delta parity gap based on today's pg-delta behavior and architecture.

## 3) Notes

- The benchmark matrix in `benchmark/README.md` is now the primary source of
  truth for solved vs unresolved historical scenarios.
- Historical benchmark markdown files were refreshed where they still claimed a
  missing pg-delta feature that is now merged and regression-tested.
- Draft text for the new unresolved historical gap (#412) is stored in
  `docs/parity-issue-drafts-2026-05-02.md`.
