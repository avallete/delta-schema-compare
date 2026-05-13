# Parity refresh — 2026-05-13

## Snapshot

Refreshed against:

- `repos/pg-toolbelt` @ `f1704bd26b80dec379cb19ef4ee2e30639dead8f`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

## Executive summary

- All existing benchmark entries from the previous snapshot
  (`005`, `007`, `008`, `013`, `015`, `016`, `017`, `018`, `019`) are now
  solved in current pg-delta.
- Benchmark **005** flipped from "tracked" to "solved" because
  [pg-toolbelt#130](https://github.com/supabase/pg-toolbelt/issues/130) is now
  closed and
  [pg-toolbelt#231](https://github.com/supabase/pg-toolbelt/pull/231) merged
  the landed `ALTER COLUMN TYPE ... USING` fix.
- Added benchmark **020** for the one remaining historical gap:
  pgschema [#412](https://github.com/pgplex/pgschema/issues/412), the
  table-constraint variant of `UNIQUE NULLS NOT DISTINCT`.
- Open parity work remains limited to the two previously known trackers:
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  (pgschema `#404`) and
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  (pgschema `#366`).

## Benchmark updates made in this refresh

- Updated `benchmark/README.md` to the new submodule SHAs and current issue / PR
  states.
- Rewrote the stale benchmark detail files that still described already-landed
  pg-delta gaps:
  - `005-alter-column-type-using-clause.md`
  - `007-function-signature-change-requires-drop.md`
  - `013-sequence-identity-transitions.md`
  - `015-trigger-update-of-columns.md`
  - `016-unique-index-nulls-not-distinct.md`
  - `017-temporal-without-overlaps-period-constraints.md`
  - `019-columnless-check-no-inherit.md`
- Added `benchmark/020-table-constraint-unique-nulls-not-distinct.md`.
- Regenerated `benchmark/review-memory.json` to match the current SHAs and the
  latest open-issue screening set.

## Open pgschema issue screening

### Tracked already in pg-toolbelt

- **pgschema #404** — deferrable unique constraints:
  tracked by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **pgschema #366** — function privilege signatures with enum argument types:
  tracked by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Covered in current pg-delta

- **pgschema #362** — numeric precision changes
- **pgschema #401** — `RETURNS SETOF <table>` dependency ordering

### Screened, but no new duplicate draft prepared

These were reviewed against the current local pg-delta checkout and upstream
GitHub state, but I did not draft new pg-toolbelt issues for them in this
refresh:

- **pgschema #408** — quoted custom / reserved type names in plan output
- **pgschema #414** — add-column plus new-view ordering in one migration
- **pgschema #418** — partitioned-parent indexes rewritten to `CONCURRENTLY`
- **pgschema #420** — `varchar(n)[]` typmod preservation
- **pgschema #421** — quoted mixed-case foreign-key columns
- **pgschema #422** — quoted mixed-case custom types
- **pgschema #427** — schema-qualified functions in RLS policies

The common pattern is that current pg-delta either already has adjacent
integration coverage for the same dependency family, or preserves the relevant
catalog text via `format_type(...)`, `quote_ident(...)`, or `pg_get_expr(...)`,
but does not yet have a one-off regression named after the exact pgschema repro.

### Not pg-delta parity work

- **pgschema #406 / #407 / #409 / #429** — `.pgschemaignore` and
  constraints-separation workflow/configuration follow-ups

## Duplicate-avoidance outcome

- No new pg-toolbelt issue was opened from the open-issue sweep.
- The only new draft captured in this refresh is for the closed historical gap
  `pgschema#412`, because that scenario is still untracked in pg-toolbelt and
  still appears uncovered in current pg-delta.
- That draft lives in
  [`docs/parity-issue-drafts-2026-05-13.md`](./parity-issue-drafts-2026-05-13.md).

## Automation caveat

The repo's automation scripts still filter pgschema issues by `Bug` / `Feature`
labels. Because current pgschema issue hygiene is inconsistent, an unlabeled
manual sweep remains necessary even when the dry-run scripts report no new
candidates.
