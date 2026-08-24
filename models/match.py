from models.player import Player


class Match:
    """Represent a chess match between two players."""

    def __init__(self, player_one, player_two):
        """Initialize a match."""
        self.player_one = player_one
        self.player_two = player_two
        self.score_one = None
        self.score_two = None

    def set_result(self, score_one, score_two):
        """Set the result of the match."""
        self.score_one = score_one
        self.score_two = score_two

    def to_dict(self):
        """Convert the match to a dictionary."""
        return {
            "player_one": self.player_one.to_dict(),
            "player_two": self.player_two.to_dict(),
            "score_one": self.score_one,
            "score_two": self.score_two,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a match from a dictionary."""
        match = cls(
            Player.from_dict(data["player_one"]),
            Player.from_dict(data["player_two"]),
        )
        match.set_result(data["score_one"], data["score_two"])
        return match
