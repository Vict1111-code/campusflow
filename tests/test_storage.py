
import unittest
import tempfile
from pathlib import Path

from campusflow.storage import (
    load_tickets,
    save_tickets,
    validate_stored_tickets,
)

from campusflow.tickets import (
    create_ticket,
    generate_ticket_id,
)


# --------------------------------------------------
# Test fixture helper
# --------------------------------------------------

def make_valid_ticket(**overrides):
    """Create a valid ticket for testing."""

    ticket = {
        "id": "T001",
        "title": "Wi-Fi down",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": "open",
        "assigned_to": None,
    }

    ticket.update(overrides)

    return ticket


# --------------------------------------------------
# JSON storage tests
# --------------------------------------------------

class TestTicketStorage(unittest.TestCase):

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            result = load_tickets(path)

            self.assertEqual(result, [])

    def test_save_and_load_tickets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            tickets = [
                make_valid_ticket()
            ]

            save_tickets(path, tickets)

            result = load_tickets(path)

            self.assertEqual(result, tickets)

    def test_malformed_json_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            path.write_text(
                "{invalid json",
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_failed_save_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            original_tickets = [
                make_valid_ticket()
            ]

            save_tickets(path, original_tickets)

            invalid_tickets = [
                {
                    "id": "T002",
                    "invalid": {1, 2, 3}
                }
            ]

            with self.assertRaises(TypeError):
                save_tickets(path, invalid_tickets)

            result = load_tickets(path)

            self.assertEqual(result, original_tickets)

    def test_ticket_id_unique_after_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            tickets = []

            create_ticket(
                tickets,
                "Wi-Fi down",
                "Network",
                "high",
                12
            )

            save_tickets(path, tickets)

            loaded_tickets = load_tickets(path)

            next_id = generate_ticket_id(loaded_tickets)

            self.assertEqual(next_id, "T002")

    def test_duplicate_ticket_ids_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            ticket = make_valid_ticket()

            tickets = [
                ticket,
                ticket.copy()
            ]

            save_tickets(path, tickets)

            with self.assertRaisesRegex(
                ValueError,
                "Duplicate ticket ID"
            ):
                load_tickets(path)

    def test_invalid_ticket_record_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            path.write_text(
                '[{"id": "T001", "title": ""}]',
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_non_list_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"

            path.write_text(
                '{"tickets": []}',
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

# --------------------------------------------------
# Stored ticket schema validation tests
# --------------------------------------------------

class TestStoredTicketValidation(unittest.TestCase):

    def test_ticket_id_must_be_string(self):
        ticket = make_valid_ticket(
            id=["T001"]
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_invalid_ticket_id_format(self):
        ticket = make_valid_ticket(
            id="ABC"
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_zero_ticket_id_rejected(self):
        ticket = make_valid_ticket(
            id="T000"
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_blank_title_rejected(self):
        ticket = make_valid_ticket(
            title=""
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_invalid_urgency_rejected(self):
        ticket = make_valid_ticket(
            urgency="urgent"
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_incorrect_priority_rejected(self):
        ticket = make_valid_ticket(
            priority="low"
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_invalid_status_rejected(self):
        ticket = make_valid_ticket(
            status="pending"
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    def test_unassigned_in_progress_rejected(self):
        ticket = make_valid_ticket(
            status="in_progress",
            assigned_to=None
        )

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])

    
    def test_invalid_category_rejected(self):
        ticket = make_valid_ticket(category="Finance")

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])


    def test_invalid_affected_users_rejected(self):
        ticket = make_valid_ticket(affected_users=0)

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])


    def test_invalid_assignment_type_rejected(self):
        ticket = make_valid_ticket(assigned_to=123)

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])


    def test_non_string_status_rejected(self):
        ticket = make_valid_ticket(status=["open"])

        with self.assertRaises(ValueError):
            validate_stored_tickets([ticket])



if __name__ == "__main__":
    unittest.main()
