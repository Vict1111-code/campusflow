
import unittest

from campusflow.reports import get_report


def make_ticket(ticket_id, priority="low", status="open"):
    priority_inputs = {
        "critical": ("high", 12),
        "high": ("high", 2),
        "medium": ("low", 4),
        "low": ("low", 1),
    }

    urgency, affected_users = priority_inputs[priority]

    return {
        "id": ticket_id,
        "title": "Campus support issue",
        "category": "Network",
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": status,
        "assigned_to": "Alice" if status != "open" else None,
    }


class TestTicketReports(unittest.TestCase):
    def test_empty_report(self):
        report = get_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(
            report["by_status"],
            {"open": 0, "in_progress": 0, "resolved": 0},
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 0, "high": 0, "medium": 0, "low": 0},
        )

    def test_total_ticket_count(self):
        tickets = [
            make_ticket("T001"),
            make_ticket("T002", "high"),
            make_ticket("T003", "critical"),
        ]

        report = get_report(tickets)

        self.assertEqual(report["total"], 3)

    def test_counts_tickets_by_status(self):
        tickets = [
            make_ticket("T001", status="open"),
            make_ticket("T002", "high", "in_progress"),
            make_ticket("T003", "critical", "resolved"),
            make_ticket("T004", status="open"),
        ]

        report = get_report(tickets)

        self.assertEqual(
            report["by_status"],
            {"open": 2, "in_progress": 1, "resolved": 1},
        )

    def test_counts_tickets_by_priority(self):
        tickets = [
            make_ticket("T001", "critical"),
            make_ticket("T002", "high"),
            make_ticket("T003", "medium"),
            make_ticket("T004", "low"),
            make_ticket("T005", "low"),
        ]

        report = get_report(tickets)

        self.assertEqual(
            report["by_priority"],
            {"critical": 1, "high": 1, "medium": 1, "low": 2},
        )

    def test_zero_counts_are_included(self):
        report = get_report([make_ticket("T001", "high")])

        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)
        self.assertEqual(report["by_priority"]["medium"], 0)

    def test_unknown_status_is_rejected(self):
        ticket = make_ticket("T001")
        ticket["status"] = "waiting"

        with self.assertRaises(ValueError):
            get_report([ticket])

    def test_unknown_priority_is_rejected(self):
        ticket = make_ticket("T001")
        ticket["priority"] = "urgent"

        with self.assertRaises(ValueError):
            get_report([ticket])


if __name__ == "__main__":
    unittest.main()