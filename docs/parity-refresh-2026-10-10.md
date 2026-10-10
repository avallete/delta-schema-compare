# Parity refresh report - 2026-10-10

This report records the 2026-10-10 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`3c60914eae50ff9d28084a8a1ce4e110b9c3d55d` to
`7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4` through merged PRs
[#514](https://github.com/supabase/pg-toolbelt/pull/514) and
[#527](https://github.com/supabase/pg-toolbelt/pull/527), while
checked-in/live `pgschema` remains `580f4040d0f3c1bfad1497918200c9c1f638a020`.

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain the only active unresolved
  gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    inherited child columns gated by `a.attislocal`, so child-local partition
    overrides never become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list
  - exact duplicate search `pgschema#499` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"PARTITION OF" --include-prs` now also
    surfaces open settle-definition issues
    [#526](https://github.com/supabase/pg-toolbelt/issues/526) and
    [#535](https://github.com/supabase/pg-toolbelt/issues/535), but those are
    separate settle-definition work rather than the exact child-local override
    fix tracked here
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence, not the
    `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - exact duplicate search `pgschema#501` still returns no dedicated
    pg-toolbelt issue or PR; keyword search for `"VIRTUAL" generated` still
    surfaces live umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus historical
    merged PRs [#378](https://github.com/supabase/pg-toolbelt/pull/378) and
    [#299](https://github.com/supabase/pg-toolbelt/pull/299)
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models table-column nullability through `a.attnotnull`; PG18
    `contype = 'n'` rows still do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - exact duplicate search `pgschema#564` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"NOT NULL" "NOT VALID"` still surfaces
    merged domain-only PR [#484](https://github.com/supabase/pg-toolbelt/pull/484)
    and diagnostics-only follow-up
    [#485](https://github.com/supabase/pg-toolbelt/pull/485)

### Upstream movement since 2026-10-09

- `gh issue list --repo pgplex/pgschema --state open --search
  'updated:>=2026-10-09'` surfaced open issues
  [#623](https://github.com/pgplex/pgschema/issues/623) and
  [#627](https://github.com/pgplex/pgschema/issues/627) through
  [#641](https://github.com/pgplex/pgschema/issues/641), while `gh pr list ...`
  surfaced open PR [#637](https://github.com/pgplex/pgschema/pull/637)
- the new pgschema global-state cluster rooted at
  [#627](https://github.com/pgplex/pgschema/issues/627) plus PR
  [#637](https://github.com/pgplex/pgschema/pull/637) does not add a new
  benchmark parity item in this repo; the schema-diff issues
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641) are already covered or
  avoided in current pg-delta
- `gh issue list --repo supabase/pg-toolbelt --state all --search
  'updated:>=2026-10-09'` plus `gh pr list --repo supabase/pg-toolbelt --state
  all --search 'updated:>=2026-10-09'` surfaced merged PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514) and
  [#527](https://github.com/supabase/pg-toolbelt/pull/527), open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#522](https://github.com/supabase/pg-toolbelt/pull/522),
  [#532](https://github.com/supabase/pg-toolbelt/pull/532),
  [#534](https://github.com/supabase/pg-toolbelt/pull/534),
  [#536](https://github.com/supabase/pg-toolbelt/pull/536), and
  [#537](https://github.com/supabase/pg-toolbelt/pull/537), open issues
  [#533](https://github.com/supabase/pg-toolbelt/issues/533) and
  [#535](https://github.com/supabase/pg-toolbelt/issues/535), plus closed
  issues [#510](https://github.com/supabase/pg-toolbelt/issues/510) and
  [#521](https://github.com/supabase/pg-toolbelt/issues/521)
- direct inspection of those updated items plus
  `git -C repos/pg-toolbelt diff --name-only 3c60914eae50ff9d28084a8a1ce4e110b9c3d55d..7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
  showed the merged code lands in `extract/routines.ts`,
  `extract/scoped-read.ts`, frontends/export / settle paths,
  `policy/policy.ts`, and related tests, not the active benchmark source paths
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-10

The current open pgschema watch list is now:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597),
  [#598](https://github.com/pgplex/pgschema/issues/598),
  [#623](https://github.com/pgplex/pgschema/issues/623),
  [#624](https://github.com/pgplex/pgschema/issues/624),
  [#625](https://github.com/pgplex/pgschema/issues/625),
  [#626](https://github.com/pgplex/pgschema/issues/626),
  [#627](https://github.com/pgplex/pgschema/issues/627),
  [#628](https://github.com/pgplex/pgschema/issues/628),
  [#629](https://github.com/pgplex/pgschema/issues/629),
  [#630](https://github.com/pgplex/pgschema/issues/630),
  [#631](https://github.com/pgplex/pgschema/issues/631),
  [#632](https://github.com/pgplex/pgschema/issues/632),
  [#633](https://github.com/pgplex/pgschema/issues/633),
  [#634](https://github.com/pgplex/pgschema/issues/634),
  [#635](https://github.com/pgplex/pgschema/issues/635),
  [#636](https://github.com/pgplex/pgschema/issues/636),
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641)
- open PR [#637](https://github.com/pgplex/pgschema/pull/637)

Current verdicts now are:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, and **#623**
  remain **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, **#626**, **#638**, **#639**,
  **#640**, and **#641** remain **covered**
- the new global-state cluster **#627 - #636** / **#637** is still **not added
  as a benchmark parity gap in this repo**
- resolved benchmark issues **#499** and **#501** remain **tracked**
- resolved benchmark issue **#564** remains **not covered**
- closed issues **#599**, **#600**, **#601**, **#602**, **#603**, and
  **#606** remain **covered**
- closed issues **#596** and **#607** remain **not parity work**
- there is currently **no open uncovered parity candidate**

No benchmark item changed status in this refresh, and no duplicate local
tracker issue exists in this repository.

## 3) What changed in this refresh

- move the checked-in/live `repos/pg-toolbelt` submodule pointer to
  `7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-10-10 latest-state snapshot
- append 2026-10-10 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` review timestamps and fingerprints for
  the current open-watch list, the new open issues **#627 - #641**, and the
  current active benchmark / recently-screened closed-issue set
- add this report as the 2026-10-10 latest-state sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git reset --hard origin/avallete/schema-comparison-benchmark-a218`
- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct submodule head checks:
  - `git -C repos/pgschema rev-parse HEAD`
  - `git -C repos/pg-toolbelt rev-parse HEAD`
  - `git -C repos/pg-toolbelt log --oneline 3c60914eae50ff9d28084a8a1ce4e110b9c3d55d..7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
  - `git -C repos/pg-toolbelt diff --name-only 3c60914eae50ff9d28084a8a1ce4e110b9c3d55d..7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4`
  - `git -C repos/pg-toolbelt diff --name-only 3c60914eae50ff9d28084a8a1ce4e110b9c3d55d..7f2fd64e05945fe3ef5860e3ee4569dc28c9ddb4 -- packages/pg-delta/src/extract/relations.ts packages/pg-delta/src/extract/dependencies.ts packages/pg-delta/src/plan/rules/tables.ts packages/pg-delta/src/plan/rules/helpers.ts packages/pg-delta/src/plan/rules/types.ts`
- GitHub CLI updated-state and duplicate checks:
  - `gh issue list --repo pgplex/pgschema --state open --search 'updated:>=2026-10-09' --json number,title,updatedAt,url`
  - `gh pr list --repo pgplex/pgschema --state all --search 'updated:>=2026-10-09' --json number,title,state,updatedAt,url`
  - `gh issue view 627 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 628 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 629 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 630 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 631 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 632 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 633 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 634 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 635 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 636 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 638 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 639 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 640 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue view 641 -R pgplex/pgschema --json number,title,body,state,url`
  - `gh issue list --repo supabase/pg-toolbelt --state all --search 'updated:>=2026-10-09' --json number,title,state,updatedAt,url`
  - `gh pr list --repo supabase/pg-toolbelt --state all --search 'updated:>=2026-10-09' --json number,title,state,updatedAt,url`
  - `gh pr view 471 -R supabase/pg-toolbelt --json number,title,body,state,url`
  - `gh pr view 493 -R supabase/pg-toolbelt --json number,title,body,state,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#499' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#501' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#564' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#627' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#638' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#639' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#640' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs 'pgschema#641' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs '"PARTITION OF"' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs '"VIRTUAL" generated' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs '"NOT NULL" "NOT VALID"' --json number,title,state,updatedAt,url`
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
- repo validation:
  - `python3 -m pip install --user -r requirements.txt`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py`
  - `PYTHONPATH="$HOME/.local/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
