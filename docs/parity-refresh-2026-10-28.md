# Parity refresh report - 2026-10-28

This report records the 2026-10-28 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `36a38ff3c25db956ae8b5be2eee552d8bc69fb47`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `6b82eff84dba925a176f0c6a78e5a16843885366`)

## 1) Benchmark status refresh

`git ls-remote` confirms `supabase/pg-toolbelt` `main` is still
`6b82eff84dba925a176f0c6a78e5a16843885366`. `pgplex/pgschema` `main` advanced
from `8703c276c3ee4bab6d4e30b14e6e8982ace14b89` to
`36a38ff3c25db956ae8b5be2eee552d8bc69fb47`. `packages/pg-delta` is unchanged,
so benchmarks **021**, **022**, **024**, and **025** keep their previous
verdicts.

One new benchmark is added:

- benchmark **026** / pgschema
  [#639](https://github.com/pgplex/pgschema/issues/639), merged PR
  [#668](https://github.com/pgplex/pgschema/pull/668): **not covered**.
  pg-delta detects bound and attachment drift by marking `partitionBound` and
  `parentTable` `"replace"`. The landed pgschema plan is
  `DETACH PARTITION` then `ATTACH PARTITION`. A search for `DETACH PARTITION`
  under `packages/pg-delta` returns no TypeScript matches. pg-delta's roadmap
  already defers this because `DROP TABLE` on a partition fails when a
  foreign key references the parent. Exact searches for `pgschema#639`,
  `DETACH PARTITION`, and `partition bound` returned no pg-toolbelt issue or
  PR. The tracker text is drafted in
  `docs/parity-issue-drafts-2026-10-28.md` and was not opened.

Solved benchmarks **005**, **007**, **008**, **013**, **015**, **016**,
**017**, **018**, **019**, **020**, **023**, and **025** stay solved.

### Current evidence on the unchanged pg-delta head

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  `relations.ts` line 189 still gates columns with `a.attislocal`;
  `tables.ts` line 52 still emits bare `PARTITION OF ... ${bound}`.
  Umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  is still the only tracker (`updatedAt` `2026-09-29T15:57:49Z`).
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  `relations.ts` lines 211 and 261 still store `generatedExpr` only;
  `tables.ts` line 712 still hard-codes `STORED`. A `VIRTUAL` search under
  `packages/pg-delta/src` still returns no matches.
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  `relations.ts` line 121 still uses `a.attnotnull`; lines 361-396 still skip
  PG18 `contype = 'n'` except for the comment diagnostic; `tables.ts` line
  449 still plans plain `SET NOT NULL` / `DROP NOT NULL`.
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  stays solved. `internal.ts` lines 779-793 still keep the same-table fold
  guard. Merged pgschema PR
  [#662](https://github.com/pgplex/pgschema/pull/662) (`MATCH FULL`) does not
  touch that guard.

## 2) pgschema movement since 2026-10-27

Commits on `8703c276..36a38ff3`:

- `36a38ff3` — [#668](https://github.com/pgplex/pgschema/pull/668) closes
  [#639](https://github.com/pgplex/pgschema/issues/639). This is benchmark
  **026**.
- `4b3bd0f6` — [#667](https://github.com/pgplex/pgschema/pull/667) closes
  [#665](https://github.com/pgplex/pgschema/issues/665). Mutually recursive
  SQL functions fail while `check_function_bodies` is on. pg-delta already
  emits `check_function_bodies = off` whenever a plan touches a routine
  (`src/plan/plan.ts` lines 823-831, covered by `src/plan/preamble.test.ts`).
  Verdict: **covered**. No new benchmark.
- `2a475ace` — [#666](https://github.com/pgplex/pgschema/pull/666) retries
  the embedded PostgreSQL launch when the probed port is taken. That is
  pgschema's process launcher, outside pg-delta schema diff.

New unlabeled issues, screened manually because the label-filtered compare
scripts still return zero rows:

- [#665](https://github.com/pgplex/pgschema/issues/665) closed completed.
  **Covered**, as above.
- [#669](https://github.com/pgplex/pgschema/issues/669) closed completed
  with no linked pull request and no source change on `main`. The report is
  pgschema's `_pgschema_new` online-index swap colliding with another
  table's index. pg-delta builds concurrent indexes under the final name
  (`src/plan/rules/indexes.ts`) and has no `_pgschema_new` candidate.
  Verdict: **not parity**.
- [#670](https://github.com/pgplex/pgschema/issues/670) open. A 63-byte
  index name plus the `_pgschema_new` suffix truncates back onto the
  original name. Same online-index mechanism. Verdict: **not parity**.
- [#671](https://github.com/pgplex/pgschema/issues/671) closed `NOT_PLANNED`.
  Apostrophes inside quoted identifiers break pgschema's desired-state
  qualifier and can plan an unexpected `DROP TABLE`. pg-delta quotes
  identifiers with `qid()` (`src/plan/render.ts`), which doubles `"` and
  leaves `'` literal inside the quotes. Verdict: **not parity**.
- [#672](https://github.com/pgplex/pgschema/issues/672) open. Resume a
  finished online index replacement without rebuilding a valid
  `_pgschema_new` candidate. Verdict: **not parity**.

The open pgschema watch list is now **#49 / #52 / #84 / #559 / #597 / #598 /
#624 / #625 / #626 / #627 / #670 / #672**. Verdicts: **#49 / #52 / #84 /
#559 / #597 / #670 / #672** = `not_parity`; **#598 / #624 / #625 / #626** =
`covered`; **#627** remains the separate global-state umbrella (PR #637
stayed closed unmerged). **#639** moves to `review-memory.resolved` as
`not_covered` (benchmark **026**). **#665** moves to `resolved` as
`covered`. **#669** and **#671** move to `resolved` as `not_parity`.

## 3) pg-toolbelt movement since 2026-10-27

Updated-since searches for `>=2026-10-27` found no merged pull requests and
no closed issues. `packages/pg-delta` on `main` did not change, so the
active-gap line citations above are unchanged.

Open items that moved:

- Issue [#561](https://github.com/supabase/pg-toolbelt/issues/561) and PR
  [#562](https://github.com/supabase/pg-toolbelt/pull/562): the Supabase
  profile hides a user-owned schema named `etl`. No pgschema counterpart.
- Issue [#563](https://github.com/supabase/pg-toolbelt/issues/563) and PR
  [#564](https://github.com/supabase/pg-toolbelt/pull/564): a non-superuser
  applier cannot plan an owner change to a role it cannot `SET ROLE` to.
  Adjacent to the global-state umbrella
  [#627](https://github.com/pgplex/pgschema/issues/627), which this repo
  still does not promote to a benchmark.
- PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) gained commit
  `67793ef` (`fix(pg-delta): pair respelled generated-name checks across a
  table rename`). The commit edits `src/frontends/settle-desired.ts` and
  `tests/schema-frontends.test.ts`. It does not touch `relations.ts`,
  `tables.ts` `columnClause()`, or the benchmark **025** fold guard. Head
  is now `67793ef`. Still unmatched rename/respell work, and still absent
  from the checked-in head.
- PR [#560](https://github.com/supabase/pg-toolbelt/pull/560) is still the
  `@supabase/pg-checks` spike. Head moved to `9dec63d` and remains outside
  schema-diff parity.

Direct views that did not move: issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332)
(`2026-09-29T15:57:49Z`), issue
[#518](https://github.com/supabase/pg-toolbelt/issues/518)
(`2026-10-26T15:10:58Z`), issue
[#554](https://github.com/supabase/pg-toolbelt/issues/554)
(`2026-10-21T15:42:52Z`), PR
[#506](https://github.com/supabase/pg-toolbelt/pull/506) (head `c284eb4`),
PR [#558](https://github.com/supabase/pg-toolbelt/pull/558) (head `9cd4770`).

Exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
`pgschema#534`, `pgschema#639`, `pgschema#665`, `pgschema#669`,
`pgschema#670`, `pgschema#671`, and `pgschema#672` returned no dedicated
pg-toolbelt issue or PR.

## 4) Review memory

`benchmark/review-memory.json` fingerprints for the revalidated open watch
list and for resolved benchmarks **499 / 501 / 534 / 564** now use pgschema
SHA `36a38ff3c25db956ae8b5be2eee552d8bc69fb47` and `reviewed_at`
`2026-10-28T08:15:00Z`. Historical resolved entries that were not revalidated
keep their older SHAs. Numeric key order is preserved, including the
pre-existing resolved inversion of `648` before `623`.
