# Parity refresh report — 2026-04-22

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `0352fc1fc6a0067f616b61b3d669265b6ed2e818`)
- `pg-delta` (`repos/pg-toolbelt` @ `b812a4698478ed92dbabb19fa819873bebe0faf8`)

## 1) Benchmark issue status refresh

The benchmark tracks nine core parity scenarios. Their current status is:

### Solved in pg-delta (merged fix PR exists)

- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) → pg-toolbelt issue [#132](https://github.com/supabase/pg-toolbelt/issues/132), PR [#214](https://github.com/supabase/pg-toolbelt/pull/214) merged
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) → pg-toolbelt issue [#138](https://github.com/supabase/pg-toolbelt/issues/138), PR [#154](https://github.com/supabase/pg-toolbelt/pull/154) merged
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) → pg-toolbelt issue [#140](https://github.com/supabase/pg-toolbelt/issues/140), PR [#200](https://github.com/supabase/pg-toolbelt/pull/200) merged
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) → pg-toolbelt issue [#183](https://github.com/supabase/pg-toolbelt/issues/183), PR [#185](https://github.com/supabase/pg-toolbelt/pull/185) merged
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) → pg-toolbelt issue [#182](https://github.com/supabase/pg-toolbelt/issues/182), PR [#213](https://github.com/supabase/pg-toolbelt/pull/213) merged
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) → pg-toolbelt issue [#198](https://github.com/supabase/pg-toolbelt/issues/198), PR [#212](https://github.com/supabase/pg-toolbelt/pull/212) merged

### Tracked (open pg-toolbelt issue and open PR)

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) → pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130), PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) open
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) → pg-toolbelt issue [#133](https://github.com/supabase/pg-toolbelt/issues/133), PR [#149](https://github.com/supabase/pg-toolbelt/pull/149) open
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) → pg-toolbelt issue [#184](https://github.com/supabase/pg-toolbelt/issues/184), PR [#187](https://github.com/supabase/pg-toolbelt/pull/187) open

## 2) New open pgschema candidate screening

### Covered in pg-delta

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric precision changes
  - Evidence: `alter-table-operations.test.ts` has numeric type-change roundtrip coverage.
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401): `RETURNS SETOF <table>` dependencies
  - Evidence: `table-function-circular-dependency.test.ts` and `table-function-dependency-ordering.test.ts`.

### Not yet covered (drafts prepared, no issue created)

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404): `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function privilege signatures with enum args

Draft issue writeups (with MREs) are stored in:

- [`docs/parity-issue-drafts-2026-04-22.md`](./parity-issue-drafts-2026-04-22.md)

## 3) Notes

- Some pg-toolbelt tracking issues remain open despite merged fix PRs; this report treats merged fix PRs as solved parity on pg-delta behavior.
- No issues were created directly from this refresh; all new findings are captured as markdown drafts first.
