"""Black-box request checks plus spies on persistence/notification. Run in a new process per variant."""
import argparse
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("mode", choices=["baseline", "acceptance"])
parser.add_argument("project", type=Path)
args = parser.parse_args()
project = args.project.resolve()
if not (project / "app.py").is_file():
    parser.error(f"Cannot find app.py under {project}")
sys.path.insert(0, str(project))
import service  # noqa: E402
from app import submit_ticket  # noqa: E402


class TicketContract(unittest.TestCase):
    def setUp(self):
        self.save = self.enter_spy("save_ticket")
        self.notify = self.enter_spy("send_notification")

    def enter_spy(self, name):
        p = patch.object(service, name, wraps=getattr(service, name))
        result = p.start()
        self.addCleanup(p.stop)
        return result

    def test_supplied_email_saves_and_notifies_once(self):
        ticket = submit_ticket("Refund", "learner@example.test")
        self.assertEqual(ticket["email"], "learner@example.test")
        self.save.assert_called_once_with("Refund", "learner@example.test")
        self.notify.assert_called_once_with(ticket)

    def test_invalid_email_does_not_save_or_notify(self):
        with self.assertRaises(ValueError):
            submit_ticket("Refund", "invalid")
        self.save.assert_not_called()
        self.notify.assert_not_called()

    def test_blank_title_does_not_save_or_notify(self):
        with self.assertRaises(ValueError):
            submit_ticket("   ", "learner@example.test")
        self.save.assert_not_called()
        self.notify.assert_not_called()

    def test_missing_email(self):
        for value in (None, "", "   "):
            with self.subTest(value=value):
                self.save.reset_mock()
                self.notify.reset_mock()
                if args.mode == "baseline":
                    # The teaching starter's membership test raises TypeError on None.
                    with self.assertRaises((ValueError, TypeError)):
                        submit_ticket("Refund", value)
                    self.save.assert_not_called()
                else:
                    ticket = submit_ticket("Refund", value)
                    self.assertIsNone(ticket["email"])
                    self.save.assert_called_once_with("Refund", None)
                self.notify.assert_not_called()


if __name__ == "__main__":
    unittest.main(argv=[__file__], verbosity=2)
