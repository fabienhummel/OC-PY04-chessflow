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
        """Manage players."""
        while True:
            self.player_view.display_menu()
            choice = self.player_view.get_choice()

            if choice == "1":
                player_data = self.player_view.get_player_data()
                self.player_controller.create_player(*player_data)
            elif choice == "2":
                players = self.player_controller.list_players()
                self.player_view.display_players(players)
            elif choice == "3":
                national_id = self.player_view.get_national_id()
                player = self.player_controller.find_player(national_id)
                self.player_view.display_player(player)
            elif choice == "4":
                national_id = self.player_view.get_national_id()
                player = self.player_controller.find_player(national_id)

                if player is None:
                    self.player_view.display_player(player)
                    continue

                player_data = self.player_view.get_updated_player_data(player)
                self.player_controller.update_player(player, *player_data)
                self.player_view.display_player(player)
            elif choice == "5":
                national_id = self.player_view.get_national_id()
                player = self.player_controller.find_player(national_id)

                if player is None:
                    self.player_view.display_player(player)
                    continue

                self.player_controller.delete_player(player)
                print("Player deleted.")
            elif choice == "6":
                break
            else:
                print("Invalid choice.")

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
