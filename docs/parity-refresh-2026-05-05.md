# Parity refresh report — 2026-05-05

This report summarizes the latest manual parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `9a0831a54e03d221f0461323ae93fb676722cc14`)

## 1) Benchmark status refresh

The benchmark now tracks ten historical parity scenarios.

### Solved in current pg-delta

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) — `ALTER COLUMN TYPE ... USING`
  - Evidence: `tests/integration/alter-table-operations.test.ts` now includes:
    - `change column type to enum with default`
    - `change varchar column type to integer with using cast`
    - `change column type from enum to text preserves default`
  - Source: `src/core/objects/table/changes/table.alter.ts` appends `USING ...` when `previousColumn.data_type_str` differs, and `table.diff.ts` passes `previousColumn: mainCol`.
  - Tracker state: pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130) is closed. PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) was closed without merge, but the behavior is present in current source/tests.

- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) — function signature changes require DROP+CREATE
  - Evidence: `tests/integration/function-operations.test.ts`
  - Source: `src/core/objects/procedure/procedure.diff.ts`
  - Tracker state: issue [#132](https://github.com/supabase/pg-toolbelt/issues/132) closed by merged PR [#214](https://github.com/supabase/pg-toolbelt/pull/214)

- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) — materialized view dependency chains
  - Evidence: `tests/integration/materialized-view-operations.test.ts` (`replace materialized view with dependent index and view`)
  - Tracker state: issue [#133](https://github.com/supabase/pg-toolbelt/issues/133) closed by merged PR [#149](https://github.com/supabase/pg-toolbelt/pull/149)

- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) — serial/identity transitions
  - Evidence: `tests/integration/sequence-operations.test.ts`
  - Source: `table.model.ts`, `table.diff.ts`, `table.alter.ts`
  - Tracker state: issue [#138](https://github.com/supabase/pg-toolbelt/issues/138) closed by merged PR [#154](https://github.com/supabase/pg-toolbelt/pull/154)

- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) — trigger `UPDATE OF` column lists
  - Evidence: `tests/integration/trigger-operations.test.ts`, `tests/integration/trigger-update-of-column-numbers.test.ts`
  - Tracker state: issue [#140](https://github.com/supabase/pg-toolbelt/issues/140) closed by merged PR [#200](https://github.com/supabase/pg-toolbelt/pull/200)

- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) — unique indexes with `NULLS NOT DISTINCT`
  - Evidence: `tests/integration/index-operations.test.ts`
  - Tracker state: issue [#183](https://github.com/supabase/pg-toolbelt/issues/183) closed by merged PR [#185](https://github.com/supabase/pg-toolbelt/pull/185)

- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) — PG18 temporal constraints
  - Evidence: `tests/integration/constraint-operations.test.ts`
  - Source: `table.model.ts` (`is_temporal`), `table.diff.ts`
  - Tracker state: issue [#182](https://github.com/supabase/pg-toolbelt/issues/182) closed by merged PR [#213](https://github.com/supabase/pg-toolbelt/pull/213)

- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) — cross-table RLS policy ordering
  - Evidence: `tests/integration/policy-dependencies.test.ts`
  - Tracker state: issue [#184](https://github.com/supabase/pg-toolbelt/issues/184) closed by merged PR [#187](https://github.com/supabase/pg-toolbelt/pull/187)

- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) — column-less `CHECK (FALSE) NO INHERIT`
  - Evidence: `tests/integration/constraint-operations.test.ts`
  - Tracker state: issue [#198](https://github.com/supabase/pg-toolbelt/issues/198) closed by merged PR [#212](https://github.com/supabase/pg-toolbelt/pull/212)

### Still unresolved historical benchmark item

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412) — table-level `UNIQUE NULLS NOT DISTINCT`
  - Added as new benchmark entry: [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - Why it remains open:
    - `AlterTableAddConstraint` serializes `constraint.definition` verbatim, so plain create/apply is likely fine.
    - However, `table.diff.ts` does **not** compare `constraint.definition`, and a regular `UNIQUE (a, b)` and `UNIQUE NULLS NOT DISTINCT (a, b)` constraint currently look identical to the structured comparator because `constraint_type`, `key_columns`, `deferrable`, and other compared fields do not change.
    - There is no focused integration regression in `tests/integration/constraint-operations.test.ts` for this table-constraint path.

## 2) Open pgschema issue screening

### Covered in current pg-delta

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362) — numeric precision changes
  - Evidence: `tests/integration/alter-table-operations.test.ts`

- pgschema [#401](https://github.com/pgplex/pgschema/issues/401) — `RETURNS SETOF <table>` dependency ordering
  - Evidence:
    - `tests/integration/table-function-dependency-ordering.test.ts`
    - `tests/integration/table-function-circular-dependency.test.ts`

- pgschema [#410](https://github.com/pgplex/pgschema/issues/410) — built-in `name` type dumped as `char[]`
  - Evidence: pg-delta still uses `format_type(a.atttypid, a.atttypmod)` for `data_type_str` in `src/core/objects/table/table.model.ts`

- pgschema [#415](https://github.com/pgplex/pgschema/issues/415) — materialized view dropped as plain view
  - Evidence:
    - `src/core/objects/materialized-view/changes/materialized-view.drop.ts`
    - `materialized-view.drop.test.ts`

- pgschema [#416](https://github.com/pgplex/pgschema/issues/416) — custom aggregates omitted from dump
  - Evidence:
    - `src/core/objects/aggregate/`
    - `tests/integration/aggregate-operations.test.ts`

- pgschema [#418](https://github.com/pgplex/pgschema/issues/418) — `CREATE INDEX CONCURRENTLY` on partitioned parents
  - Evidence:
    - current pg-delta indexes are catalog-driven via `pg_get_indexdef(...)`
    - `tests/integration/partitioned-table-operations.test.ts` has parent-index coverage without pgschema's online rewrite path

- pgschema [#420](https://github.com/pgplex/pgschema/issues/420) — `varchar(n)[]` typmod dropped in dump
  - Evidence: `table.model.ts` still uses `format_type(a.atttypid, a.atttypmod)` for column types

- pgschema [#421](https://github.com/pgplex/pgschema/issues/421) / [#422](https://github.com/pgplex/pgschema/issues/422) — quoted mixed-case FK columns / custom types
  - Evidence:
    - pg-delta stores quoted identifiers via `quote_ident(...)`
    - type / table extraction uses catalog-derived `data_type_str`
    - there is quoted-type coverage in `tests/integration/type-operations.test.ts`
  - No duplicate issue drafted in this pass.

- pgschema [#423](https://github.com/pgplex/pgschema/issues/423) — `UNLOGGED` table persistence dropped from dump
  - Evidence:
    - `src/core/objects/table/table.model.ts`
    - `src/core/objects/table/table.diff.ts`
    - `src/core/objects/table/changes/table.create.ts`
    - serializer / diff tests for `SET UNLOGGED`, `SET LOGGED`, and `CREATE UNLOGGED TABLE`

- pgschema [#427](https://github.com/pgplex/pgschema/issues/427) — schema-qualified functions in RLS policies
  - Likely not a pg-delta parity gap: pg-delta extracts policy expressions with `pg_get_expr(...)` in `src/core/objects/rls-policy/rls-policy.model.ts` instead of replaying pgschema's temp-schema dump/apply flow.

### Tracked in existing pg-toolbelt issues

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) — `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - Existing tracker: [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - Why still tracked:
    - `table.model.ts` extracts `deferrable` and `initially_deferred`
    - `table.diff.ts` compares them
    - but there is still no dedicated integration regression for this exact table-constraint scenario

- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) — enum-arg function privilege signatures
  - Existing tracker: [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  - Still no dedicated integration regression for GRANT/REVOKE on enum-typed function signatures.

### Newly concerning / draft-only follow-up

- pgschema [#414](https://github.com/pgplex/pgschema/issues/414) — add-column vs view ordering inside the same transaction group
  - This looks like a real pg-delta follow-up candidate.
  - Evidence:
    - `AlterTableAddColumn.requires` only depends on the table stable ID:
      - `src/core/objects/table/changes/table.alter.ts`
    - `CreateView.requires` intentionally does not parse new-object query dependencies:
      - `src/core/objects/view/changes/view.create.ts`
    - `tests/integration/mixed-objects.test.ts` contains an `"Add column and update view"` case, but it uses `sortChangesCallback` to force the view ahead of the table alter. That custom ordering masks the default sorter instead of proving the natural dependency edge exists.
  - No existing pg-toolbelt issue or PR was found for this exact scenario.
  - Draft issue body is saved in [`docs/parity-issue-drafts-2026-05-05.md`](./parity-issue-drafts-2026-05-05.md).

- pgschema [#408](https://github.com/pgplex/pgschema/issues/408) — quoted reserved composite type names
  - Current pg-delta evidence trends positive because table/view extraction uses quoted identifiers and catalog-derived `data_type_str`, but I did not open a duplicate issue in this pass because I did not confirm an end-to-end failing pg-delta repro.
  - This remains a watch item rather than a benchmarked gap.

## 3) Notes

- Manual unlabeled-issue screening remains necessary. The automation scripts still only fetch pgschema issues labeled `Bug` or `Feature`, and many current parity-relevant pgschema issues are unlabeled.
- Benchmark writeups for 005, 007, 013, 015, 016, 017, and 019 were updated because their body text still described old pg-delta gaps that are now solved in current source/tests.
- The benchmark source of truth now has a single unresolved historical item: table-level `UNIQUE NULLS NOT DISTINCT` constraints (pgschema #412).
