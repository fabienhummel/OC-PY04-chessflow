"""Tournament business model."""

from dataclasses import dataclass, field
from datetime import date

from models.match import Match
from models.player import Player
from models.round import Round


@dataclass(slots=True)
class Tournament:
    """Aggregate participants, rounds and tournament-specific scores."""

    name: str
    location: str
    start_date: date
    end_date: date
    description: str = ""
    number_of_rounds: int = 4
    participants: list[Player] = field(default_factory=list)
    rounds: list[Round] = field(default_factory=list)
    player_scores: dict[str, float] = field(default_factory=dict)
    current_round: int = 0

    def __post_init__(self) -> None:
        """Validate tournament metadata and reconstruct its invariants."""
        self.name = self.name.strip()
        self.location = self.location.strip()
        self.description = self.description.strip()
        if not self.name or not self.location:
            raise ValueError("Tournament name and location are required.")
        if not isinstance(self.start_date, date) or not isinstance(self.end_date, date):
            raise TypeError("Tournament dates must be date instances.")
        if self.end_date < self.start_date:
            raise ValueError("Tournament end date cannot precede its start date.")
        if not isinstance(self.number_of_rounds, int) or isinstance(self.number_of_rounds, bool):
            raise TypeError("Number of rounds must be an integer.")
        if self.number_of_rounds <= 0:
            raise ValueError("A tournament must contain at least one round.")

        initial_participants = list(self.participants)
        initial_rounds = list(self.rounds)
        initial_scores = dict(self.player_scores)
        self.participants = []
        self.rounds = []
        self.player_scores = {}
        self.current_round = 0

        for participant in initial_participants:
            self.add_participant(participant)
        for national_id, score in initial_scores.items():
            if national_id not in self.player_scores:
                raise ValueError("A score cannot reference a non-participant.")
            self.player_scores[national_id] = float(score)
        for round_ in initial_rounds:
            self.add_round(round_)

    @property
    def status(self) -> str:
        """Return a status derived from the tournament lifecycle."""
        if self.is_finished():
            return "finished"
        if self.rounds:
            return "in_progress"
        return "planned"

    def add_participant(self, player: Player) -> None:
        """Register an existing player without assigning a global score."""
        if self.rounds:
            raise RuntimeError("Participants cannot change after the tournament starts.")
        if not isinstance(player, Player):
            raise TypeError("Tournament participants must be Player instances.")
        if any(existing.national_id == player.national_id for existing in self.participants):
            raise ValueError("A player cannot be registered twice.")
        self.participants.append(player)
        self.player_scores[player.national_id] = 0.0

    def can_start(self) -> bool:
        """Return whether the tournament has a valid even participant count."""
        return len(self.participants) >= 2 and len(self.participants) % 2 == 0 and not self.rounds

    def start_round(self, matches: list[Match]) -> Round:
        """Create the next round from pairings supplied by a controller."""
        round_ = Round(name=f"Round {len(self.rounds) + 1}", matches=matches)
        self.add_round(round_)
        return round_

    def add_round(self, round_: Round) -> None:
        """Add a round progressively while preserving tournament invariants."""
        if not isinstance(round_, Round):
            raise TypeError("A tournament can only contain Round instances.")
        if len(self.participants) < 2 or len(self.participants) % 2:
            raise RuntimeError("A tournament requires an even number of participants.")
        if len(self.rounds) >= self.number_of_rounds:
            raise RuntimeError("The configured number of rounds has already been reached.")
        if self.rounds and self.rounds[-1].end_datetime is None:
            raise RuntimeError("The current round must close before starting the next one.")

        expected_ids = {player.national_id for player in self.participants}
        round_ids = {
            player.national_id
            for match in round_.matches
            for player in (match.player_one, match.player_two)
        }
        if round_ids != expected_ids:
            raise ValueError("Every participant must play exactly once in a round.")
        self.rounds.append(round_)
        self.current_round = len(self.rounds)

    def update_scores(self) -> None:
        """Recalculate tournament-only scores from entered results."""
        self.player_scores = {player.national_id: 0.0 for player in self.participants}
        for round_ in self.rounds:
            for match in round_.matches:
                if match.has_result():
                    self.player_scores[match.player_one.national_id] += match.score_one or 0.0
                    self.player_scores[match.player_two.national_id] += match.score_two or 0.0

    def is_finished(self) -> bool:
        """Return whether all configured rounds are closed."""
        return len(self.rounds) == self.number_of_rounds and all(round_.end_datetime for round_ in self.rounds)

    def to_dict(self) -> dict[str, object]:
        """Serialize the tournament to JSON-compatible data."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "participants": [player.to_dict() for player in self.participants],
            "rounds": [round_.to_dict() for round_ in self.rounds],
            "player_scores": dict(self.player_scores),
            "current_round": self.current_round,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Tournament":
        """Build a tournament from serialized data."""
        participants_data = data.get("participants", [])
        rounds_data = data.get("rounds", [])
        scores_data = data.get("player_scores", {})
        if not isinstance(participants_data, list) or not isinstance(rounds_data, list):
            raise TypeError("Serialized participants and rounds must be lists.")
        if not isinstance(scores_data, dict):
            raise TypeError("Serialized tournament scores must be a dictionary.")

        return cls(
            name=str(data["name"]),
            location=str(data["location"]),
            start_date=date.fromisoformat(str(data["start_date"])),
            end_date=date.fromisoformat(str(data["end_date"])),
            description=str(data.get("description", "")),
            number_of_rounds=int(data.get("number_of_rounds", 4)),
            participants=[Player.from_dict(player_data) for player_data in participants_data],
            rounds=[Round.from_dict(round_data) for round_data in rounds_data],
            player_scores={str(key): float(value) for key, value in scores_data.items()},
        )
