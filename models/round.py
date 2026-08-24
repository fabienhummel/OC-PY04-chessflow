class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_datetime = None
        self.end_datetime = None

    def add_match(self, match):
        pass

    def close(self):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass
