import unittest

from models.match import Match
from models.player import Player


class MatchTestCase(unittest.TestCase):
    """Test the Match model."""

    def setUp(self):
        """Create two players for the tests."""
        self.player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.player_two = Player("Martin", "Bob", "1988-03-20", "CD67890")

    def test_create_match(self):
        """Create a match with two players."""
        match = Match(self.player_one, self.player_two)

        self.assertEqual(match.player_one, self.player_one)
        self.assertEqual(match.player_two, self.player_two)
        self.assertIsNone(match.score_one)
        self.assertIsNone(match.score_two)

    def test_match_uses_required_tuple_representation(self):
        """Store match data as a tuple containing two player-score lists."""
        match = Match(self.player_one, self.player_two)

        self.assertIsInstance(match.pair, tuple)
        self.assertEqual(len(match.pair), 2)
        self.assertIsInstance(match.pair[0], list)
        self.assertIsInstance(match.pair[1], list)
        self.assertEqual(match.pair[0], [self.player_one, None])
        self.assertEqual(match.pair[1], [self.player_two, None])

    def test_set_result(self):
        """Set the result of a match."""
        match = Match(self.player_one, self.player_two)

        match.set_result(1, 0)

        self.assertEqual(match.score_one, 1)
        self.assertEqual(match.score_two, 0)
        self.assertEqual(match.pair[0][1], 1)
        self.assertEqual(match.pair[1][1], 0)

    def test_match_to_dict(self):
        """Convert a match to a dictionary."""
        match = Match(self.player_one, self.player_two)
        match.set_result(0.5, 0.5)

        data = match.to_dict()

        self.assertEqual(data["score_one"], 0.5)
        self.assertEqual(data["score_two"], 0.5)
        self.assertEqual(data["player_one"]["national_id"], "AB12345")

    def test_match_from_dict(self):
        """Create a match from a dictionary."""
        match = Match(self.player_one, self.player_two)
        match.set_result(1, 0)

        restored_match = Match.from_dict(match.to_dict())

        self.assertEqual(restored_match.player_one.national_id, "AB12345")
        self.assertEqual(restored_match.player_two.national_id, "CD67890")
        self.assertEqual(restored_match.score_one, 1)
        self.assertEqual(restored_match.score_two, 0)
        self.assertIsInstance(restored_match.pair, tuple)


if __name__ == "__main__":
    unittest.main()
