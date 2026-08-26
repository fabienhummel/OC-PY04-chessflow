import unittest
from datetime import datetime

from controllers.tournament_controller import TournamentController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class RoundWorkflowTestCase(unittest.TestCase):
    """Test tournament round workflow rules."""

    def setUp(self):
        """Create tournament test data."""
        self.controller = TournamentController()
        self.player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.player_two = Player("Martin", "Paul", "1985-03-08", "CD67890")
        self.tournament = Tournament(
            "Test tournament",
            "Thann",
            "2026-09-05",
            "2026-09-05",
        )

    def test_open_round_blocks_next_round(self):
        """Do not allow a new round while another round is open."""
        round_one = Round("Round 1")
        self.tournament.add_round(round_one)

        result = self.controller.can_create_next_round(self.tournament)

        self.assertFalse(result)

    def test_round_is_incomplete_without_all_results(self):
        """A round is incomplete while a match has no result."""
        round_one = Round("Round 1")
        match = Match(self.player_one, self.player_two)
        round_one.add_match(match)

        result = self.controller.is_round_complete(round_one)

        self.assertFalse(result)

    def test_get_open_round_returns_oldest_open_round(self):
        """Return the first open round when more than one exists."""
        round_one = Round("Round 1")
        round_one.end_datetime = datetime.now()
        round_two = Round("Round 2")
        round_three = Round("Round 3")

        self.tournament.add_round(round_one)
        self.tournament.add_round(round_two)
        self.tournament.add_round(round_three)

        result = self.controller.get_open_round(self.tournament)

        self.assertIs(result, round_two)


if __name__ == "__main__":
    unittest.main()
