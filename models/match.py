"""Match business model."""

from dataclasses import dataclass
from typing import ClassVar

from models.player import Player


@dataclass(slots=True)
class Match:
    """Represent a game between exactly two players and its result."""

    player_one: Player
    player_two: Player
    score_one: float | None = None
    score_two: float | None = None

    VALID_RESULTS: ClassVar[set[tuple[float, float]]] = {
        (1.0, 0.0),
        (0.0, 1.0),
        (0.5, 0.5),
    }

    def __post_init__(self) -> None:
        """Validate participants and an optional initial result."""
        if not isinstance(self.player_one, Player) or not isinstance(self.player_two, Player):
            raise TypeError("A match must contain two Player instances.")
        if self.player_one.national_id == self.player_two.national_id:
            raise ValueError("A player cannot play against themselves.")
        if (self.score_one is None) != (self.score_two is None):
            raise ValueError("Both match scores must be provided together.")
        if self.score_one is not None and self.score_two is not None:
            self.set_result(self.score_one, self.score_two)

    def set_result(self, score_one: float, score_two: float) -> None:
        """Record a win, loss or draw."""
        if isinstance(score_one, bool) or isinstance(score_two, bool):
            raise ValueError("Match scores must be numeric chess scores.")

        result = (float(score_one), float(score_two))
        if result not in self.VALID_RESULTS:
            raise ValueError("A result must be 1-0, 0-1 or 0.5-0.5.")
        self.score_one, self.score_two = result

    def has_result(self) -> bool:
        """Return whether the result has been entered."""
        return self.score_one is not None and self.score_two is not None

    def involves(self, player: Player) -> bool:
        """Return whether a player participates in the match."""
        return player.national_id in {self.player_one.national_id, self.player_two.national_id}

    def as_pair(self) -> tuple[list[Player | float | None], list[Player | float | None]]:
        """Return the required pair-of-lists match representation."""
        return ([self.player_one, self.score_one], [self.player_two, self.score_two])

    def to_dict(self) -> dict[str, object]:
        """Serialize the match to JSON-compatible data."""
        return {
            "player_one": self.player_one.to_dict(),
            "score_one": self.score_one,
            "player_two": self.player_two.to_dict(),
            "score_two": self.score_two,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Match":
        """Build a match from serialized data."""
        player_one_data = data["player_one"]
        player_two_data = data["player_two"]
        if not isinstance(player_one_data, dict) or not isinstance(player_two_data, dict):
            raise TypeError("Serialized match players must be dictionaries.")

        return cls(
            player_one=Player.from_dict(player_one_data),
            player_two=Player.from_dict(player_two_data),
            score_one=data.get("score_one"),
            score_two=data.get("score_two"),
        )
