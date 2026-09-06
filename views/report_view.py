from views.console_screen import ConsoleScreen


class ReportView:
    """Display application reports."""

    MENU_LINES = [
        "1. List all players",
        "2. List all tournaments",
        "3. Tournament details",
        "4. Tournament players",
        "5. Tournament rounds and matches",
        "6. Tournament ranking",
        "0. Back",
    ]

    def __init__(self):
        """Initialize the report output area."""
        self.output_lines = []
        self.screen_active = False

    def display_menu(self):
        """Display the reports menu and current output."""
        self.screen_active = True
        ConsoleScreen.render(
            "ChessFlow > Reports",
            self.MENU_LINES,
            self.output_lines,
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
        """Store report lines for the screen or display them directly."""
        if self.screen_active:
            self.output_lines = [title, "", *lines]
            return

        print(f"\n=== {title} ===")
        for line in lines:
            print(line)

    def display_players(self, players):
        """Display players."""
        if not players:
            self.set_output("Players report", ["No players registered."])
            return

        lines = [
            (
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )
            for player in players
        ]
        self.set_output("Players report", lines)

    def display_tournaments(self, tournaments):
        """Display tournaments."""
        if not tournaments:
            self.set_output("Tournaments report", ["No tournaments registered."])
            return

        lines = [
            (
                f"{tournament.name} - {tournament.location} - "
                f"{tournament.start_date} to {tournament.end_date}"
            )
            for tournament in tournaments
        ]
        self.set_output("Tournaments report", lines)

    def display_tournament_details(self, tournament):
        """Display tournament details."""
        lines = [
            f"Name: {tournament.name}",
            f"Location: {tournament.location}",
            f"Start date: {tournament.start_date}",
            f"End date: {tournament.end_date}",
            f"Description: {tournament.description}",
            f"Number of rounds: {tournament.number_of_rounds}",
            f"Current round: {tournament.current_round}",
        ]
        self.set_output("Tournament details", lines)

    def display_tournament_players(self, tournament_name, players):
        """Display players registered in a tournament."""
        if not players:
            self.set_output(
                f"{tournament_name} players",
                ["No players registered."],
            )
            return

        lines = [
            (
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )
            for player in players
        ]
        self.set_output(f"{tournament_name} players", lines)

    def display_rounds(self, rounds):
        """Display tournament rounds and matches."""
        if not rounds:
            self.set_output("Rounds report", ["No rounds registered."])
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

        self.set_output("Rounds report", lines)

    def display_ranking(self, ranking):
        """Display a tournament ranking."""
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
