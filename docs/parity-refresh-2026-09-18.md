# Parity refresh report - 2026-09-18

This report records the 2026-09-18 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `11678c582923fc1a27ed2edf37f3503d1fc466a8`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0882fc4cb6b792b79b599a414b434e4e048b6672`)

## 1) Benchmark status refresh

This refresh finds one upstream `pg-toolbelt` code delta and two new open
pgschema issues versus
[`docs/parity-refresh-2026-09-17.md`](./parity-refresh-2026-09-17.md):

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
  - merged PR [#480](https://github.com/supabase/pg-toolbelt/pull/480) is
    adjacent only: it fixes attached child indexes on a partition drop root,
    not child-local column override extraction or rendering
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

The target repo still has no local tracker issues. Current pg-toolbelt open
issue/PR lists are still adjacent to the active benchmark set: umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the only
tracker context for benchmarks **021** / **022**, benchmark **024** still has
no exact pg-toolbelt issue or PR, open pg-toolbelt issue
[#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
[#477](https://github.com/supabase/pg-toolbelt/issues/477), PR
[#478](https://github.com/supabase/pg-toolbelt/pull/478), merged PR
[#480](https://github.com/supabase/pg-toolbelt/pull/480), and open release PR
[#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
cluster-global role / identity-sequence privilege / partition-index / release
work rather than duplicates of the active benchmarks.

## 2) Open / resolved pgschema delta on 2026-09-18

There is real upstream activity since the 2026-09-17 refresh:

- new open pgschema issue
  [#606](https://github.com/pgplex/pgschema/issues/606) (`Inconsistent
  behaviour with multi-column primary key and partitioning`)
- new open pgschema issue
  [#607](https://github.com/pgplex/pgschema/issues/607) (`plan/apply still
  fails on extension-owned types even when plan and target schemas agree`)
- new open pgschema PR
  [#608](https://github.com/pgplex/pgschema/pull/608) as the upstream fix path
  for issue **#607**
- new merged pg-toolbelt PR
  [#480](https://github.com/supabase/pg-toolbelt/pull/480)
- new open pg-toolbelt release PR
  [#481](https://github.com/supabase/pg-toolbelt/pull/481)

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#588](https://github.com/pgplex/pgschema/issues/588),
  [#594](https://github.com/pgplex/pgschema/issues/594),
  [#596](https://github.com/pgplex/pgschema/issues/596),
  [#597](https://github.com/pgplex/pgschema/issues/597), and
  [#607](https://github.com/pgplex/pgschema/issues/607) remain
  **not parity work for pg-delta**
- open issues [#593](https://github.com/pgplex/pgschema/issues/593),
  [#598](https://github.com/pgplex/pgschema/issues/598),
  [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602),
  [#603](https://github.com/pgplex/pgschema/issues/603), and
  [#606](https://github.com/pgplex/pgschema/issues/606) remain **covered** in
  current pg-delta
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### Focus notes for the new open issues

- **#606** is **covered** in current pg-delta:
  - `tests/parallel-extract.test.ts` already exercises a partitioned table
    with `PRIMARY KEY (id, at)`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    table constraints via `pg_get_constraintdef(con.oid)`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts`
    replays the preserved `PRIMARY KEY (...)` text verbatim in
    `ADD CONSTRAINT`
- **#607** remains **not parity work** for pg-delta:
  - it is the same temp comparison schema / `search_path` resolution class as
    previously screened pgschema issue
    [#518](https://github.com/pgplex/pgschema/issues/518)
  - pg-delta diffs live catalogs rather than applying desired-state SQL to a
    temporary comparison schema
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/scope.ts` pins extraction
    `search_path` to `pg_catalog`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    type text via `format_type(...)`
  - `repos/pg-toolbelt/packages/pg-delta/tests/supabase-integration.test.ts`
    covers non-public `pgvector` type usage

## 3) What changed in this refresh

- advance the checked-in `repos/pg-toolbelt` submodule pointer to
  `0882fc4cb6b792b79b599a414b434e4e048b6672`
- refresh `benchmark/README.md` to the 2026-09-18 latest-state snapshot
- add fresh 2026-09-18 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- refresh `benchmark/review-memory.json` review timestamps for the rechecked
  open watch-list items and active benchmark issues, and add new open issues
  **#606** and **#607**
- add this report as the 2026-09-18 latest-state sweep
- no new benchmark files and no new draft-only uncovered issue docs were
  needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 30 --json number,title,updatedAt,labels,url`
  - `gh issue list -R pgplex/pgschema --state closed --limit 20 --json number,title,updatedAt,labels,url`
  - `gh pr list -R pgplex/pgschema --state merged --limit 20 --json number,title,updatedAt,mergedAt,url`
  - `gh pr list -R pgplex/pgschema --state open --limit 20 --json number,title,updatedAt,isDraft,url`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 40 --json number,title,updatedAt,labels,url`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 30 --json number,title,updatedAt,isDraft,url`
  - `gh pr list -R supabase/pg-toolbelt --state merged --limit 25 --json number,title,updatedAt,mergedAt,url`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 120 --json number,title,state,updatedAt,url`
- source inspection for the new issues and active benchmarks:
  - `git -C repos/pg-toolbelt diff --stat 94de18e34e9758e36cd0c18f7ffadeb2291bb446..0882fc4cb6b792b79b599a414b434e4e048b6672 -- packages/pg-delta/src/extract/relations.ts packages/pg-delta/src/plan/rules/helpers.ts packages/pg-delta/src/plan/rules/tables.ts packages/pg-delta/src/plan/rules/constraints.ts packages/pg-delta/src/plan/rules/indexes.ts packages/pg-delta/src/plan/partition-index-attach.test.ts packages/pg-delta/tests/supabase-integration.test.ts packages/pg-delta/tests/parallel-extract.test.ts`
  - `gh issue view 606 -R pgplex/pgschema --json number,title,body,updatedAt,url,state,labels`
  - `gh issue view 607 -R pgplex/pgschema --json number,title,body,updatedAt,url,state,labels`
  - `gh issue view 518 -R pgplex/pgschema --json number,title,body,updatedAt,url,state`
- repo Python validation:
  - `python3 -m pip install -r requirements.txt`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this pod because Bun and Docker
  are unavailable here; the new issue verdicts rely on source inspection plus
  already checked-in test coverage
