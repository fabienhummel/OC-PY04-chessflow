import os


class ConsoleScreen:
    """Render a simple two-zone console screen."""

    WIDTH = 72
    context_lines = []

    @classmethod
    def clear(cls):
        """Clear the current terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def separator(cls, character="-"):
        """Return a full-width separator line."""
        return character * cls.WIDTH

    @classmethod
    def set_context(cls, lines=None):
        """Set the global application context displayed on every screen."""
        cls.context_lines = list(lines or [])

    @classmethod
    def render(cls, title, menu_lines, output_lines=None):
        """Render the menu zone and the output zone."""
        cls.clear()
        print(cls.separator("="))
        print(title)

        for line in cls.context_lines:
            print(line)

        print(cls.separator("="))

        for line in menu_lines:
            print(line)

        print(cls.separator())
        print("OUTPUT")
        print(cls.separator())

        for line in output_lines or []:
            print(line)

        print(cls.separator("="))
