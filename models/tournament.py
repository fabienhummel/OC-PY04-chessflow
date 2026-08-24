class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        description="",
        number_of_rounds=4,
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.players = []
        self.rounds = []

    def add_player(self, player):
        pass

    def add_round(self, round_):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass
