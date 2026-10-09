# Parity refresh report - 2026-10-09

This report records the 2026-10-09 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `3c60914eae50ff9d28084a8a1ce4e110b9c3d55d`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pg-delta` from
`8a62438b03300c1922cb04b292d2140fcc694b25` to
`3c60914eae50ff9d28084a8a1ce4e110b9c3d55d` through merged PRs
[#528](https://github.com/supabase/pg-toolbelt/pull/528) and
[#529](https://github.com/supabase/pg-toolbelt/pull/529), while
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
    surfaces open issue
    [#530](https://github.com/supabase/pg-toolbelt/issues/530), but that issue
    is about rewrite-risk declarations for inherited / partition children,
    not child-local override extraction
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated`, but only preserves generated-expression presence, not the
    `VIRTUAL` versus `STORED` kind itself
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - exact duplicate search `pgschema#501` still returns no dedicated
    pg-toolbelt issue or PR; keyword `"VIRTUAL" generated --include-prs"` still
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
    pg-toolbelt issue or PR; keyword `"NOT NULL" "NOT VALID" --include-prs"`
    still surfaces merged domain-only PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484)

### Upstream movement since 2026-10-08

- `gh search issues --repo pgplex/pgschema --updated '>=2026-10-08'`
  surfaced open issues [#625](https://github.com/pgplex/pgschema/issues/625)
  and [#626](https://github.com/pgplex/pgschema/issues/626)
- both new pgschema issues remain **covered** in current pg-delta:
  - **#625** by composite `typeAttribute` facts plus
    `ALTER TYPE ... ADD ATTRIBUTE ... CASCADE` planning in
    `src/plan/rules/types.ts`
  - **#626** by dependency extraction in
    `src/extract/dependencies.ts`, which resolves composite-attribute edges
    through array / row-type resolution onto the owning table fact
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-08'`
  surfaced merged PRs [#528](https://github.com/supabase/pg-toolbelt/pull/528)
  and [#529](https://github.com/supabase/pg-toolbelt/pull/529), open PRs
  [#514](https://github.com/supabase/pg-toolbelt/pull/514),
  [#522](https://github.com/supabase/pg-toolbelt/pull/522),
  [#527](https://github.com/supabase/pg-toolbelt/pull/527), and
  [#532](https://github.com/supabase/pg-toolbelt/pull/532), open issues
  [#525](https://github.com/supabase/pg-toolbelt/issues/525),
  [#530](https://github.com/supabase/pg-toolbelt/issues/530), and
  [#531](https://github.com/supabase/pg-toolbelt/issues/531), plus closed
  issue [#519](https://github.com/supabase/pg-toolbelt/issues/519)
- direct inspection of those updated items plus
  `git -C repos/pg-toolbelt diff --name-only 8a62438b03300c1922cb04b292d2140fcc694b25..3c60914eae50ff9d28084a8a1ce4e110b9c3d55d`
  showed the merged code lands in declarative-e2e infrastructure plus
  extension-member grant export / policy handling, not the active benchmark
  source paths
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  returned `[]`

The active benchmark set therefore remains **021**, **022**, and **024**.
There is still **no open uncovered parity candidate** on the pgschema side.

## 2) Open / resolved pgschema delta on 2026-10-09

The current open pgschema watch list is now:

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597),
  [#598](https://github.com/pgplex/pgschema/issues/598),
  [#623](https://github.com/pgplex/pgschema/issues/623),
  [#624](https://github.com/pgplex/pgschema/issues/624),
  [#625](https://github.com/pgplex/pgschema/issues/625), and
  [#626](https://github.com/pgplex/pgschema/issues/626)
- open PRs [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622)

Current verdicts remain:

- open issues **#49**, **#52**, **#84**, **#559**, **#597**, and **#623**
  remain **not parity work for pg-delta**
- open issues **#598**, **#624**, **#625**, and **#626** remain **covered**
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
  `3c60914eae50ff9d28084a8a1ce4e110b9c3d55d`
- keep the checked-in/live `repos/pgschema` submodule pointer at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- refresh `benchmark/README.md` to the 2026-10-09 latest-state snapshot
- append 2026-10-09 refresh notes to active benchmarks **021**, **022**, and
  **024**
- refresh `benchmark/review-memory.json` review timestamps and fingerprints for
  the current open-watch list, the two new open issues **#625** / **#626**, and
  the current active benchmark / recently-screened closed-issue set
- add this report as the 2026-10-09 latest-state sweep

No benchmark file changed verdict, and no new tracker issue draft was needed.

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- direct submodule head checks:
  - `git -C repos/pgschema rev-parse HEAD`
  - `git -C repos/pg-toolbelt rev-parse HEAD`
  - `git -C repos/pg-toolbelt log --oneline 8a62438b03300c1922cb04b292d2140fcc694b25..3c60914eae50ff9d28084a8a1ce4e110b9c3d55d`
  - `git -C repos/pg-toolbelt diff --name-only 8a62438b03300c1922cb04b292d2140fcc694b25..3c60914eae50ff9d28084a8a1ce4e110b9c3d55d`
  - `git -C repos/pg-toolbelt diff --name-only 8a62438b03300c1922cb04b292d2140fcc694b25..3c60914eae50ff9d28084a8a1ce4e110b9c3d55d -- packages/pg-delta/src/extract/relations.ts packages/pg-delta/src/extract/dependencies.ts packages/pg-delta/src/plan/rules/tables.ts packages/pg-delta/src/plan/rules/helpers.ts packages/pg-delta/src/plan/rules/types.ts`
- GitHub CLI updated-state and duplicate checks:
  - `gh search issues --repo pgplex/pgschema --updated '>=2026-10-08' --json number,title,state,updatedAt,url`
  - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-08' --json number,title,state,updatedAt,url`
  - `gh issue view 625 -R pgplex/pgschema --json number,title,body,state,updatedAt,url`
  - `gh issue view 626 -R pgplex/pgschema --json number,title,body,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-08' --json number,title,state,updatedAt,url`
  - `gh issue view 530 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url`
  - `gh issue view 531 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url`
  - `gh issue view 525 -R supabase/pg-toolbelt --json number,title,body,state,updatedAt,url`
  - `gh pr view 529 -R supabase/pg-toolbelt --json number,title,body,state,mergedAt,url,headRefName,baseRefName`
  - `gh pr view 532 -R supabase/pg-toolbelt --json number,title,body,state,url,headRefName,baseRefName`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#499' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#501' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#564' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#625' --json number,title,state,updatedAt,url`
  - `gh search issues --repo supabase/pg-toolbelt 'pgschema#626' --json number,title,state,updatedAt,url`
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
