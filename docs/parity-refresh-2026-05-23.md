# Parity refresh report - 2026-05-23

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `ee9385daf75f72d443882020247ffd2599050090`)

## 1) Benchmark issue status refresh

The benchmark now tracks ten core parity scenarios. Their current state after
refreshing the submodules and upstream issue mappings is:

### Solved in pg-delta

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) ->
  pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130)
  closed, replacement PR
  [#231](https://github.com/supabase/pg-toolbelt/pull/231) merged
- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) ->
  pg-toolbelt issue [#132](https://github.com/supabase/pg-toolbelt/issues/132)
  closed, PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) merged
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) ->
  pg-toolbelt issue [#133](https://github.com/supabase/pg-toolbelt/issues/133)
  closed, PR [#149](https://github.com/supabase/pg-toolbelt/pull/149) merged
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) ->
  pg-toolbelt issue [#138](https://github.com/supabase/pg-toolbelt/issues/138)
  closed, PR [#154](https://github.com/supabase/pg-toolbelt/pull/154) merged
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) ->
  pg-toolbelt issue [#140](https://github.com/supabase/pg-toolbelt/issues/140)
  closed, PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) merged
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) ->
  pg-toolbelt issue [#183](https://github.com/supabase/pg-toolbelt/issues/183)
  closed, PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) merged
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) ->
  pg-toolbelt issue [#182](https://github.com/supabase/pg-toolbelt/issues/182)
  closed, PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) merged
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) ->
  pg-toolbelt issue [#184](https://github.com/supabase/pg-toolbelt/issues/184)
  closed, PR [#187](https://github.com/supabase/pg-toolbelt/pull/187) merged
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) ->
  pg-toolbelt issue [#198](https://github.com/supabase/pg-toolbelt/issues/198)
  closed, PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) merged

### Not yet covered in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - No matching pg-toolbelt issue or PR found during this refresh.
  - Added benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)

## 2) Existing open pgschema issue refresh

### Covered in pg-delta

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric
  precision changes
  - Evidence: `alter-table-operations.test.ts` contains roundtrip coverage for
    `numeric(8,2) -> numeric(12,4)` changes and default-safe type changes.
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401):
  `RETURNS SETOF <table>` dependency ordering
  - Evidence:
    `table-function-dependency-ordering.test.ts` and
    `table-function-circular-dependency.test.ts`.
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom
  or reserved type names in plan output
  - Evidence: pg-delta stores `data_type_str` from `format_type(...)` for
    columns and already has quoted custom-type coverage in
    `type-operations.test.ts`.

### Already tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - Existing tracker:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - Existing tracker:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Newly screened uncovered open candidates

- pgschema [#427](https://github.com/pgplex/pgschema/issues/427):
  schema-qualified functions in RLS policy expressions
  - No matching pg-toolbelt issue or PR found during this refresh.
  - Draft-only issue text saved in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - No matching pg-toolbelt issue or PR found during this refresh.
  - Draft-only issue text saved in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)

### Open candidates not escalated to draft issues yet

- pgschema [#420](https://github.com/pgplex/pgschema/issues/420):
  `varchar(n)[]` typmod preservation
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421): quoted
  mixed-case foreign-key column names
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422): quoted
  mixed-case custom types

These three scenarios still need exact roundtrip confirmation against the
current pg-delta submodule. The current source path looks closer to correct
than pgschema's dump/plan path, but there is not enough local evidence yet to
promote them into benchmark entries or pg-toolbelt issue drafts.

## 3) Recent resolved pgschema issue screening

- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED`
  tables
  - Covered in pg-delta's table persistence handling:
    `relpersistence` extraction plus `SET UNLOGGED` / `SET LOGGED` diff tests.

## 4) Notes

- Benchmark item **005** moved from tracked to solved because pg-toolbelt PR
  [#231](https://github.com/supabase/pg-toolbelt/pull/231) merged and closed
  issue [#130](https://github.com/supabase/pg-toolbelt/issues/130).
- Two older benchmark-linked pg-toolbelt issues finally caught up to the merged
  fix state and are now closed: [#132](https://github.com/supabase/pg-toolbelt/issues/132)
  and [#182](https://github.com/supabase/pg-toolbelt/issues/182).
- The benchmark now has one active resolved-issue parity gap:
  [`020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md).
