# Temporal `WITHOUT OVERLAPS` / `PERIOD` Constraints

> pgschema issue [#364](https://github.com/pgplex/pgschema/issues/364) (closed), fixed by [pgschema#365](https://github.com/pgplex/pgschema/pull/365)

## Context

pgschema issue #364 reports that PostgreSQL 18 temporal constraints were being
silently downgraded: `WITHOUT OVERLAPS` was dropped from temporal primary keys
and `PERIOD` was dropped from temporal foreign keys in generated plan and dump
output. That changes the constraint semantics even though the emitted DDL still
looks superficially valid.

pgschema fixed this in PR #365 by reading `pg_constraint.conperiod`,
propagating a temporal flag through its constraint IR, and re-emitting
`WITHOUT OVERLAPS` / `PERIOD` in its diff and plan paths. In pg-delta, the
constraint catalog model does not expose any temporal flag, and the table
constraint diff logic in
`repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
never compares the rendered constraint definition. As a result, pg-delta cannot
detect a transition between a regular PK/FK and a temporal PK/FK when the
column lists are otherwise unchanged.

This matters because temporal constraints are not decorative syntax. A temporal
primary key prevents overlapping periods for the same business key, and a
temporal foreign key enforces containment over time ranges. Silently treating
them as ordinary composite constraints weakens data integrity.

## Reproduction SQL

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE SCHEMA test_schema;

CREATE TABLE test_schema.contacts (
    id uuid NOT NULL,
    name text NOT NULL,
    valid_period tstzrange NOT NULL DEFAULT tstzrange(now(), 'infinity', '[)'),
    PRIMARY KEY (id, valid_period)
);

CREATE TABLE test_schema.conversations (
    id uuid NOT NULL,
    contact_id uuid NOT NULL,
    valid_period tstzrange NOT NULL DEFAULT tstzrange(now(), 'infinity', '[)'),
    PRIMARY KEY (id, valid_period),
    FOREIGN KEY (contact_id, valid_period)
      REFERENCES test_schema.contacts (id, valid_period)
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.contacts
  DROP CONSTRAINT contacts_pkey;

ALTER TABLE test_schema.contacts
  ADD CONSTRAINT contacts_pkey
  PRIMARY KEY (id, valid_period WITHOUT OVERLAPS);

ALTER TABLE test_schema.conversations
  DROP CONSTRAINT conversations_pkey;

ALTER TABLE test_schema.conversations
  ADD CONSTRAINT conversations_pkey
  PRIMARY KEY (id, valid_period WITHOUT OVERLAPS);

ALTER TABLE test_schema.conversations
  DROP CONSTRAINT conversations_contact_id_valid_period_fkey;

ALTER TABLE test_schema.conversations
  ADD CONSTRAINT conversations_contact_id_valid_period_fkey
  FOREIGN KEY (contact_id, PERIOD valid_period)
  REFERENCES test_schema.contacts (id, PERIOD valid_period);
```

**Expected:** pg-delta detects that the PK and FK definitions changed and emits
the necessary drop/recreate DDL preserving `WITHOUT OVERLAPS` and `PERIOD`.

**Actual:** pg-delta treats the constraints as unchanged because
`table.diff.ts` compares `constraint_type`, `key_columns`,
`foreign_key_columns`, and related scalar properties, but does not compare any
temporal attribute or the full constraint definition.

## How pgschema handled it

pgschema PR #365 added temporal constraint support by extracting
`conperiod` from `pg_constraint` through `to_jsonb(c) ->> 'conperiod'`, which
keeps the catalog query backward-compatible on PostgreSQL 14-17 where the
column does not exist. The value is mapped to a constraint-level temporal flag
and then used by the diff and plan layers to emit `WITHOUT OVERLAPS` for
primary/unique constraints and `PERIOD` for foreign keys.

The merged PR also added concrete regression coverage in
`repos/pgschema/testdata/diff/create_table/add_pk/` and
`repos/pgschema/testdata/diff/create_table/add_fk/`, including
`PRIMARY KEY (id, valid_period WITHOUT OVERLAPS)` and
`FOREIGN KEY (product_id, PERIOD adjustment_period) ...`.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Temporal flag extracted from `pg_constraint` | ❌ Missing from `src/core/objects/table/table.model.ts` |
| Temporal flag in table constraint schema | ❌ `tableConstraintPropsSchema` has no `is_temporal`-style field |
| Diff detects regular ↔ temporal constraint transition | ❌ `src/core/objects/table/table.diff.ts` does not compare the full definition or any temporal field |
| Add-constraint serialization can preserve PG catalog definition | ✅ `definition` is captured from `pg_get_constraintdef(c.oid, true)` |
| PostgreSQL 18 included in test matrix | ❌ `tests/constants.ts` only lists PostgreSQL 15 and 17 |
| Integration test for temporal PK/FK scenarios | ❌ Missing from `tests/integration/` |
| Existing pg-toolbelt issue / PR for this exact scenario | ❌ None found during review |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Catalog extraction** | Reads temporal metadata from `pg_constraint.conperiod` safely across PG versions | Does not read temporal metadata |
| **Internal representation** | Tracks a temporal constraint flag in IR | No temporal property in table constraint model |
| **Diff behavior** | Compares temporal vs non-temporal constraints explicitly | Compares only structured scalar fields and column arrays |
| **Coverage** | Has PG18 regression fixtures for temporal PK/FK creation | Has no PG18 test target and no temporal constraint integration case |

## Plan to handle it in pg-delta

1. Extend
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.model.ts`
   to extract a temporal flag from `pg_constraint`, using a PG-version-safe
   expression like pgschema's `to_jsonb(c) ->> 'conperiod'` approach.
2. Add the new field to `tableConstraintPropsSchema` and preserve it through the
   table object model.
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/table/table.diff.ts`
   so temporal vs non-temporal constraints are treated as a drop/recreate
   change.
4. Add PostgreSQL 18 to
   `repos/pg-toolbelt/packages/pg-delta/tests/constants.ts`.
5. Add integration coverage for temporal primary key and foreign key roundtrips
   in `repos/pg-toolbelt/packages/pg-delta/tests/integration/constraint-operations.test.ts`.
