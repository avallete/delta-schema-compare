# Parity refresh report - 2026-10-18

This report records the 2026-10-18 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0abee28a54bd855c13d45e2d7ebb5cb647b46693`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live submodule SHAs unchanged from the
2026-10-17 sweep. There is **no benchmark-status reclassification today**:

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, **024**, and **025** remain the active
  unresolved parity set
- there is still **no open uncovered parity candidate** on the pgschema side

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    inherited child columns gated by `a.attislocal`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no child column
    elements for local `DEFAULT` / `NOT NULL` overrides
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence rather
    than the `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows remain outside diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
    still treats a genuine self-reference as inline-safe by skipping it in
    `cyclicForeignKeys()`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts` and
    `repos/pg-toolbelt/packages/pg-delta/src/plan/internal.ts` still allow
    validated FOREIGN KEY constraints to fold inline during export
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-reorder-on-failure.test.ts`
    still proves the loader cannot repair same-file order once the FK and the
    backing unique index land in the same file

### Upstream movement since 2026-10-17

- `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-17'`
  returned `[]`
- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-17'`
  surfaced open PR [#662](https://github.com/pgplex/pgschema/pull/662) only
- PR [#662](https://github.com/pgplex/pgschema/pull/662) adds `MATCH FULL`
  preservation for foreign keys on the pgschema side, but:
  - it has no linked pgschema issue
  - exact duplicate searches for `"MATCH FULL"` and `confmatchtype` still found
    no pg-toolbelt issue or PR
  - current pg-delta source likely preserves the clause already through
    verbatim `pg_get_constraintdef(con.oid)` extraction in
    `src/extract/relations.ts` and verbatim `def` replay in
    `src/plan/rules/constraints.ts`
  - the current pg-delta tree still lacks a dedicated `MATCH FULL`
    extract/export round-trip test, so this remains a **watch-only** note
    rather than a new benchmark item
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-17'`
  still surfaced only issues
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544)
- no new open or merged pg-toolbelt PRs surfaced in the updated-since search
- issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) remains the
  exact current tracker for benchmark **025** /
  [#534](https://github.com/pgplex/pgschema/issues/534)
- issue [#544](https://github.com/supabase/pg-toolbelt/issues/544) still has
  no matching pgschema counterpart from keyword searches
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore remains **021**, **022**, **024**, and
**025**. There is still **no open uncovered parity candidate** on the
pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-18

The current open pgschema issue watch list is unchanged:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639), and
[#653](https://github.com/pgplex/pgschema/issues/653).

Current verdicts remain:

- open issues **#49**, **#52**, **#84**, **#559**, and **#597** remain
  **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**, and
  **#653** remain **covered**
- the broader global-state cluster remains open umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637); it is still **not added
  as a benchmark parity gap in this repo**
- resolved benchmark issues **#499**, **#501**, and **#534** remain
  **tracked**
- resolved benchmark issue **#564** remains **not covered**
- there is currently **no open uncovered parity candidate**

The only new manual-review note is pgschema PR
[#662](https://github.com/pgplex/pgschema/pull/662). Because it is PR-only
context rather than an issue, and because the current pg-delta source already
appears to carry the `MATCH FULL` text path generically without a dedicated
test, it is recorded as watch-only rather than promoted into benchmark docs.

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-18 latest-state snapshot
- add this report as the 2026-10-18 parity snapshot
- do **not** change `benchmark/review-memory.json`, because:
  - no tracked pgschema issue `updated_at` changed in today's open-issue sweep
  - the checked-in/live `pgschema` and `pg-delta` heads stayed fixed
  - the only new upstream context was PR-only (pgschema PR #662), so there was
    no issue fingerprint to update

No new local tracker issue draft was needed:

- benchmark **025** already has open pg-toolbelt issue
  [#543](https://github.com/supabase/pg-toolbelt/issues/543)
- issue [#544](https://github.com/supabase/pg-toolbelt/issues/544) still has no
  matching pgschema counterpart
- PR [#662](https://github.com/pgplex/pgschema/pull/662) is still watch-only
  context rather than a benchmark promotion

## 4) Validation notes

This refresh was validated with:

- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH` when needed:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true python3 scripts/compare_resolved.py`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `git diff --check`

The dry-run compare scripts still returned **0 labeled open issues** and
**0 labeled resolved issues**, which means manual unlabeled sweeps remain
required. Today's review would not have surfaced PR
[#662](https://github.com/pgplex/pgschema/pull/662) from the label-filtered
issue scripts alone because it is PR-only upstream context.
