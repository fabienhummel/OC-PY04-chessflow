from models.player import Player


class PlayerController:
    """Manage player-related actions."""

    def __init__(self):
        """Initialize the player controller."""
        self.players = []

    def create_player(self, last_name, first_name, birth_date, national_id):
        """Create a player."""
        player = Player(last_name, first_name, birth_date, national_id)
        self.players.append(player)
        return player

    def list_players(self):
        """List all players."""
        return self.players
