from views.console_screen import ConsoleScreen


class MainMenuView:
    """Display the main menu."""

    MENU_LINES = [
        "1. Manage players",
        "2. Manage tournaments",
        "3. Reports",
        "0. Quit",
    ]

    def display_menu(self):
        """Display the main menu."""
        ConsoleScreen.render(
            "ChessFlow",
            self.MENU_LINES,
        )

    def get_choice(self):
        """Get the user choice."""
        return input("Choose an option: ")
