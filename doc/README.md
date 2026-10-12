# CampusFlow — Campus IT Helpdesk CLI

**Learn2Earn AI-Native Engineering Sprint** · Python standard library · Two fellows

CampusFlow is a working Python command-line helpdesk for recording technical incidents, calculating priority, assigning staff, tracking resolution, viewing queues and reports, and persisting tickets to JSON.

## Quick start

Requires Python 3.10+; no third-party dependencies.

```bash
python3 main.py
```

The interactive menu supports creating, listing, viewing, assigning, starting, resolving, and reopening tickets, displaying the open priority queue and reports, and exiting. Changes are saved to `data/tickets.json` after each successful mutation; the file is loaded at startup. Do not commit this local data file.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

**Verification:** Vejeh supplied terminal output on 2026-10-12 showing **84 tests passed** after adding the CLI and integration tests. This is local test evidence, not a claim that GitHub CI has run.

## Project layout

```text
main.py                    # CLI and persistence orchestration
campusflow/
  __init__.py
  tickets.py               # Validation, priority, creation, ticket IDs
  workflow.py              # Assignment, transitions, open queue
  reports.py               # Summary counts
  storage.py               # JSON loading, validation, atomic replacement
tests/
  test_tickets.py
  test_storage.py
  test_workflow.py
  test_report.py
  test_cli.py
PRD.md
IMPLEMENTATION_ROADMAP.md
AGENT.md
AGENTS.md
vejehpart.md
gideonpart.md
docs/
  design-decisions.md
  ai-learning-log.md
```

## Ticket schema

Each ticket has `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, and `assigned_to`.

- Categories: Network, Hardware, Software, Other.
- Urgency: low, medium, high.
- Priority: critical (high urgency and >=10 users), otherwise high (high urgency or >=10 users), otherwise medium (medium urgency or >=3 users), otherwise low.
- Lifecycle: open → in_progress → resolved. Assignment is required to start work; resolved tickets require explicit reopening before modification.
- Queue: open tickets only, highest priority first, ties by numeric ticket ID.

## Collaboration and delivery

Vejeh implemented the ticket engine, validation, persistence and CLI. Gideon implemented assignment, workflow, priority queue and reporting. The code is currently assembled on `integration/campusflow-reviewed`; **the default `master` branch has not yet received this integrated implementation**.

Before final submission: conduct genuine reciprocal PR reviews and approvals, record at least two substantive observations per review, merge approved work to `master`, rerun the test suite on `master`, complete real individual AI learning logs, and perform a manual demo of the full lifecycle and persistence.

## Documentation

- [Product requirements](PRD.md)
- [Implementation roadmap](IMPLEMENTATION_ROADMAP.md)
- [Agent instructions](AGENT.md)
- [Design decisions](design-decisions.md)
- [AI learning log](ai-learning-log.md)
- [Vejeh's ownership](vejehpart.md) and [Gideon's ownership](gideonpart.md)

## Scope

No web interface, external database, authentication, AI inference, or third-party Python libraries are required.
