import unittest
from unittest.mock import patch

from controllers.tournament_controller import TournamentController
from models.player import Player
from models.tournament import Tournament


class MatchValidationTestCase(unittest.TestCase):
    """Test match validation in the tournament controller."""

    def setUp(self):
        """Create controller and match test data."""
        self.controller = TournamentController()
        self.player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.player_two = Player("Martin", "Bob", "1988-03-20", "CD67890")
        self.tournament = Tournament(
            "Test tournament",
            "Thann",
            "2026-09-05",
            "2026-09-05",
        )

    def test_controller_rejects_same_player_twice(self):
        """Reject a match containing the same player twice."""
        with self.assertRaises(ValueError):
            self.controller.create_match(self.player_one, self.player_one)

    @patch("controllers.tournament_controller.save_tournament")
    def test_controller_rejects_invalid_result(self, mock_save_tournament):
        """Reject a result outside the three allowed combinations."""
        match = self.controller.create_match(self.player_one, self.player_two)

        with self.assertRaises(ValueError):
            self.controller.record_result(self.tournament, match, 2, 0)

        mock_save_tournament.assert_not_called()


if __name__ == "__main__":
    unittest.main()
