import os
import random
from datetime import datetime

from models.match import Match
from models.round import Round
from models.tournament import Tournament
from utils.json_manager import load_tournament, save_tournament


class TournamentController:
    """Manage tournament-related actions."""

    def __init__(self):
        """Initialize the tournament controller."""
        self.tournaments = []

    def create_tournament(
        self,
        name,
        location,
        start_date,
        end_date,
        description="",
        number_of_rounds=4,
    ):
        """Create a tournament."""
        tournament = Tournament(
            name,
            location,
            start_date,
            end_date,
            description,
            number_of_rounds,
        )
        self.tournaments.append(tournament)
        save_tournament(tournament, f"{tournament.name}.json")
        return tournament

    def list_tournament_files(self):
        """List saved tournament files."""
        folder = "data/tournaments"

        if not os.path.exists(folder):
            return []

        return sorted(
            filename
            for filename in os.listdir(folder)
            if filename.endswith(".json")
        )

    def load_tournament(self, filename):
        """Load a tournament."""
        tournament = load_tournament(filename)
        self.tournaments.append(tournament)
        return tournament

    def add_player(self, tournament, player):
        """Add a player to a tournament."""
        tournament.add_player(player)
        save_tournament(tournament, f"{tournament.name}.json")

    def create_round(self, tournament):
        """Create a tournament round."""
        round_ = Round(f"Round {tournament.current_round + 1}")
        round_.start_datetime = datetime.now()
        tournament.add_round(round_)
        save_tournament(tournament, f"{tournament.name}.json")
        return round_

    def get_player_score(self, tournament, player):
        """Calculate a player's total score in a tournament."""
        score = 0

        for round_ in tournament.rounds:
            for match in round_.matches:
                if match.player_one.national_id == player.national_id:
                    if match.score_one is not None:
                        score += match.score_one
                elif match.player_two.national_id == player.national_id:
                    if match.score_two is not None:
                        score += match.score_two

        return score

    def get_ranking(self, tournament):
        """Return tournament players sorted by score."""
        return sorted(
            tournament.players,
            key=lambda player: self.get_player_score(tournament, player),
            reverse=True,
        )

    def create_matches(self, tournament, round_):
        """Create matches for a round."""
        if tournament.current_round == 1:
            players = tournament.players.copy()
            random.shuffle(players)
        else:
            players = self.get_ranking(tournament)

        for index in range(0, len(players), 2):
            match = Match(players[index], players[index + 1])
            round_.add_match(match)

        save_tournament(tournament, f"{tournament.name}.json")
        return round_.matches

    def record_result(self, tournament, match, score_one, score_two):
        """Record a match result."""
        match.set_result(score_one, score_two)
        save_tournament(tournament, f"{tournament.name}.json")

    def close_round(self, tournament, round_):
        """Close a round."""
        round_.close()
        save_tournament(tournament, f"{tournament.name}.json")
