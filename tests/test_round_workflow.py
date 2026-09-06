import unittest
from datetime import datetime
from unittest.mock import patch

from controllers.round_controller import RoundController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class RoundWorkflowTestCase(unittest.TestCase):
    """Test tournament round workflow rules."""

    def setUp(self):
        """Create tournament test data."""
        self.controller = RoundController()
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
        self.tournament.add_round(Round("Round 1"))

        self.assertFalse(self.controller.can_create_next_round(self.tournament))

    def test_round_is_incomplete_without_all_results(self):
        """A round is incomplete while a match has no result."""
        round_one = Round("Round 1")
        round_one.add_match(Match(self.player_one, self.player_two))

        self.assertFalse(self.controller.is_round_complete(round_one))

    def test_get_open_round_returns_oldest_open_round(self):
        """Return the first open round when more than one exists."""
        round_one = Round("Round 1")
        round_one.end_datetime = datetime.now()
        round_two = Round("Round 2")
        round_three = Round("Round 3")
        self.tournament.add_round(round_one)
        self.tournament.add_round(round_two)
        self.tournament.add_round(round_three)

        self.assertIs(self.controller.get_open_round(self.tournament), round_two)

    @patch("controllers.round_controller.save_tournament")
    def test_create_round_requires_players(self, mock_save_tournament):
        """Reject round creation when the tournament has no players."""
        with self.assertRaises(ValueError):
            self.controller.create_round(self.tournament)

        mock_save_tournament.assert_not_called()

    @patch("controllers.round_controller.save_tournament")
    def test_create_round_requires_even_players(self, mock_save_tournament):
        """Reject round creation with an odd number of players."""
        self.tournament.add_player(self.player_one)

        with self.assertRaises(ValueError):
            self.controller.create_round(self.tournament)

        mock_save_tournament.assert_not_called()

    @patch("controllers.round_controller.save_tournament")
    def test_create_round_rejects_open_round(self, mock_save_tournament):
        """Reject a new round while the current round is open."""
        self.tournament.add_player(self.player_one)
        self.tournament.add_player(self.player_two)
        self.tournament.add_round(Round("Round 1"))

        with self.assertRaises(ValueError):
            self.controller.create_round(self.tournament)

        mock_save_tournament.assert_not_called()

    @patch("controllers.round_controller.save_tournament")
    def test_close_round_requires_all_results(self, mock_save_tournament):
        """Reject closing a round before every result is entered."""
        round_one = Round("Round 1")
        round_one.add_match(Match(self.player_one, self.player_two))

        with self.assertRaises(ValueError):
            self.controller.close_round(self.tournament, round_one)

        mock_save_tournament.assert_not_called()

    def test_get_player_score(self):
        """Calculate a player's total score across rounds."""
        round_one = Round("Round 1")
        match_one = Match(self.player_one, self.player_two)
        match_one.set_result(1, 0)
        round_one.add_match(match_one)

        round_two = Round("Round 2")
        match_two = Match(self.player_two, self.player_one)
        match_two.set_result(0.5, 0.5)
        round_two.add_match(match_two)

        self.tournament.add_round(round_one)
        self.tournament.add_round(round_two)

        self.assertEqual(
            self.controller.get_player_score(self.tournament, self.player_one),
            1.5,
        )

    def test_get_player_score_ignores_unplayed_match(self):
        """Ignore a match without a recorded result."""
        round_one = Round("Round 1")
        round_one.add_match(Match(self.player_one, self.player_two))
        self.tournament.add_round(round_one)

        self.assertEqual(
            self.controller.get_player_score(self.tournament, self.player_one),
            0,
        )

    def test_get_ranking_sorts_players_by_score(self):
        """Sort tournament players from highest to lowest score."""
        player_three = Player("Bernard", "Claire", "1992-07-01", "EF24680")
        self.tournament.players = [
            self.player_one,
            self.player_two,
            player_three,
        ]
        round_one = Round("Round 1")
        match_one = Match(self.player_one, self.player_two)
        match_one.set_result(1, 0)
        round_one.add_match(match_one)
        match_two = Match(player_three, self.player_two)
        match_two.set_result(0.5, 0.5)
        round_one.add_match(match_two)
        self.tournament.add_round(round_one)

        ranking = self.controller.get_ranking(self.tournament)

        self.assertIs(ranking[0], self.player_one)
        self.assertEqual(set(ranking[1:]), {self.player_two, player_three})

    def test_have_played_together(self):
        """Detect players who have already played together."""
        round_one = Round("Round 1")
        round_one.add_match(Match(self.player_one, self.player_two))
        self.tournament.add_round(round_one)

        self.assertTrue(
            self.controller.have_played_together(
                self.tournament,
                self.player_one,
                self.player_two,
            )
        )

    @patch("controllers.round_controller.save_tournament")
    def test_create_matches_avoids_previous_opponent(self, mock_save_tournament):
        """Avoid a previous opponent when another player is available."""
        player_three = Player("Bernard", "Claire", "1992-07-01", "EF24680")
        player_four = Player("Petit", "Lucas", "1994-04-20", "GH13579")
        self.tournament.players = [
            self.player_one,
            self.player_two,
            player_three,
            player_four,
        ]
        round_one = Round("Round 1")
        round_one.add_match(Match(self.player_one, self.player_two))
        self.tournament.add_round(round_one)
        self.tournament.current_round = 2
        round_two = Round("Round 2")
        ranking = [
            self.player_one,
            self.player_two,
            player_three,
            player_four,
        ]

        with patch.object(self.controller, "get_ranking", return_value=ranking):
            matches = self.controller.create_matches(self.tournament, round_two)

        self.assertIs(matches[0].player_one, self.player_one)
        self.assertIs(matches[0].player_two, player_three)
        self.assertIs(matches[1].player_one, self.player_two)
        self.assertIs(matches[1].player_two, player_four)
        mock_save_tournament.assert_called_once()

    @patch("controllers.round_controller.save_tournament")
    def test_create_matches_uses_ranking_after_first_round(
        self,
        mock_save_tournament,
    ):
        """Use ranking order to pair players after round one."""
        player_three = Player("Bernard", "Claire", "1992-07-01", "EF24680")
        player_four = Player("Petit", "Lucas", "1994-04-20", "GH13579")
        self.tournament.players = [
            self.player_one,
            self.player_two,
            player_three,
            player_four,
        ]
        self.tournament.current_round = 2
        round_two = Round("Round 2")
        ranking = [
            player_three,
            self.player_one,
            player_four,
            self.player_two,
        ]

        with patch.object(
            self.controller,
            "get_ranking",
            return_value=ranking,
        ) as mock_get_ranking:
            matches = self.controller.create_matches(self.tournament, round_two)

        mock_get_ranking.assert_called_once_with(self.tournament)
        self.assertIs(matches[0].player_one, player_three)
        self.assertIs(matches[0].player_two, self.player_one)
        self.assertIs(matches[1].player_one, player_four)
        self.assertIs(matches[1].player_two, self.player_two)
        mock_save_tournament.assert_called_once()

    @patch("controllers.round_controller.save_tournament")
    def test_second_round_with_eight_players_has_no_repeat(
        self,
        mock_save_tournament,
    ):
        """Avoid all first-round pairs with eight players."""
        players = [
            Player("Player1", "A", "1990-01-01", "AA00001"),
            Player("Player2", "B", "1990-01-02", "BB00002"),
            Player("Player3", "C", "1990-01-03", "CC00003"),
            Player("Player4", "D", "1990-01-04", "DD00004"),
            Player("Player5", "E", "1990-01-05", "EE00005"),
            Player("Player6", "F", "1990-01-06", "FF00006"),
            Player("Player7", "G", "1990-01-07", "GG00007"),
            Player("Player8", "H", "1990-01-08", "HH00008"),
        ]
        self.tournament.players = players
        previous_pairs = [
            (players[0], players[1]),
            (players[2], players[3]),
            (players[4], players[5]),
            (players[6], players[7]),
        ]
        round_one = Round("Round 1")
        for player_one, player_two in previous_pairs:
            round_one.add_match(Match(player_one, player_two))
        self.tournament.add_round(round_one)
        self.tournament.current_round = 2
        round_two = Round("Round 2")

        with patch.object(self.controller, "get_ranking", return_value=players):
            matches = self.controller.create_matches(self.tournament, round_two)

        old_pairs = {
            frozenset([player_one.national_id, player_two.national_id])
            for player_one, player_two in previous_pairs
        }
        for match in matches:
            pair = frozenset(
                [match.player_one.national_id, match.player_two.national_id]
            )
            self.assertNotIn(pair, old_pairs)

        mock_save_tournament.assert_called_once()

    @patch("controllers.round_controller.save_tournament")
    def test_third_round_with_eight_players_has_no_repeat(
        self,
        mock_save_tournament,
    ):
        """Avoid pairs from both previous rounds with eight players."""
        players = [
            Player("Player1", "A", "1990-01-01", "AA00001"),
            Player("Player2", "B", "1990-01-02", "BB00002"),
            Player("Player3", "C", "1990-01-03", "CC00003"),
            Player("Player4", "D", "1990-01-04", "DD00004"),
            Player("Player5", "E", "1990-01-05", "EE00005"),
            Player("Player6", "F", "1990-01-06", "FF00006"),
            Player("Player7", "G", "1990-01-07", "GG00007"),
            Player("Player8", "H", "1990-01-08", "HH00008"),
        ]
        self.tournament.players = players
        round_one_pairs = [
            (players[0], players[1]),
            (players[2], players[3]),
            (players[4], players[5]),
            (players[6], players[7]),
        ]
        round_two_pairs = [
            (players[0], players[2]),
            (players[1], players[3]),
            (players[4], players[6]),
            (players[5], players[7]),
        ]
        round_one = Round("Round 1")
        for player_one, player_two in round_one_pairs:
            round_one.add_match(Match(player_one, player_two))
        round_two = Round("Round 2")
        for player_one, player_two in round_two_pairs:
            round_two.add_match(Match(player_one, player_two))
        self.tournament.add_round(round_one)
        self.tournament.add_round(round_two)
        self.tournament.current_round = 3
        round_three = Round("Round 3")

        with patch.object(self.controller, "get_ranking", return_value=players):
            matches = self.controller.create_matches(self.tournament, round_three)

        old_pairs = {
            frozenset([player_one.national_id, player_two.national_id])
            for player_one, player_two in round_one_pairs + round_two_pairs
        }
        for match in matches:
            pair = frozenset(
                [match.player_one.national_id, match.player_two.national_id]
            )
            self.assertNotIn(pair, old_pairs)

        mock_save_tournament.assert_called_once()


if __name__ == "__main__":
    unittest.main()
