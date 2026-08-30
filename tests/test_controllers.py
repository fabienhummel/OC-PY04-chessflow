import unittest
from unittest.mock import patch

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


class PlayerControllerTestCase(unittest.TestCase):
    """Test player controller actions."""

    def setUp(self):
        """Create a controller with test players."""
        self.controller = PlayerController.__new__(PlayerController)
        self.player = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.controller.players = [self.player]

    def test_find_player(self):
        """Find a player by national ID."""
        player = self.controller.find_player("AB12345")
        self.assertIs(player, self.player)

    def test_find_unknown_player_returns_none(self):
        """Return None for an unknown player."""
        player = self.controller.find_player("ZZ99999")
        self.assertIsNone(player)

    @patch("controllers.player_controller.save_players")
    def test_create_player_rejects_duplicate_national_id(self, mock_save_players):
        """Reject a national chess ID that already belongs to a player."""
        with self.assertRaises(ValueError):
            self.controller.create_player(
                "Petit",
                "Claire",
                "1992-07-01",
                "ab12345",
            )

        self.assertEqual(len(self.controller.players), 1)
        mock_save_players.assert_not_called()

    @patch("controllers.player_controller.save_players")
    def test_create_player_accepts_unique_national_id(self, mock_save_players):
        """Create and save a player with a unique national chess ID."""
        player = self.controller.create_player(
            "Petit",
            "Claire",
            "1992-07-01",
            " ef24680 ",
        )

        self.assertEqual(player.national_id, "EF24680")
        self.assertIn(player, self.controller.players)
        mock_save_players.assert_called_once_with(self.controller.players)

    @patch("controllers.player_controller.save_players")
    def test_update_player_rejects_duplicate_national_id(self, mock_save_players):
        """Reject an ID already used by another player during an update."""
        other_player = Player("Martin", "Paul", "1988-01-01", "CD67890")
        self.controller.players.append(other_player)

        with self.assertRaises(ValueError):
            self.controller.update_player(
                self.player,
                "Dupont",
                "Alice",
                "1990-05-12",
                "cd67890",
            )

        self.assertEqual(self.player.national_id, "AB12345")
        mock_save_players.assert_not_called()

    @patch("controllers.player_controller.save_players")
    def test_update_player_can_keep_its_national_id(self, mock_save_players):
        """Allow a player to keep its own national chess ID."""
        self.controller.update_player(
            self.player,
            "Dupont",
            "Alicia",
            "1990-05-12",
            "ab12345",
        )

        self.assertEqual(self.player.first_name, "Alicia")
        self.assertEqual(self.player.national_id, "AB12345")
        mock_save_players.assert_called_once_with(self.controller.players)

    @patch("controllers.player_controller.save_players")
    def test_update_player(self, mock_save_players):
        """Update a player and save the list."""
        self.controller.update_player(
            self.player,
            "Martin",
            "Paul",
            "1988-01-01",
            "MP54321",
        )

        self.assertEqual(self.player.last_name, "Martin")
        self.assertEqual(self.player.first_name, "Paul")
        self.assertEqual(self.player.birth_date, "1988-01-01")
        self.assertEqual(self.player.national_id, "MP54321")
        mock_save_players.assert_called_once_with(self.controller.players)

    @patch("controllers.player_controller.save_players")
    def test_delete_player(self, mock_save_players):
        """Delete a player and save the list."""
        self.controller.delete_player(self.player)

        self.assertEqual(self.controller.players, [])
        mock_save_players.assert_called_once_with(self.controller.players)


class TournamentControllerTestCase(unittest.TestCase):
    """Test tournament controller actions."""

    def setUp(self):
        """Create tournament test data."""
        self.controller = TournamentController()
        self.player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.player_two = Player("Martin", "Paul", "1985-03-08", "CD67890")
        self.match = Match(self.player_one, self.player_two)
        self.tournament = Tournament(
            "Test tournament",
            "Thann",
            "2026-09-05",
            "2026-09-05",
        )

    @patch("controllers.tournament_controller.save_tournament")
    def test_record_result(self, mock_save_tournament):
        """Record a match result."""
        self.controller.record_result(self.tournament, self.match, 1, 0)

        self.assertEqual(self.match.score_one, 1)
        self.assertEqual(self.match.score_two, 0)
        mock_save_tournament.assert_called_once()

    @patch("controllers.tournament_controller.save_tournament")
    def test_record_result_can_be_updated(self, mock_save_tournament):
        """Replace an existing match result."""
        self.match.set_result(1, 0)

        self.controller.record_result(self.tournament, self.match, 0.5, 0.5)

        self.assertEqual(self.match.score_one, 0.5)
        self.assertEqual(self.match.score_two, 0.5)
        mock_save_tournament.assert_called_once()

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

        score = self.controller.get_player_score(
            self.tournament,
            self.player_one,
        )

        self.assertEqual(score, 1.5)

    def test_get_player_score_ignores_unplayed_match(self):
        """Ignore a match without a recorded result."""
        round_one = Round("Round 1")
        round_one.add_match(self.match)
        self.tournament.add_round(round_one)

        score = self.controller.get_player_score(
            self.tournament,
            self.player_one,
        )

        self.assertEqual(score, 0)

    def test_get_ranking_sorts_players_by_score(self):
        """Sort tournament players from highest to lowest score."""
        player_three = Player(
            "Bernard",
            "Claire",
            "1992-07-01",
            "EF24680",
        )
        self.tournament.add_player(self.player_one)
        self.tournament.add_player(self.player_two)
        self.tournament.add_player(player_three)

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
        round_one.add_match(self.match)
        self.tournament.add_round(round_one)

        result = self.controller.have_played_together(
            self.tournament,
            self.player_one,
            self.player_two,
        )

        self.assertTrue(result)

    @patch("controllers.tournament_controller.save_tournament")
    def test_create_matches_avoids_previous_opponent(
        self,
        mock_save_tournament,
    ):
        """Avoid a previous opponent when another player is available."""
        player_three = Player(
            "Bernard",
            "Claire",
            "1992-07-01",
            "EF24680",
        )
        player_four = Player(
            "Petit",
            "Lucas",
            "1994-04-20",
            "GH13579",
        )
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

        with patch.object(
            self.controller,
            "get_ranking",
            return_value=ranking,
        ):
            matches = self.controller.create_matches(
                self.tournament,
                round_two,
            )

        self.assertIs(matches[0].player_one, self.player_one)
        self.assertIs(matches[0].player_two, player_three)
        self.assertIs(matches[1].player_one, self.player_two)
        self.assertIs(matches[1].player_two, player_four)
        mock_save_tournament.assert_called_once()

    @patch("controllers.tournament_controller.save_tournament")
    def test_create_matches_uses_ranking_after_first_round(
        self,
        mock_save_tournament,
    ):
        """Use ranking order to pair players after round one."""
        player_three = Player(
            "Bernard",
            "Claire",
            "1992-07-01",
            "EF24680",
        )
        player_four = Player(
            "Petit",
            "Lucas",
            "1994-04-20",
            "GH13579",
        )
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
            matches = self.controller.create_matches(
                self.tournament,
                round_two,
            )

        mock_get_ranking.assert_called_once_with(self.tournament)
        self.assertIs(matches[0].player_one, player_three)
        self.assertIs(matches[0].player_two, self.player_one)
        self.assertIs(matches[1].player_one, player_four)
        self.assertIs(matches[1].player_two, self.player_two)
        mock_save_tournament.assert_called_once()

    @patch("controllers.tournament_controller.save_tournament")
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

        round_one = Round("Round 1")
        previous_pairs = [
            (players[0], players[1]),
            (players[2], players[3]),
            (players[4], players[5]),
            (players[6], players[7]),
        ]

        for player_one, player_two in previous_pairs:
            round_one.add_match(Match(player_one, player_two))

        self.tournament.add_round(round_one)
        self.tournament.current_round = 2
        round_two = Round("Round 2")

        with patch.object(
            self.controller,
            "get_ranking",
            return_value=players,
        ):
            matches = self.controller.create_matches(
                self.tournament,
                round_two,
            )

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

    @patch("controllers.tournament_controller.save_tournament")
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

        with patch.object(
            self.controller,
            "get_ranking",
            return_value=players,
        ):
            matches = self.controller.create_matches(
                self.tournament,
                round_three,
            )

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
