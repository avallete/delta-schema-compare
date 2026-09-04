# PostgreSQL 18 `VIRTUAL` generated columns

> pgschema issue [#501](https://github.com/pgplex/pgschema/issues/501) (closed), fixed by [pgschema#503](https://github.com/pgplex/pgschema/pull/503)

## Context

pgschema issue #501 reports that PostgreSQL 18 `VIRTUAL` generated columns
were being rewritten into invalid non-generated SQL during pgschema's plan
output. pg-delta does not share that exact desired-state SQL rewrite path,
but the user-visible parity gap still exists: current pg-delta does not
preserve the generated-column kind and collapses PostgreSQL's
`VIRTUAL` versus `STORED` distinction away.

That means pg-delta can still lose the distinction between `VIRTUAL` and
`STORED` generated columns even though it avoids the precise upstream bug
mechanism. This benchmark tracks the now-resolved upstream scenario after
pgschema merged its fix on `main`, while current pg-delta still lacks exact
coverage.

## Refresh note (2026-09-04)

This recheck keeps checked-in/live `pg-delta` at
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) and advances checked-in/live
`pgschema` from `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` to
`89265906bd4d1a5c65971529989a81eb8b159d96` through merged PR
[#577](https://github.com/pgplex/pgschema/pull/577).

The upstream delta since the 2026-09-03 refresh is on the pgschema side only.
It fixes sequence ownership / SERIAL collapsing for issues
[#573](https://github.com/pgplex/pgschema/issues/573),
[#574](https://github.com/pgplex/pgschema/issues/574), and
[#576](https://github.com/pgplex/pgschema/issues/576), and does not touch the
active generated-column extract / plan path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, while keyword duplicate searches for `VIRTUAL
generated` still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Benchmark 022
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-09-03)

This recheck advances checked-in/live `pg-delta` from
`107ac3df4b889c527215d1f6a37df64b33154c16`
(`@supabase/pg-delta@1.0.0-alpha.48`) to
`08219f1a8832f86e7287e50bab793a498129db7a`
(`@supabase/pg-delta@1.0.0-alpha.49`) through merged PR
[#455](https://github.com/supabase/pg-toolbelt/pull/455) and release
[#457](https://github.com/supabase/pg-toolbelt/pull/457), and advances
checked-in/live `pgschema` from
`97d8d60dd72a46704cc63b71b63aab2784847658`
(`v1.12.5`) to `5f76bfd8c8ca63cfbd3f0c43e55f7ad34ecca623` through merged PR
[#572](https://github.com/pgplex/pgschema/pull/572).

The new pg-delta delta only touches `packages/pg-delta/src/plan/internal.ts`
plus enum/default ordering tests and corpus fixtures, while the new pgschema
delta only touches quoted-identifier dependency detection for issue
[#571](https://github.com/pgplex/pgschema/issues/571). The active generated-
column extract / plan path is unchanged:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The last focused 2026-08-14 runtime observation therefore still stands and
serialized the generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`, and
the proof loop still returned `proofOk: true` with zero drift after that
rewrite. Direct exact searches for `pgschema#501` still return no dedicated
pg-toolbelt issue or PR, while keyword duplicate searches for `VIRTUAL
generated` still only surface umbrella fidelity tracker
[#332](https://github.com/supabase/pg-toolbelt/issues/332). Benchmark 022
therefore remains **behaviorally uncovered** with only **umbrella-thread
tracker context**.

## Refresh note (2026-08-31)

This recheck keeps checked-in/live `pg-delta` at
`107ac3df4b889c527215d1f6a37df64b33154c16`
(`@supabase/pg-delta@1.0.0-alpha.48`) and advances checked-in/live
`pgschema` to `97d8d60dd72a46704cc63b71b63aab2784847658`
(`v1.12.5`) through merged PRs
[#565](https://github.com/pgplex/pgschema/pull/565),
[#566](https://github.com/pgplex/pgschema/pull/566),
[#567](https://github.com/pgplex/pgschema/pull/567), and
[#568](https://github.com/pgplex/pgschema/pull/568).

A source recheck on the current pg-delta head still finds the same uncovered
path:

- `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
  `attgenerated` but only preserves generated-expression presence as
  `generatedExpr`, not the actual `VIRTUAL` versus `STORED` kind.
- `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
  hard-codes generated-column rendering as
  `GENERATED ALWAYS AS (...) STORED`.

The upstream delta since the 2026-08-30 refresh is on the pgschema side rather
than the pg-delta side. Those new pgschema changes land in online rewrite,
constraint-validation, docs, and release surfaces, while the active
`relations.ts` / `helpers.ts` codepaths above remain unchanged, so the last
focused 2026-08-14 runtime observation still stands and serialized the
generated column as:

```sql
ALTER TABLE "test_schema"."users"
  ADD COLUMN "full_name" text GENERATED ALWAYS AS (((first_name || ' '::text) || last_name)) STORED
```

The PostgreSQL 18 `VIRTUAL` keyword is still collapsed back to `STORED`.
The same proof still returned `proofOk: true` with zero drift, which means
the current extract/model path is also collapsing the kind strongly enough
that the proof loop cannot see the mismatch yet.

There is still no dedicated exact pg-toolbelt issue or PR for this scenario on
2026-08-31. Direct exact searches for `pgschema#501` still return nothing, and
keyword duplicate searches for `VIRTUAL generated` still only surface umbrella
fidelity tracker [#332](https://github.com/supabase/pg-toolbelt/issues/332).
Comments on that issue thread (not the original issue body) still carry the
PG17/18 virtual-generated-column note. Benchmark 022 therefore remains
**behaviorally uncovered** with only **umbrella-thread tracker context**.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.users (
    first_name text,
    last_name text
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.users
  ADD COLUMN full_name text GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL;
```

**Expected:** pg-delta preserves the PostgreSQL 18 `VIRTUAL` generated-
column kind when diffing and serializing the migration plan.

**Actual on current pg-delta:** current pg-delta emits `... STORED`
instead. The focused 2026-08-14 proof also reported zero drift afterward,
which means the current extract/model path is not preserving the
`VIRTUAL` / `STORED` distinction as diff-visible state yet.

## How pgschema handled it

pgschema fixed the issue in PR #503 by preserving the generated-column kind
through inspection and diff planning instead of collapsing it to a single
generated/not-generated state.

The merged fix added regression data under:

- `repos/pgschema/testdata/diff/create_table/issue_501_virtual_generated_column/`

That fixture now records `GENERATED ALWAYS AS (...) VIRTUAL` in the
expected plan output, confirming that upstream keeps the PostgreSQL 18
keyword intact in the resolved scenario.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Extract reads generated columns at all | Partially - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` reads `attgenerated`, but only uses it to decide whether `default_expr` should be treated as a generated expression |
| Extract / IR preserves `VIRTUAL` vs `STORED` kind | No - the current payload stores `generatedExpr` but not the actual generated kind |
| SQL emission preserves `VIRTUAL` | No - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` hard-codes `... STORED` in `columnClause()` |
| Focused proof on the exact PG18 scenario | No user-visible fidelity - the focused 2026-08-14 probe emitted `... STORED` yet still proved cleanly because the current model collapses the kind |
| Existing exact pg-toolbelt issue / PR | No dedicated exact tracker or PR yet; keyword duplicate searches only surface umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332), and comments on that issue thread now carry the PG17/18 virtual-generated-column note |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog / IR representation** | Preserves generated-column kind through the resolved fix | Collapses `attgenerated` down to generated-expression presence |
| **Plan / SQL emission** | Emits `VIRTUAL` when the schema requires it | Emits `GENERATED ALWAYS AS (...) STORED` |
| **Current parity state** | Fixed | Only umbrella-thread context under [#332](https://github.com/supabase/pg-toolbelt/issues/332); still behaviorally uncovered |

## Plan to handle it in pg-delta

1. Preserve the actual PostgreSQL generated-column kind from
   `attgenerated` in the extracted facts instead of collapsing it to
   generated-expression presence.
2. Update the diff path so `VIRTUAL` versus `STORED` is treated as a
   meaningful change.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts`
   (and any related create/alter rule helpers) so generated-column SQL
   preserves the correct PostgreSQL 18 keyword.
4. Add a focused pg18 regression under `packages/pg-delta/tests/` for the
   exact `VIRTUAL` scenario above, and make sure the proof loop fails until
   the kind is preserved end-to-end.
