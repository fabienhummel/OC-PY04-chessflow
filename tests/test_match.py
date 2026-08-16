"""Tests for the Match model."""

import unittest
from datetime import date

from models.match import Match
from models.player import Player


class MatchTestCase(unittest.TestCase):
    """Validate match participants, results and representation."""

    def setUp(self) -> None:
        self.player_one = Player("Alpha", "Alice", date(1990, 1, 1), "AA00001")
        self.player_two = Player("Beta", "Bob", date(1991, 2, 2), "BB00002")

    def test_match_uses_required_pair_representation(self) -> None:
        match = Match(self.player_one, self.player_two)

        self.assertEqual(match.as_pair(), ([self.player_one, None], [self.player_two, None]))

    def test_match_accepts_supported_results(self) -> None:
        for result in ((1, 0), (0, 1), (0.5, 0.5)):
            with self.subTest(result=result):
                match = Match(self.player_one, self.player_two)
                match.set_result(*result)
                self.assertTrue(match.has_result())

    def test_match_rejects_an_invalid_result(self) -> None:
        match = Match(self.player_one, self.player_two)

        with self.assertRaises(ValueError):
            match.set_result(0.75, 0.25)

    def test_match_rejects_the_same_player_twice(self) -> None:
        with self.assertRaises(ValueError):
            Match(self.player_one, self.player_one)

    def test_match_round_trip_serialization(self) -> None:
        match = Match(self.player_one, self.player_two)
        match.set_result(0.5, 0.5)

        restored_match = Match.from_dict(match.to_dict())

        self.assertEqual(restored_match.to_dict(), match.to_dict())


if __name__ == "__main__":
    unittest.main()
