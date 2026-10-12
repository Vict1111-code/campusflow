
import unittest

from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_open_queue,
    get_ticket,
    reopen_ticket,
)


def make_ticket(ticket_id, priority="medium",
                status="open", assigned_to=None):
    return {
        "id": ticket_id,
        "title": "Example ticket",
        "category": "technical",
        "urgency": priority,
        "priority": priority,
        "affected_users": 1,
        "status": status,
        "assigned_to": assigned_to,
    }


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket("T010", "critical"),
            make_ticket("T002", "critical"),
            make_ticket("T003", "low"),
        ]

    def test_assign_ticket(self):
        ticket = assign_ticket(self.tickets, "T002", " Alice ")
        self.assertEqual(ticket["assigned_to"], "Alice")

    def test_blank_staff_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T002", "   ")

    def test_unknown_ticket(self):
        with self.assertRaises(KeyError):
            get_ticket(self.tickets, "T999")

    def test_cannot_start_unassigned_ticket(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T002", "in_progress")

    def test_valid_status_lifecycle(self):
        assign_ticket(self.tickets, "T002", "Alice")
        change_status(self.tickets, "T002", "in_progress")
        change_status(self.tickets, "T002", "resolved")

        self.assertEqual(
            get_ticket(self.tickets, "T002")["status"],
            "resolved",
        )

    def test_reopen_resolved_ticket(self):
        ticket = make_ticket("T020", status="resolved")
        tickets = [ticket]

        reopen_ticket(tickets, "T020")
        self.assertEqual(ticket["status"], "open")

    def test_queue_priority_and_numeric_id(self):
        queue = get_open_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T010", "T003"],
        )

    def test_queue_excludes_non_open_tickets(self):
        self.tickets[0]["status"] = "resolved"

        queue = get_open_queue(self.tickets)

        self.assertNotIn("T010", [ticket["id"] for ticket in queue])


if __name__ == "__main__":
    unittest.main()

