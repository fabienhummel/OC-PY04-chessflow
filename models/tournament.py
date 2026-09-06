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
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.players = []
        self.rounds = []

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
