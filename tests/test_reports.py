import unittest
from unittest.mock import MagicMock, patch

from controllers.application_controller import ApplicationController
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.player import Player
from models.tournament import Tournament


class ReportsTestCase(unittest.TestCase):
    """Test reports-related actions."""

    def test_list_players_sorts_without_changing_stored_order(self):
        """Sort players by last name then first name without changing storage."""
        controller = PlayerController.__new__(PlayerController)
        player_one = Player("martin", "Zoe", "1990-01-01", "AA00001")
        player_two = Player("Dupont", "bob", "1990-01-02", "BB00002")
        player_three = Player("dupont", "Alice", "1990-01-03", "CC00003")
        player_four = Player("Bernard", "Claire", "1990-01-04", "DD00004")
        controller.players = [
            player_one,
            player_two,
            player_three,
            player_four,
        ]
        stored_order = controller.players.copy()

        players = controller.list_players()

        self.assertEqual(
            players,
            [player_four, player_three, player_two, player_one],
        )
        self.assertEqual(controller.players, stored_order)

    def test_list_tournament_players_sorts_without_changing_stored_order(self):
        """Sort tournament players without changing their stored order."""
        controller = TournamentController()
        tournament = Tournament(
            "September",
            "Thann",
            "2026-09-12",
            "2026-09-12",
        )
        player_one = Player("martin", "Zoe", "1990-01-01", "AA00001")
        player_two = Player("Dupont", "bob", "1990-01-02", "BB00002")
        player_three = Player("dupont", "Alice", "1990-01-03", "CC00003")
        tournament.players = [player_one, player_two, player_three]
        stored_order = tournament.players.copy()

        players = controller.list_tournament_players(tournament)

        self.assertEqual(players, [player_three, player_two, player_one])
        self.assertEqual(tournament.players, stored_order)

    @patch("controllers.tournament_controller.load_tournament")
    def test_list_saved_tournaments_loads_all_files(self, mock_load_tournament):
        """Load every saved tournament for reports."""
        controller = TournamentController()
        tournament_one = Tournament(
            "January",
            "Thann",
            "2026-01-10",
            "2026-01-10",
        )
        tournament_two = Tournament(
            "September",
            "Thann",
            "2026-09-12",
            "2026-09-12",
        )
        mock_load_tournament.side_effect = [tournament_one, tournament_two]

        with patch.object(
            controller,
            "list_tournament_files",
            return_value=["January.json", "September.json"],
        ):
            tournaments = controller.list_saved_tournaments()

        self.assertEqual(tournaments, [tournament_one, tournament_two])
        self.assertEqual(mock_load_tournament.call_count, 2)

    def test_select_report_tournament_loads_selected_file(self):
        """Load the tournament selected from the reports menu."""
        controller = ApplicationController.__new__(ApplicationController)
        controller.tournament_controller = MagicMock()
        controller.tournament_view = MagicMock()
        tournament = Tournament(
            "September",
            "Thann",
            "2026-09-12",
            "2026-09-12",
        )
        controller.tournament_controller.list_tournament_files.return_value = [
            "September.json"
        ]
        controller.tournament_view.get_filename.return_value = "September.json"
        controller.tournament_controller.load_tournament.return_value = tournament

        selected = controller.select_report_tournament()

        self.assertIs(selected, tournament)
        controller.tournament_controller.load_tournament.assert_called_once_with(
            "September.json"
        )


if __name__ == "__main__":
    unittest.main()
