import unittest
from unittest.mock import patch

from controllers.player_controller import PlayerController
from models.player import Player


class PlayerControllerTestCase(unittest.TestCase):
    """Test player controller actions."""

    def setUp(self):
        """Create a controller with test players."""
        self.controller = PlayerController.__new__(PlayerController)
        self.player = Player("Dupont", "Alice", "1990-05-12", "AB12345")
        self.controller.players = [self.player]

    def test_find_player(self):
        """Find a player by national ID."""
        player = self.controller.find_player("AB12345")
        self.assertIs(player, self.player)

    def test_find_unknown_player_returns_none(self):
        """Return None for an unknown player."""
        player = self.controller.find_player("ZZ99999")
        self.assertIsNone(player)

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

        self.assertEqual(len(self.controller.players), 1)
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
        other_player = Player("Martin", "Paul", "1988-01-01", "CD67890")
        self.controller.players.append(other_player)

        with self.assertRaises(ValueError):
            self.controller.update_player(
                self.player,
                "Dupont",
                "Alice",
                "1990-05-12",
                "cd67890",
            )

        self.assertEqual(self.player.national_id, "AB12345")
        mock_save_players.assert_not_called()

    @patch("controllers.player_controller.save_players")
    def test_update_player_can_keep_its_national_id(self, mock_save_players):
        """Allow a player to keep its own national chess ID."""
        self.controller.update_player(
            self.player,
            "Dupont",
            "Alicia",
            "1990-05-12",
            "ab12345",
        )

        self.assertEqual(self.player.first_name, "Alicia")
        self.assertEqual(self.player.national_id, "AB12345")
        mock_save_players.assert_called_once_with(self.controller.players)

    @patch("controllers.player_controller.save_players")
    def test_update_player(self, mock_save_players):
        """Update a player and save the list."""
        self.controller.update_player(
            self.player,
            "Martin",
            "Paul",
            "1988-01-01",
            "MP54321",
        )

        self.assertEqual(self.player.last_name, "Martin")
        self.assertEqual(self.player.first_name, "Paul")
        self.assertEqual(self.player.birth_date, "1988-01-01")
        self.assertEqual(self.player.national_id, "MP54321")
        mock_save_players.assert_called_once_with(self.controller.players)

    @patch("controllers.player_controller.save_players")
    def test_delete_player(self, mock_save_players):
        """Delete a player and save the list."""
        self.controller.delete_player(self.player)

        self.assertEqual(self.controller.players, [])
        mock_save_players.assert_called_once_with(self.controller.players)


if __name__ == "__main__":
    unittest.main()
