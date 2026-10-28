# Parity issue draft (2026-10-28)

Draft only. Exact searches for `pgschema#639`, `DETACH PARTITION`, and
`partition bound` on `supabase/pg-toolbelt` returned no issue or pull request.
Umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) does
not describe partition rebind. This refresh does not open a tracker.

## Draft — pgschema #639 (partition rebind via DETACH / ATTACH)

## Context

pgschema issue #639 reported that a re-bounded or detached partition produced
`No changes detected`. Merged PR
[#668](https://github.com/pgplex/pgschema/pull/668) now compares the partition
parent and bound and applies the change as `ALTER TABLE ... DETACH PARTITION`
followed by `ALTER TABLE ... ATTACH PARTITION`.

pg-delta already extracts `partitionBound` and `parentTable`
(`src/extract/relations.ts`) and marks both `"replace"`
(`src/plan/rules/tables.ts`). Replace expands to `DROP TABLE` plus
`CREATE TABLE ... PARTITION OF`. That detects the drift and converges simple
empty-database corpuses. It deletes rows on a bound change, and PostgreSQL
rejects the drop when a foreign key references the partitioned parent.
`docs/roadmap/pg-delta-next-follow-ups.md` already defers a `DETACH PARTITION`
strategy for that apply failure.

Relates to pgschema issue #639: https://github.com/pgplex/pgschema/issues/639

## Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE TABLE public.events (
    id bigint NOT NULL,
    at date NOT NULL,
    PRIMARY KEY (id, at)
) PARTITION BY RANGE (at);

CREATE TABLE public.events_2026_01 PARTITION OF public.events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE public.audit_log (
    event_id bigint NOT NULL,
    at date NOT NULL,
    FOREIGN KEY (event_id, at) REFERENCES public.events (id, at)
);

INSERT INTO public.events_2026_01 (id, at) VALUES (1, DATE '2026-01-10');
```

**Change to diff (branch only):**

```sql
ALTER TABLE public.events DETACH PARTITION public.events_2026_01;
ALTER TABLE public.events ATTACH PARTITION public.events_2026_01
    FOR VALUES FROM ('2026-01-01') TO ('2026-01-15');
```

**Expected:** pg-delta emits `DETACH PARTITION` and then `ATTACH PARTITION`
with the new bound. The inserted row is still in `events_2026_01` after apply.

**Actual:** pg-delta plans `DROP TABLE public.events_2026_01` and a new
`CREATE TABLE ... PARTITION OF`. The drop fails while `audit_log`'s foreign
key references `events`. On a database with no such foreign key, the drop
succeeds and the row is gone.

## Suggested Fix

- Replace the `partitionBound` / `parentTable` `"replace"` strategy in
  `src/plan/rules/tables.ts` with detach and attach actions when the table id
  itself is unchanged.
- Order every detach before parent drops and before attaches that would
  overlap the old bound. Order attaches after the child satisfies the new
  parent's column and constraint requirements.
- Keep constraint copies that detach turns into local constraints, and let
  attach adopt a matching copy.
- Add a planner unit test and a corpus case next to
  `corpus/table-ops--attach-partition`, plus an integration test that asserts
  the row survives.
