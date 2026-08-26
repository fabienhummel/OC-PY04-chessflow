from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController


class ApplicationController:
    """Control the main application flow."""

    def __init__(self):
        """Initialize the application controller."""
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()

    def run(self):
        """Run the application."""
        pass
