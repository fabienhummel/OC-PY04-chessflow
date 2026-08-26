import unittest

from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from utils.json_manager import (
    delete_tournament,
    load_players,
    load_tournament,
    save_players,
    save_tournament,
)


class PersistenceTestCase(unittest.TestCase):
    """Test JSON persistence."""

    def test_save_and_load_players(self):
        """Save and reload players."""
        original_players = load_players()

        try:
            players = [Player("Dupont", "Alice", "1990-05-12", "AB12345")]
            save_players(players)

            loaded_players = load_players()

            self.assertEqual(len(loaded_players), 1)
            self.assertEqual(loaded_players[0].national_id, "AB12345")
        finally:
            save_players(original_players)

    def test_save_and_load_finished_tournament(self):
        """Save and reload a finished tournament."""
        filename = "test_finished_tournament.json"

        try:
            player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
            player_two = Player("Martin", "Paul", "1985-03-08", "CD67890")
            match = Match(player_one, player_two)
            match.set_result(1, 0)

            round_ = Round("Round 1")
            round_.add_match(match)
            round_.close()

            tournament = Tournament("Test finished", "Thann", "2026-09-10", "2026-09-10")
            tournament.add_player(player_one)
            tournament.add_player(player_two)
            tournament.add_round(round_)

            save_tournament(tournament, filename)
            loaded_tournament = load_tournament(filename)

            self.assertEqual(loaded_tournament.current_round, 1)
            self.assertEqual(loaded_tournament.rounds[0].matches[0].score_one, 1)
            self.assertIsNotNone(loaded_tournament.rounds[0].end_datetime)
        finally:
            delete_tournament(filename)

    def test_save_and_load_tournament_in_progress(self):
        """Save and reload a tournament in progress."""
        filename = "test_tournament_in_progress.json"

        try:
            player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
            player_two = Player("Martin", "Paul", "1985-03-08", "CD67890")
            match = Match(player_one, player_two)

            round_ = Round("Round 1")
            round_.add_match(match)

            tournament = Tournament("Test in progress", "Thann", "2026-09-10", "2026-09-10")
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
        finally:
            delete_tournament(filename)


if __name__ == "__main__":
    unittest.main()
