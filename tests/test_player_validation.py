import unittest
from unittest.mock import patch

from controllers.player_controller import PlayerController
from models.player import Player


class PlayerValidationTestCase(unittest.TestCase):
    """Test player validation rules handled by the controller."""

    def setUp(self):
        """Create a controller without reading local JSON data."""
        self.controller = PlayerController.__new__(PlayerController)
        self.player_one = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.player_two = Player("Martin", "Paul", "1988-01-01", "CD67890")
        self.controller.players = [self.player_one, self.player_two]

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

        self.assertEqual(len(self.controller.players), 2)
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
        with self.assertRaises(ValueError):
            self.controller.update_player(
                self.player_one,
                "Dupont",
                "Alice",
                "1990-05-12",
                "cd67890",
            )

        self.assertEqual(self.player_one.national_id, "AB12345")
        mock_save_players.assert_not_called()

    @patch("controllers.player_controller.save_players")
    def test_update_player_can_keep_its_national_id(self, mock_save_players):
        """Allow a player to keep its own national chess ID."""
        self.controller.update_player(
            self.player_one,
            "Dupont",
            "Alicia",
            "1990-05-12",
            "ab12345",
        )

        self.assertEqual(self.player_one.first_name, "Alicia")
        self.assertEqual(self.player_one.national_id, "AB12345")
        mock_save_players.assert_called_once_with(self.controller.players)


if __name__ == "__main__":
    unittest.main()
