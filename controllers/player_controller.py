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

    def find_player(self, national_id):
        """Find a player by national chess ID."""
        for player in self.players:
            if player.national_id == national_id:
                return player

        return None

    def update_player(
        self,
        player,
        last_name,
        first_name,
        birth_date,
        national_id,
    ):
        """Update a player."""
        player.last_name = last_name
        player.first_name = first_name
        player.birth_date = birth_date
        player.national_id = national_id
        save_players(self.players)

    def delete_player(self, player):
        """Delete a player."""
        self.players.remove(player)
        save_players(self.players)
