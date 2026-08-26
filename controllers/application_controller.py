from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.main_menu_view import MainMenuView
from views.player_view import PlayerView
from views.report_view import ReportView
from views.tournament_view import TournamentView


class ApplicationController:
    """Control the main application flow."""

    def __init__(self):
        """Initialize the application controller."""
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.main_menu_view = MainMenuView()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.report_view = ReportView()

    def run(self):
        """Run the application."""
        while True:
            self.main_menu_view.display_menu()
            choice = self.main_menu_view.get_choice()

            if choice == "1":
                self.manage_players()
            elif choice == "2":
                self.manage_tournaments()
            elif choice == "3":
                self.display_reports()
            elif choice == "4":
                print("Goodbye.")
                break
            else:
                print("Invalid choice.")

    def manage_players(self):
        """Create and display players."""
        player_data = self.player_view.get_player_data()
        self.player_controller.create_player(*player_data)
        players = self.player_controller.list_players()
        self.player_view.display_players(players)

    def manage_tournaments(self):
        """Create and display a tournament."""
        tournament_data = self.tournament_view.get_tournament_data()
        tournament = self.tournament_controller.create_tournament(*tournament_data)
        self.tournament_view.display_tournament(tournament)

    def display_reports(self):
        """Display players and tournaments reports."""
        players = self.player_controller.list_players()
        tournaments = self.tournament_controller.tournaments
        self.report_view.display_players(players)
        self.report_view.display_tournaments(tournaments)
