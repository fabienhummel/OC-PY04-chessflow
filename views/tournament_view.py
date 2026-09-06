from views.console_screen import ConsoleScreen


class TournamentView:
    """Display tournament-related information."""

    MENU_LINES = [
        "1. Create a tournament",
        "2. List saved tournaments",
        "3. Load a tournament",
        "0. Back",
    ]

    LOADED_MENU_LINES = [
        "1. Display tournament",
        "2. Manage tournament players",
        "3. Manage rounds",
        "4. Display ranking",
        "0. Back",
    ]

    PLAYERS_MENU_LINES = [
        "1. List tournament players",
        "2. Add a player",
        "3. Remove a player",
        "0. Back",
    ]

    ROUNDS_MENU_LINES = [
        "1. List rounds",
        "2. Create next round",
        "3. Enter or edit round results",
        "4. Close current round",
        "0. Back",
    ]

    def __init__(self):
        """Initialize the tournament output area."""
        self.output_lines = []
        self.screen_active = False
        self.current_title = None
        self.current_menu_lines = []

    def render_menu(self, title, menu_lines):
        """Render a tournament menu and its current output."""
        if self.current_title != title:
            self.output_lines = []

        self.current_title = title
        self.current_menu_lines = menu_lines
        self.screen_active = True
        self.render_current_screen()

    def render_current_screen(self):
        """Render the currently active tournament screen."""
        ConsoleScreen.render(
            self.current_title,
            self.current_menu_lines,
            self.output_lines,
        )

    def display_menu(self):
        """Display the tournament menu."""
        self.render_menu("ChessFlow > Tournaments", self.MENU_LINES)

    def display_loaded_menu(self):
        """Display the loaded tournament menu."""
        self.render_menu("ChessFlow > Tournament", self.LOADED_MENU_LINES)

    def display_players_menu(self):
        """Display the tournament players menu."""
        self.render_menu(
            "ChessFlow > Tournament > Players",
            self.PLAYERS_MENU_LINES,
        )

    def display_rounds_menu(self):
        """Display the tournament rounds menu."""
        self.render_menu(
            "ChessFlow > Tournament > Rounds",
            self.ROUNDS_MENU_LINES,
        )

    def get_choice(self):
        """Get the user choice."""
        choice = input("Choose an option: ")

        if choice == "0":
            self.output_lines = []
            self.screen_active = False
            ConsoleScreen.clear()

        return choice

    def set_output(self, title, lines):
        """Store tournament lines for the screen or display them directly."""
        if self.screen_active:
            self.output_lines = [title, "", *lines]
            self.render_current_screen()
            return

        print(f"\n=== {title} ===")
        for line in lines:
            print(line)

    def display_message(self, message, title="Message"):
        """Display a message in the current output area."""
        self.set_output(title, [message])

    def get_tournament_data(self):
        """Get tournament data from the user."""
        print("\nCreate a tournament")
        name = input("Name: ")
        location = input("Location: ")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        description = input("Description: ")
        number_of_rounds = input("Number of rounds (default 4): ")

        return (
            name,
            location,
            start_date,
            end_date,
            description,
            number_of_rounds,
        )

    def display_tournament(self, tournament):
        """Display a tournament."""
        if tournament is None:
            self.set_output("Tournament", ["No tournament loaded."])
            return

        lines = [
            f"Name: {tournament.name}",
            f"Location: {tournament.location}",
            f"Start date: {tournament.start_date}",
            f"End date: {tournament.end_date}",
            f"Description: {tournament.description}",
            f"Rounds: {tournament.current_round}/{tournament.number_of_rounds}",
            f"Players: {len(tournament.players)}",
        ]
        self.set_output("Tournament", lines)

    def display_tournament_files(self, filenames):
        """Display saved tournament files."""
        if not filenames:
            self.set_output("Saved tournaments", ["No saved tournaments."])
            return

        self.set_output("Saved tournaments", filenames)

    def display_players(self, players):
        """Display players registered in the loaded tournament."""
        if not players:
            self.set_output("Tournament players", ["No players registered."])
            return

        lines = [
            (
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )
            for player in players
        ]
        self.set_output("Tournament players", lines)

    def display_ranking(self, ranking):
        """Display the loaded tournament ranking in the current output area."""
        if not ranking:
            self.set_output("Tournament ranking", ["No players registered."])
            return

        lines = []

        for position, item in enumerate(ranking, start=1):
            player, score = item
            lines.append(
                f"{position}. {player.last_name} {player.first_name} "
                f"- {score} points"
            )

        self.set_output("Tournament ranking", lines)

    def get_filename(self):
        """Get a tournament filename."""
        return input("Tournament filename: ")

    def get_player_national_id(self):
        """Get a player national ID."""
        return input("Player national chess ID (AA12345): ")

    def display_rounds(self, rounds):
        """Display tournament rounds in the current output area."""
        if not rounds:
            self.set_output("Rounds", ["No rounds registered."])
            return

        lines = []

        for round_ in rounds:
            if lines:
                lines.append("")

            lines.extend(
                [
                    round_.name,
                    f"Start: {round_.start_datetime}",
                    f"End: {round_.end_datetime}",
                ]
            )

            for match in round_.matches:
                lines.append(
                    f"{match.player_one.last_name} {match.player_one.first_name} "
                    f"({match.score_one}) - "
                    f"{match.player_two.last_name} {match.player_two.first_name} "
                    f"({match.score_two})"
                )

        self.set_output("Rounds", lines)

    def display_round_choices(self, rounds):
        """Display rounds that can be selected."""
        lines = [
            f"{index}. {round_.name}"
            for index, round_ in enumerate(rounds, start=1)
        ]
        lines.append("0. Back")
        self.set_output("Select a round", lines)

    def get_round_choice(self):
        """Get the round to edit."""
        return input("Choose a round: ")

    def display_matches(self, round_, message=None):
        """Display the matches of a round."""
        lines = []

        if message:
            lines.extend([message, ""])

        for index, match in enumerate(round_.matches, start=1):
            lines.append(
                f"{index}. {match.player_one.last_name} "
                f"{match.player_one.first_name} ({match.score_one}) - "
                f"{match.player_two.last_name} "
                f"{match.player_two.first_name} ({match.score_two})"
            )

        lines.append("0. Back")
        self.set_output(f"{round_.name} matches", lines)

    def get_match_choice(self):
        """Get the match to edit."""
        return input("Choose a match: ")

    def get_match_result(self, match):
        """Get a match result from the user."""
        print(
            f"\n{match.player_one.first_name} {match.player_one.last_name} "
            f"vs {match.player_two.first_name} {match.player_two.last_name}"
        )
        print(f"Current result: {match.score_one} - {match.score_two}")
        score_one = input("Score player 1: ")
        score_two = input("Score player 2: ")
        return score_one, score_two
