# Partition rebind via `DETACH` / `ATTACH`

> pgschema issue [#639](https://github.com/pgplex/pgschema/issues/639) (closed), fixed by [pgschema#668](https://github.com/pgplex/pgschema/pull/668)

Severity: **Critical**. A bound-only change planned as `DROP TABLE` deletes the partition's rows. When a foreign key references the partitioned parent, PostgreSQL also rejects `DROP TABLE` on the partition, so the plan fails at apply.

## Refresh note (2026-10-30)

This recheck moves checked-in/live `pg-delta` from
`6b82eff84dba925a176f0c6a78e5a16843885366` to
`36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c` and `pgschema` from
`36a38ff3c25db956ae8b5be2eee552d8bc69fb47` to
`9de190efdf78cd422850a3bc3db13ee84a11462d`.

The non-destructive rebind stays open:

- `src/plan/rules/tables.ts` still marks `partitionBound` and `parentTable`
  `"replace"` (lines 246-247)
- `src/extract/relations.ts` still stores both (lines 92-96)
- a `DETACH PARTITION` search under `packages/pg-delta` TypeScript still
  returns no matches
- exact search for `pgschema#639` still returns no dedicated pg-toolbelt
  issue or PR. The draft remains
  [`docs/parity-issue-drafts-2026-10-28.md`](../docs/parity-issue-drafts-2026-10-28.md)
- merged PR [#555](https://github.com/supabase/pg-toolbelt/pull/555) does
  not add a detach/attach plan

Benchmark 026 therefore stays **Not covered**.

## Context

pgschema issue #639 reported that `plan` ignored a partition's bound and whether it was attached. A re-attached partition with a narrower bound, or a detached partition, produced `No changes detected`. Merged PR #668 closes that issue by comparing `PartitionOf` and `PartitionBound` and applying a parent or bound change as `ALTER TABLE ... DETACH PARTITION` followed by `ALTER TABLE ... ATTACH PARTITION`.

pg-delta already stores `partitionBound` and `parentTable` on table facts and treats both attributes as `"replace"`. That detects the drift the original report described. The replacement is `DROP TABLE` plus `CREATE TABLE ... PARTITION OF`, which is a different migration from the one pgschema now emits. pg-delta's own follow-up note already records the apply failure: PostgreSQL refuses `DROP TABLE` on a partition while a foreign key references the partitioned parent, because the per-partition foreign-key clone depends on the leaf.

This matters for any schema migration that moves a partition boundary, re-parents a leaf, or drops a partitioned parent while keeping the former child. The catalog can converge on an empty database for the simple cases the existing corpuses cover. A populated partition, a sibling boundary move, or an incoming foreign key does not.

## Reproduction SQL

**Initial state (both databases):**

```sql
CREATE TABLE public.events (
    id bigint NOT NULL,
    at date NOT NULL,
    PRIMARY KEY (id, at)
) PARTITION BY RANGE (at);

CREATE TABLE public.events_2026_01 PARTITION OF public.events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE public.events_2026_02 PARTITION OF public.events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE public.audit_log (
    event_id bigint NOT NULL,
    at date NOT NULL,
    FOREIGN KEY (event_id, at) REFERENCES public.events (id, at)
);
```

**Change to diff (branch only):** narrow `events_2026_01` and shift `events_2026_02` into the range that was given up.

```sql
ALTER TABLE public.events DETACH PARTITION public.events_2026_01;
ALTER TABLE public.events ATTACH PARTITION public.events_2026_01
    FOR VALUES FROM ('2026-01-01') TO ('2026-01-15');

ALTER TABLE public.events DETACH PARTITION public.events_2026_02;
ALTER TABLE public.events ATTACH PARTITION public.events_2026_02
    FOR VALUES FROM ('2026-01-15') TO ('2026-03-01');
```

**Expected:** pg-delta detaches every moved partition before any attach, then attaches each leaf to its new bound. Rows stay in the same table. The foreign key that references `events` stays in place.

**Actual:** `partitionBound: "replace"` expands to `DROP TABLE` plus `CREATE TABLE ... PARTITION OF`. The drop deletes the partition's rows. With `audit_log`'s foreign key pointing at the parent, PostgreSQL rejects `DROP TABLE public.events_2026_01` because of the per-partition foreign-key clone. A sibling recreate can also fail with an overlap error if the new bound is created while the old sibling bound is still attached.

The full upstream fixture is `testdata/diff/create_table/issue_639_partition_attach_detach/` in pgschema. It also covers a child that must survive `DROP` of its parent, a standalone table that becomes a partition, and constraint copies that `DETACH` turns into local constraints and `ATTACH` adopts again.

## How pgschema handled it

PR #668 adds `internal/diff/partition.go` and threads it through table diff and plan ordering.

- `partitionChanged` compares parent name, parent schema, and `PartitionBound`.
- Every `DETACH` runs in the drop phase, before table drops and before any table create, so a child leaves a parent that is about to be dropped and sibling bounds do not overlap mid-plan.
- Every `ATTACH` runs at the end of the table modifications, after the child has the columns and constraints the new parent requires, and before deferred foreign keys that reference a key the child only gains from its parent.
- `withConstraintsRetainedByDetach` adds the parent's primary-key, unique, and foreign-key copies to the old state so a detached table that still declares them keeps them.
- `keepConstraintsAdoptedByAttach` leaves a matching local copy in place so attach reuses it instead of rebuilding the index or re-validating the foreign key.

The emitted plan for the fixture starts with `ALTER TABLE ... DETACH PARTITION` and later emits `ALTER TABLE ... ATTACH PARTITION ... FOR VALUES ...`. It does not `DROP` a partition whose only change is its bound or parent.

## Current pg-delta status

Checked on `repos/pg-toolbelt` @ `36ac91d3c3a5d5b578edf192d2e7d3b6b6b9687c`. The 2026-10-28 check used `6b82eff84dba925a176f0c6a78e5a16843885366`. Merged PR #555 did not move these lines.

- `src/extract/relations.ts` (lines 92-96) stores `partitionBound` from `pg_get_expr(relpartbound)` and `parentTable` from the first inheritance parent.
- `src/plan/rules/tables.ts` line 246 marks `partitionBound` and `parentTable` as `"replace"`. The create path (line 52) emits `CREATE TABLE ... PARTITION OF ... ${bound}` for a new partition.
- A search for `DETACH PARTITION` under `packages/pg-delta` returns no TypeScript matches. The corpus SQL files also contain no `DETACH PARTITION`.
- `corpus/table-ops--attach-partition` and `corpus/table-ops--detach-partition` cover a standalone table becoming a partition and a partition becoming standalone. Those scenarios still go through table replace.
- `docs/roadmap/pg-delta-next-follow-ups.md` (inherited-object dependency edges) already defers this: replacing a partition of an FK-referenced partitioned table needs a `DETACH PARTITION` strategy because `DROP TABLE` fails at apply.
- Exact searches for `pgschema#639`, `DETACH PARTITION`, and `partition bound` return no pg-toolbelt issue or PR. Umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) does not describe this rebind.

Detection of the original "no changes detected" bug is already present. The non-destructive rebind pgschema now ships is **not covered**.

## Comparison of approaches

pgschema keeps the partition relation and moves it with `DETACH` then `ATTACH`. Constraint copies travel with the table. Detaches are ordered before creates so sibling ranges can slide without an overlap error, and a child is detached before `DROP ... CASCADE` on a parent that is going away.

pg-delta models the same facts and then replaces the table identity. Replace is the right tool when the partition key itself changes (the parent must be rebuilt). It is the wrong tool when only the bound or the parent link changes: the leaf relation, its rows, and its adopted constraints can stay.

## Plan to handle it in pg-delta

1. In `src/plan/rules/tables.ts`, stop using `"replace"` for a stable table id whose only semantic changes are `partitionBound` and/or `parentTable`. Emit `ALTER TABLE <old parent> DETACH PARTITION <child>` and `ALTER TABLE <new parent> ATTACH PARTITION <child> <bound>`.
2. Schedule every detach in the drop phase, before `DROP TABLE` of a parent and before any `CREATE` / `ATTACH` that could overlap the old bound. Schedule attaches after the child has the columns and constraints the new parent requires.
3. Preserve primary-key, unique, and foreign-key copies that `DETACH` turns into local constraints, and let `ATTACH` adopt a matching copy instead of dropping and re-adding it.
4. Add a planner unit test plus corpus cases for a bound change, a sibling boundary move, a parent drop that keeps the former child, and a foreign key that references the partitioned parent.
5. Add an integration test under `packages/pg-delta/tests/integration/` that round-trips the reproduction SQL above, including rows inserted before the migration.

Draft tracker text for that work is in [`docs/parity-issue-drafts-2026-10-28.md`](../docs/parity-issue-drafts-2026-10-28.md). No pg-toolbelt issue was opened from this refresh.
