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
        print("6. Enter or edit round results")
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

    def display_round_choices(self, rounds):
        """Display rounds that can be selected."""
        print("\n=== Select a round ===")

        for index, round_ in enumerate(rounds, start=1):
            print(f"{index}. {round_.name}")

        print("0. Back")

    def get_round_choice(self):
        """Get the round to edit."""
        return input("Choose a round: ")

    def display_matches(self, round_):
        """Display the matches of a round."""
        print(f"\n=== {round_.name} matches ===")

        for index, match in enumerate(round_.matches, start=1):
            print(
                f"{index}. {match.player_one.last_name} "
                f"{match.player_one.first_name} ({match.score_one}) - "
                f"{match.player_two.last_name} "
                f"{match.player_two.first_name} ({match.score_two})"
            )

        print("0. Back")

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

        while True:
            score_one = input("Score player 1: ").replace(",", ".")
            score_two = input("Score player 2: ").replace(",", ".")

            try:
                score_one = float(score_one)
                score_two = float(score_two)
            except ValueError:
                print("Invalid score.")
                continue

            if (score_one, score_two) in ((1, 0), (0, 1), (0.5, 0.5)):
                return score_one, score_two

            print("Valid results are 1-0, 0-1 or 0.5-0.5.")
