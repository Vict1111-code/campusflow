# Gideon — Engineering Work Package (Focused / Smaller Scope)

**Owner:** Gideon (Engineer B). **Relative scope:** smaller, self-contained business features. **Partner:** Victor. Read `PRD.md`, `AGENT.md`, and the agreed `docs/design-decisions.md` before coding.

## Mission
Implement ticket assignment, status lifecycle, work queue, and reports with automated tests. These are real core features, not documentation-only tasks.

## Owned files
- `campusflow/workflow.py`: assignment, valid status changes, explicit reopen, queue ordering (or a separately agreed queue module).
- `campusflow/reports.py`: ticket count breakdowns.
- `tests/test_workflow.py`, `tests/test_reports.py`: your own meaningful tests.
- Collaborate on `docs/design-decisions.md` and AI learning log.

## Dependencies
Wait for the jointly agreed ticket schema and function contracts; use the same ticket collection format and error policy as Victor. Core functions should take data as arguments, not prompt users or read JSON themselves.

## Work breakdown
### G1 Assignment
- Find ticket by ID; reject unknown IDs.
- Trim and reject blank staff names.
- Set `assigned_to` only for an eligible ticket.
- A resolved ticket cannot be modified unless explicitly reopened.
- Test success, blank name, unknown ID and resolved modification.

### G2 Status lifecycle
- New ticket begins `open`.
- Allow `open → in_progress` only if assigned.
- Allow `in_progress → resolved`.
- Reject skipped/backward/unknown transitions.
- Implement explicit `reopen_ticket` to set resolved ticket back to open; subsequent modification requires this operation.
- Test unassigned rejection, valid progression, invalid transition and reopen.

### G3 Open work queue
- Include only `status == open` tickets.
- Sort critical, high, medium, low; for equal priority, smaller numeric ticket ID first (T002 before T010).
- Do not accidentally include in_progress or resolved tickets.
- Test mixed priorities, ties and empty queue.

### G4 Reports
- Total count; counts for each status and priority.
- Include zero counts when empty.
- Return structured values; Victor's CLI handles printing.
- Test empty store and mixed records.

## Branch and PR
Use an issue-numbered branch, e.g. `feat/2-workflow-queue-reports` (replace with actual Issue number). Make small commits, push your branch, open a PR against `master`, link the Issue and include actual test output. Victor must review and approve. Review Victor's PR with at least two substantive observations and request changes if necessary.

## Acceptance checklist
- [ ] Assignment rejects blank staff and unknown IDs.
- [ ] Unassigned ticket cannot enter in_progress.
- [ ] Assigned ticket can complete valid lifecycle.
- [ ] Resolved ticket cannot be edited without explicit reopen.
- [ ] Queue includes only open tickets and sorts correctly.
- [ ] Reports work for empty and populated ticket sets.
- [ ] Own Python implementation and tests committed.
- [ ] Three genuine AI learning experiments documented, one critically evaluated.
- [ ] Own PR authored and Victor's PR reviewed substantively.
- [ ] Can explain status guards, queue tie-breaking and test assertions.

## Handoff to Victor
Share exported function names, expected inputs/outputs, exception behavior and a test run result. Do not edit Victor's storage or CLI modules without discussing first.

## Suggested AI learning topics
Python list sorting with `key=`; safe dictionary updates; exceptions; `unittest` assertions. Use tiny unrelated experiments first, then apply and independently verify.
