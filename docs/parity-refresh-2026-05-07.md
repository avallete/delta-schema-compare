# Parity refresh report — 2026-05-07

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `102ef99ae5aabb29510d48b39fbb8ecee34f5458`)

## 1) Benchmark issue status refresh

The historical benchmark now has one remaining unresolved gap and nine scenarios
that are solved in current pg-delta.

### Solved in current pg-delta

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) -> pg-toolbelt
  [#130](https://github.com/supabase/pg-toolbelt/issues/130)
  - Current `main` emits `USING` for type changes and safely sequences default
    handling; the old issue is no longer active even though PR
    [#146](https://github.com/supabase/pg-toolbelt/pull/146) closed unmerged.
- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) -> pg-toolbelt
  [#132](https://github.com/supabase/pg-toolbelt/issues/132), fixed by merged PR
  [#214](https://github.com/supabase/pg-toolbelt/pull/214)
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) -> pg-toolbelt
  [#133](https://github.com/supabase/pg-toolbelt/issues/133), fixed by merged PR
  [#149](https://github.com/supabase/pg-toolbelt/pull/149)
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) -> pg-toolbelt
  [#138](https://github.com/supabase/pg-toolbelt/issues/138), fixed by merged PR
  [#154](https://github.com/supabase/pg-toolbelt/pull/154)
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) -> pg-toolbelt
  [#140](https://github.com/supabase/pg-toolbelt/issues/140), fixed by merged PR
  [#200](https://github.com/supabase/pg-toolbelt/pull/200)
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) -> pg-toolbelt
  [#183](https://github.com/supabase/pg-toolbelt/issues/183), fixed by merged PR
  [#185](https://github.com/supabase/pg-toolbelt/pull/185)
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) -> pg-toolbelt
  [#182](https://github.com/supabase/pg-toolbelt/issues/182), fixed by merged PR
  [#213](https://github.com/supabase/pg-toolbelt/pull/213)
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) -> pg-toolbelt
  [#184](https://github.com/supabase/pg-toolbelt/issues/184), fixed by merged PR
  [#187](https://github.com/supabase/pg-toolbelt/pull/187)
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) -> pg-toolbelt
  [#198](https://github.com/supabase/pg-toolbelt/issues/198), fixed by merged PR
  [#212](https://github.com/supabase/pg-toolbelt/pull/212)

Benchmark writeups 005, 007, 013, 015, 016, 017, and 019 were rewritten in
this refresh to mark them as historical solved gaps instead of active parity
problems. Benchmark entries 008 and 018 already had accurate solved-state
writeups, so they remained unchanged.

### Still not covered

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412): table-level
  `UNIQUE NULLS NOT DISTINCT` constraints remain uncovered in current pg-delta.
  This is now benchmark item 020, and a draft-only pg-toolbelt issue body is
  saved in
  [`docs/parity-issue-drafts-2026-05-07.md`](./parity-issue-drafts-2026-05-07.md).

## 2) Open pgschema issue screening

### Covered in current pg-delta; no duplicate pg-toolbelt issue drafted

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric
  precision changes
  - Evidence: `alter-table-operations.test.ts` includes numeric precision and
    scale change coverage.
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401): dependency
  ordering for `RETURNS SETOF <table>`
  - Evidence: `table-function-circular-dependency.test.ts` and
    `table-function-dependency-ordering.test.ts`.
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted
  custom or reserved type names in plan output
  - Evidence: pg-delta stores `data_type_str` from `format_type(...)` and has
    quoted-type coverage in `type-operations.test.ts`.
- pgschema [#427](https://github.com/pgplex/pgschema/issues/427):
  schema-qualified functions in RLS policy expressions
  - Evidence: `rls-policy.model.ts` preserves referenced procedure signatures,
    and `dbdev-roundtrip.test.ts` already covers auth-backed RLS policies.

### Already tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED` remains tracked by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum arguments remain tracked by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Watch item; no draft issue yet

- pgschema [#414](https://github.com/pgplex/pgschema/issues/414): `CREATE VIEW`
  ordering after `ALTER TABLE ... ADD COLUMN`
  - Upstream fix PR
    [#417](https://github.com/pgplex/pgschema/pull/417) is still open, so this
    refresh keeps it as a watch item instead of drafting a new pg-toolbelt
    issue prematurely.

### Not pg-delta parity work

- pgschema #406 / #407 / #409 / #419 (`.pgschemaignore` and related workflow
  follow-ups) were intentionally skipped as pgschema-specific surface area.

## 3) Recent closed-issue screening

### Covered in current pg-delta; no new benchmark item needed

- pgschema [#410](https://github.com/pgplex/pgschema/issues/410): `name`-typed
  columns
  - Evidence: pg-delta column extraction already uses
    `format_type(a.atttypid, a.atttypmod)`.
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED`
  tables
  - Evidence: pg-delta supports `CREATE UNLOGGED TABLE`,
    `ALTER TABLE ... SET UNLOGGED`, and `ALTER TABLE ... SET LOGGED`.

### New unresolved historical gap

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412): table-level
  `UNIQUE NULLS NOT DISTINCT`
  - This is distinct from the already-solved unique-index issue
    [pg-toolbelt#183](https://github.com/supabase/pg-toolbelt/issues/183) /
    [#185](https://github.com/supabase/pg-toolbelt/pull/185), so it was added
    as a separate benchmark entry instead of being treated as a duplicate.

## 4) Review-memory refresh

`benchmark/review-memory.json` was regenerated against the latest submodule SHAs
so automation now records:

- resolved historical gaps that are covered in current pg-delta,
- still-tracked open issues (#366 and #404),
- newly covered open issues (#408 and #427), and
- the remaining unresolved historical gap (#412).

Watch items such as #414 and the intentionally skipped non-parity pgschema
issues are documented in the human-readable refresh report, but are not stored
in `review-memory.json` because that file is only used for issues with a clear
parity verdict.

## 5) Notes

- Duplicate checks were performed against current pg-toolbelt issues and PRs
  before keeping or drafting any gap writeups.
- Manual unlabeled-issue sweeps are still necessary because recent pgschema
  issues often ship without `Bug` / `Feature` labels, which means the scripted
  automation can miss real parity work even when upstream has changed.
