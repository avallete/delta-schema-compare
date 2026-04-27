# Materialized View Cascade Dependencies

> pgschema issue [#268](https://github.com/pgplex/pgschema/issues/268) (closed)

## Context

When a materialized view is modified, PostgreSQL requires it to be dropped and
recreated. If other objects depend on it (indexes, other views, policies),
those dependent objects must also be dropped and recreated in the correct
order. pgschema was not searching for dependent objects before dropping a
materialized view, causing `ERROR: cannot drop materialized view ... because
other objects depend on it`.

Refresh note (2026-04-27): this parity gap is now fixed in pg-delta. The
tracking issue [pg-toolbelt#133](https://github.com/supabase/pg-toolbelt/issues/133)
is closed, and
[pg-toolbelt#149](https://github.com/supabase/pg-toolbelt/pull/149) merged
dedicated replace-dependency handling plus integration coverage for a
materialized view with both a dependent index and a dependent regular view.

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
| Materialized view modification | ✅ Tested |
| Cascade dependency handling | ✅ Fixed in `pg-toolbelt#149` |
| Index on mat view + dependent view | ✅ Covered by `tests/integration/materialized-view-operations.test.ts` |
| Existing pg-toolbelt issue / PR for this exact scenario | ✅ `#133` closed by merged PR `#149` |

Latest merged coverage includes the integration case
`"replace materialized view with dependent index and view"` in
`repos/pg-toolbelt/packages/pg-delta/tests/integration/materialized-view-operations.test.ts`,
which asserts that the dependent index and view are dropped before the
materialized view and recreated after it.

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Historical root cause** | No dependency traversal before DROP | Replacement flow did not expand through dependent index/view chain |
| **Current fix** | Traverses `pg_depend` before emitting DROP/CREATE | Expands replace-dependency chains to include dependent indexes and views |
| **Regression coverage** | Fixture coverage in pgschema | Integration coverage for drop/recreate order in pg-delta |

## Remaining follow-up

No active parity gap remains for this benchmark item after pg-toolbelt #149.
Future work, if needed, would be limited to extending the same replacement-chain
logic to any additional dependent object types that show up in real-world
reports.
