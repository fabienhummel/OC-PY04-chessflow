import unittest
from unittest.mock import patch

from controllers.player_controller import PlayerController
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

        self.assertEqual(
            player.to_dict(),
            {
                "last_name": "Dupont",
                "first_name": "Alice",
                "birth_date": "1990-05-12",
                "national_id": "AB12345",
            },
        )

    def test_player_from_dict(self):
        """Create a player from a dictionary."""
        player = Player.from_dict(
            {
                "last_name": "Dupont",
                "first_name": "Alice",
                "birth_date": "1990-05-12",
                "national_id": "AB12345",
            }
        )

        self.assertEqual(player.last_name, "Dupont")
        self.assertEqual(player.first_name, "Alice")
        self.assertEqual(player.birth_date, "1990-05-12")
        self.assertEqual(player.national_id, "AB12345")


class PlayerValidationTestCase(unittest.TestCase):
    """Test player validation in the controller."""

    def setUp(self):
        """Create a controller without loading application data."""
        self.controller = PlayerController.__new__(PlayerController)
        self.controller.players = []

    @patch("controllers.player_controller.save_players")
    def test_controller_normalizes_player_data(self, mock_save_players):
        """Normalize valid user data before creating the model."""
        player = self.controller.create_player(
            " Dupont ",
            " Alice ",
            " 1990-05-12 ",
            " ab12345 ",
        )

        self.assertEqual(player.last_name, "Dupont")
        self.assertEqual(player.first_name, "Alice")
        self.assertEqual(player.birth_date, "1990-05-12")
        self.assertEqual(player.national_id, "AB12345")
        mock_save_players.assert_called_once()

    @patch("controllers.player_controller.save_players")
    def test_controller_rejects_empty_names(self, mock_save_players):
        """Reject empty required names before creating a player."""
        with self.assertRaises(ValueError):
            self.controller.create_player(
                "   ",
                "Alice",
                "1990-05-12",
                "AB12345",
            )

        mock_save_players.assert_not_called()

    @patch("controllers.player_controller.save_players")
    def test_controller_rejects_invalid_birth_date(self, mock_save_players):
        """Reject an invalid birth date before creating a player."""
        with self.assertRaises(ValueError):
            self.controller.create_player(
                "Dupont",
                "Alice",
                "2026-02-30",
                "AB12345",
            )

        mock_save_players.assert_not_called()

    @patch("controllers.player_controller.save_players")
    def test_controller_rejects_invalid_national_id(self, mock_save_players):
        """Reject an invalid national chess ID before creating a player."""
        with self.assertRaises(ValueError):
            self.controller.create_player(
                "Dupont",
                "Alice",
                "1990-05-12",
                "ABC1234",
            )

        mock_save_players.assert_not_called()


if __name__ == "__main__":
    unittest.main()
