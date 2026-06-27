# Parity issue drafts (2026-06-19)

This document records draft-only text from the 2026-06-19 pgschema ->
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
  - [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285)
    and [#291](https://github.com/supabase/pg-toolbelt/pull/291) are adjacent
    dependency-ordering work, but not about trigger enabled state
- No matching pg-toolbelt issue or PR was found for:
  - pgschema PR #479 trigger enabled / disabled state parity

---

## Draft 1 - pgschema PR #479 (trigger enabled / disabled state)

Relates to pgschema PR #479:
https://github.com/pgplex/pgschema/pull/479

### Context

pgschema PR #479 bundles several trigger / sequence metadata gaps together:
trigger comments, trigger enabled / disabled state, sequence comments, and a
serial-sequence comment follow-up. Current pg-delta already covers trigger
comments and sequence comments, so those parts are not new parity gaps. The
remaining uncovered piece is trigger enabled state.

Current pg-delta already extracts `pg_trigger.tgenabled` into the trigger
model and treats `enabled` as a non-alterable semantic difference during diff.
That is enough to detect the difference, but not enough to converge it.
`ReplaceTrigger.serialize()` currently emits only `CREATE OR REPLACE TRIGGER`
for ordinary triggers, which recreates the trigger definition but does not
carry PostgreSQL's enabled mode (`DISABLED`, `REPLICA`, `ALWAYS`, `ORIGIN`).

This is observable in the current unit coverage: the trigger alter test builds
a branch-side trigger with `enabled: "D"` and the serialized SQL is still only
`CREATE OR REPLACE TRIGGER ...`, with no `ALTER TABLE ... DISABLE TRIGGER ...`
follow-up. That means pg-delta can notice the change but cannot roundtrip the
disabled state itself.

### Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;

CREATE TABLE test_schema.audit_log (
  id integer PRIMARY KEY,
  payload text
);

CREATE FUNCTION test_schema.audit_log_touch()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN NEW;
END;
$$;

CREATE TRIGGER audit_log_touch_trigger
BEFORE INSERT OR UPDATE ON test_schema.audit_log
FOR EACH ROW
EXECUTE FUNCTION test_schema.audit_log_touch();
```

**Change to diff (branch only):**

```sql
ALTER TABLE test_schema.audit_log
  DISABLE TRIGGER audit_log_touch_trigger;
```

**Expected:** pg-delta emits SQL that converges the trigger state, for example:
`ALTER TABLE test_schema.audit_log DISABLE TRIGGER audit_log_touch_trigger;`
or an equivalent plan that faithfully preserves the disabled mode.

**Actual:** current pg-delta detects `enabled` as a trigger difference, but the
trigger replacement path serializes only `CREATE OR REPLACE TRIGGER ...`, so
the branch-side disabled state is not preserved.

### Suggested Fix

1. Add a focused regression in
   `repos/pg-toolbelt/packages/pg-delta/tests/integration/trigger-operations.test.ts`
   that toggles a trigger from enabled -> disabled (and ideally also exercises
   `ENABLE ALWAYS` / `ENABLE REPLICA`).
2. Split trigger enabled-state changes out of the generic replacement path in:
   - `repos/pg-toolbelt/packages/pg-delta/src/core/objects/trigger/trigger.diff.ts`
   - `repos/pg-toolbelt/packages/pg-delta/src/core/objects/trigger/changes/trigger.alter.ts`
3. Introduce explicit trigger-state change classes that serialize:
   - `ALTER TABLE ... ENABLE TRIGGER ...`
   - `ALTER TABLE ... DISABLE TRIGGER ...`
   - and, if supported in scope, `ENABLE REPLICA` / `ENABLE ALWAYS`
4. Keep comments and definition replacement separate so that changing enabled
   state alone does not unnecessarily rebuild the trigger definition.
