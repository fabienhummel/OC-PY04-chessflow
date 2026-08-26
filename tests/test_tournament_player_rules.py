import unittest

from controllers.tournament_controller import TournamentController
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


if __name__ == "__main__":
    unittest.main()
