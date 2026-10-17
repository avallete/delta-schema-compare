# Parity refresh report - 2026-10-17

This report records the 2026-10-17 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0abee28a54bd855c13d45e2d7ebb5cb647b46693`)

## 1) Benchmark status refresh

This refresh keeps both checked-in/live submodule SHAs unchanged from the
2026-10-16 sweep. The parity change is on the tracker side:

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain the same active unresolved
  gaps as yesterday
- resolved pgschema issue
  [#534](https://github.com/pgplex/pgschema/issues/534) must now be promoted
  back into the active set as new benchmark **025**, because open pg-toolbelt
  issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) shows the
  current declarative export path still fails the same self-referencing
  non-PK-UNIQUE-key dependency family

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

### Upstream movement since 2026-10-16

- `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-16'`
  surfaced open PRs [#645](https://github.com/pgplex/pgschema/pull/645) and
  [#661](https://github.com/pgplex/pgschema/pull/661) only
- PR [#661](https://github.com/pgplex/pgschema/pull/661) is the upstream fix
  path for covered issue [#638](https://github.com/pgplex/pgschema/issues/638)
  and does not change pg-delta parity
- `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-16'`
  surfaced new open issues
  [#543](https://github.com/supabase/pg-toolbelt/issues/543) and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544)
- issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) is the
  exact current tracker for pgschema issue
  [#534](https://github.com/pgplex/pgschema/issues/534)
- targeted pgschema keyword searches found no matching counterpart for issue
  [#544](https://github.com/supabase/pg-toolbelt/issues/544) beyond unrelated
  closed issue [#445](https://github.com/pgplex/pgschema/issues/445), so #544
  does not become a parity benchmark item today
- direct exact searches for `pgschema#499`, `pgschema#501`, `pgschema#564`, and
  `pgschema#534` still returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

The active benchmark set therefore becomes **021**, **022**, **024**, and
**025**. There is still **no open uncovered parity candidate** on the
pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-17

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

Current verdicts now are:

- open issues **#49**, **#52**, **#84**, **#559**, and **#597** remain
  **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**, and
  **#653** remain **covered**
- the broader global-state cluster remains open umbrella issue
  [#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637); it is still **not added
  as a benchmark parity gap in this repo**
- resolved benchmark issues **#499**, **#501**, and **#534** now remain
  **tracked**
- resolved benchmark issue **#564** remains **not covered**
- there is currently **no open uncovered parity candidate**

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-10-17 latest-state snapshot
- add benchmark
  [025](../benchmark/025-self-referencing-fk-nonpk-unique-ordering.md) for the
  newly reclassified pgschema issue **#534**
- refresh `benchmark/review-memory.json` to:
  - update issue **#534** to the current head fingerprints
  - correct issue **#534** from `covered` to `tracked`
- add this report as the 2026-10-17 parity snapshot

No new local tracker issue draft was needed because the current pg-delta gap is
already tracked by open issue
[#543](https://github.com/supabase/pg-toolbelt/issues/543), and issue
[#544](https://github.com/supabase/pg-toolbelt/issues/544) had no matching
pgschema counterpart from today's keyword review.

## 4) Validation notes

This refresh was validated with:

- `python3 -m pip install --user -r requirements.txt`
- dry-run compare scripts with the repo token exported as `GITHUB_TOKEN` and
  user-site `PYTHONPATH`:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true python3 scripts/compare_resolved.py`
- `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
- `python3 -m json.tool benchmark/review-memory.json >/dev/null`
- `git diff --check`

The dry-run compare scripts still returned **0 labeled open issues** and
**0 labeled resolved issues**, which means manual unlabeled sweeps remain
required. Today's parity change would not have been captured from the labeled
issue filters alone because it came from a new pg-toolbelt issue
[#543](https://github.com/supabase/pg-toolbelt/issues/543) plus a manual
re-check of resolved pgschema issue
[#534](https://github.com/pgplex/pgschema/issues/534).
