"""Round business model."""

from dataclasses import dataclass, field
from datetime import datetime

from models.match import Match


@dataclass(slots=True)
class Round:
    """Group matches played during the same tournament round."""

    name: str
    matches: list[Match] = field(default_factory=list)
    start_datetime: datetime = field(default_factory=datetime.now)
    end_datetime: datetime | None = None

    def __post_init__(self) -> None:
        """Validate the round and its initial matches."""
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Round name is required.")
        initial_matches = list(self.matches)
        initial_end_datetime = self.end_datetime
        self.matches = []
        self.end_datetime = None
        for match in initial_matches:
            self.add_match(match)
        self.end_datetime = initial_end_datetime

    def add_match(self, match: Match) -> None:
        """Add a match while ensuring each player appears only once."""
        if self.end_datetime is not None:
            raise RuntimeError("A closed round cannot be modified.")
        if not isinstance(match, Match):
            raise TypeError("A round can only contain Match instances.")

        registered_ids = {
            player.national_id
            for existing_match in self.matches
            for player in (existing_match.player_one, existing_match.player_two)
        }
        match_ids = {match.player_one.national_id, match.player_two.national_id}
        if registered_ids & match_ids:
            raise ValueError("A player can only appear once in a round.")
        self.matches.append(match)

    def is_complete(self) -> bool:
        """Return whether every match has a result."""
        return bool(self.matches) and all(match.has_result() for match in self.matches)

    def close(self) -> None:
        """Automatically timestamp a completed round."""
        if self.end_datetime is not None:
            return
        if not self.is_complete():
            raise RuntimeError("A round cannot close before all results are entered.")
        self.end_datetime = datetime.now()

    def to_dict(self) -> dict[str, object]:
        """Serialize the round to JSON-compatible data."""
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Round":
        """Build a round from serialized data."""
        serialized_matches = data.get("matches", [])
        if not isinstance(serialized_matches, list):
            raise TypeError("Serialized round matches must be a list.")
        start_datetime = data["start_datetime"]
        end_datetime = data.get("end_datetime")
        if not isinstance(start_datetime, str):
            raise TypeError("Serialized start date must be an ISO string.")

        return cls(
            name=str(data["name"]),
            matches=[Match.from_dict(match_data) for match_data in serialized_matches],
            start_datetime=datetime.fromisoformat(start_datetime),
            end_datetime=datetime.fromisoformat(end_datetime) if isinstance(end_datetime, str) else None,
        )
