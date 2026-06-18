# Parity issue drafts (2026-06-18)

This document records draft-only text from the 2026-06-18 pgschema ->
pg-delta parity refresh.

No GitHub issues were opened as part of this refresh. This draft is saved so
the finding can be reviewed in a PR first and then promoted to a real
pg-toolbelt issue only if it still looks correct.

## Duplicate-check summary (pg-toolbelt)

Before writing the draft below, I checked the current open and closed
pg-toolbelt issues and PRs for overlapping work:

- Existing parity trackers already cover:
  - pgschema #404 -> [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema #366 -> [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- Related but not duplicate work:
  - [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263)
    tracks broader replacement-dependency ordering
  - [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
    recreates rules and triggers for replacement dependencies
  - [pg-toolbelt#291](https://github.com/supabase/pg-toolbelt/pull/291)
    fixes additional procedure-expression replacement dependents
- Current open pgschema items screened without drafting duplicates:
  - pgschema #474 is already covered in pg-delta's policy dependency path
  - pgschema #477 is already covered in pg-delta's restrictive-policy path
  - pgschema #478 is already covered in pg-delta's index storage-parameter path
  - pgschema #480 overlaps the broader dependency-replacement work above, so no
    new exact duplicate draft was added yet
- No matching pg-toolbelt issue or PR was found for:
  - the remaining trigger enabled / disabled state gap inside pgschema PR #479

---

## Draft 1 - pgschema PR #479 (preserve trigger enabled / disabled state)

Relates to pgschema PR #479:
https://github.com/pgplex/pgschema/pull/479

## Context

pgschema PR #479 bundles four related trigger / sequence metadata gaps, but the
current pg-delta parity delta is narrower than the upstream PR title suggests.
Current pg-delta already supports and tests trigger comments plus sequence
comments, so opening a tracker for the whole bundled upstream PR would
overstate the remaining gap.

The still-missing parity case is trigger enabled state. pg-delta extracts
`pg_trigger.tgenabled` into the trigger model and compares it as a
non-alterable field, so it can detect drift between enabled and disabled
triggers. However, the current replacement path recreates the trigger from
`pg_get_triggerdef(...)`, and PostgreSQL recreates triggers enabled by default.
There is no change class or serializer for `ALTER TABLE ... ENABLE/DISABLE
TRIGGER ...`, so apply cannot preserve a branch-side disabled trigger state.

This matters because the drift is silent in the generated DDL. A plan can look
reasonable because the trigger itself is present, yet the trigger's runtime
behavior still differs after apply.

## Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.accounts (
  id integer PRIMARY KEY,
  balance integer NOT NULL
);

CREATE FUNCTION test_schema.guard_balance()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN NEW;
END;
$$;

CREATE TRIGGER guard_balance_trigger
BEFORE UPDATE ON test_schema.accounts
FOR EACH ROW
EXECUTE FUNCTION test_schema.guard_balance();
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.accounts
  DISABLE TRIGGER guard_balance_trigger;
```

**Expected:** pg-delta emits:

```sql
ALTER TABLE test_schema.accounts DISABLE TRIGGER guard_balance_trigger;
```

and the roundtrip converges with the trigger present but disabled.

**Actual:** current pg-delta detects `tgenabled` drift but has no serializer for
`ENABLE/DISABLE TRIGGER`. The diff path instead treats the state change as a
replacement and recreates the trigger from `pg_get_triggerdef(...)`, which
restores the default enabled state.

## Suggested Fix

1. Add focused integration coverage in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/trigger-operations.test.ts`
   for:
   - `ALTER TABLE ... DISABLE TRIGGER trigger_name`
   - `ALTER TABLE ... ENABLE TRIGGER trigger_name`
   - ideally `ENABLE REPLICA` and `ENABLE ALWAYS`
2. Introduce a trigger-state change class and serializer in
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/trigger/changes/`
   that emits:
   - `ALTER TABLE schema.table DISABLE TRIGGER name`
   - `ALTER TABLE schema.table ENABLE TRIGGER name`
   - `ALTER TABLE schema.table ENABLE REPLICA TRIGGER name`
   - `ALTER TABLE schema.table ENABLE ALWAYS TRIGGER name`
3. Update
   `repos/pg-toolbelt/packages/pg-delta/src/core/objects/trigger/trigger.diff.ts`
   so `tgenabled` differences route through that new change class instead of
   forcing full trigger replacement.
4. Keep the existing comment coverage intact: trigger comments and sequence
   comments are already supported, so the new regression should stay narrowly
   focused on state preservation.
