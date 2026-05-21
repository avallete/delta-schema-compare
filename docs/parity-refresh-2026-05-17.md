# Parity refresh — 2026-05-17

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
- Today's additional sweep of recent open pgschema issues found no new
  pg-delta tracker to draft:
  - **#415** matview refactor drops are already covered by pg-delta's
    dedicated materialized-view replacement path.
  - **#416** custom aggregates omitted from pgschema dumps do not currently map
    to a pg-delta parity gap; pg-delta models aggregates directly from catalog
    state and already covers aggregate create/drop flows.
  - **#419** `.pgschemaignore` packaging behavior remains pgschema-specific and
    is not parity work for pg-delta.
  - **#436** required extensions in dump output are already covered by
    pg-delta's first-class extension support and declarative export tests.
- Benchmark **020** remains the one outstanding historical gap:
  pgschema [#412](https://github.com/pgplex/pgschema/issues/412), the
  table-constraint variant of `UNIQUE NULLS NOT DISTINCT`. No pg-toolbelt issue
  or PR exists yet for that scenario.

## Benchmark updates made in this refresh

- Ported the latest unmerged parity refresh baseline onto the current
  automation branch so this PR reflects the repo's most recent benchmark work.
- Updated `benchmark/README.md` to today's snapshot date and refreshed the
  screening notes for recent open issues.
- Kept benchmark **020** as the only unresolved historical gap.
- Regenerated `benchmark/review-memory.json` to capture the latest open-issue
  sweep, including new entries for pgschema issues `#415`, `#416`, `#419`, and
  `#436`.

## Open pgschema issue screening

### Tracked already in pg-toolbelt

- **pgschema #404** — deferrable unique constraints:
  tracked by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **pgschema #366** — function privilege signatures with enum argument types:
  tracked by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Covered in current pg-delta

- **pgschema #362** — numeric precision changes
- **pgschema #401** — `RETURNS SETOF <table>` dependency ordering
- **pgschema #415** — materialized-view refactor uses the correct
  `DROP MATERIALIZED VIEW` behavior in pg-delta's replacement flow
- **pgschema #436** — required extensions in dump output

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
- **pgschema #416** — custom aggregates are omitted from pgschema's dump path,
  but pg-delta models aggregates directly as first-class catalog objects and
  already covers aggregate create/drop flows
- **pgschema #406 / #407 / #409 / #419 / #429** — `.pgschemaignore` and
  constraints-separation workflow/configuration follow-ups

## Duplicate-avoidance outcome

- No new pg-toolbelt issue was opened from the open-issue sweep.
- The only live open parity trackers remain `pg-toolbelt#218` and
  `pg-toolbelt#219`.
- The only remaining untracked historical draft is for `pgschema#412`, because
  that scenario still appears uncovered in current pg-delta.
- That draft lives in
  [`docs/parity-issue-drafts-2026-05-17.md`](./parity-issue-drafts-2026-05-17.md).

## Automation caveat

The repo's automation scripts still filter pgschema issues by `Bug` / `Feature`
labels. Because current pgschema issue hygiene is inconsistent, an unlabeled
manual sweep remains necessary even when the dry-run scripts report no new
candidates.
