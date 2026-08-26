import unittest
from datetime import datetime

from models.match import Match
from models.player import Player
from models.round import Round


class RoundTestCase(unittest.TestCase):
    """Test the Round model."""

    def setUp(self):
        """Create a match for the tests."""
        player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        player_two = Player("Martin", "Bob", "1988-03-20", "CD67890")
        self.match = Match(player_one, player_two)
        self.match.set_result(1, 0)

    def test_create_round(self):
        """Create an empty round."""
        round_ = Round("Round 1")

        self.assertEqual(round_.name, "Round 1")
        self.assertEqual(round_.matches, [])
        self.assertIsNone(round_.start_datetime)
        self.assertIsNone(round_.end_datetime)

    def test_add_match(self):
        """Add a match to a round."""
        round_ = Round("Round 1")

        round_.add_match(self.match)

        self.assertEqual(len(round_.matches), 1)
        self.assertEqual(round_.matches[0], self.match)

    def test_close_round(self):
        """Close a round and store its end date."""
        round_ = Round("Round 1")

        round_.close()

        self.assertIsInstance(round_.end_datetime, datetime)

    def test_round_to_dict_and_from_dict(self):
        """Convert a round to a dictionary and recreate it."""
        round_ = Round("Round 1")
        round_.add_match(self.match)
        round_.start_datetime = datetime.now()
        round_.close()

        restored_round = Round.from_dict(round_.to_dict())

        self.assertEqual(restored_round.name, "Round 1")
        self.assertEqual(len(restored_round.matches), 1)
        self.assertIsInstance(restored_round.start_datetime, datetime)
        self.assertIsInstance(restored_round.end_datetime, datetime)


if __name__ == "__main__":
    unittest.main()
