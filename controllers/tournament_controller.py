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

    def can_add_player(self, tournament):
        """Check if players can still be added to a tournament."""
        return tournament.current_round == 0

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

    def get_open_round(self, tournament):
        """Return the first round that is still open."""
        for round_ in tournament.rounds:
            if round_.end_datetime is None:
                return round_

        return None

    def can_create_next_round(self, tournament):
        """Check if a new round can be created."""
        return self.get_open_round(tournament) is None

    def is_round_complete(self, round_):
        """Check if every match in a round has a result."""
        for match in round_.matches:
            if match.score_one is None or match.score_two is None:
                return False

        return True

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

    def have_played_together(self, tournament, player_one, player_two):
        """Check if two players have already played together."""
        for round_ in tournament.rounds:
            for match in round_.matches:
                players = {
                    match.player_one.national_id,
                    match.player_two.national_id,
                }

                if players == {
                    player_one.national_id,
                    player_two.national_id,
                }:
                    return True

        return False

    def create_matches(self, tournament, round_):
        """Create matches for a round."""
        if tournament.current_round == 1:
            players = tournament.players.copy()
            random.shuffle(players)
        else:
            players = self.get_ranking(tournament)

        while players:
            player_one = players.pop(0)
            opponent_index = None

            for index, player_two in enumerate(players):
                if not self.have_played_together(
                    tournament,
                    player_one,
                    player_two,
                ):
                    opponent_index = index
                    break

            if opponent_index is None:
                opponent_index = 0

            player_two = players.pop(opponent_index)
            match = Match(player_one, player_two)
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
