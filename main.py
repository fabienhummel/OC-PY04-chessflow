"""ChessFlow application entry point."""

from controllers.application_controller import ApplicationController


def main():
    """Start the ChessFlow application."""
    application = ApplicationController()
    application.run()


if __name__ == "__main__":
    main()
