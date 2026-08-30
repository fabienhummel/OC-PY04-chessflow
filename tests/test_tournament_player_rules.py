import unittest
from unittest.mock import patch

from controllers.tournament_controller import TournamentController
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class TournamentPlayerRulesTestCase(unittest.TestCase):
    """Test when players can be added to a tournament."""

    def setUp(self):
        """Create a controller and tournament."""
        self.controller = TournamentController()
        self.tournament = Tournament(
            "Test tournament",
            "Thann",
            "2026-09-05",
            "2026-09-05",
        )
        self.player = Player(
            "Dupont",
            "Alice",
            "1990-05-12",
            "AB12345",
        )

    def test_player_can_be_added_before_first_round(self):
        """Allow players before the tournament starts."""
        self.assertTrue(
            self.controller.can_add_player(self.tournament)
        )

    def test_player_cannot_be_added_after_first_round_starts(self):
        """Block players after the first round starts."""
        self.tournament.add_round(Round("Round 1"))

        self.assertFalse(
            self.controller.can_add_player(self.tournament)
        )

    @patch("controllers.tournament_controller.save_tournament")
    def test_add_player_rejects_duplicate_player(self, mock_save_tournament):
        """Reject a player already registered in the tournament."""
        self.tournament.add_player(self.player)

        with self.assertRaises(ValueError):
            self.controller.add_player(self.tournament, self.player)

        self.assertEqual(len(self.tournament.players), 1)
        mock_save_tournament.assert_not_called()

    @patch("controllers.tournament_controller.save_tournament")
    def test_add_player_saves_unique_player(self, mock_save_tournament):
        """Add and save a player who is not already registered."""
        self.controller.add_player(self.tournament, self.player)

        self.assertEqual(self.tournament.players, [self.player])
        mock_save_tournament.assert_called_once_with(
            self.tournament,
            "Test tournament.json",
        )


if __name__ == "__main__":
    unittest.main()
