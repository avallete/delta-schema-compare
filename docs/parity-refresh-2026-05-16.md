# Parity refresh — 2026-05-16

## Snapshot

Refreshed against:

- `repos/pg-toolbelt` @ `f1704bd26b80dec379cb19ef4ee2e30639dead8f`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

## Executive summary

- No parity-state delta was found versus the most recent unmerged May refresh
  branches: benchmark **020** remains the only unresolved historical gap, and
  the two open parity trackers remain
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  (pgschema `#404`) plus
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  (pgschema `#366`).
- This branch ports the latest unmerged benchmark/docs refresh onto the current
  automation branch, updates the repo snapshot to today's date, and revalidates
  the mapped pg-toolbelt issue / PR states live from GitHub.
- Benchmark **020** remains the one outstanding historical gap:
  pgschema [#412](https://github.com/pgplex/pgschema/issues/412), the
  table-constraint variant of `UNIQUE NULLS NOT DISTINCT`. No pg-toolbelt issue
  or PR exists yet for that scenario.
- Added pgschema [#49](https://github.com/pgplex/pgschema/issues/49) to the
  manual screening notes as **not pg-delta parity work**; it proposes an
  explicit rename/refactor workflow rather than a concrete pg-delta diff gap.

## Benchmark updates made in this refresh

- Ported the latest unmerged parity refresh baseline onto the current
  automation branch so this PR reflects the repo's most recent benchmark work.
- Updated `benchmark/README.md` to today's snapshot date and revalidated issue
  / PR states.
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

- **pgschema #49** — explicit rename/refactor workflow proposal
- **pgschema #406 / #407 / #409 / #429** — `.pgschemaignore` and
  constraints-separation workflow/configuration follow-ups

## Duplicate-avoidance outcome

- No new pg-toolbelt issue was opened from the open-issue sweep.
- The only new draft captured in this refresh is for the closed historical gap
  `pgschema#412`, because that scenario is still untracked in pg-toolbelt and
  still appears uncovered in current pg-delta.
- That draft lives in
  [`docs/parity-issue-drafts-2026-05-16.md`](./parity-issue-drafts-2026-05-16.md).

## Automation caveat

The repo's automation scripts still filter pgschema issues by `Bug` / `Feature`
labels. Because current pgschema issue hygiene is inconsistent, an unlabeled
manual sweep remains necessary even when the dry-run scripts report no new
candidates.
