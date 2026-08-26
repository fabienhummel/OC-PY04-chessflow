class MainMenuView:
    """Display the main menu."""

    def display_menu(self):
        """Display the main menu."""
        print("\n=== ChessFlow ===")
        print("1. Manage players")
        print("2. Manage tournaments")
        print("3. Reports")
        print("4. Quit")

    def get_choice(self):
        """Get the user choice."""
        return input("Choose an option: ")
