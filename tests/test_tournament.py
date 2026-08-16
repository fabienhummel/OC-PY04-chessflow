"""Tests for the Tournament model."""

import unittest
from datetime import date

from models.match import Match
from models.player import Player
from models.tournament import Tournament


class TournamentTestCase(unittest.TestCase):
    """Validate tournament invariants, lifecycle and scores."""

    def setUp(self) -> None:
        self.players = [
            Player("Alpha", "Alice", date(1990, 1, 1), "AA00001"),
            Player("Beta", "Bob", date(1991, 2, 2), "BB00002"),
            Player("Gamma", "Gina", date(1992, 3, 3), "CC00003"),
            Player("Delta", "Dan", date(1993, 4, 4), "DD00004"),
        ]
        self.tournament = Tournament("Open", "Paris", date(2026, 8, 16), date(2026, 8, 17))

    def test_tournament_defaults_to_four_rounds(self) -> None:
        self.assertEqual(self.tournament.number_of_rounds, 4)

    def test_tournament_requires_an_even_participant_count_to_start(self) -> None:
        self.tournament.add_participant(self.players[0])
        self.assertFalse(self.tournament.can_start())

        self.tournament.add_participant(self.players[1])
        self.assertTrue(self.tournament.can_start())

    def test_tournament_tracks_round_and_tournament_scores(self) -> None:
        for player in self.players:
            self.tournament.add_participant(player)
        first_match = Match(self.players[0], self.players[1])
        second_match = Match(self.players[2], self.players[3])
        round_ = self.tournament.start_round([first_match, second_match])

        first_match.set_result(1, 0)
        second_match.set_result(0.5, 0.5)
        round_.close()
        self.tournament.update_scores()

        self.assertEqual(self.tournament.current_round, 1)
        self.assertEqual(self.tournament.player_scores["AA00001"], 1.0)
        self.assertEqual(self.tournament.player_scores["CC00003"], 0.5)

    def test_tournament_rejects_an_incomplete_pairing(self) -> None:
        for player in self.players:
            self.tournament.add_participant(player)

        with self.assertRaises(ValueError):
            self.tournament.start_round([Match(self.players[0], self.players[1])])

    def test_tournament_round_trip_serialization(self) -> None:
        for player in self.players[:2]:
            self.tournament.add_participant(player)
        match = Match(*self.players[:2])
        round_ = self.tournament.start_round([match])
        match.set_result(1, 0)
        round_.close()
        self.tournament.update_scores()

        restored = Tournament.from_dict(self.tournament.to_dict())

        self.assertEqual(restored.to_dict(), self.tournament.to_dict())


if __name__ == "__main__":
    unittest.main()
