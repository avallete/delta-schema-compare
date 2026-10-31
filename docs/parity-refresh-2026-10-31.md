# Parity refresh report - 2026-10-31

This report records the 2026-10-31 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `9de190efdf78cd422850a3bc3db13ee84a11462d`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`)

## 1) Benchmark status refresh

`git ls-remote` confirms both `main` branches are unchanged since the
2026-10-30 refresh.

- `supabase/pg-toolbelt` is still
  `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`.
- `pgplex/pgschema` is still
  `9de190efdf78cd422850a3bc3db13ee84a11462d`.

No benchmark verdict changed. Active gaps remain **021**, **022**, **024**,
and **026**. Benchmark **025** stays solved. Solved benchmarks **005**,
**007**, **008**, **013**, **015**, **016**, **017**, **018**, **019**,
**020**, and **023** stay solved.

### Current evidence on the unchanged pg-delta head

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
  `2026-10-28T11:36:22Z`). Verdict stays **tracked**.
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  `relations.ts` line 121 still uses `a.attnotnull`; lines 361-396 still
  skip PG18 `contype = 'n'` except for the comment diagnostic; `tables.ts`
  line 449 still plans plain `SET NOT NULL` / `DROP NOT NULL`. Verdict
  stays **not covered**.
- benchmark **025** / pgschema
  [#534](https://github.com/pgplex/pgschema/issues/534):
  stays **covered**. The same-table fold guard is still `internal.ts`
  lines 783-797.
- benchmark **026** / pgschema
  [#639](https://github.com/pgplex/pgschema/issues/639):
  stays **not covered**. `partitionBound` and `parentTable` are still
  `"replace"` (`tables.ts` lines 246-247). A `DETACH PARTITION` search
  under `packages/pg-delta` TypeScript still returns no matches. The
  2026-10-28 draft remains
  [`docs/parity-issue-drafts-2026-10-28.md`](parity-issue-drafts-2026-10-28.md).

Exact duplicate searches for `pgschema#499`, `pgschema#501`,
`pgschema#564`, `pgschema#534`, `pgschema#639`, `pgschema#670`,
`pgschema#673`, `pgschema#674`, and `pgschema#677` still returned no
dedicated pg-toolbelt issue or PR.

## 2) pgschema movement since 2026-10-30

No commits landed on `pgschema` `main`. The newest issue is still closed
[#677](https://github.com/pgplex/pgschema/issues/677), already recorded as
**covered**.

The only newer item is open PR
[#679](https://github.com/pgplex/pgschema/pull/679), created
`2026-10-30T08:51:42Z` and updated `2026-10-30T09:11:22Z` (commit
`16b7d85e`). It is not merged. It would close
[#670](https://github.com/pgplex/pgschema/issues/670) by shortening the
online-index `_pgschema_new` candidate when `name + "_pgschema_new"` would
exceed 63 bytes. Issue #670's `updatedAt` is still
`2026-10-27T21:05:08Z`.

That candidate-name collision is **not parity** for pg-delta. pg-delta does
not stage concurrent index builds under `_pgschema_new`. A search for that
token under `packages/pg-delta` returns no matches. #670 stays on the open
watch list as `not_parity`. No benchmark and no tracker.

Open PR [#676](https://github.com/pgplex/pgschema/pull/676) is still the
unmerged upstream fix for
[#673](https://github.com/pgplex/pgschema/issues/673). The pg-delta verdict
stays **covered** (`pg_get_constraintdef` stored as `def` and emitted
verbatim). No tracker.

[#674](https://github.com/pgplex/pgschema/issues/674) stays open and
**not covered** for a child constraint comment that differs from the
parent. The draft remains
[`docs/parity-issue-drafts-2026-10-30.md`](parity-issue-drafts-2026-10-30.md)
and was not opened. The issue is still open in pgschema, so it stays on
the watch list instead of becoming a numbered benchmark.

The open pgschema watch list is unchanged: **#49 / #52 / #84 / #559 / #597 /
#598 / #624 / #625 / #626 / #627 / #670 / #672 / #673 / #674**.

## 3) pg-toolbelt movement since 2026-10-30

`gh search issues` and `gh search prs` for `supabase/pg-toolbelt` updated
`>=2026-10-30` returned no rows. The open set is the same as the previous
refresh:

- PR [#564](https://github.com/supabase/pg-toolbelt/pull/564) still bridges
  non-superuser owner changes (issue
  [#563](https://github.com/supabase/pg-toolbelt/issues/563), `updatedAt`
  `2026-10-29T16:49:51Z`). Adjacent to #627, not a new benchmark.
- PR [#565](https://github.com/supabase/pg-toolbelt/pull/565) is still the
  alpha release (`updatedAt` `2026-10-29T10:43:18Z`).
- PR [#560](https://github.com/supabase/pg-toolbelt/pull/560) is still the
  `@supabase/pg-checks` spike (`updatedAt` `2026-10-28T10:40:32Z`).
- Issue #332 `updatedAt` is still `2026-09-29T15:57:49Z`.
- Issue #554 `updatedAt` is still `2026-10-28T11:36:22Z`.

No merged pg-toolbelt PR closes benchmarks **021**, **022**, **024**, or
**026**.

## 4) Review memory

`benchmark/review-memory.json` is unchanged. Both submodule SHAs match the
2026-10-30 fingerprints, and no watched pgschema issue `updated_at` moved.
PR #679 is open PR-only context for issue #670, which is already
`not_parity` in review memory. Numeric key order stays as it was, including
the resolved inversion of `648` before `623`.

This repository still has no local tracker issues
(`gh issue list` returned `[]`).
