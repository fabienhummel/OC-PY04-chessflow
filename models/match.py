from models.player import Player


class Match:
    """Represent a chess match between two players."""

    def __init__(self, player_one, player_two):
        """Initialize a match."""
        self.pair = (
            [player_one, None],
            [player_two, None],
        )

    @property
    def player_one(self):
        """Return the first player."""
        return self.pair[0][0]

    @property
    def player_two(self):
        """Return the second player."""
        return self.pair[1][0]

    @property
    def score_one(self):
        """Return the first player's score."""
        return self.pair[0][1]

    @property
    def score_two(self):
        """Return the second player's score."""
        return self.pair[1][1]

    def set_result(self, score_one, score_two):
        """Set the result of the match."""
        self.pair[0][1] = score_one
        self.pair[1][1] = score_two

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

        score_one = data["score_one"]
        score_two = data["score_two"]

        if score_one is not None or score_two is not None:
            match.set_result(score_one, score_two)

        return match
