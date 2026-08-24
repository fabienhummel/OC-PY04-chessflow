import unittest

from models.player import Player
from models.round import Round
from models.tournament import Tournament


class TournamentTestCase(unittest.TestCase):
    """Test the Tournament model."""

    def setUp(self):
        """Create a tournament and a player for the tests."""
        self.tournament = Tournament(
            "Tournoi de Thann",
            "Thann",
            "2026-09-10",
            "2026-09-11",
        )
        self.player = Player("Dupont", "Alice", "1990-05-12", "AB12345")

    def test_create_tournament(self):
        """Create a tournament with default values."""
        self.assertEqual(self.tournament.name, "Tournoi de Thann")
        self.assertEqual(self.tournament.location, "Thann")
        self.assertEqual(self.tournament.number_of_rounds, 4)
        self.assertEqual(self.tournament.current_round, 0)
        self.assertEqual(self.tournament.players, [])
        self.assertEqual(self.tournament.rounds, [])

    def test_add_player(self):
        """Add a player to the tournament."""
        self.tournament.add_player(self.player)

        self.assertEqual(len(self.tournament.players), 1)
        self.assertEqual(self.tournament.players[0], self.player)

    def test_add_round(self):
        """Add a round to the tournament."""
        round_ = Round("Round 1")

        self.tournament.add_round(round_)

        self.assertEqual(len(self.tournament.rounds), 1)
        self.assertEqual(self.tournament.current_round, 1)

    def test_tournament_to_dict_and_from_dict(self):
        """Convert a tournament to a dictionary and recreate it."""
        self.tournament.add_player(self.player)
        self.tournament.add_round(Round("Round 1"))

        restored_tournament = Tournament.from_dict(self.tournament.to_dict())

        self.assertEqual(restored_tournament.name, "Tournoi de Thann")
        self.assertEqual(len(restored_tournament.players), 1)
        self.assertEqual(len(restored_tournament.rounds), 1)
        self.assertEqual(restored_tournament.current_round, 1)


if __name__ == "__main__":
    unittest.main()
