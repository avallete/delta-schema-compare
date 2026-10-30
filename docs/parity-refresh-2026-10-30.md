# Parity refresh report - 2026-10-30

This report records the 2026-10-30 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9de190efdf78cd422850a3bc3db13ee84a11462d`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`)

## 1) Benchmark status refresh

`git ls-remote` confirms both `main` branches moved since the 2026-10-28
refresh.

- `supabase/pg-toolbelt` advanced from
  `6b82eff84dba925a176f0c6a78e5a16843885366` to
  `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`.
- `pgplex/pgschema` advanced from
  `36a38ff3c25db956ae8b5be2eee552d8bc69fb47` to
  `9de190efdf78cd422850a3bc3db13ee84a11462d`.

No benchmark verdict changed. Active gaps remain **021**, **022**, **024**,
and **026**. Benchmark **025** stays solved. Solved benchmarks **005**,
**007**, **008**, **013**, **015**, **016**, **017**, **018**, **019**,
**020**, and **023** stay solved.

### Current evidence on the new pg-delta head

Merged PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) is the
only `packages/pg-delta` change. It settles renamed check spelling before
rename discovery and inserts a rename-cycle guard in
`src/plan/internal.ts`. It does not edit `relations.ts` or
`src/plan/rules/tables.ts`.

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  `relations.ts` line 189 still gates columns with `a.attislocal`;
  `tables.ts` line 52 still emits bare `PARTITION OF ... ${bound}`.
  Umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  is still the only tracker (`updatedAt` `2026-09-29T15:57:49Z`).
  Verdict stays **tracked**.
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  `relations.ts` lines 211 and 261 still store `generatedExpr` only;
  `tables.ts` line 712 still hard-codes `STORED`. A `VIRTUAL` search under
  `packages/pg-delta` TypeScript still returns no matches.
  Open follow-up [#554](https://github.com/supabase/pg-toolbelt/issues/554)
  is still that zero-arg IMMUTABLE apply failure (`updatedAt`
  `2026-10-28T11:36:22Z`, no comments). Verdict stays **tracked**.
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  `relations.ts` line 121 still uses `a.attnotnull`; lines 361-396 still
  skip PG18 `contype = 'n'` except for the comment diagnostic; `tables.ts`
  line 449 still plans plain `SET NOT NULL` / `DROP NOT NULL`. Verdict
  stays **not covered**.
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  stays **covered**. The same-table fold guard moved from `internal.ts`
  lines 779-793 to lines 783-797. The check itself is unchanged.
- benchmark **026** / pgschema
  [#639](https://github.com/pgplex/pgschema/issues/639):
  stays **not covered**. `partitionBound` and `parentTable` are still
  `"replace"` (`tables.ts` lines 246-247). A `DETACH PARTITION` search
  under `packages/pg-delta` TypeScript still returns no matches. The
  2026-10-28 draft remains
  [`docs/parity-issue-drafts-2026-10-28.md`](parity-issue-drafts-2026-10-28.md).

Exact duplicate searches for `pgschema#499`, `pgschema#501`,
`pgschema#564`, `pgschema#534`, and `pgschema#639` still returned no
dedicated pg-toolbelt issue or PR.

## 2) pgschema movement since 2026-10-28

Commits on `36a38ff3..9de190ef`:

- `9de190ef` — [#678](https://github.com/pgplex/pgschema/pull/678) closes
  [#677](https://github.com/pgplex/pgschema/issues/677). When a function or
  procedure is planned as `DROP` + `CREATE`, an unchanged `COMMENT ON` was
  omitted, so the next plan re-added it. pg-delta already recreates
  unchanged child facts of a replaced routine
  (`src/plan/phases/action-emitter.ts` lines 373-389). Comment rendering
  for functions and procedures is pinned in
  `src/plan/routine-metadata.test.ts`. Verdict: **covered**. No new
  benchmark.
- `f2ebe96b` — [#675](https://github.com/pgplex/pgschema/pull/675) updates
  the Alpine base image. Outside schema-diff parity.

PR #678 also notes that unchanged `GRANT`s on a recreated function are
lost in pgschema, and that the same loss applies to recreated views and
materialized views. That follow-up is not filed as a pgschema issue.
pg-delta recreates ACL children on the same replace walk, so it is not a
pg-delta gap. It stays watch-only until pgschema files it.

New unlabeled issues, screened manually because the label-filtered compare
scripts still return zero rows:

- [#673](https://github.com/pgplex/pgschema/issues/673) open. Dump and plan
  drop `INCLUDE` columns from PRIMARY KEY and UNIQUE constraints. pg-delta
  stores `pg_get_constraintdef` as `def` (`relations.ts` line 335) and
  emits that text verbatim (`constraints.ts` lines 18-21 and the fold
  clause). `def` is `"replace"`, so an INCLUDE-only change is a constraint
  replace. Partition children clone the parent definition through
  `PARTITION OF`, which is why `conislocal = false` child constraints stay
  unextracted without losing INCLUDE. Open pgschema PR
  [#676](https://github.com/pgplex/pgschema/pull/676) is not merged.
  Exact search for `pgschema#673` returned no pg-toolbelt issue or PR.
  Verdict: **covered**. No tracker opened.
- [#674](https://github.com/pgplex/pgschema/issues/674) open. Distinct
  comments on a partitioned parent's constraint and on the inherited child
  constraint are lost. Local constraint comments are already covered:
  `pushWithMeta` attaches `obj_description`, `metadata.ts` alters comment
  text in place, and `commentTarget` renders
  `COMMENT ON CONSTRAINT ... ON table` (`render.ts` lines 51-52). Inherited
  rows are filtered with `con.conislocal` (`relations.ts` line 360).
  `tests/diagnostic-noise.test.ts` already calls that skip a separate
  pre-existing gap. A child comment therefore never becomes a fact, and
  PostgreSQL does not copy the parent's comment onto the clone. Exact
  search for `pgschema#674` returned no pg-toolbelt issue or PR. Umbrella
  issue #332 item 4 is view and materialized-view column comments, not
  this case. Verdict: **not covered** for the inherited child comment.
  Drafted in
  [`docs/parity-issue-drafts-2026-10-30.md`](parity-issue-drafts-2026-10-30.md)
  and not opened. The issue is still open in pgschema, so it stays on the
  watch list instead of becoming a numbered benchmark.
- [#677](https://github.com/pgplex/pgschema/issues/677) closed completed.
  **Covered**, as above.

The open pgschema watch list is now **#49 / #52 / #84 / #559 / #597 / #598 /
#624 / #625 / #626 / #627 / #670 / #672 / #673 / #674**. Verdicts are
unchanged for the previous twelve. **#673** is `covered`. **#674** is
`not_covered`. **#677** moves to `resolved` as `covered`.

## 3) pg-toolbelt movement since 2026-10-28

Updated-since searches for `>=2026-10-28`:

- Merged PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) closes
  issue [#535](https://github.com/supabase/pg-toolbelt/issues/535). This is
  the settle-before-rename work. It does not close benchmarks **021**,
  **022**, **024**, or **026**. The roadmap gained a "PR #555 review
  triage" section for deferred rename-settling gaps (generated child names,
  ambiguous respelled checks, owner cycles). Those are unmatched on the
  pgschema side and are not new benchmarks.
- Issue [#561](https://github.com/supabase/pg-toolbelt/issues/561) closed.
  PR [#562](https://github.com/supabase/pg-toolbelt/pull/562) closed
  unmerged. Supabase `etl` schema hiding. No pgschema counterpart.
- PR [#506](https://github.com/supabase/pg-toolbelt/pull/506), PR
  [#493](https://github.com/supabase/pg-toolbelt/pull/493), and PR
  [#548](https://github.com/supabase/pg-toolbelt/pull/548) closed unmerged.
  Policy suppression, unsettable owners, and `pgrst.*` role settings.
  Adjacent to pgschema [#627](https://github.com/pgplex/pgschema/issues/627),
  which stays a separate global-state umbrella.
- Issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) closed.
  Cluster-global roles in database scope. Not a pgschema parity benchmark.
- Open PR [#564](https://github.com/supabase/pg-toolbelt/pull/564) still
  bridges non-superuser owner changes (issue
  [#563](https://github.com/supabase/pg-toolbelt/issues/563)). Adjacent to
  #627, not a new benchmark.
- Open PR [#565](https://github.com/supabase/pg-toolbelt/pull/565) is the
  alpha release. Open PR
  [#560](https://github.com/supabase/pg-toolbelt/pull/560) is still the
  `@supabase/pg-checks` spike (head `1b3a5bc`).

Direct views that did not change behavior: issue #332
(`updatedAt` `2026-09-29T15:57:49Z`). Issue #554's timestamp moved and its
body did not.

## 4) Review memory

`benchmark/review-memory.json` fingerprints for the revalidated open watch
list and for resolved benchmarks **499 / 501 / 534 / 564 / 639** now use
pg-delta SHA `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`, pgschema SHA
`9de190efdf78cd422850a3bc3db13ee84a11462d`, and `reviewed_at`
`2026-10-30T08:00:00Z`. **#673** and **#674** are added under `open`.
**#677** is added under `resolved` as `covered`. Historical resolved
entries that were not revalidated keep their older SHAs. Numeric key order
is preserved, including the pre-existing resolved inversion of `648` before
`623`.
