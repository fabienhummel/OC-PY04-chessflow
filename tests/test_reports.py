import unittest
from unittest.mock import MagicMock, patch

from controllers.application_controller import ApplicationController
from controllers.tournament_controller import TournamentController
from models.tournament import Tournament


class ReportsTestCase(unittest.TestCase):
    """Test reports-related actions."""

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
