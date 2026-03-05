# pgvector Type Modifier (Dimensions) Lost

> pgschema issue [#295](https://github.com/pgplex/pgschema/issues/295) (closed)

## Context

The `pgvector` extension provides `vector(N)` and `halfvec(N)` types where `N`
specifies the number of dimensions. When these dimensions are dropped (e.g.
`halfvec(384)` → `halfvec`), HNSW/IVFFlat index creation fails with
`ERROR: column does not have dimensions`.

pgschema was stripping the typmod (dimension specifier) from column type
definitions during plan/apply.

pg-delta has **no tests for pgvector types or any extension type with custom
typmods**. While pg-delta reads column types from the catalog (which preserves
typmods), the roundtrip has never been verified for extension types with
modifiers.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;
CREATE EXTENSION IF NOT EXISTS vector SCHEMA test_schema;

CREATE TABLE test_schema.embeddings (
    id serial PRIMARY KEY,
    title text NOT NULL,
    embedding test_schema.halfvec(384) NOT NULL
);

CREATE INDEX embeddings_hnsw_idx
  ON test_schema.embeddings
  USING hnsw (embedding test_schema.halfvec_l2_ops)
  WITH (m = 16, ef_construction = 64);
```

**Change to diff:**

```sql
ALTER TABLE test_schema.embeddings
  ADD COLUMN embedding_v2 test_schema.vector(768);
```

## How pgschema handled it

pgschema fixed its type serialiser to emit the full type including
typmod/dimensions (e.g. `halfvec(384)` instead of `halfvec`).

## Current pg-delta status

| Aspect | Status |
|---|---|
| Column `data_type` includes typmod from catalog | ✅ Likely (via `format_type()`) |
| Extension type support | ✅ Extension module exists |
| Test for pgvector or any typmod extension type | ❌ None |
| HNSW/IVFFlat index operator classes | ❌ Not tested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | Type serialiser dropped typmod text | Untested — catalog likely preserves it |
| **Fix scope** | IR type serialiser | Integration test to confirm round-trip |
| **Dependency** | pgvector extension needed for test | Same — requires pgvector in test container |

## Plan to handle it in pg-delta

1. **Add integration test** in `tests/integration/extension-operations.test.ts`
   or a new `pgvector-operations.test.ts`:
   - Create a table with `vector(384)` and `halfvec(768)` columns
   - Add an HNSW index with dimension-specific operator class
   - Modify a column's dimension count (e.g. `vector(384)` → `vector(512)`)
   - Verify the generated DDL preserves dimensions
2. **Verify `format_type()` output** — confirm that the catalog query used by
   pg-delta returns `halfvec(384)` not `halfvec` for the `data_type` field.
3. **Consider gating** the test behind a pgvector availability check since the
   extension may not be installed in all test environments.
