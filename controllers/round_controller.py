import random
from datetime import datetime

from models.match import Match
from models.round import Round
from persistence.json_repository import save_tournament


class RoundController:
    """Manage tournament rounds."""

    def create_round(self, tournament):
        """Validate and create a tournament round."""
        if tournament.current_round >= tournament.number_of_rounds:
            raise ValueError("All rounds have already been created.")

        if not self.can_create_next_round(tournament):
            raise ValueError(
                "The current round must be closed before creating the next round."
            )

        if not tournament.players:
            raise ValueError("Add players before creating a round.")

        if len(tournament.players) % 2 != 0:
            raise ValueError("The tournament must have an even number of players.")

        round_ = Round(f"Round {tournament.current_round + 1}")
        round_.start_datetime = datetime.now()
        tournament.add_round(round_)
        save_tournament(tournament, f"{tournament.name}.json")
        return round_

    @staticmethod
    def get_open_round(tournament):
        """Return the first round that is still open."""
        for round_ in tournament.rounds:
            if round_.end_datetime is None:
                return round_

        return None

    def can_create_next_round(self, tournament):
        """Check if a new round can be created."""
        return self.get_open_round(tournament) is None

    @staticmethod
    def is_round_complete(round_):
        """Check if every match in a round has a result."""
        return all(
            match.score_one is not None and match.score_two is not None
            for match in round_.matches
        )

    @staticmethod
    def get_player_score(tournament, player):
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

    def get_ranking_with_scores(self, tournament):
        """Return the ranking with each player's score."""
        return [
            (player, self.get_player_score(tournament, player))
            for player in self.get_ranking(tournament)
        ]

    @staticmethod
    def have_played_together(tournament, player_one, player_two):
        """Check if two players have already played together."""
        expected_players = {player_one.national_id, player_two.national_id}

        for round_ in tournament.rounds:
            for match in round_.matches:
                players = {
                    match.player_one.national_id,
                    match.player_two.national_id,
                }
                if players == expected_players:
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
            opponent_index = 0

            for index, player_two in enumerate(players):
                if not self.have_played_together(
                    tournament,
                    player_one,
                    player_two,
                ):
                    opponent_index = index
                    break

            player_two = players.pop(opponent_index)
            round_.add_match(Match(player_one, player_two))

        save_tournament(tournament, f"{tournament.name}.json")
        return round_.matches

    def close_round(self, tournament, round_):
        """Validate and close a round."""
        if round_.end_datetime is not None:
            raise ValueError("This round is already closed.")

        if not self.is_round_complete(round_):
            raise ValueError("Enter all match results before closing the round.")

        round_.close()
        save_tournament(tournament, f"{tournament.name}.json")
