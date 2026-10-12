"""CampusFlow: command-line campus IT support ticket manager."""

from pathlib import Path

from campusflow.tickets import create_ticket
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import (
    get_ticket, assign_ticket, change_status, reopen_ticket, get_open_queue,
)
from campusflow.reports import get_report

DEFAULT_DATA_PATH = Path("data/tickets.json")


def display_ticket(ticket):
    print(f"\n{ticket['id']} | {ticket['title']}")
    print(f"  Category: {ticket['category']} | Urgency: {ticket['urgency']}")
    print(f"  Affected users: {ticket['affected_users']} | Priority: {ticket['priority']}")
    print(f"  Status: {ticket['status']} | Assigned to: {ticket['assigned_to'] or 'Unassigned'}")


def display_tickets(tickets):
    if not tickets:
        print("No tickets found.")
        return
    for ticket in tickets:
        display_ticket(ticket)


def show_report(tickets):
    report = get_report(tickets)
    print(f"\nTotal tickets: {report['total']}")
    print("By status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")
    print("By priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")


def run_cli(data_path=DEFAULT_DATA_PATH):
    """Run the CLI; persist each successful change before confirming it."""
    try:
        tickets = load_tickets(data_path)
    except (ValueError, OSError) as error:
        print(f"Cannot load tickets: {error}")
        return 1

    menu = (
        "\n=== CampusFlow ===\n"
        "1. Create ticket\n"
        "2. List all tickets\n"
        "3. View ticket\n"
        "4. Assign ticket\n"
        "5. Start ticket\n"
        "6. Resolve ticket\n"
        "7. Reopen ticket\n"
        "8. Open priority queue\n"
        "9. Summary report\n"
        "0. Exit\n"
    )

    while True:
        try:
            print(menu)
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye!")
                return 0

            if choice == "1":
                title = input("Title: ")
                category = input("Category (Network/Hardware/Software/Other): ")
                urgency = input("Urgency (low/medium/high): ")
                users_text = input("Number of affected users: ").strip()
                try:
                    affected_users = int(users_text)
                except ValueError as error:
                    raise ValueError("Affected users must be a whole number.") from error
                # Work on a copy so a failed save never changes in-memory state.
                updated = [dict(ticket) for ticket in tickets]
                ticket = create_ticket(updated, title, category, urgency, affected_users)
                save_tickets(data_path, updated)
                tickets = updated
                print(f"Created ticket {ticket['id']} (priority: {ticket['priority']}).")

            elif choice == "2":
                display_tickets(tickets)

            elif choice == "3":
                ticket_id = input("Ticket ID: ").strip().upper()
                display_ticket(get_ticket(tickets, ticket_id))

            elif choice in {"4", "5", "6", "7"}:
                ticket_id = input("Ticket ID: ").strip().upper()
                updated = [dict(ticket) for ticket in tickets]
                if choice == "4":
                    staff_name = input("Staff name: ")
                    ticket = assign_ticket(updated, ticket_id, staff_name)
                    action = "Assigned"
                elif choice == "5":
                    ticket = change_status(updated, ticket_id, "in_progress")
                    action = "Started"
                elif choice == "6":
                    ticket = change_status(updated, ticket_id, "resolved")
                    action = "Resolved"
                else:
                    ticket = reopen_ticket(updated, ticket_id)
                    action = "Reopened"
                save_tickets(data_path, updated)
                tickets = updated
                print(f"{action} ticket {ticket['id']}.")

            elif choice == "8":
                display_tickets(get_open_queue(tickets))

            elif choice == "9":
                show_report(tickets)

            else:
                print("Invalid menu option. Choose 0 through 9.")

        except (ValueError, KeyError, OSError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
