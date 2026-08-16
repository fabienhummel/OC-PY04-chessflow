"""Tests for the Player model."""

import unittest
from datetime import date

from models.player import Player


class PlayerTestCase(unittest.TestCase):
    """Validate player creation and serialization."""

    def test_player_normalizes_its_identity(self) -> None:
        player = Player(" Hummel ", " Fabien ", date(1990, 1, 2), "ab12345")

        self.assertEqual(player.last_name, "Hummel")
        self.assertEqual(player.first_name, "Fabien")
        self.assertEqual(player.national_id, "AB12345")

    def test_player_rejects_invalid_national_id(self) -> None:
        with self.assertRaises(ValueError):
            Player("Hummel", "Fabien", date(1990, 1, 2), "A12345")

    def test_player_round_trip_serialization(self) -> None:
        player = Player("Hummel", "Fabien", date(1990, 1, 2), "AB12345")

        self.assertEqual(Player.from_dict(player.to_dict()), player)


if __name__ == "__main__":
    unittest.main()
