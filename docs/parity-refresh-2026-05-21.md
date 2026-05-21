# Parity refresh — 2026-05-21

## Snapshot

Refreshed against:

- `repos/pg-toolbelt` @ `0bd7dc229340157e31ae816261cf01744e5ad295`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

## Executive summary

- No parity-state delta was found versus the 2026-05-19 refresh. Benchmark
  **020** remains the only unresolved historical gap, and the two live open
  parity trackers remain
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  (pgschema `#404`) plus
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  (pgschema `#366`).
- Benchmark **005** remains solved in current upstream state:
  [pg-toolbelt#130](https://github.com/supabase/pg-toolbelt/issues/130) is
  closed and [pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231)
  is still the merged fix.
- There is still no open pg-toolbelt PR targeting `#218` or `#219`, and the
  live pg-toolbelt issue/PR sweep did not surface any newer duplicate tracker
  for pgschema `#412`, `#404`, or `#366`.
- Today's manual open-issue sweep added one new classification only:
  pgschema `#439` (`DROP CONSTRAINT ... CASCADE`) looks operational-policy
  specific rather than a current pg-delta parity gap.

## Open pgschema issue screening

### Tracked already in pg-toolbelt

- **pgschema #404** — deferrable unique constraints:
  tracked by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **pgschema #366** — function privilege signatures with enum argument types:
  tracked by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Covered in current pg-delta

- **pgschema #362** — numeric precision changes
- **pgschema #401** — `RETURNS SETOF <table>` dependency ordering
- **pgschema #415** — materialized-view refactor drops
- **pgschema #436** — required extensions in dump output

### Screened, but no duplicate draft prepared

- **pgschema #408** — quoted custom / reserved type names in plan output
- **pgschema #414** — add-column plus new-view ordering in one migration
- **pgschema #418** — partitioned-parent indexes rewritten to `CONCURRENTLY`
- **pgschema #420** — `varchar(n)[]` typmod preservation
- **pgschema #421** — quoted mixed-case foreign-key columns
- **pgschema #422** — quoted mixed-case custom types
- **pgschema #427** — schema-qualified functions in RLS policies

These were rechecked against the current pg-delta checkout and live GitHub
issue/PR state. Current pg-delta still lacks one-off regressions named after
the exact pgschema repros for several of these cases, but the present source
and adjacent integration coverage were not strong enough to justify drafting
new pg-toolbelt issues without a cleaner pg-delta-specific failing reproduction.

### Not pg-delta parity work

- **pgschema #49** — explicit rename/refactor workflow proposal
- **pgschema #406 / #407 / #409 / #419 / #429 / #439** — `.pgschemaignore`,
  constraint-separation, or operational workflow follow-ups
- **pgschema #416** — custom aggregates omitted from dump; current pg-delta
  already extracts aggregates as first-class catalog objects and covers
  aggregate create / drop / privilege paths

## Recent closed-issue screening

- **pgschema #410** — built-in `name` columns dumped as `char[]`
  - Current pg-delta column extraction stores `data_type_str` with
    `format_type(a.atttypid, a.atttypmod)` in
    `packages/pg-delta/src/core/objects/table/table.model.ts`, so this does not
    currently look like a pg-delta parity gap.
- **pgschema #423** — `UNLOGGED` dropped from table definitions
  - Current pg-delta models table persistence explicitly in
    `packages/pg-delta/src/core/objects/table/table.diff.ts` and has unit
    coverage for both `CREATE UNLOGGED TABLE` and `ALTER TABLE ... SET UNLOGGED`.
- **pgschema #412** — table-level `UNIQUE NULLS NOT DISTINCT`
  - Still not covered in current pg-delta and remains benchmark
    [020](../benchmark/020-table-constraint-unique-nulls-not-distinct.md).

## Duplicate-avoidance outcome

- No new pg-toolbelt issue was drafted from this refresh.
- The only live open parity trackers remain `pg-toolbelt#218` and
  `pg-toolbelt#219`.
- The only remaining untracked historical draft is still for `pgschema#412`;
  that draft already exists in
  [`docs/parity-issue-drafts-2026-05-17.md`](./parity-issue-drafts-2026-05-17.md).

## Automation caveat

The repo's automation scripts still filter pgschema issues by `Bug` / `Feature`
labels. Because current pgschema issue hygiene is inconsistent, a manual sweep
remains necessary even when dry-run `compare_issues.py` /
`compare_resolved.py` report no candidates.
