from models.player import Player
from utils.json_manager import load_players, save_players


class PlayerController:
    """Manage player-related actions."""

    def __init__(self):
        """Initialize the player controller."""
        self.load_error = None

        try:
            self.players = load_players()
        except ValueError as error:
            self.players = []
            self.load_error = str(error)

    def ensure_players_loaded(self):
        """Prevent writes when the player registry could not be loaded."""
        if self.load_error is not None:
            raise ValueError(
                f"{self.load_error} Fix the players file before modifying the registry."
            )

    def create_player(self, last_name, first_name, birth_date, national_id):
        """Create a player."""
        self.ensure_players_loaded()
        player = Player(last_name, first_name, birth_date, national_id)

        if self.find_player(player.national_id) is not None:
            raise ValueError("A player with this national chess ID already exists.")

        self.players.append(player)
        save_players(self.players)
        return player

    def list_players(self):
        """List all players in alphabetical order."""
        return sorted(
            self.players,
            key=lambda player: (
                player.last_name.lower(),
                player.first_name.lower(),
            ),
        )

    def find_player(self, national_id):
        """Find a player by national chess ID."""
        normalized_id = national_id.strip().upper()

        for player in self.players:
            if player.national_id == normalized_id:
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
        self.ensure_players_loaded()
        normalized_id = Player.validate_national_id(national_id)

        for existing_player in self.players:
            if (
                existing_player is not player
                and existing_player.national_id == normalized_id
            ):
                raise ValueError(
                    "A player with this national chess ID already exists."
                )

        player.last_name = last_name
        player.first_name = first_name
        player.birth_date = birth_date
        player.national_id = normalized_id
        save_players(self.players)

    def delete_player(self, player):
        """Delete a player."""
        self.ensure_players_loaded()
        self.players.remove(player)
        save_players(self.players)
