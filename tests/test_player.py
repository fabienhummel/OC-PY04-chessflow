import unittest

from models.player import Player


class PlayerTestCase(unittest.TestCase):
    """Test the Player model."""

    def test_create_player(self):
        """Create a player with the expected attributes."""
        player = Player("Dupont", "Alice", "1990-05-12", "AB12345")

        self.assertEqual(player.last_name, "Dupont")
        self.assertEqual(player.first_name, "Alice")
        self.assertEqual(player.birth_date, "1990-05-12")
        self.assertEqual(player.national_id, "AB12345")

    def test_player_to_dict(self):
        """Convert a player to a dictionary."""
        player = Player("Dupont", "Alice", "1990-05-12", "AB12345")

        data = player.to_dict()

        self.assertEqual(data["last_name"], "Dupont")
        self.assertEqual(data["first_name"], "Alice")
        self.assertEqual(data["birth_date"], "1990-05-12")
        self.assertEqual(data["national_id"], "AB12345")

    def test_player_from_dict(self):
        """Create a player from a dictionary."""
        data = {
            "last_name": "Dupont",
            "first_name": "Alice",
            "birth_date": "1990-05-12",
            "national_id": "AB12345",
        }

        player = Player.from_dict(data)

        self.assertEqual(player.last_name, "Dupont")
        self.assertEqual(player.first_name, "Alice")


if __name__ == "__main__":
    unittest.main()
