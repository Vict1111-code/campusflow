# CampusFlow — Campus IT Helpdesk CLI

**Learn2Earn AI-Native Engineering Sprint** · Python standard library · Two fellows · Six-hour challenge

CampusFlow is a command-line helpdesk for recording technical incidents, calculating priority, assigning staff, tracking resolution, viewing work queues and reports, and persisting tickets to JSON.

> Status: planning/documentation. Features and tests described below are acceptance targets, **not claims of completed implementation**.

## Start here
1. Read [PRD.md](PRD.md) for exact product rules and acceptance criteria.
2. Read [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) for milestones and dependencies.
3. Read [AGENT.md](AGENT.md) (and [AGENTS.md](AGENTS.md)) before using coding agents.
4. Victor: [vejehpart.md](vejehpart.md). Gideon: [gideonpart.md](gideonpart.md).
5. Agree on interfaces in `docs/design-decisions.md` before writing code.

## Proposed repository structure
```text
main.py
campusflow/
  __init__.py
  tickets.py
  workflow.py
  storage.py
  reports.py
tests/
  test_tickets.py
  test_workflow.py
  test_storage.py
  test_reports.py
docs/
  design-decisions.md
  ai-learning-log.md
```
This is the proposed target structure, not a claim that these files exist.

## Runtime (once implemented)
- Python 3.10+ recommended; standard library only.
- Run: `python main.py`
- Test: `python -m unittest discover -s tests -v`
- Local ticket data: `data/tickets.json` (excluded from Git).

## Features
1. Create validated tickets with IDs and deterministic priority.
2. List tickets and inspect one by ID.
3. Assign a ticket to a nonblank staff name.
4. Enforce open → in_progress → resolved and explicit reopen.
5. Sort open work by critical, high, medium, low, then numeric ID.
6. Report totals and breakdowns by status/priority.
7. Save and reload JSON safely, including unique IDs after restart.

## Collaboration
Each fellow must implement real Python code and tests on their own branch, author one feature PR, review the partner's PR with at least two substantive observations, and approve before merge. Never commit directly to the shared default branch during implementation. The repo currently uses `master` as its default branch; references to `main` in the challenge guide mean the repository's integration/default branch.

## Definition of done
All seven features work through a repeating CLI menu; at least eight meaningful `unittest` tests pass on the integrated default branch; invalid inputs and transitions do not corrupt data; JSON round-trips and IDs remain unique; both approved PRs and authentic AI-learning logs exist; both fellows can demonstrate and defend their own code.

## Documentation and evidence
Complete `docs/design-decisions.md` and `docs/ai-learning-log.md` during the sprint. Record actual commands/results and PR URLs; never invent test output or review evidence.

## Scope boundaries
No website, GUI, database server, AI model integration, third-party dependencies, authentication, or notifications are required. AI is used to learn and verify, not to calculate ticket priority.
