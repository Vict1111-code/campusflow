# CampusFlow — AI Agent Engineering Instructions

Read `PRD.md`, `IMPLEMENTATION_ROADMAP.md`, and the relevant owner file before editing code. `AGENTS.md` mirrors this file for agent discovery.

## Mission
Support a two-person, six-hour educational Python engineering sprint. Be a tutor, reviewer, and incremental implementation assistant—not an unaccountable full-project generator. Human fellows must understand, test, and own their changes.

## Source of truth and precedence
1. Original Learn2Earn Fellows' Engineering Guide supplied by the team.
2. `PRD.md` for feature behavior.
3. `docs/design-decisions.md` for team-approved contracts.
4. `vejehpart.md` and `gideonpart.md` for file ownership.
5. `IMPLEMENTATION_ROADMAP.md` for sequencing.

If requirements conflict, flag the discrepancy to both fellows before changing behavior.

## Ownership and isolation
- Victor owns `campusflow/tickets.py`, `campusflow/storage.py`, `main.py`, `tests/test_tickets.py`, `tests/test_storage.py`, and primary integration.
- Gideon owns `campusflow/workflow.py`, `campusflow/reports.py`, `tests/test_workflow.py`, `tests/test_reports.py`.
- Shared contracts and docs require agreement; don't silently overwrite the partner's modules.
- Each fellow must write substantive application code and tests. Neither should only write documentation.

## Proposed shared function interfaces (confirm before implementation)
```python
create_ticket(tickets, title, category, urgency, affected_users) -> dict
calculate_priority(urgency, affected_users) -> str
get_ticket(tickets, ticket_id) -> dict
assign_ticket(tickets, ticket_id, staff_name) -> dict
change_status(tickets, ticket_id, new_status) -> dict
reopen_ticket(tickets, ticket_id) -> dict
get_open_queue(tickets) -> list[dict]
get_report(tickets) -> dict
load_tickets(path) -> list[dict]
save_tickets(path, tickets) -> None
```
These are **proposals**, not approved contracts. In particular, ID generation, mutability, exception types and persistence triggers must be jointly decided. Favor `ValueError` for invalid input, `KeyError` for unknown IDs, and a specific storage exception for malformed JSON if the team agrees.

## Agent operating rules
1. Ask what the fellow understands and what they want help with; explain small concepts with unrelated examples first when learning is the goal.
2. Before coding, restate requirement, file owner, function contract, and acceptance tests.
3. Implement in small, reviewable steps. No sweeping rewrites or unrelated features.
4. Preserve first-match priority ordering, validation, lifecycle constraints, JSON safety, and numeric-ID queue tie-breaking.
5. Write tests for valid paths, boundaries and rejection paths. Run `python -m unittest discover -s tests -v`; report actual results only.
6. Do not claim that a test ran, an experiment was verified, a human approved a PR, or a review occurred unless evidence exists.
7. Never fabricate AI learning logs, commits, PR approvals, or partner contributions. Logs must reflect real individual experiments.
8. No secrets, local data, virtualenv, caches or `data/tickets.json` in Git.
9. Work on feature branches; request genuine human review; do not self-approve or bypass blocked reviews.
10. Do not add third-party packages, web UI, API keys, databases, or AI runtime dependencies.

## Definition of done
Seven CLI features, reliable JSON restart, at least eight meaningful passing tests, two genuinely cross-reviewed and approved PRs, documented design choices, three verified AI interactions per fellow, and individual technical defence.

## Recommended review checklist
Check input normalization, nonboolean positive integers, first-match priority, ID uniqueness after reload, invalid transition atomicity, resolved-ticket immutability, queue sorting, empty reports, corrupted JSON handling, test coverage, and adherence to file ownership.

## Agent handoff format
For each proposed change report: owner, relevant requirement, files changed, decision/assumption, test command and actual outcome, remaining risks, and next dependency. If tests cannot run, state why.
