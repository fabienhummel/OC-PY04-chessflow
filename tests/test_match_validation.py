import unittest
from unittest.mock import patch

from controllers.match_controller import MatchController
from models.match import Match
from models.player import Player
from models.tournament import Tournament


class MatchValidationTestCase(unittest.TestCase):
    """Test match result validation."""

    def setUp(self):
        """Create controller and match test data."""
        self.controller = MatchController()
        self.player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.player_two = Player("Martin", "Bob", "1988-03-20", "CD67890")
        self.match = Match(self.player_one, self.player_two)
        self.tournament = Tournament(
            "Test tournament",
            "Thann",
            "2026-09-05",
            "2026-09-05",
        )

    @patch("controllers.match_controller.save_tournament")
    def test_controller_normalizes_string_result(self, mock_save_tournament):
        """Convert user score strings before storing the result."""
        self.controller.record_result(
            self.tournament,
            self.match,
            "0,5",
            "0.5",
        )

        self.assertEqual(self.match.score_one, 0.5)
        self.assertEqual(self.match.score_two, 0.5)
        mock_save_tournament.assert_called_once()

    @patch("controllers.match_controller.save_tournament")
    def test_controller_rejects_invalid_result(self, mock_save_tournament):
        """Reject a result outside the three allowed combinations."""
        with self.assertRaises(ValueError):
            self.controller.record_result(
                self.tournament,
                self.match,
                2,
                0,
            )

        mock_save_tournament.assert_not_called()


if __name__ == "__main__":
    unittest.main()
