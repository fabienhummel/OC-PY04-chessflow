from datetime import date
import re

from models.player import Player
from persistence.json_repository import load_players, save_players


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
        load_error = getattr(self, "load_error", None)

        if load_error is not None:
            raise ValueError(
                f"{load_error} Fix the players file before modifying the registry."
            )

    @staticmethod
    def validate_required_text(value, field_name):
        """Validate and normalize required text."""
        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} is required.")

        return value

    @staticmethod
    def validate_birth_date(value):
        """Validate and normalize a birth date."""
        value = value.strip()

        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                "Birth date must be a valid date in YYYY-MM-DD format."
            ) from None

        return value

    @staticmethod
    def validate_national_id(value):
        """Validate and normalize a national chess ID."""
        value = value.strip().upper()

        if re.fullmatch(r"[A-Z]{2}[0-9]{5}", value) is None:
            raise ValueError(
                "National chess ID must contain two letters followed by five digits."
            )

        return value

    def create_player(self, last_name, first_name, birth_date, national_id):
        """Validate and create a player."""
        self.ensure_players_loaded()
        last_name = self.validate_required_text(last_name, "Last name")
        first_name = self.validate_required_text(first_name, "First name")
        birth_date = self.validate_birth_date(birth_date)
        national_id = self.validate_national_id(national_id)

        if self.find_player(national_id) is not None:
            raise ValueError("A player with this national chess ID already exists.")

        player = Player(last_name, first_name, birth_date, national_id)
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
        national_id = national_id.strip().upper()

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
        """Validate and update a player."""
        self.ensure_players_loaded()
        last_name = self.validate_required_text(last_name, "Last name")
        first_name = self.validate_required_text(first_name, "First name")
        birth_date = self.validate_birth_date(birth_date)
        national_id = self.validate_national_id(national_id)

        for existing_player in self.players:
            if (
                existing_player is not player
                and existing_player.national_id == national_id
            ):
                raise ValueError(
                    "A player with this national chess ID already exists."
                )

        player.last_name = last_name
        player.first_name = first_name
        player.birth_date = birth_date
        player.national_id = national_id
        save_players(self.players)

    def delete_player(self, player):
        """Delete a player."""
        self.ensure_players_loaded()
        self.players.remove(player)
        save_players(self.players)
