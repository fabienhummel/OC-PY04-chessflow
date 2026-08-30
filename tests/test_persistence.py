import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from utils import json_manager
from utils.json_manager import (
    delete_tournament,
    load_players,
    load_tournament,
    save_players,
    save_tournament,
)


class PersistenceTestCase(unittest.TestCase):
    """Test JSON persistence."""

    def test_data_paths_are_anchored_to_project_root(self):
        """Use project data paths independently from the working directory."""
        self.assertTrue(json_manager.PLAYERS_FILE.is_absolute())
        self.assertEqual(
            json_manager.PLAYERS_FILE,
            json_manager.DATA_FOLDER / "players.json",
        )
        self.assertEqual(
            json_manager.TOURNAMENTS_FOLDER,
            json_manager.DATA_FOLDER / "tournaments",
        )

    def test_missing_players_file_returns_empty_list(self):
        """Start with an empty registry when the players file is absent."""
        with tempfile.TemporaryDirectory() as directory:
            players_file = Path(directory) / "players.json"

            with patch("utils.json_manager.PLAYERS_FILE", players_file):
                self.assertEqual(load_players(), [])

    def test_save_and_load_players(self):
        """Save and reload players without touching local application data."""
        with tempfile.TemporaryDirectory() as directory:
            players_file = Path(directory) / "players.json"

            with patch("utils.json_manager.PLAYERS_FILE", players_file):
                players = [Player("Dupont", "Alice", "1990-05-12", "AB12345")]
                save_players(players)
                loaded_players = load_players()

            self.assertEqual(len(loaded_players), 1)
            self.assertEqual(loaded_players[0].national_id, "AB12345")

    def test_empty_players_file_raises_clear_error(self):
        """Reject an empty players JSON file."""
        with tempfile.TemporaryDirectory() as directory:
            players_file = Path(directory) / "players.json"
            players_file.write_text("", encoding="utf-8")

            with patch("utils.json_manager.PLAYERS_FILE", players_file):
                with self.assertRaisesRegex(ValueError, "empty"):
                    load_players()

    def test_invalid_players_json_raises_clear_error(self):
        """Reject invalid JSON in the players file."""
        with tempfile.TemporaryDirectory() as directory:
            players_file = Path(directory) / "players.json"
            players_file.write_text("{invalid", encoding="utf-8")

            with patch("utils.json_manager.PLAYERS_FILE", players_file):
                with self.assertRaisesRegex(ValueError, "invalid JSON"):
                    load_players()

    @patch("controllers.player_controller.save_players")
    @patch("controllers.player_controller.load_players")
    def test_player_load_error_blocks_registry_overwrite(
        self,
        mock_load_players,
        mock_save_players,
    ):
        """Do not overwrite a player registry that failed to load."""
        mock_load_players.side_effect = ValueError(
            "The players JSON file contains invalid JSON."
        )
        controller = PlayerController()

        with self.assertRaisesRegex(ValueError, "Fix the players file"):
            controller.create_player(
                "Dupont",
                "Alice",
                "1990-05-12",
                "AB12345",
            )

        mock_save_players.assert_not_called()

    def test_save_and_load_finished_tournament(self):
        """Save and reload a finished tournament."""
        with tempfile.TemporaryDirectory() as directory:
            tournaments_folder = Path(directory) / "tournaments"
            filename = "test_finished_tournament.json"

            with patch(
                "utils.json_manager.TOURNAMENTS_FOLDER",
                tournaments_folder,
            ):
                player_one = Player(
                    "Dupont",
                    "Alice",
                    "1990-05-12",
                    "AB12345",
                )
                player_two = Player(
                    "Martin",
                    "Paul",
                    "1985-03-08",
                    "CD67890",
                )
                match = Match(player_one, player_two)
                match.set_result(1, 0)

                round_ = Round("Round 1")
                round_.add_match(match)
                round_.close()

                tournament = Tournament(
                    "Test finished",
                    "Thann",
                    "2026-09-10",
                    "2026-09-10",
                )
                tournament.add_player(player_one)
                tournament.add_player(player_two)
                tournament.add_round(round_)

                save_tournament(tournament, filename)
                loaded_tournament = load_tournament(filename)

                self.assertEqual(loaded_tournament.current_round, 1)
                self.assertEqual(
                    loaded_tournament.rounds[0].matches[0].score_one,
                    1,
                )
                self.assertIsNotNone(
                    loaded_tournament.rounds[0].end_datetime
                )
                delete_tournament(filename)

    def test_save_and_load_tournament_in_progress(self):
        """Save and reload a tournament in progress."""
        with tempfile.TemporaryDirectory() as directory:
            tournaments_folder = Path(directory) / "tournaments"
            filename = "test_tournament_in_progress.json"

            with patch(
                "utils.json_manager.TOURNAMENTS_FOLDER",
                tournaments_folder,
            ):
                player_one = Player(
                    "Dupont",
                    "Alice",
                    "1990-05-12",
                    "AB12345",
                )
                player_two = Player(
                    "Martin",
                    "Paul",
                    "1985-03-08",
                    "CD67890",
                )
                match = Match(player_one, player_two)

                round_ = Round("Round 1")
                round_.add_match(match)

                tournament = Tournament(
                    "Test in progress",
                    "Thann",
                    "2026-09-10",
                    "2026-09-10",
                )
                tournament.add_player(player_one)
                tournament.add_player(player_two)
                tournament.add_round(round_)

                save_tournament(tournament, filename)
                loaded_tournament = load_tournament(filename)

                loaded_match = loaded_tournament.rounds[0].matches[0]
                loaded_round = loaded_tournament.rounds[0]

                self.assertIsNone(loaded_match.score_one)
                self.assertIsNone(loaded_match.score_two)
                self.assertIsNone(loaded_round.end_datetime)
                delete_tournament(filename)

    def test_missing_tournament_file_raises_clear_error(self):
        """Report a missing tournament file clearly."""
        with tempfile.TemporaryDirectory() as directory:
            tournaments_folder = Path(directory) / "tournaments"

            with patch(
                "utils.json_manager.TOURNAMENTS_FOLDER",
                tournaments_folder,
            ):
                with self.assertRaisesRegex(ValueError, "not found"):
                    load_tournament("missing.json")

    def test_empty_tournament_file_raises_clear_error(self):
        """Reject an empty tournament file."""
        with tempfile.TemporaryDirectory() as directory:
            tournaments_folder = Path(directory) / "tournaments"
            tournaments_folder.mkdir()
            tournament_file = tournaments_folder / "empty.json"
            tournament_file.write_text("", encoding="utf-8")

            with patch(
                "utils.json_manager.TOURNAMENTS_FOLDER",
                tournaments_folder,
            ):
                with self.assertRaisesRegex(ValueError, "empty"):
                    load_tournament("empty.json")

    def test_invalid_tournament_json_raises_clear_error(self):
        """Reject invalid JSON in a tournament file."""
        with tempfile.TemporaryDirectory() as directory:
            tournaments_folder = Path(directory) / "tournaments"
            tournaments_folder.mkdir()
            tournament_file = tournaments_folder / "invalid.json"
            tournament_file.write_text("{invalid", encoding="utf-8")

            with patch(
                "utils.json_manager.TOURNAMENTS_FOLDER",
                tournaments_folder,
            ):
                with self.assertRaisesRegex(ValueError, "invalid JSON"):
                    load_tournament("invalid.json")

    @patch("controllers.tournament_controller.save_tournament")
    def test_existing_tournament_file_is_not_overwritten(
        self,
        mock_save_tournament,
    ):
        """Refuse to create a tournament over an existing file."""
        with tempfile.TemporaryDirectory() as directory:
            tournaments_folder = Path(directory) / "tournaments"
            tournaments_folder.mkdir()
            tournament_file = tournaments_folder / "Existing.json"
            tournament_file.write_text("valid existing data", encoding="utf-8")
            controller = TournamentController()

            with patch(
                "controllers.tournament_controller.TOURNAMENTS_FOLDER",
                tournaments_folder,
            ):
                with self.assertRaisesRegex(ValueError, "already exists"):
                    controller.create_tournament(
                        "Existing",
                        "Thann",
                        "2026-09-10",
                        "2026-09-10",
                    )

            self.assertEqual(
                tournament_file.read_text(encoding="utf-8"),
                "valid existing data",
            )
            mock_save_tournament.assert_not_called()


if __name__ == "__main__":
    unittest.main()
