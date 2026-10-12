
PRIORITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


def get_ticket(tickets, ticket_id):
    """Find a ticket by ID or raise an error."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise KeyError(f"Ticket {ticket_id} not found")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an eligible ticket to a staff member."""
    ticket = get_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before modifying it.")

    if not isinstance(staff_name, str):
        raise ValueError("Staff name must be text.")

    staff_name = staff_name.strip()

    if not staff_name:
        raise ValueError("Staff name cannot be blank.")

    ticket["assigned_to"] = staff_name
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Apply only the allowed ticket status transitions."""
    ticket = get_ticket(tickets, ticket_id)
    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValueError("Reopen the ticket before modifying it.")

    if current_status == "open":
        if new_status != "in_progress":
            raise ValueError("Invalid status transition.")

        if not ticket.get("assigned_to"):
            raise ValueError("Assign the ticket before starting work.")

    elif current_status == "in_progress":
        if new_status != "resolved":
            raise ValueError("Invalid status transition.")

    else:
        raise ValueError(f"Unknown current status: {current_status}")

    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    """Reopen a resolved ticket."""
    ticket = get_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"
    return ticket


def get_open_queue(tickets):
    """Return open tickets by priority, then numeric ticket ID."""
    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    for ticket in open_tickets:
        priority = ticket["priority"].lower()

        if priority not in PRIORITY_ORDER:
            raise ValueError(f"Unknown priority: {ticket['priority']}")

        ticket_id_number = ticket["id"][1:]

        if not ticket_id_number.isdigit():
            raise ValueError(f"Invalid ticket ID: {ticket['id']}")

    return sorted(
        open_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"].lower()],
            int(ticket["id"][1:]),
        ),
    )