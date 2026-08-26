from models.player import Player
from utils.json_manager import load_players, save_players


class PlayerController:
    """Manage player-related actions."""

    def __init__(self):
        """Initialize the player controller."""
        self.players = load_players()

    def create_player(self, last_name, first_name, birth_date, national_id):
        """Create a player."""
        player = Player(last_name, first_name, birth_date, national_id)
        self.players.append(player)
        save_players(self.players)
        return player

    def list_players(self):
        """List all players."""
        return self.players
