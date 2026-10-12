
import unittest

from campusflow.tickets import (
    calculate_priority,
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    generate_ticket_id,
    create_ticket
)

class TestCalculatePriority(unittest.TestCase):

    def test_critical_priority(self):
        result = calculate_priority("high", 12)
        self.assertEqual(result, "critical")

    def test_critical_priority_boundary(self):
        result = calculate_priority("high", 10)
        self.assertEqual(result, "critical")

    def test_high_priority_below_critical_boundary(self):
        result = calculate_priority("high", 9)
        self.assertEqual(result, "high")

    def test_high_priority(self):
        result = calculate_priority("high", 2)
        self.assertEqual(result, "high")

    def test_medium_priority(self):
        result = calculate_priority("low", 4)
        self.assertEqual(result, "medium")

    def test_low_priority(self):
        result = calculate_priority("low", 1)
        self.assertEqual(result, "low")

    def test_medium_urgency_with_many_users(self):
        result = calculate_priority("medium", 15)
        self.assertEqual(result, "high")

    def test_validated_urgency_works_with_priority(self):
        urgency = validate_urgency(" HIGH ")
        priority = calculate_priority(urgency, 12)

        self.assertEqual(priority, "critical")

class TestValidateTitle(unittest.TestCase):

    def test_valid_title(self):
        result = validate_title("Wi-Fi down")
        self.assertEqual(result, "Wi-Fi down")

    def test_title_with_whitespace(self):
        result = validate_title("  Wi-Fi down  ")
        self.assertEqual(result, "Wi-Fi down")

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            validate_title("")

    def test_whitespace_only_title(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    def test_non_string_title(self):
        with self.assertRaises(ValueError):
            validate_title(123)
            
class TestValidateCategory(unittest.TestCase):

    def test_valid_category_whitespace(self):
        result = validate_category("  NETWORK  ")
        self.assertEqual(result, "Network")

    def test_value_error_for_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_category("invalid_category")

class TestValidateUrgency(unittest.TestCase):
    def test_valid_urgency_whitespace(self):
        result = validate_urgency("  HIGH  ")
        self.assertEqual(result, "high")

    def test_value_error_for_invalid_urgency(self):
        with self.assertRaises(ValueError):
            validate_urgency("invalid_urgency")

class TestValidateAffectedUsers(unittest.TestCase): 
    def test_valid_affected_users(self):
        result = validate_affected_users(10)
        self.assertEqual(result, 10)

    def test_value_error_for_invalid_affected_users(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_value_error_for_negative_affected_users(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-3)

    def test_value_error_for_non_integer_affected_users(self):
        with self.assertRaises(ValueError):
            validate_affected_users(True)

    def test_value_error_for_non_integer_affected_users_float(self):
        with self.assertRaises(ValueError):
            validate_affected_users(2.5)


class TestGenerateTicketId(unittest.TestCase):

    def test_first_ticket_id(self):
        result = generate_ticket_id([])
        self.assertEqual(result, "T001")

    def test_sequential_ticket_id(self):
        tickets = [
            {"id": "T001"},
            {"id": "T002"}
        ]

        result = generate_ticket_id(tickets)
        self.assertEqual(result, "T003")

    def test_non_sequential_ticket_ids(self):
        tickets = [
            {"id": "T001"},
            {"id": "T005"},
            {"id": "T003"}
        ]

        result = generate_ticket_id(tickets)
        self.assertEqual(result, "T006")


class TestCreateTicket(unittest.TestCase):

    def test_create_valid_ticket(self):
        tickets = []

        ticket = create_ticket(
            tickets,
            "Wi-Fi down",
            "Network",
            "high",
            12
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(tickets), 1)

    def test_create_ticket_normalizes_input(self):
        tickets = []

        ticket = create_ticket(
            tickets,
            "  Wi-Fi down  ",
            " NETWORK ",
            " HIGH ",
            12
        )

        self.assertEqual(ticket["title"], "Wi-Fi down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")

    def test_create_multiple_tickets(self):
        tickets = []

        first = create_ticket(
            tickets, "Wi-Fi down", "Network", "high", 12
        )

        second = create_ticket(
            tickets, "Broken mouse", "Hardware", "low", 1
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")
        self.assertEqual(len(tickets), 2)

    def test_invalid_ticket_does_not_modify_list(self):
        tickets = []

        with self.assertRaises(ValueError):
            create_ticket(
                tickets, "", "Network", "high", 12
            )

        self.assertEqual(tickets, [])


if __name__ == "__main__":
    unittest.main()
