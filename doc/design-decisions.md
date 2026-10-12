# CampusFlow — Implemented Design Decisions

This document describes the interfaces currently implemented on `integration/campusflow-reviewed`. Team members should confirm these reflect their shared agreement before final submission.

## Ticket representation
Tickets are mutable dictionaries stored in a list. Required keys: `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.

## Function contracts
- `create_ticket(tickets, title, category, urgency, affected_users)` validates and appends a new ticket, returning the ticket.
- `calculate_priority(urgency, affected_users)` applies first-matching priority rule.
- `generate_ticket_id(tickets)` returns next ID based on the highest existing numeric ID.
- `get_ticket(tickets, ticket_id)` returns matching ticket or raises `KeyError`.
- `assign_ticket(tickets, ticket_id, staff_name)` validates staff and assigns eligible ticket.
- `change_status(tickets, ticket_id, new_status)` allows only open → in_progress → resolved, with assignment required to start.
- `reopen_ticket(tickets, ticket_id)` changes resolved → open.
- `get_open_queue(tickets)` returns a sorted list without reordering the source list.
- `get_report(tickets)` returns `total`, `by_status`, `by_priority`.
- `load_tickets(path)` returns [] when missing, rejects malformed JSON and invalid stored records.
- `save_tickets(path, tickets)` writes a temporary file and replaces the destination.
- `run_cli(data_path)` loads tickets, runs a repeating menu, and saves each successful mutation.

## Validation and errors
- Categories normalized to title case, urgency to lowercase; titles and staff names trimmed.
- `affected_users` must be a positive integer, excluding booleans.
- `ValueError` signals invalid input/state, `KeyError` unknown ticket IDs.
- Malformed JSON fails visibly instead of silently resetting data.

## Storage and mutation
The CLI operates on copies for mutations and only updates its in-memory list after a successful save. Runtime JSON is ignored by Git.

## Remaining review points
- Verify the manual full lifecycle and restart in the CLI.
- Correct inconsistent urgency/priority combinations in any workflow test fixtures even if isolated tests pass.
- Obtain actual fellow approval for these decisions and record real PR review evidence.
