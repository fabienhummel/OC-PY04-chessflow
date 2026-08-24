import random
from datetime import datetime

from models.match import Match
from models.round import Round
from models.tournament import Tournament


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
        return tournament

    def add_player(self, tournament, player):
        """Add a player to a tournament."""
        tournament.add_player(player)

    def create_round(self, tournament):
        """Create a tournament round."""
        round_ = Round(f"Round {tournament.current_round + 1}")
        round_.start_datetime = datetime.now()
        tournament.add_round(round_)
        return round_

    def create_matches(self, tournament, round_):
        """Create matches for a round."""
        players = tournament.players.copy()

        if tournament.current_round == 1:
            random.shuffle(players)

        for index in range(0, len(players), 2):
            match = Match(players[index], players[index + 1])
            round_.add_match(match)

        return round_.matches

    def record_result(self, match, score_one, score_two):
        """Record a match result."""
        match.set_result(score_one, score_two)

    def close_round(self, round_):
        """Close a round."""
        round_.close()
