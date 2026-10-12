PRIORITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


def get_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise KeyError(f"Ticket {ticket_id} not found")


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = get_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before modifying it")

    staff_name = staff_name.strip()

    if not staff_name:
        raise ValueError("Staff name cannot be blank")

    ticket["assigned_to"] = staff_name
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = get_ticket(tickets, ticket_id)
    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValueError("Reopen the ticket before modifying it")

    if current_status == "open" and new_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError("Assign the ticket before starting work")

    elif current_status == "in_progress" and new_status == "resolved":
        pass

    else:
        raise ValueError("Invalid status transition")

    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    ticket = get_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened")

    ticket["status"] = "open"
    return ticket


def get_open_queue(tickets):
    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"].lower()],
            int(ticket["id"][1:])
        )
    )

