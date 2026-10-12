
import unittest

from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_open_queue,
    get_ticket,
    reopen_ticket,
)


def make_ticket(
    ticket_id,
    priority="medium",
    status="open",
    assigned_to=None,
):
    return {
        "id": ticket_id,
        "title": "Campus support issue",
        "category": "Network",
        "urgency": "high",
        "affected_users": 5,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket("T010", "critical"),
            make_ticket("T002", "critical"),
            make_ticket("T004", "high"),
            make_ticket("T005", "medium"),
            make_ticket("T003", "low"),
        ]

    def test_assign_ticket(self):
        ticket = assign_ticket(self.tickets, "T002", "Alice")
        self.assertEqual(ticket["assigned_to"], "Alice")

    def test_assignment_trims_staff_name(self):
        ticket = assign_ticket(self.tickets, "T002", " Alice ")
        self.assertEqual(ticket["assigned_to"], "Alice")

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T002", "   ")

    def test_non_text_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T002", None)

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(KeyError):
            get_ticket(self.tickets, "T999")

    def test_cannot_assign_resolved_ticket(self):
        ticket = make_ticket(
            "T020", status="resolved", assigned_to="Alice"
        )
        with self.assertRaises(ValueError):
            assign_ticket([ticket], "T020", "Bob")
        self.assertEqual(ticket["assigned_to"], "Alice")

    def test_cannot_start_unassigned_ticket(self):
        ticket = self.tickets[0]
        with self.assertRaises(ValueError):
            change_status(self.tickets, ticket["id"], "in_progress")
        self.assertEqual(ticket["status"], "open")

    def test_assigned_ticket_can_start(self):
        assign_ticket(self.tickets, "T002", "Alice")
        ticket = change_status(self.tickets, "T002", "in_progress")
        self.assertEqual(ticket["status"], "in_progress")

    def test_in_progress_ticket_can_be_resolved(self):
        ticket = make_ticket(
            "T020", status="in_progress", assigned_to="Alice"
        )
        change_status([ticket], "T020", "resolved")
        self.assertEqual(ticket["status"], "resolved")

    def test_valid_status_lifecycle(self):
        assign_ticket(self.tickets, "T002", "Alice")
        change_status(self.tickets, "T002", "in_progress")
        change_status(self.tickets, "T002", "resolved")
        self.assertEqual(
            get_ticket(self.tickets, "T002")["status"], "resolved"
        )

    def test_cannot_skip_from_open_to_resolved(self):
        ticket = self.tickets[0]
        with self.assertRaises(ValueError):
            change_status(self.tickets, ticket["id"], "resolved")
        self.assertEqual(ticket["status"], "open")

    def test_cannot_move_back_to_open(self):
        ticket = make_ticket(
            "T020", status="in_progress", assigned_to="Alice"
        )
        with self.assertRaises(ValueError):
            change_status([ticket], "T020", "open")
        self.assertEqual(ticket["status"], "in_progress")

    def test_unknown_new_status_is_rejected(self):
        ticket = self.tickets[0]
        with self.assertRaises(ValueError):
            change_status(self.tickets, ticket["id"], "waiting")
        self.assertEqual(ticket["status"], "open")

    def test_resolved_ticket_cannot_change_status(self):
        ticket = make_ticket("T020", status="resolved")
        with self.assertRaises(ValueError):
            change_status([ticket], "T020", "in_progress")
        self.assertEqual(ticket["status"], "resolved")

    def test_reopen_resolved_ticket(self):
        ticket = make_ticket("T020", status="resolved")
        reopen_ticket([ticket], "T020")
        self.assertEqual(ticket["status"], "open")

    def test_cannot_reopen_unresolved_ticket(self):
        ticket = make_ticket("T020", status="open")
        with self.assertRaises(ValueError):
            reopen_ticket([ticket], "T020")
        self.assertEqual(ticket["status"], "open")

    def test_queue_priority_and_numeric_id(self):
        queue = get_open_queue(self.tickets)
        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T010", "T004", "T005", "T003"],
        )

    def test_queue_excludes_non_open_tickets(self):
        self.tickets[0]["status"] = "resolved"
        self.tickets[1]["status"] = "in_progress"
        queue = get_open_queue(self.tickets)
        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T004", "T005", "T003"],
        )

    def test_empty_queue(self):
        self.assertEqual(get_open_queue([]), [])

    def test_queue_does_not_reorder_original_list(self):
        original_ids = [ticket["id"] for ticket in self.tickets]
        get_open_queue(self.tickets)
        self.assertEqual(
            [ticket["id"] for ticket in self.tickets], original_ids
        )

    def test_unknown_queue_priority_is_rejected(self):
        ticket = make_ticket("T020", priority="urgent")
        with self.assertRaises(ValueError):
            get_open_queue([ticket])

    def test_invalid_numeric_ticket_id_is_rejected(self):
        ticket = make_ticket("ABC", priority="high")
        with self.assertRaises(ValueError):
            get_open_queue([ticket])


if __name__ == "__main__":
    unittest.main()