from views.console_screen import ConsoleScreen


class MainMenuView:
    """Display the main menu."""

    MENU_LINES = [
        "1. Manage players",
        "2. Manage tournaments",
        "3. Reports",
        "0. Quit",
    ]

    def __init__(self):
        """Initialize the main menu output area."""
        self.output_lines = []

    def display_menu(self):
        """Display the main menu."""
        ConsoleScreen.render(
            "ChessFlow",
            self.MENU_LINES,
            self.output_lines,
        )

    def get_choice(self):
        """Get the user choice."""
        return input("Choose an option: ")

    def display_message(self, message, title="Message"):
        """Display a message in the main menu output area."""
        self.output_lines = [title, "", message]
