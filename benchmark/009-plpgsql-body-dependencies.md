# plpgsql Function Body References Not in Dependency Ordering

> pgschema issue [#256](https://github.com/pgplex/pgschema/issues/256) (closed)

## Context

PostgreSQL's `pg_depend` system catalog does not track function-to-function
dependencies that exist only within plpgsql function bodies. For example, if
function `a_wrapper()` calls `z_helper()` in its body, `pg_depend` shows no
dependency between them. Both pgschema and pg-delta rely on `pg_depend` for
ordering, so functions may be created in the wrong order.

pgschema worked around this by parsing function bodies for references to other
functions.

pg-delta has **table-function dependency tests** but no tests for
**function-to-function body references** in plpgsql.

## Reproduction SQL

```sql
CREATE SCHEMA test_schema;

-- Helper function (named 'z_' to sort after the caller alphabetically)
CREATE OR REPLACE FUNCTION test_schema.z_helper_parse(input text)
RETURNS text LANGUAGE plpgsql IMMUTABLE AS $$
BEGIN
  RETURN upper(input);
END;
$$;

-- Wrapper function that calls z_helper_parse (named 'a_' to sort before it)
CREATE OR REPLACE FUNCTION test_schema.a_wrapper(input text)
RETURNS text LANGUAGE plpgsql IMMUTABLE AS $$
BEGIN
  RETURN test_schema.z_helper_parse(input) || '!';
END;
$$;
```

**Issue:** If pg-delta creates `a_wrapper` before `z_helper_parse` (alphabetical
order), the function body reference will fail because `z_helper_parse` doesn't
exist yet.

## How pgschema handled it

pgschema parses function bodies to extract references to other functions and
adds them as explicit dependencies in the ordering graph. This is a heuristic
approach since SQL parsing in Go is non-trivial.

## Current pg-delta status

| Aspect | Status |
|---|---|
| `pg_depend`-based ordering | ✅ |
| Function body reference parsing | ❌ Not implemented |
| Integration test for function-to-function body deps | ❌ None |
| Table-function dependency tests | ✅ Present |

## Comparison of approaches

| | pgschema | pg-delta |
|---|---|---|
| **Root cause** | `pg_depend` doesn't track body refs | Same limitation |
| **Fix approach** | Parse function bodies for references | Could parse bodies or use `CREATE OR REPLACE` semantics |
| **Alternative** | N/A | Since pg-delta uses `CREATE OR REPLACE`, creation order only matters if the function is called during creation (e.g. in a DEFAULT or CHECK). For pure plpgsql bodies, the function will be replaced at call time. |

**Important nuance**: Unlike pgschema which applies DDL line-by-line,
`CREATE OR REPLACE FUNCTION` in PostgreSQL does **not** validate body
references at creation time for plpgsql functions. The body is only checked
at execution time. So this may be a non-issue for pg-delta in practice, but
only for plpgsql. For `LANGUAGE SQL` functions, the body IS validated at
creation time, making ordering critical.

## Plan to handle it in pg-delta

1. **Add integration test** confirming behavior:
   - Two functions where one calls the other in its body
   - Verify DDL executes successfully regardless of order (for plpgsql)
   - Test with `LANGUAGE SQL` functions where order DOES matter
2. **For SQL-language functions**: consider parsing function bodies for
   schema-qualified function references and adding dependency edges.
3. **Evaluate risk**: plpgsql bodies are not validated at creation time, so
   ordering may only matter for SQL-language functions and for functions
   referenced in DEFAULT expressions or CHECK constraints.
