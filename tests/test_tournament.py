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

    def test_tournament_normalizes_required_fields(self):
        """Normalize text fields and convert a valid round count to an integer."""
        tournament = Tournament(
            " Tournoi de Thann ",
            " Thann ",
            " 2026-09-10 ",
            " 2026-09-11 ",
            number_of_rounds="5",
        )

        self.assertEqual(tournament.name, "Tournoi de Thann")
        self.assertEqual(tournament.location, "Thann")
        self.assertEqual(tournament.start_date, "2026-09-10")
        self.assertEqual(tournament.end_date, "2026-09-11")
        self.assertEqual(tournament.number_of_rounds, 5)

    def test_tournament_rejects_missing_required_data(self):
        """Reject missing tournament name, location or dates."""
        invalid_values = [
            ("", "Thann", "2026-09-10", "2026-09-11"),
            ("Tournament", "", "2026-09-10", "2026-09-11"),
            ("Tournament", "Thann", "", "2026-09-11"),
            ("Tournament", "Thann", "2026-09-10", ""),
        ]

        for name, location, start_date, end_date in invalid_values:
            with self.subTest(
                name=name,
                location=location,
                start_date=start_date,
                end_date=end_date,
            ):
                with self.assertRaises(ValueError):
                    Tournament(name, location, start_date, end_date)

    def test_tournament_rejects_invalid_dates(self):
        """Reject impossible dates and an end date before the start date."""
        with self.assertRaises(ValueError):
            Tournament("Tournament", "Thann", "2026-02-30", "2026-09-11")

        with self.assertRaises(ValueError):
            Tournament("Tournament", "Thann", "2026-09-12", "2026-09-11")

    def test_tournament_rejects_invalid_round_count(self):
        """Reject non-numeric, zero and negative round counts."""
        for number_of_rounds in ("abc", 0, -1):
            with self.subTest(number_of_rounds=number_of_rounds):
                with self.assertRaises(ValueError):
                    Tournament(
                        "Tournament",
                        "Thann",
                        "2026-09-10",
                        "2026-09-11",
                        number_of_rounds=number_of_rounds,
                    )

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
