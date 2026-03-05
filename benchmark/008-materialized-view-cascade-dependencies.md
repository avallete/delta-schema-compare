# Materialized View Cascade Dependencies

> pgschema issue [#268](https://github.com/pgplex/pgschema/issues/268) (closed)

## Context

When a materialized view is modified, PostgreSQL requires it to be dropped and
recreated. If other objects depend on it (indexes, other views, policies),
those dependent objects must also be dropped and recreated in the correct
order. pgschema was not searching for dependent objects before dropping a
materialized view, causing `ERROR: cannot drop materialized view ... because
other objects depend on it`.

pg-delta has materialized view tests but **no test for cascade dependency
handling** when a materialized view is modified and has dependent objects.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.orders (
    id serial PRIMARY KEY,
    customer text NOT NULL,
    total numeric NOT NULL,
    created_at timestamptz DEFAULT now()
);

CREATE MATERIALIZED VIEW test_schema.order_summary AS
    SELECT customer, sum(total) AS total_spent, count(*) AS order_count
    FROM test_schema.orders
    GROUP BY customer;

CREATE UNIQUE INDEX order_summary_customer_idx
  ON test_schema.order_summary (customer);

CREATE VIEW test_schema.top_customers AS
    SELECT * FROM test_schema.order_summary
    WHERE total_spent > 1000;
```

**Change to diff (modify the materialized view):**

```sql
CREATE MATERIALIZED VIEW test_schema.order_summary AS
    SELECT customer,
           sum(total) AS total_spent,
           count(*) AS order_count,
           max(created_at) AS last_order
    FROM test_schema.orders
    GROUP BY customer;
```

**Expected DDL order:**

```sql
DROP VIEW test_schema.top_customers;
DROP INDEX test_schema.order_summary_customer_idx;
DROP MATERIALIZED VIEW test_schema.order_summary;
CREATE MATERIALIZED VIEW test_schema.order_summary AS ...;
CREATE UNIQUE INDEX order_summary_customer_idx ON ...;
CREATE VIEW test_schema.top_customers AS ...;
```

## How pgschema handled it

pgschema now traverses `pg_depend` to find all objects that depend on a
materialized view before dropping it, and emits DROP/CREATE statements for
the entire dependency chain.

## Current pg-delta status

| Aspect | Status |
|---|---|
| Materialized view create/drop | ✅ Tested |
| Materialized view modification | ✅ Basic test |
| Cascade dependency handling | ❌ Not tested |
| Index on mat view + dependent view | ❌ Not tested |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | No dependency traversal before DROP | Untested cascade scenario |
| **Fix scope** | Dependency walker + DDL planner | Dependency graph + sort module |
| **pg-delta advantage** | N/A | Already has dependency graph infrastructure |

## Plan to handle it in pg-delta

1. **Add integration test** in
   `tests/integration/materialized-view-operations.test.ts`:
   - Create a mat view with a dependent index and a dependent regular view
   - Modify the mat view definition
   - Verify the DDL drops dependents first and recreates them after
2. **Verify the dependency graph** in `src/core/sort/` — ensure that
   indexes and views depending on a materialized view have edges in the
   topological sort.
3. **Test with `REFRESH MATERIALIZED VIEW`** — ensure refresh doesn't
   trigger unnecessary cascade drops.
