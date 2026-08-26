import unittest
from datetime import datetime

from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class ModelsTestCase(unittest.TestCase):
    """Test the complete model workflow."""

    def test_complete_model_workflow(self):
        """Create and restore a complete tournament."""
        player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        player_two = Player("Martin", "Bob", "1988-03-20", "CD67890")

        match = Match(player_one, player_two)
        match.set_result(1, 0)

        round_ = Round("Round 1")
        round_.start_datetime = datetime.now()
        round_.add_match(match)
        round_.close()

        tournament = Tournament(
            "Tournoi de Thann",
            "Thann",
            "2026-09-10",
            "2026-09-11",
        )
        tournament.add_player(player_one)
        tournament.add_player(player_two)
        tournament.add_round(round_)

        restored_tournament = Tournament.from_dict(tournament.to_dict())

        self.assertEqual(restored_tournament.name, "Tournoi de Thann")
        self.assertEqual(len(restored_tournament.players), 2)
        self.assertEqual(len(restored_tournament.rounds), 1)
        self.assertEqual(restored_tournament.rounds[0].matches[0].score_one, 1)
        self.assertEqual(restored_tournament.rounds[0].matches[0].score_two, 0)


if __name__ == "__main__":
    unittest.main()
