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
| 001 | [EXCLUDE constraints](001-exclude-constraints.md) | [#281](https://github.com/pgplex/pgschema/issues/281) | Constraint DDL | Medium |
| 002 | [BEGIN ATOMIC functions](002-begin-atomic-functions.md) | [#241](https://github.com/pgplex/pgschema/issues/241) | Function DDL | Medium |
| 003 | [INSTEAD OF triggers](003-instead-of-triggers.md) | [#287](https://github.com/pgplex/pgschema/issues/287) | Trigger DDL | Medium |
| 004 | [pgvector typmod](004-pgvector-typmod.md) | [#295](https://github.com/pgplex/pgschema/issues/295) | Type modifiers | High |
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | Column DDL | Critical |
| 006 | [Composite FK column order](006-composite-fk-column-order.md) | [#266](https://github.com/pgplex/pgschema/issues/266) | Constraint DDL | High |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | Function DDL | Critical |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | Dependency ordering | High |
| 009 | [plpgsql body deps](009-plpgsql-body-dependencies.md) | [#256](https://github.com/pgplex/pgschema/issues/256) | Dependency ordering | Medium |
| 010 | [Domain CHECK + function](010-domain-check-function-deps.md) | [#254](https://github.com/pgplex/pgschema/issues/254) | Dependency ordering | Medium |
| 011 | [Default priv + REVOKE](011-default-privileges-revoke-convergence.md) | [#253](https://github.com/pgplex/pgschema/issues/253) | Privilege DDL | Medium |
| 012 | [Trigger function drop](012-trigger-function-drop-order.md) | [#148](https://github.com/pgplex/pgschema/issues/148) | Dependency ordering | High |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | Column DDL | High |
| 014 | [View SELECT * + column add](014-view-select-star-column-add.md) | [#308](https://github.com/pgplex/pgschema/issues/308) | View DDL | Medium |
| 015 | [Grant/Revoke ordering](015-grant-revoke-ordering.md) | [#324](https://github.com/pgplex/pgschema/issues/324) | Privilege DDL | Critical |

## Covered by pg-delta (excluded from benchmark)

The following pgschema issues were found to be **already covered** by pg-delta
and are not included above:

- **#214** — FORCE ROW LEVEL SECURITY (`table.alter.test.ts`)
- **#191** — Overloaded functions (`function-operations.test.ts`)
- **#183** — Generated columns (`alter-table-operations.test.ts`)
- **#335** — Table/function dependency order (`table-function-*.test.ts`)
- **#307** — View dependency ordering (`view-operations.test.ts`)
- **#248/#155** — FK constraint ordering (`fk-constraint-ordering.test.ts`)
- **#246** — Function-to-function ordering (`complex-dependency-ordering.test.ts`)
- **#122** — Cross-schema FK constraints (`fk-constraint-ordering.test.ts`)
- **#83** — Named FK constraints (`constraint-operations.test.ts`)
- **#104** — View UNION subquery (`view-operations.test.ts`)
- **#101** — Table functions / RETURNS SETOF (`table-function-*.test.ts`)
