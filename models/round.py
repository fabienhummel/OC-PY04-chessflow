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
        pass

    def close(self):
        """Close the round."""
        pass

    def to_dict(self):
        """Convert the round to a dictionary."""
        pass

    @classmethod
    def from_dict(cls, data):
        """Create a round from a dictionary."""
        pass
