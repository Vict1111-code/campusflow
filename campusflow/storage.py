import json
from pathlib import Path
import os
import tempfile
import re

from campusflow.tickets import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    calculate_priority,
)

REQUIRED_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}

VALID_STATUSES = {"open", "in_progress", "resolved"}



def validate_stored_tickets(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Ticket storage must contain a list.")

    seen_ids = set()

    for ticket in tickets:
        # 1. Check the record structure.
        if not isinstance(ticket, dict):
            raise ValueError(
                "Each ticket must be a dictionary."
            )

        missing_fields = REQUIRED_FIELDS - ticket.keys()

        if missing_fields:
            raise ValueError(
                f"Ticket is missing fields: {sorted(missing_fields)}"
            )

        # 2. Validate the ticket ID.
        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str):
            raise ValueError(
                "Ticket ID must be a string."
            )

        if not re.fullmatch(r"T[0-9]{3,}", ticket_id):
            raise ValueError(
                f"Invalid ticket ID format: {ticket_id}"
            )

        if int(ticket_id[1:]) == 0:
            raise ValueError(
                "Ticket ID number must be positive."
            )

        # 3. Check for duplicate IDs.
        if ticket_id in seen_ids:
            raise ValueError(
                f"Duplicate ticket ID: {ticket_id}"
            )

        seen_ids.add(ticket_id)

        # 4. Validate the ticket fields.
        try:
            title = validate_title(ticket["title"])

            category = validate_category(
                ticket["category"]
            )

            urgency = validate_urgency(
                ticket["urgency"]
            )

            affected_users = validate_affected_users(
                ticket["affected_users"]
            )

        except ValueError as error:
            raise ValueError(
                f"Invalid ticket {ticket_id}: {error}"
            ) from error

        # 5. Check normalized stored values.
        if ticket["title"] != title:
            raise ValueError(
                f"Title is not normalized: {ticket_id}"
            )

        if ticket["category"] != category:
            raise ValueError(
                f"Category is not normalized: {ticket_id}"
            )

        if ticket["urgency"] != urgency:
            raise ValueError(
                f"Urgency is not normalized: {ticket_id}"
            )

        # 6. Verify the calculated priority.
        expected_priority = calculate_priority(
            urgency,
            affected_users
        )

        if ticket["priority"] != expected_priority:
            raise ValueError(
                f"Incorrect priority for ticket {ticket_id}"
            )

        # 7. Validate ticket status.
        status = ticket["status"]

        if not isinstance(status, str):
            raise ValueError(
                "Ticket status must be a string."
            )

        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status for ticket {ticket_id}"
            )

        # 8. Validate staff assignment.
        assigned_to = ticket["assigned_to"]

        if assigned_to is not None:
            if not isinstance(assigned_to, str):
                raise ValueError(
                    "Assigned staff must be a string."
                )

            if not assigned_to.strip():
                raise ValueError(
                    "Assigned staff cannot be blank."
                )

            if assigned_to != assigned_to.strip():
                raise ValueError(
                    "Assigned staff is not normalized."
                )

        # 9. Enforce the workflow invariant.
        if status == "in_progress" and assigned_to is None:
            raise ValueError(
                "In-progress tickets must be assigned."
            )

    return tickets


def load_tickets(path):
    path = Path(path)

    if not path.exists():
        return []
    
    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError("Ticket storage contains invalid JSON.") from error

    
    return validate_stored_tickets(tickets)

def save_tickets(path, tickets):
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False
        ) as file:
            temporary_path = Path(file.name)
            json.dump(tickets, file, indent=4)
            file.flush()

        os.replace(temporary_path, path)

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
