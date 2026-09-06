from datetime import date

from models.tournament import Tournament
from persistence.json_repository import (
    list_tournament_files as get_tournament_files,
    load_tournament,
    save_tournament,
)


class TournamentController:
    """Manage tournament-related actions."""

    @staticmethod
    def validate_required_text(value, field_name):
        """Validate and normalize required text."""
        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} is required.")

        return value

    @staticmethod
    def validate_date(value, field_name):
        """Validate and normalize a date."""
        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} is required.")

        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f"{field_name} must be a valid date in YYYY-MM-DD format."
            ) from None

        return value

    @staticmethod
    def validate_number_of_rounds(value):
        """Validate the number of rounds."""
        if value in ("", None):
            return 4

        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Number of rounds must be a positive integer.") from None

        if value <= 0:
            raise ValueError("Number of rounds must be a positive integer.")

        return value

    def create_tournament(
        self,
        name,
        location,
        start_date,
        end_date,
        description="",
        number_of_rounds=4,
    ):
        """Validate and create a tournament."""
        name = self.validate_required_text(name, "Tournament name")
        location = self.validate_required_text(location, "Location")
        start_date = self.validate_date(start_date, "Start date")
        end_date = self.validate_date(end_date, "End date")
        number_of_rounds = self.validate_number_of_rounds(number_of_rounds)

        if date.fromisoformat(end_date) < date.fromisoformat(start_date):
            raise ValueError("End date cannot be earlier than start date.")

        filename = f"{name}.json"

        if filename in self.list_tournament_files():
            raise ValueError("A tournament with this name already exists.")

        tournament = Tournament(
            name,
            location,
            start_date,
            end_date,
            description,
            number_of_rounds,
        )
        save_tournament(tournament, filename)
        return tournament

    @staticmethod
    def list_tournament_files():
        """List saved tournament files."""
        return get_tournament_files()

    def list_saved_tournaments(self):
        """Load all saved tournaments for reports."""
        return [
            load_tournament(filename)
            for filename in self.list_tournament_files()
        ]

    @staticmethod
    def load_tournament(filename):
        """Load a tournament."""
        return load_tournament(filename)

    @staticmethod
    def list_tournament_players(tournament):
        """List tournament players in alphabetical order."""
        return sorted(
            tournament.players,
            key=lambda player: (
                player.last_name.lower(),
                player.first_name.lower(),
            ),
        )

    @staticmethod
    def can_add_player(tournament):
        """Check if players can still be added to a tournament."""
        return tournament.current_round == 0

    def add_player(self, tournament, player):
        """Validate and add a player to a tournament."""
        if not self.can_add_player(tournament):
            raise ValueError(
                "Players cannot be added after the first round has started."
            )

        for existing_player in tournament.players:
            if existing_player.national_id == player.national_id:
                raise ValueError("This player is already registered in the tournament.")

        tournament.add_player(player)
        save_tournament(tournament, f"{tournament.name}.json")
