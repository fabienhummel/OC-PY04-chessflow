from datetime import datetime

from models.match import Match


class Round:
    """Represent a round of a chess tournament."""

    def __init__(self, name):
        """Initialize a round."""
        self.name = name
        self.matches = []
        self.start_datetime = None
        self.end_datetime = None

    def add_match(self, match):
        """Add a match to the round."""
        self.matches.append(match)

    def close(self):
        """Close the round."""
        self.end_datetime = datetime.now()

    def to_dict(self):
        """Convert the round to a dictionary."""
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_datetime": self.start_datetime.isoformat() if self.start_datetime else None,
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a round from a dictionary."""
        round_ = cls(data["name"])
        round_.matches = [Match.from_dict(match) for match in data["matches"]]
        if data["start_datetime"]:
            round_.start_datetime = datetime.fromisoformat(data["start_datetime"])
        if data["end_datetime"]:
            round_.end_datetime = datetime.fromisoformat(data["end_datetime"])
        return round_
