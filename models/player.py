import re


class Player:
    """Represent a chess player."""

    def __init__(self, last_name, first_name, birth_date, national_id):
        """Initialize a player."""
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = self.validate_national_id(national_id)

    @staticmethod
    def validate_national_id(national_id):
        """Validate and normalize a national chess ID."""
        normalized_id = national_id.strip().upper()

        if re.fullmatch(r"[A-Z]{2}[0-9]{5}", normalized_id) is None:
            raise ValueError(
                "National chess ID must contain two letters followed by five digits."
            )

        return normalized_id

    def to_dict(self):
        """Convert the player to a dictionary."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a player from a dictionary."""
        return cls(
            data["last_name"],
            data["first_name"],
            data["birth_date"],
            data["national_id"],
        )
