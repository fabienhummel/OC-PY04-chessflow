class ReportView:
    """Display application reports."""

    def display_menu(self):
        """Display the reports menu."""
        print("\n=== Reports ===")
        print("1. List all players")
        print("2. List all tournaments")
        print("3. Tournament details")
        print("4. Tournament players")
        print("5. Tournament rounds and matches")
        print("6. Tournament ranking")
        print("0. Back")

    def get_choice(self):
        """Get the user choice."""
        return input("Choose an option: ")

    def display_players(self, players):
        """Display players."""
        print("\n=== Players report ===")

        if not players:
            print("No players registered.")
            return

        for player in players:
            print(
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )

    def display_tournaments(self, tournaments):
        """Display tournaments."""
        print("\n=== Tournaments report ===")

        if not tournaments:
            print("No tournaments registered.")
            return

        for tournament in tournaments:
            print(
                f"{tournament.name} - {tournament.location} - "
                f"{tournament.start_date} to {tournament.end_date}"
            )

    def display_tournament_details(self, tournament):
        """Display tournament details."""
        print("\n=== Tournament details ===")
        print(f"Name: {tournament.name}")
        print(f"Location: {tournament.location}")
        print(f"Start date: {tournament.start_date}")
        print(f"End date: {tournament.end_date}")
        print(f"Description: {tournament.description}")
        print(f"Number of rounds: {tournament.number_of_rounds}")
        print(f"Current round: {tournament.current_round}")

    def display_tournament_players(self, tournament_name, players):
        """Display players registered in a tournament."""
        print(f"\n=== {tournament_name} players ===")

        if not players:
            print("No players registered.")
            return

        for player in players:
            print(
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )

    def display_rounds(self, rounds):
        """Display tournament rounds and matches."""
        print("\n=== Rounds report ===")

        if not rounds:
            print("No rounds registered.")
            return

        for round_ in rounds:
            print(f"\n{round_.name}")
            print(f"Start: {round_.start_datetime}")
            print(f"End: {round_.end_datetime}")

            for match in round_.matches:
                print(
                    f"{match.player_one.last_name} {match.player_one.first_name} "
                    f"({match.score_one}) - "
                    f"{match.player_two.last_name} {match.player_two.first_name} "
                    f"({match.score_two})"
                )

    def display_ranking(self, ranking):
        """Display a tournament ranking."""
        print("\n=== Tournament ranking ===")

        if not ranking:
            print("No players registered.")
            return

        for position, item in enumerate(ranking, start=1):
            player, score = item
            print(
                f"{position}. {player.last_name} {player.first_name} "
                f"- {score} points"
            )
