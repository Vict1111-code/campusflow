"""CLI integration tests using temporary JSON files and mocked user input."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import run_cli
from campusflow.storage import load_tickets


class TestCampusFlowCLI(unittest.TestCase):
    def run_script(self, inputs, path):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with contextlib.redirect_stdout(output):
                result = run_cli(path)
        return result, output.getvalue()

    def test_complete_lifecycle_persists(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            actions = [
                "1", "Wi-Fi down", "Network", "high", "12",
                "4", "T001", "  Alice  ",
                "5", "T001",
                "6", "T001",
                "7", "T001",
                "9", "0",
            ]
            result, output = self.run_script(actions, path)
            self.assertEqual(result, 0)
            self.assertIn("Created ticket T001 (priority: critical)", output)
            self.assertIn("Total tickets: 1", output)
            ticket = load_tickets(path)[0]
            self.assertEqual(ticket["status"], "open")
            self.assertEqual(ticket["assigned_to"], "Alice")

    def test_invalid_create_does_not_persist(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            result, output = self.run_script(
                ["1", "Bad", "Network", "low", "0", "0"], path
            )
            self.assertEqual(result, 0)
            self.assertIn("Error:", output)
            self.assertEqual(load_tickets(path), [])

    def test_unassigned_ticket_cannot_start(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            result, output = self.run_script(
                ["1", "Printer", "Hardware", "low", "1", "5", "T001", "0"],
                path,
            )
            self.assertEqual(result, 0)
            self.assertIn("Assign the ticket before starting work", output)
            self.assertEqual(load_tickets(path)[0]["status"], "open")

    def test_reload_and_unique_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            self.run_script(["1", "First", "Other", "low", "1", "0"], path)
            _, output = self.run_script(
                ["1", "Second", "Software", "medium", "2", "0"], path
            )
            self.assertIn("Created ticket T002", output)
            self.assertEqual(len(load_tickets(path)), 2)

    def test_invalid_json_exits_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{broken", encoding="utf-8")
            result, output = self.run_script([], path)
            self.assertEqual(result, 1)
            self.assertIn("Cannot load tickets:", output)
            self.assertEqual(path.read_text(encoding="utf-8"), "{broken")

    def test_queue_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            actions = [
                "1", "Minor issue", "Other", "low", "1",
                "1", "Major outage", "Network", "high", "12",
                "8", "9", "0",
            ]
            result, output = self.run_script(actions, path)
            self.assertEqual(result, 0)
            self.assertIn("Total tickets: 2", output)
            self.assertLess(output.index("T002 | Major outage"), output.index("T001 | Minor issue"))


if __name__ == "__main__":
    unittest.main()
