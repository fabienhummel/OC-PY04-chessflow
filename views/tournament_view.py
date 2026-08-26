class TournamentView:
    """Display tournament-related information."""

    def display_menu(self):
        """Display the tournament menu."""
        print("\n=== Manage tournaments ===")
        print("1. Create a tournament")
        print("2. List saved tournaments")
        print("3. Load a tournament")
        print("4. Back")

    def display_loaded_menu(self):
        """Display the loaded tournament menu."""
        print("\n=== Loaded tournament ===")
        print("1. Display tournament")
        print("2. List tournament players")
        print("3. Add a player")
        print("4. List rounds")
        print("5. Create next round")
        print("6. Enter current round results")
        print("7. Close current round")
        print("8. Back")

    def get_choice(self):
        """Get the user choice."""
        return input("Choose an option: ")

    def get_tournament_data(self):
        """Get tournament data from the user."""
        print("\n=== Create a tournament ===")
        name = input("Name: ")
        location = input("Location: ")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        description = input("Description: ")
        number_of_rounds = input("Number of rounds (default 4): ")

        if number_of_rounds:
            number_of_rounds = int(number_of_rounds)
        else:
            number_of_rounds = 4

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
            print("No tournament loaded.")
            return

        print("\n=== Tournament ===")
        print(f"Name: {tournament.name}")
        print(f"Location: {tournament.location}")
        print(f"Start date: {tournament.start_date}")
        print(f"End date: {tournament.end_date}")
        print(f"Description: {tournament.description}")
        print(f"Rounds: {tournament.current_round}/{tournament.number_of_rounds}")
        print(f"Players: {len(tournament.players)}")

    def display_tournament_files(self, filenames):
        """Display saved tournament files."""
        print("\n=== Saved tournaments ===")

        if not filenames:
            print("No saved tournaments.")
            return

        for filename in filenames:
            print(filename)

    def get_filename(self):
        """Get a tournament filename."""
        return input("Tournament filename: ")

    def get_player_national_id(self):
        """Get a player national ID."""
        return input("Player national chess ID: ")

    def get_match_result(self, match):
        """Get a match result from the user."""
        print(
            f"\n{match.player_one.first_name} {match.player_one.last_name} "
            f"vs {match.player_two.first_name} {match.player_two.last_name}"
        )
        score_one = float(input("Score player 1: "))
        score_two = float(input("Score player 2: "))

        return score_one, score_two
