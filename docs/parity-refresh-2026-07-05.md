# Parity refresh report - 2026-07-05

This report records the 2026-07-05 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2`)
- `pg-delta` (`repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`)

## 1) Benchmark state on this branch

The working branch originally started from the stale April benchmark snapshot, so
the first step in this run was to fast-forward it to the existing 2026-07-04
parity baseline from
`origin/avallete-ia/schema-comparison-benchmark-d7f6`.

That baseline already contains the latest benchmark-state change from the prior
refresh:

- benchmark **020** remains active for pgschema
  [#412](https://github.com/pgplex/pgschema/issues/412)
- benchmark **021** remains active for pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499)
- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta

There is therefore **no new benchmark-matrix delta on 2026-07-05** beyond the
already-ported 2026-07-04 changes.

## 2) Upstream delta versus 2026-07-04

Today’s live sweep found **no pgschema code-head delta** and **no new
parity-relevant pgschema issue / PR delta** after the 2026-07-04 refresh:

- `git -C repos/pgschema ls-remote origin HEAD` still returned
  `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2`
- `git -C repos/pg-toolbelt ls-remote origin HEAD` still returned
  `9284412d71635308ebb0c1537e0b0183d2cfa4da`
- `gh issue list --repo pgplex/pgschema --state all --search 'updated:>=2026-07-04 sort:updated-desc' --json ...`
  returned `[]`
- `gh pr list --repo pgplex/pgschema --state all --search 'updated:>=2026-07-04 sort:updated-desc' --json ...`
  returned `[]`

That means the July 4 classifications still stand:

- pgschema [#499](https://github.com/pgplex/pgschema/issues/499) remains
  **not covered** in current pg-delta and stays benchmarked as **021**
- pgschema [#501](https://github.com/pgplex/pgschema/issues/501) remains an
  **open, draft-only not_covered** parity finding with no exact pg-toolbelt
  tracker
- pgschema [#502](https://github.com/pgplex/pgschema/issues/502) remains
  **not parity work for pg-delta**
- resolved pgschema [#439](https://github.com/pgplex/pgschema/issues/439) and
  [#444](https://github.com/pgplex/pgschema/issues/444) remain **not covered**
  with no exact pg-toolbelt tracker promoted yet

## 3) pg-toolbelt tracker check

The existing exact pg-toolbelt trackers also remain unchanged:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218) is
  still open
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219) is
  still open
- the broader dependency-ordering work around resolved pgschema
  [#444](https://github.com/pgplex/pgschema/issues/444) still has only adjacent
  pg-toolbelt work in [#263](https://github.com/supabase/pg-toolbelt/issues/263)
  and [#285](https://github.com/supabase/pg-toolbelt/pull/285), not an exact
  dedicated tracker for the `DROP COLUMN` / dependent-view scenario

The only pg-toolbelt PR updated after the 2026-07-04 cutoff in today’s GitHub
sweep was
[pg-toolbelt#315](https://github.com/supabase/pg-toolbelt/pull/315), but it is
still `pg-delta-next` work rather than a default-branch parity change. No new
exact issue or PR appeared for benchmark **020**, benchmark **021**, pgschema
**#439**, **#444**, or open issue **#501**.

## 4) What changed in this refresh

This pass is intentionally a **no-new-delta confirmation refresh**:

- port the already-open 2026-07-04 benchmark refresh onto this working branch
- verify that both checked-in submodule SHAs still match upstream HEAD
- recheck the known exact trackers and draft-only candidates to avoid duplicating
  pg-toolbelt issues
- record that no additional benchmark promotion, status flip, or new draft issue
  is needed on 2026-07-05

Because the matrix, tracker state, and upstream code heads are unchanged, this
refresh does **not** modify `benchmark/README.md` or
`benchmark/review-memory.json` beyond the imported July 4 baseline.

## 5) Commands executed for this confirmation pass

```bash
git -C /workspace merge --ff-only origin/avallete-ia/schema-comparison-benchmark-d7f6
git -C /workspace submodule update --init --recursive

git -C /workspace/repos/pgschema ls-remote origin HEAD
git -C /workspace/repos/pg-toolbelt ls-remote origin HEAD

env -u GITHUB_TOKEN gh issue view 499 --repo pgplex/pgschema
env -u GITHUB_TOKEN gh issue view 501 --repo pgplex/pgschema
env -u GITHUB_TOKEN gh issue view 502 --repo pgplex/pgschema
env -u GITHUB_TOKEN gh issue view 439 --repo pgplex/pgschema
env -u GITHUB_TOKEN gh issue view 444 --repo pgplex/pgschema

env -u GITHUB_TOKEN gh issue view 218 --repo supabase/pg-toolbelt
env -u GITHUB_TOKEN gh issue view 219 --repo supabase/pg-toolbelt
env -u GITHUB_TOKEN gh issue view 263 --repo supabase/pg-toolbelt
env -u GITHUB_TOKEN gh pr view 285 --repo supabase/pg-toolbelt

env -u GITHUB_TOKEN gh issue list --repo pgplex/pgschema --state all --search 'updated:>=2026-07-04 sort:updated-desc' --json number,title,state,updatedAt,url
env -u GITHUB_TOKEN gh pr list --repo pgplex/pgschema --state all --search 'updated:>=2026-07-04 sort:updated-desc' --json number,title,state,updatedAt,url
env -u GITHUB_TOKEN gh issue list --repo supabase/pg-toolbelt --state all --search 'updated:>=2026-07-04 sort:updated-desc' --json number,title,state,updatedAt,url
env -u GITHUB_TOKEN gh pr list --repo supabase/pg-toolbelt --state all --search 'updated:>=2026-07-04 sort:updated-desc' --json number,title,state,updatedAt,url
```

## 6) Conclusion

The latest state on 2026-07-05 is:

- **no new parity delta** versus the 2026-07-04 refresh
- active benchmarked gaps remain **020** and **021**
- existing tracked open parity issues remain **pg-toolbelt#218** and
  **pg-toolbelt#219**
- draft-only unresolved parity candidates remain **pgschema #501**, plus the
  already-documented resolved-but-untracked items **#439** and **#444**

So the correct action for this run is to preserve the July 4 benchmark state on
this branch, avoid opening duplicate trackers, and save this dated confirmation
report in the PR.
