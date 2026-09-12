# PostgreSQL 18 native `NOT NULL` validation workflow

> pgschema issue [#564](https://github.com/pgplex/pgschema/issues/564) (closed), implemented by [pgschema#566](https://github.com/pgplex/pgschema/pull/566) and follow-up [pgschema#587](https://github.com/pgplex/pgschema/pull/587)

## Context

pgschema issue #564 started as a request for a safer way to introduce `NOT NULL`
requirements without collapsing everything to a single immediate
`ALTER COLUMN ... SET NOT NULL` step. Upstream now handles that family on
PostgreSQL 18 in two pieces:

1. PR #566 rewrites nullable -> `NOT NULL` changes to PostgreSQL 18's native
   `ADD CONSTRAINT ... NOT NULL <column> NOT VALID` plus
   `VALIDATE CONSTRAINT`.
2. PR #587 fixes the follow-up drift hole where a pending invalid PG18 `NOT
   NULL` constraint was invisible on the next run because `attnotnull` was
   already true.

Current pg-delta does not preserve that PG18-native state. It still models
column nullability only as a boolean `notNull` fact, emits a direct
`ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`, and does not extract PG18's
`contype = 'n'` constraint rows as diff-visible state.

## Refresh note (2026-09-12)

This recheck keeps checked-in/live `pg-delta` at
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) and keeps checked-in/live
`pgschema` at `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`.

There is no upstream code delta on either side since the 2026-09-11 refresh.
The only new pgschema activity is open issue
[#594](https://github.com/pgplex/pgschema/issues/594), which is a
`.pgschemaignore` view-filtering report and remains outside this PG18
nullability workflow. The active not-null gap is therefore unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still records
  column nullability from `a.attnotnull` and filters table constraints to
  `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` pending-
  validation state remains invisible.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits a
  plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` in `notNull.alter`.
- open PRs [#470](https://github.com/supabase/pg-toolbelt/pull/470),
  [#471](https://github.com/supabase/pg-toolbelt/pull/471), and
  [#472](https://github.com/supabase/pg-toolbelt/pull/472) remain adjacent or
  unrelated; none closes this PG18 native not-null workflow gap.

Direct exact searches for `pgschema#564` and `pgschema#594` still return no
dedicated pg-toolbelt issue or PR for this nullability workflow. Benchmark 024
therefore remains **not covered** in current pg-delta.

## Refresh note (2026-09-11)

This recheck advances checked-in/live `pg-delta` from
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) to
`85e8946a79b0a5b149fe9a772fef882c14cb9567`
(`@supabase/pg-delta@1.0.0-alpha.50`) and advances checked-in/live
`pgschema` from `738a3bb40cf6b062928eeb564e3a98ec7f3c6989` to
`319b88c83d62b2c9a62eff7a09ec6563954bcf4b` through merged PR
[#592](https://github.com/pgplex/pgschema/pull/592).

Today's upstream delta is elsewhere, and the active PG18 not-null path remains
unchanged:

- `git diff` between the two pg-delta heads is empty for the active files
  `src/extract/relations.ts`, `src/plan/rules/helpers.ts`,
  `src/plan/rules/tables.ts`, and the generated-column corpus, so alpha.50
  still carries the same nullability modeling limits as alpha.49.
- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still records
  column nullability from `a.attnotnull` and filters table constraints to
  `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` pending-
  validation state remains invisible.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits a
  plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` in `notNull.alter`.
- resolved pgschema issue [#591](https://github.com/pgplex/pgschema/issues/591)
  and open issue [#593](https://github.com/pgplex/pgschema/issues/593) cover
  adjacent generated-column and collation fidelity work, but neither changes
  this nullability workflow.

Direct exact searches for `pgschema#564`, `pgschema#591`, and `pgschema#593`
still return no dedicated pg-toolbelt issue or PR for this nullability
workflow. Benchmark 024 therefore remains **not covered** in current
pg-delta.

## Refresh note (2026-09-10)

This recheck keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main`
still at `ce61f01c24962fe21b9d02b319d8c26be0b5fd13`, and keeps
checked-in/live `pgschema` at `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`.

Today's new upstream activity is elsewhere: open pgschema issue
[#591](https://github.com/pgplex/pgschema/issues/591) plus PR
[#592](https://github.com/pgplex/pgschema/pull/592) land in generated-column
comparison, open issue [#593](https://github.com/pgplex/pgschema/issues/593)
lands in column-collation dump fidelity, and open pg-toolbelt PRs
[#470](https://github.com/supabase/pg-toolbelt/pull/470),
[#471](https://github.com/supabase/pg-toolbelt/pull/471), and
[#472](https://github.com/supabase/pg-toolbelt/pull/472) stay adjacent. The
active PG18 not-null gap therefore remains unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still records
  column nullability from `a.attnotnull` and filters table constraints to
  `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` pending-
  validation state remains invisible
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits a
  plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` in `notNull.alter`

Direct exact searches for `pgschema#564`, `pgschema#591`, and `pgschema#593`
still return no dedicated pg-toolbelt issue or PR for this nullability
workflow. Benchmark 024 therefore remains **not covered** in current
pg-delta.

## Refresh note (2026-09-09)

This benchmark is newly promoted from the earlier draft note in
[`docs/parity-issue-drafts-2026-08-31.md`](../docs/parity-issue-drafts-2026-08-31.md).

The 2026-09-09 refresh keeps the checked-in `pg-delta` baseline at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`), observes live `pg-toolbelt/main` at
`ce61f01c24962fe21b9d02b319d8c26be0b5fd13` through merged PRs
[#460](https://github.com/supabase/pg-toolbelt/pull/460),
[#461](https://github.com/supabase/pg-toolbelt/pull/461),
[#462](https://github.com/supabase/pg-toolbelt/pull/462),
[#464](https://github.com/supabase/pg-toolbelt/pull/464),
[#467](https://github.com/supabase/pg-toolbelt/pull/467), and
[#469](https://github.com/supabase/pg-toolbelt/pull/469), and advances
checked-in/live `pgschema` to `738a3bb40cf6b062928eeb564e3a98ec7f3c6989`
through merged PRs
[#585](https://github.com/pgplex/pgschema/pull/585),
[#586](https://github.com/pgplex/pgschema/pull/586),
[#587](https://github.com/pgplex/pgschema/pull/587), and
[#590](https://github.com/pgplex/pgschema/pull/590).

The new live pg-delta delta is adjacent rather than gap-closing for this
benchmark. Between the checked-in alpha.49 head and live `main`, the active
nullability path is still unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still records
  column nullability from `a.attnotnull` and extracts table constraints only
  when `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18
  `contype = 'n'` state remains invisible.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits a
  plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` in `notNull.alter`.

Direct exact searches for `pgschema#564` still return no dedicated pg-toolbelt
issue or PR. Benchmark 024 therefore enters the resolved-issue benchmark set as
**not covered** in current pg-delta.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
    id integer PRIMARY KEY,
    email text
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.users
  ADD CONSTRAINT users_email_not_null
  NOT NULL email
  NOT VALID;
```

**Expected:** on PostgreSQL 18+, pg-delta preserves the native `NOT NULL`
constraint state or emits an equivalent two-step plan such as:

```sql
ALTER TABLE test_schema.users
  ADD CONSTRAINT users_email_not_null NOT NULL email NOT VALID;

ALTER TABLE test_schema.users
  VALIDATE CONSTRAINT users_email_not_null;
```

and a later re-check can still see a pending validation step if the constraint
exists but remains unvalidated.

**Actual on current pg-delta:** the extractor collapses the branch state to
`notNull = true` on the column, ignores the PG18 `contype = 'n'` constraint
row, and the planner falls back to a direct
`ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`. A later pending-validate-only
state is also invisible because there is no extracted invalid-not-null fact to
diff.

## How pgschema handled it

pgschema PR #566 threads the target PostgreSQL major version into planning and,
on PostgreSQL 18+, rewrites nullability changes to the native `NOT NULL ...
NOT VALID` form plus `VALIDATE CONSTRAINT`. It keeps older PostgreSQL versions
on the previous portable fallback path.

pgschema PR #587 then closes the remaining gap by joining `pg_constraint` for
pending `contype = 'n'` rows with `convalidated = false`, exposing that as
column-level state, and re-emitting `VALIDATE CONSTRAINT <name>` on the next
plan when validation is still pending.

The merged upstream fixtures now cover both the native rewrite and the
follow-up revalidation path in `testdata/diff/online/add_not_null/`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| PG18 native `NOT NULL ... NOT VALID` state preserved as a diff-visible fact | No - `src/extract/relations.ts` tracks `a.attnotnull` on columns but filters extracted constraints to `con.contype IN ('p', 'u', 'f', 'c', 'x')` |
| Pending invalid PG18 `NOT NULL` constraint can be revalidated on the next diff | No - there is no `invalid_not_null_constraint`-style field in the extracted column payload |
| Planner rewrite for nullable -> `NOT NULL` on PG18+ | No - `src/plan/rules/tables.ts` still emits plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` |
| Generic `VALIDATE CONSTRAINT` support exists at all | Partial - `src/plan/rules/constraints.ts` can emit `VALIDATE CONSTRAINT`, but only for extracted table/domain constraints, not PG18 native not-null constraints |
| Existing exact pg-toolbelt issue / PR | No dedicated exact tracker found during the 2026-09-09 refresh |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **PG18 nullability representation** | Preserves native `NOT NULL ... NOT VALID` state and pending validation | Collapses the state to column `notNull = true` |
| **Planner behavior** | Emits native PG18 add + validate workflow | Emits a direct `SET NOT NULL` |
| **Follow-up visibility after interrupted validation** | Re-emits `VALIDATE CONSTRAINT` | Pending validation is invisible |
| **Current parity state** | Fixed | Not covered |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
   (or an adjacent extractor) so PG18 native not-null constraints become
   diff-visible state instead of collapsing entirely into `attnotnull`.
2. Preserve a pending-invalid marker in the column or constraint payload so a
   later diff can emit `VALIDATE CONSTRAINT`.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
   so PG18+ nullability changes can emit
   `ADD CONSTRAINT ... NOT NULL <column> NOT VALID` plus
   `VALIDATE CONSTRAINT`.
4. Add focused regression coverage for both:
   - nullable -> `NOT NULL` on PostgreSQL 18
   - a pre-existing invalid PG18 not-null constraint that should re-emit
     `VALIDATE CONSTRAINT`
