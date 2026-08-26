class PlayerView:
    """Display player-related information."""

    def display_menu(self):
        """Display the player menu."""
        print("\n=== Manage players ===")
        print("1. Add a player")
        print("2. List players")
        print("3. Search a player")
        print("4. Edit a player")
        print("5. Delete a player")
        print("6. Back")

    def get_choice(self):
        """Get the user choice."""
        return input("Choose an option: ")

    def get_player_data(self):
        """Get player data from the user."""
        print("\n=== Add a player ===")
        last_name = input("Last name: ")
        first_name = input("First name: ")
        birth_date = input("Birth date (YYYY-MM-DD): ")
        national_id = input("National chess ID: ")

        return last_name, first_name, birth_date, national_id

    def get_national_id(self):
        """Get a national chess ID."""
        return input("National chess ID: ")

    def get_updated_player_data(self, player):
        """Get updated player data from the user."""
        print("\nPress Enter to keep the current value.")

        last_name = input(f"Last name [{player.last_name}]: ")
        first_name = input(f"First name [{player.first_name}]: ")
        birth_date = input(f"Birth date [{player.birth_date}]: ")
        national_id = input(f"National chess ID [{player.national_id}]: ")

        if not last_name:
            last_name = player.last_name
        if not first_name:
            first_name = player.first_name
        if not birth_date:
            birth_date = player.birth_date
        if not national_id:
            national_id = player.national_id

        return last_name, first_name, birth_date, national_id

    def display_player(self, player):
        """Display one player."""
        if player is None:
            print("Player not found.")
            return

        print(
            f"{player.last_name} {player.first_name} - "
            f"{player.birth_date} - {player.national_id}"
        )

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
