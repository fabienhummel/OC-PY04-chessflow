import random
from datetime import date, datetime

from models.match import Match
from models.round import Round
from models.tournament import Tournament
from persistence.json_repository import (
    TOURNAMENTS_FOLDER,
    load_tournament,
    save_tournament,
)


class TournamentController:
    """Manage tournament-related actions."""

    @staticmethod
    def validate_required_text(value, field_name):
        """Validate and normalize required text."""
        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} is required.")

        return value

    @staticmethod
    def validate_date(value, field_name):
        """Validate and normalize a date."""
        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} is required.")

        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f"{field_name} must be a valid date in YYYY-MM-DD format."
            ) from None

        return value

    @staticmethod
    def validate_number_of_rounds(value):
        """Validate the number of rounds."""
        if value in ("", None):
            return 4

        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Number of rounds must be a positive integer.") from None

        if value <= 0:
            raise ValueError("Number of rounds must be a positive integer.")

        return value

    @staticmethod
    def create_match(player_one, player_two):
        """Validate and create a match."""
        if player_one.national_id == player_two.national_id:
            raise ValueError("A match must contain two different players.")

        return Match(player_one, player_two)

    @staticmethod
    def validate_result(score_one, score_two):
        """Validate and normalize a match result."""
        try:
            score_one = float(str(score_one).replace(",", "."))
            score_two = float(str(score_two).replace(",", "."))
        except ValueError:
            raise ValueError("Scores must be numbers.") from None

        if (score_one, score_two) not in ((1, 0), (0, 1), (0.5, 0.5)):
            raise ValueError("Valid results are 1-0, 0-1 or 0.5-0.5.")

        return score_one, score_two

    def create_tournament(
        self,
        name,
        location,
        start_date,
        end_date,
        description="",
        number_of_rounds=4,
    ):
        """Validate and create a tournament."""
        name = self.validate_required_text(name, "Tournament name")
        location = self.validate_required_text(location, "Location")
        start_date = self.validate_date(start_date, "Start date")
        end_date = self.validate_date(end_date, "End date")
        number_of_rounds = self.validate_number_of_rounds(number_of_rounds)

        if date.fromisoformat(end_date) < date.fromisoformat(start_date):
            raise ValueError("End date cannot be earlier than start date.")

        filename = f"{name}.json"

        if filename in self.list_tournament_files():
            raise ValueError("A tournament with this name already exists.")

        tournament = Tournament(
            name,
            location,
            start_date,
            end_date,
            description,
            number_of_rounds,
        )
        save_tournament(tournament, filename)
        return tournament

    def list_tournament_files(self):
        """List saved tournament files."""
        if not TOURNAMENTS_FOLDER.exists():
            return []

        return sorted(
            path.name
            for path in TOURNAMENTS_FOLDER.iterdir()
            if path.is_file() and path.suffix == ".json"
        )

    def list_saved_tournaments(self):
        """Load all saved tournaments for reports."""
        return [
            load_tournament(filename)
            for filename in self.list_tournament_files()
        ]

    def load_tournament(self, filename):
        """Load a tournament."""
        return load_tournament(filename)

    def list_tournament_players(self, tournament):
        """List tournament players in alphabetical order."""
        return sorted(
            tournament.players,
            key=lambda player: (
                player.last_name.lower(),
                player.first_name.lower(),
            ),
        )

    def can_add_player(self, tournament):
        """Check if players can still be added to a tournament."""
        return tournament.current_round == 0

    def add_player(self, tournament, player):
        """Validate and add a player to a tournament."""
        if not self.can_add_player(tournament):
            raise ValueError(
                "Players cannot be added after the first round has started."
            )

        for existing_player in tournament.players:
            if existing_player.national_id == player.national_id:
                raise ValueError("This player is already registered in the tournament.")

        tournament.add_player(player)
        save_tournament(tournament, f"{tournament.name}.json")

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

    def get_ranking_with_scores(self, tournament):
        """Return the ranking with each player's score."""
        return [
            (player, self.get_player_score(tournament, player))
            for player in self.get_ranking(tournament)
        ]

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
            match = self.create_match(player_one, player_two)
            round_.add_match(match)

        save_tournament(tournament, f"{tournament.name}.json")
        return round_.matches

    def record_result(self, tournament, match, score_one, score_two):
        """Validate and record a match result."""
        score_one, score_two = self.validate_result(score_one, score_two)
        match.set_result(score_one, score_two)
        save_tournament(tournament, f"{tournament.name}.json")

    def close_round(self, tournament, round_):
        """Validate and close a round."""
        if round_.end_datetime is not None:
            raise ValueError("This round is already closed.")

        if not self.is_round_complete(round_):
            raise ValueError("Enter all match results before closing the round.")

        round_.close()
        save_tournament(tournament, f"{tournament.name}.json")
