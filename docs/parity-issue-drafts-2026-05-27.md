# Parity issue drafts (2026-05-27)

This document records draft-only text from the 2026-05-27 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. These drafts are saved so
the findings can be reviewed in a PR first and then promoted to real
pg-toolbelt issues only if they still look correct.

Latest status note (2026-06-03): current pg-delta already preserves array
typmods via `format_type(a.atttypid, a.atttypmod)` and verbatim
`data_type_str` serialization, so pgschema #420 is now treated as covered. The
draft below is retained as historical review context only.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing trackers already cover:
  - pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Related but not duplicate work:
  - [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263)
    covers dependency-chain failures for `ALTER COLUMN TYPE` and `DROP FUNCTION`
    with policy/view dependents, not array typmod preservation
- Upstream pgschema fix work is now merged for:
  - pgschema #420 -> [pgschema#438](https://github.com/pgplex/pgschema/pull/438)
- No matching pg-toolbelt issue or PR was found for:
  - pgschema #420

---

## Draft 1 - pgschema #420 (`varchar(n)[]` typmod preservation)

Relates to pgschema issue #420: https://github.com/pgplex/pgschema/issues/420

Upstream pgschema now has merged fix PR
[#438](https://github.com/pgplex/pgschema/pull/438), but the issue itself
remains open, so this stays saved as a draft-only pg-delta parity candidate
rather than a duplicate live issue.

### Context

pgschema issue #420 reports that `varchar(n)[]` columns are dumped as `varchar[]`
and silently lose their element length modifier. That changes database-level
validation behavior and can make dump/plan/apply roundtrips lossy. The merged
pgschema PR #438 confirms upstream has already landed a focused fix for this
exact array-typmod bug.

pg-delta's catalog extraction currently reads column type strings using
`format_type(a.atttypid, a.atttypmod)` in
`src/core/objects/table/table.model.ts`, which suggests the source path is
closer to correct than pgschema's dump path. However, the exact scenario is not
covered by dedicated integration tests in
`packages/pg-delta/tests/integration/alter-table-operations.test.ts` or related
catalog/export tests, so parity for `varchar(n)[]` remains unverified.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;
CREATE TABLE test_schema.items (
  id bigint PRIMARY KEY,
  tags varchar(128)[] NOT NULL
);
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.items
  ALTER COLUMN tags TYPE varchar(256)[];
```

**Expected:** pg-delta preserves the element typmod and emits migration SQL that
roundtrips with `varchar(256)[]` rather than degrading the column type to
`varchar[]`.

**Actual (current parity evidence):** the extractor uses `format_type(...)`,
but there is no dedicated regression test asserting typmod preservation for
`varchar(n)[]`, so this exact array-typmod scenario is still not covered by the
current test suite.

### Suggested Fix

1. Add a roundtrip regression in:
   - `repos/pg-toolbelt/packages/pg-delta/tests/integration/alter-table-operations.test.ts`
   - or another table/column integration suite if that file is a better fit
2. Include assertions for both:
   - initial creation of `varchar(128)[]`
   - a diff to `varchar(256)[]`
3. If the test fails, inspect and update:
   - `src/core/objects/table/table.model.ts`
   - `src/core/objects/table/changes/table.alter.ts`
   - any declarative-export path that serializes `data_type_str`
4. Add a regression assertion that emitted SQL keeps the array element typmod
   (`varchar(256)[]`) instead of collapsing to `varchar[]`.
