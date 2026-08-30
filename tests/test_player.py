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

    def test_player_normalizes_required_fields(self):
        """Remove surrounding spaces from required player fields."""
        player = Player(
            " Dupont ",
            " Alice ",
            " 1990-05-12 ",
            "AB12345",
        )

        self.assertEqual(player.last_name, "Dupont")
        self.assertEqual(player.first_name, "Alice")
        self.assertEqual(player.birth_date, "1990-05-12")

    def test_player_rejects_empty_last_name(self):
        """Reject a player without a last name."""
        with self.assertRaises(ValueError):
            Player("   ", "Alice", "1990-05-12", "AB12345")

    def test_player_rejects_empty_first_name(self):
        """Reject a player without a first name."""
        with self.assertRaises(ValueError):
            Player("Dupont", "   ", "1990-05-12", "AB12345")

    def test_player_rejects_invalid_birth_date(self):
        """Reject a birth date that does not exist."""
        with self.assertRaises(ValueError):
            Player("Dupont", "Alice", "2026-02-30", "AB12345")

    def test_player_normalizes_national_id(self):
        """Normalize a valid national chess ID."""
        player = Player("Dupont", "Alice", "1990-05-12", " ab12345 ")

        self.assertEqual(player.national_id, "AB12345")

    def test_player_rejects_invalid_national_id(self):
        """Reject national chess IDs with an invalid format."""
        invalid_ids = [
            "A12345",
            "ABC12345",
            "AB1234",
            "AB123456",
            "1234567",
            "AB12C45",
        ]

        for national_id in invalid_ids:
            with self.subTest(national_id=national_id):
                with self.assertRaises(ValueError):
                    Player("Dupont", "Alice", "1990-05-12", national_id)

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
