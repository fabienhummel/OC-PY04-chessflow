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
        pass

    @classmethod
    def from_dict(cls, data):
        """Create a player from a dictionary."""
        pass
