class Match:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.score_one = None
        self.score_two = None

    def set_result(self, score_one, score_two):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass
