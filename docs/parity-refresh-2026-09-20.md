# Parity refresh report - 2026-09-20

This report records the 2026-09-20 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `b8e7e26a9db221ea01cdd64f4cfb8ca96923c536`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0882fc4cb6b792b79b599a414b434e4e048b6672`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pgschema` from
`11678c582923fc1a27ed2edf37f3503d1fc466a8` to
`b8e7e26a9db221ea01cdd64f4cfb8ca96923c536` through merged PRs
[#610](https://github.com/pgplex/pgschema/pull/610),
[#612](https://github.com/pgplex/pgschema/pull/612),
[#613](https://github.com/pgplex/pgschema/pull/613),
[#614](https://github.com/pgplex/pgschema/pull/614), and
[#615](https://github.com/pgplex/pgschema/pull/615), while checked-in/live
`pg-delta` remains unchanged at `0882fc4cb6b792b79b599a414b434e4e048b6672`.

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; open issues
    [#476](https://github.com/supabase/pg-toolbelt/issues/476) and
    [#477](https://github.com/supabase/pg-toolbelt/issues/477), open PR
    [#478](https://github.com/supabase/pg-toolbelt/pull/478), merged PR
    [#480](https://github.com/supabase/pg-toolbelt/pull/480), and open release
    PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain
    adjacent rather than benchmark-closing
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; there is still no exact pg-toolbelt
    issue or PR for the generated-kind gap itself
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - there is still no exact pg-toolbelt issue or PR for this benchmark

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-20

There is real upstream activity since the 2026-09-19 refresh even though the
active pg-delta benchmark set does not change:

- issue [#559](https://github.com/pgplex/pgschema/issues/559) is open again
  after merged revert PR [#612](https://github.com/pgplex/pgschema/pull/612)
- issues [#593](https://github.com/pgplex/pgschema/issues/593),
  [#594](https://github.com/pgplex/pgschema/issues/594),
  [#596](https://github.com/pgplex/pgschema/issues/596), and
  [#606](https://github.com/pgplex/pgschema/issues/606) are now closed via
  merged PRs
  [#613](https://github.com/pgplex/pgschema/pull/613),
  [#614](https://github.com/pgplex/pgschema/pull/614),
  [#615](https://github.com/pgplex/pgschema/pull/615), and
  [#610](https://github.com/pgplex/pgschema/pull/610)
- issue [#588](https://github.com/pgplex/pgschema/issues/588) is now closed as
  feedback / design discussion
- open PR [#616](https://github.com/pgplex/pgschema/pull/616) continues a
  follow-up fix on the same `#596` family
- open PR [#611](https://github.com/pgplex/pgschema/pull/611) remains the
  upstream fix path for covered issue
  [#598](https://github.com/pgplex/pgschema/issues/598)
- open PR [#608](https://github.com/pgplex/pgschema/pull/608) remains the
  upstream fix path for upstream-only issue
  [#607](https://github.com/pgplex/pgschema/issues/607)

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597), and
  [#607](https://github.com/pgplex/pgschema/issues/607) remain
  **not parity work for pg-delta**
- open issues [#598](https://github.com/pgplex/pgschema/issues/598),
  [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602), and
  [#603](https://github.com/pgplex/pgschema/issues/603) remain **covered** in
  current pg-delta
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### Focus notes for the changed upstream items

- **#559** remains **not parity work** for pg-delta:
  - merged revert PR [#612](https://github.com/pgplex/pgschema/pull/612)
    removes config-data management from `main`
  - pg-delta remains a schema-diff tool and does not attempt row-data
    synchronization
- **#593** remains **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    explicit non-default `attcollation` on column facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` replays
    that state as `COLLATE ...`
- **#594** remains **not parity work** for pg-delta:
  - merged PR [#614](https://github.com/pgplex/pgschema/pull/614) only hardens
    `.pgschemaignore` parsing by rejecting unknown keys
  - this is an upstream configuration / dump-filtering path rather than a
    pg-delta live-catalog diff or apply gap
- **#596** remains **not parity work** for pg-delta:
  - merged PR [#615](https://github.com/pgplex/pgschema/pull/615) fixes
    managed-schema qualifiers in inlined SQL function bodies
  - open follow-up PR [#616](https://github.com/pgplex/pgschema/pull/616)
    fixes SQL-function batch ordering in the same temp-schema apply path
  - pg-delta diffs live catalogs and does not apply desired-state SQL into a
    temporary comparison schema
- **#606** remains **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    table constraints via `pg_get_constraintdef(con.oid)`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts`
    replays the preserved `PRIMARY KEY (...)` text verbatim in
    `ADD CONSTRAINT`
- **#598** remains **covered** in current pg-delta:
  - current pg-delta captures regular-index validity as semantic `valid`
  - `tests/index-invalid-repair.test.ts` covers the invalid-index repair path
  - open PR [#611](https://github.com/pgplex/pgschema/pull/611) is the
    upstream fix path on the pgschema side
- **#607** remains **not parity work** for pg-delta:
  - it is still the same temp comparison schema / `search_path` resolution
    class as previously screened issue
    [#518](https://github.com/pgplex/pgschema/issues/518)
  - pg-delta diffs live catalogs instead of applying desired-state SQL to a
    temporary comparison schema
  - open PR [#608](https://github.com/pgplex/pgschema/pull/608) remains the
    upstream fix path

## 3) What changed in this refresh

- advance the checked-in `repos/pgschema` submodule pointer to
  `b8e7e26a9db221ea01cdd64f4cfb8ca96923c536`
- keep the checked-in `repos/pg-toolbelt` submodule pointer at
  `0882fc4cb6b792b79b599a414b434e4e048b6672`
- refresh `benchmark/README.md` to the 2026-09-20 latest-state snapshot
- add fresh 2026-09-20 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- refresh `benchmark/review-memory.json` bookkeeping: move issue **#559** back
  to the open watch list, move issues **#588** / **#593** / **#594** /
  **#596** / **#606** to resolved status, and refresh the active benchmark
  fingerprints
- add this report as the 2026-09-20 latest-state sweep
- no new benchmark files and no new draft-only uncovered issue docs were
  needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 60 --json number,title,updatedAt,labels,url`
  - `gh issue list -R pgplex/pgschema --state closed --limit 25 --json number,title,updatedAt,labels,url`
  - `gh pr list -R pgplex/pgschema --state open --limit 25 --json number,title,updatedAt,isDraft,url,headRefName,baseRefName`
  - `gh pr list -R pgplex/pgschema --state merged --limit 25 --json number,title,updatedAt,mergedAt,url`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 60 --json number,title,updatedAt,labels,url`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 30 --json number,title,updatedAt,isDraft,url,headRefName,baseRefName`
  - `gh pr list -R supabase/pg-toolbelt --state merged --limit 30 --json number,title,updatedAt,mergedAt,url`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 120 --json number,title,state,updatedAt,url`
- focused issue / PR inspection for the changed upstream items:
  - `gh issue view 559 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 588 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 593 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 594 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 596 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 598 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 606 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh issue view 607 -R pgplex/pgschema --json number,title,body,updatedAt,state,closedAt,url`
  - `gh pr view 608 -R pgplex/pgschema --json number,title,body,updatedAt,state,isDraft,mergeStateStatus,commits,url`
  - `gh pr view 611 -R pgplex/pgschema --json number,title,body,updatedAt,state,isDraft,mergeStateStatus,commits,url`
  - `gh pr view 615 -R pgplex/pgschema --json number,title,body,updatedAt,state,isDraft,mergeStateStatus,commits,url`
  - `gh pr view 616 -R pgplex/pgschema --json number,title,body,updatedAt,state,isDraft,mergeStateStatus,commits,url`
- repo Python validation:
  - `python3 -m pip install -r requirements.txt`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this refresh because
  `pg-toolbelt` did not move and the active gap verdicts are unchanged at the
  source / codepath level
