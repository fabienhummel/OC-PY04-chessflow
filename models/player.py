class Player:
    """Represent a chess player."""

    def __init__(self, last_name, first_name, birth_date, national_id):
        """Initialize a player."""
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = national_id

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
