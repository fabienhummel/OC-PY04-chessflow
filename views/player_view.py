class PlayerView:
    """Display player-related information."""

    def get_player_data(self):
        """Get player data from the user."""
        print("\n=== Add a player ===")
        last_name = input("Last name: ")
        first_name = input("First name: ")
        birth_date = input("Birth date (YYYY-MM-DD): ")
        national_id = input("National chess ID: ")

        return last_name, first_name, birth_date, national_id

    def display_players(self, players):
        """Display a list of players."""
        print("\n=== Players ===")

        if not players:
            print("No players registered.")
            return

        for player in players:
            print(
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )
