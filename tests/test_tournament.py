import unittest
from unittest.mock import patch

from controllers.tournament_controller import TournamentController
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


class TournamentValidationTestCase(unittest.TestCase):
    """Test tournament validation in the controller."""

    def setUp(self):
        """Create a tournament controller."""
        self.controller = TournamentController()

    @patch("controllers.tournament_controller.save_tournament")
    def test_controller_normalizes_tournament_data(self, mock_save_tournament):
        """Normalize valid user data before creating the model."""
        with patch.object(self.controller, "list_tournament_files", return_value=[]):
            tournament = self.controller.create_tournament(
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
        mock_save_tournament.assert_called_once()

    @patch("controllers.tournament_controller.save_tournament")
    def test_controller_uses_default_round_count(self, mock_save_tournament):
        """Use four rounds when the user leaves the field empty."""
        with patch.object(self.controller, "list_tournament_files", return_value=[]):
            tournament = self.controller.create_tournament(
                "Tournament",
                "Thann",
                "2026-09-10",
                "2026-09-11",
                number_of_rounds="",
            )

        self.assertEqual(tournament.number_of_rounds, 4)
        mock_save_tournament.assert_called_once()

    @patch("controllers.tournament_controller.save_tournament")
    def test_controller_rejects_missing_required_data(self, mock_save_tournament):
        """Reject missing required tournament data."""
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
                    self.controller.create_tournament(
                        name,
                        location,
                        start_date,
                        end_date,
                    )

        mock_save_tournament.assert_not_called()

    @patch("controllers.tournament_controller.save_tournament")
    def test_controller_rejects_invalid_dates(self, mock_save_tournament):
        """Reject invalid dates and an end date before the start date."""
        with self.assertRaises(ValueError):
            self.controller.create_tournament(
                "Tournament",
                "Thann",
                "2026-02-30",
                "2026-09-11",
            )

        with self.assertRaises(ValueError):
            self.controller.create_tournament(
                "Tournament",
                "Thann",
                "2026-09-12",
                "2026-09-11",
            )

        mock_save_tournament.assert_not_called()

    @patch("controllers.tournament_controller.save_tournament")
    def test_controller_rejects_invalid_round_count(self, mock_save_tournament):
        """Reject non-numeric, zero and negative round counts."""
        for number_of_rounds in ("abc", 0, -1):
            with self.subTest(number_of_rounds=number_of_rounds):
                with self.assertRaises(ValueError):
                    self.controller.create_tournament(
                        "Tournament",
                        "Thann",
                        "2026-09-10",
                        "2026-09-11",
                        number_of_rounds=number_of_rounds,
                    )

        mock_save_tournament.assert_not_called()


if __name__ == "__main__":
    unittest.main()
