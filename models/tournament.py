from datetime import date

from models.player import Player
from models.round import Round


class Tournament:
    """Represent a chess tournament."""

    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        description="",
        number_of_rounds=4,
    ):
        """Initialize a tournament."""
        self.name = self.validate_required_text(name, "Tournament name")
        self.location = self.validate_required_text(location, "Location")
        self.start_date = self.validate_date(start_date, "Start date")
        self.end_date = self.validate_date(end_date, "End date")

        if date.fromisoformat(self.end_date) < date.fromisoformat(self.start_date):
            raise ValueError("End date cannot be earlier than start date.")

        self.description = description
        self.number_of_rounds = self.validate_number_of_rounds(number_of_rounds)
        self.current_round = 0
        self.players = []
        self.rounds = []

    @staticmethod
    def validate_required_text(value, field_name):
        """Validate and normalize required tournament text."""
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(f"{field_name} is required.")

        return normalized_value

    @staticmethod
    def validate_date(value, field_name):
        """Validate and normalize a tournament date."""
        normalized_date = value.strip()

        if not normalized_date:
            raise ValueError(f"{field_name} is required.")

        try:
            date.fromisoformat(normalized_date)
        except ValueError:
            raise ValueError(
                f"{field_name} must be a valid date in YYYY-MM-DD format."
            ) from None

        return normalized_date

    @staticmethod
    def validate_number_of_rounds(number_of_rounds):
        """Validate the tournament number of rounds."""
        try:
            number_of_rounds = int(number_of_rounds)
        except (TypeError, ValueError):
            raise ValueError("Number of rounds must be a positive integer.") from None

        if number_of_rounds <= 0:
            raise ValueError("Number of rounds must be a positive integer.")

        return number_of_rounds

    def add_player(self, player):
        """Add a player to the tournament."""
        self.players.append(player)

    def add_round(self, round_):
        """Add a round to the tournament."""
        self.rounds.append(round_)
        self.current_round += 1

    def to_dict(self):
        """Convert the tournament to a dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": [player.to_dict() for player in self.players],
            "rounds": [round_.to_dict() for round_ in self.rounds],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a tournament from a dictionary."""
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data["description"],
            data["number_of_rounds"],
        )
        tournament.current_round = data["current_round"]
        tournament.players = [Player.from_dict(player) for player in data["players"]]
        tournament.rounds = [Round.from_dict(round_) for round_ in data["rounds"]]
        return tournament
