"""Tests for the Round model."""

import unittest
from datetime import date, datetime

from models.match import Match
from models.player import Player
from models.round import Round


class RoundTestCase(unittest.TestCase):
    """Validate round lifecycle and participant invariants."""

    def setUp(self) -> None:
        self.players = [
            Player("Alpha", "Alice", date(1990, 1, 1), "AA00001"),
            Player("Beta", "Bob", date(1991, 2, 2), "BB00002"),
            Player("Gamma", "Gina", date(1992, 3, 3), "CC00003"),
        ]

    def test_round_sets_its_start_automatically(self) -> None:
        before_creation = datetime.now()
        round_ = Round("Round 1")

        self.assertGreaterEqual(round_.start_datetime, before_creation)

    def test_round_rejects_a_player_registered_twice(self) -> None:
        round_ = Round("Round 1", [Match(self.players[0], self.players[1])])

        with self.assertRaises(ValueError):
            round_.add_match(Match(self.players[0], self.players[2]))

    def test_round_closes_only_when_all_matches_have_results(self) -> None:
        match = Match(self.players[0], self.players[1])
        round_ = Round("Round 1", [match])

        with self.assertRaises(RuntimeError):
            round_.close()

        match.set_result(1, 0)
        round_.close()
        self.assertIsNotNone(round_.end_datetime)

    def test_round_round_trip_serialization(self) -> None:
        match = Match(self.players[0], self.players[1])
        match.set_result(0.5, 0.5)
        round_ = Round("Round 1", [match])
        round_.close()

        self.assertEqual(Round.from_dict(round_.to_dict()).to_dict(), round_.to_dict())


if __name__ == "__main__":
    unittest.main()
