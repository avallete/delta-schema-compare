# EXCLUDE Constraints Incorrectly Handled

> pgschema issue [#281](https://github.com/pgplex/pgschema/issues/281) (closed)

## Context

EXCLUDE constraints (e.g. `EXCLUDE USING gist`) are a PostgreSQL feature that
enforces row-level uniqueness predicates more powerful than UNIQUE. pgschema
was incorrectly dumping them as regular `CREATE INDEX` statements, losing the
exclusion semantics entirely.

pg-delta's index model has an `is_exclusion` boolean flag and the table
constraint type `"x"`, but there are **no integration tests** exercising the
full lifecycle of EXCLUDE constraints: creation, detection, diffing, and DDL
generation.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.reservations (
    id int PRIMARY KEY,
    room_id int NOT NULL,
    during tstzrange NOT NULL,
    CONSTRAINT no_overlap EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.reservations
  DROP CONSTRAINT no_overlap;

ALTER TABLE test_schema.reservations
  ADD CONSTRAINT no_overlap EXCLUDE USING gist (
    room_id WITH =, during WITH &&
  ) WHERE (room_id > 0);
```

## How pgschema handled it

pgschema fixed the dump to emit `EXCLUDE USING gist (...)` instead of
converting it to `CREATE INDEX`.  The fix lives in the IR constraint
serialiser that now checks the constraint type before choosing output format.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Model field `is_exclusion` | ✅ Present in `index.model.ts` |
| Table constraint type `"x"` | ✅ Present in `table.model.ts` |
| Integration test | ❌ None |
| Unit tests | ❌ All existing tests set `is_exclusion: false` |

The model captures the flag from the catalog but there is no test proving that
pg-delta produces correct DDL when an EXCLUDE constraint is created, modified,
or dropped.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Dump serialiser treated all index-backed constraints as plain indexes | Model has the flag but no tests prove it works end-to-end |
| **Fix scope** | IR serialiser only | Add integration test + verify DDL output |
| **Risk** | Low – single serialiser path | Low – model already supports it |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/constraint-operations.test.ts`:
   - Test creating a table with an `EXCLUDE USING gist` constraint
   - Test modifying the exclusion predicate (e.g. adding a WHERE clause)
   - Test dropping the constraint
2. **Verify DDL output** — ensure the generated DDL uses `ADD CONSTRAINT ... EXCLUDE USING gist (...)` rather than `CREATE INDEX`.
3. **Check the constraint diff path** in `src/core/objects/table/` to confirm
   type `"x"` constraints are detected and serialised distinctly from regular
   indexes.
