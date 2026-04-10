# Benchmark — pgschema Issues Not Covered by pg-delta

This directory contains benchmark files for closed
[pgschema](https://github.com/pgplex/pgschema) issues that represent bugs or
features **not currently covered** by
[@supabase/pg-delta](https://github.com/supabase/pg-toolbelt/tree/main/packages/pg-delta).

## How issues were selected

1. All [closed pgschema issues](https://github.com/pgplex/pgschema/issues?q=is%3Aissue+state%3Aclosed)
   were reviewed.
2. Issues were filtered to include only **bugs** and **features** relevant to
   schema diffing and DDL generation — excluding pgschema-specific concerns
   like dump formatting, CLI flags, binary distribution, and connection
   handling.
3. Each remaining issue was cross-referenced against pg-delta's integration
   tests (`tests/integration/`) and source modules (`src/core/objects/`) to
   determine whether the specific scenario is covered.
4. Issues already covered by pg-delta (e.g. overloaded functions, FORCE ROW
   LEVEL SECURITY, view dependency ordering, named FK constraints) were
   excluded.

## File structure

Each file follows this template:

- **Context** — what the pgschema issue describes and why it matters
- **Reproduction SQL** — runnable SQL demonstrating the scenario
- **How pgschema handled it** — the approach taken in the Go codebase
- **Current pg-delta status** — what pg-delta supports today (with evidence)
- **Comparison of approaches** — pgschema vs pg-delta architecture differences
- **Plan to handle it in pg-delta** — concrete steps to close the gap

## Summary of gaps

| # | File | pgschema Issue | Category | Severity |
|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | Column DDL | Critical |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | Function DDL | Critical |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | Dependency ordering | High |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | Column DDL | High |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | Trigger DDL | High |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | Index DDL | High |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | Constraint DDL | High |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | Dependency ordering | High |

## Covered by pg-delta (excluded from benchmark)

The following pgschema issues were found to be **already covered** by pg-delta
and are not included above:

- **#214** — FORCE ROW LEVEL SECURITY (`table.alter.test.ts`)
- **#191** — Overloaded functions (`function-operations.test.ts`)
- **#183** — Generated columns (`alter-table-operations.test.ts`)
- **#148** — Drop trigger before drop function (`trigger-operations.test.ts`)
- **#241** — `BEGIN ATOMIC` SQL functions (`function-operations.test.ts`)
- **#253** — Default privileges + selective `REVOKE` convergence (`default-privileges-edge-case.test.ts`)
- **#254** — Domain `CHECK` function dependency ordering (`type-operations.test.ts`)
- **#256** — `plpgsql`/SQL function body dependency ordering (`function-operations.test.ts`)
- **#266** — Composite FK referenced column order (`constraint-operations.test.ts`)
- **#281** — `EXCLUDE USING` constraints (`constraint-operations.test.ts`)
- **#287** — `INSTEAD OF` view triggers (`trigger-operations.test.ts`)
- **#295** — pgvector typmod preservation (`extension-operations.test.ts`)
- **#335** — Table/function dependency order (`table-function-*.test.ts`)
- **#307** — View dependency ordering (`view-operations.test.ts`)
- **#308** — View `SELECT *` recreation on base-table column changes (`view-operations.test.ts`)
- **#248/#155** — FK constraint ordering (`fk-constraint-ordering.test.ts`)
- **#246** — Function-to-function ordering (`complex-dependency-ordering.test.ts`)
- **#122** — Cross-schema FK constraints (`fk-constraint-ordering.test.ts`)
- **#83** — Named FK constraints (`constraint-operations.test.ts`)
- **#104** — View UNION subquery (`view-operations.test.ts`)
- **#101** — Table functions / RETURNS SETOF (`table-function-*.test.ts`)
- **#343** — View `security_invoker` reloptions (`view-operations.test.ts`)
- **#350** — ALTER VIEW `SET/RESET` reloptions incl. `security_invoker` (`view-operations.test.ts`)
- **#324** — Grant/Revoke ordering (`privilege-operations.test.ts`)
