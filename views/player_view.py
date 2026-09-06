from views.console_screen import ConsoleScreen


class PlayerView:
    """Display player-related information."""

    MENU_LINES = [
        "1. Add a player",
        "2. List players",
        "3. Search a player",
        "4. Edit a player",
        "5. Delete a player",
        "0. Back",
    ]

    def __init__(self):
        """Initialize the player output area."""
        self.output_lines = []
        self.screen_active = False

    def display_menu(self):
        """Display the player menu and current output."""
        self.screen_active = True
        ConsoleScreen.render(
            "ChessFlow > Players",
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
        """Store player lines for the screen or display them directly."""
        if self.screen_active:
            self.output_lines = [title, "", *lines]
            return

        print(f"\n=== {title} ===")
        for line in lines:
            print(line)

    def get_player_data(self):
        """Get player data from the user."""
        print("\nAdd a player")
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
            self.set_output("Player", ["Player not found."])
            return

        self.set_output(
            "Player",
            [
                (
                    f"{player.last_name} {player.first_name} - "
                    f"{player.birth_date} - {player.national_id}"
                )
            ],
        )

    def display_players(self, players):
        """Display a list of players."""
        if not players:
            self.set_output("Players", ["No players registered."])
            return

        lines = [
            (
                f"{player.last_name} {player.first_name} - "
                f"{player.birth_date} - {player.national_id}"
            )
            for player in players
        ]
        self.set_output("Players", lines)
