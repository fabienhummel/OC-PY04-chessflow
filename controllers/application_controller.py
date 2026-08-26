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
        self.current_tournament = None

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
        """Manage tournaments."""
        while True:
            self.tournament_view.display_menu()
            choice = self.tournament_view.get_choice()

            if choice == "1":
                tournament_data = self.tournament_view.get_tournament_data()
                self.current_tournament = (
                    self.tournament_controller.create_tournament(*tournament_data)
                )
                self.tournament_view.display_tournament(self.current_tournament)

            elif choice == "2":
                filenames = self.tournament_controller.list_tournament_files()
                self.tournament_view.display_tournament_files(filenames)

            elif choice == "3":
                filenames = self.tournament_controller.list_tournament_files()
                self.tournament_view.display_tournament_files(filenames)

                if not filenames:
                    continue

                filename = self.tournament_view.get_filename()

                if filename not in filenames:
                    print("Tournament not found.")
                    continue

                self.current_tournament = (
                    self.tournament_controller.load_tournament(filename)
                )
                self.tournament_view.display_tournament(self.current_tournament)

            elif choice == "4":
                self.tournament_view.display_tournament(self.current_tournament)

            elif choice == "5":
                if self.current_tournament is None:
                    print("No tournament loaded.")
                    continue

                national_id = self.tournament_view.get_player_national_id()
                player = self.player_controller.find_player(national_id)

                if player is None:
                    print("Player not found.")
                    continue

                self.tournament_controller.add_player(
                    self.current_tournament,
                    player,
                )
                print("Player added to tournament.")

            elif choice == "6":
                if self.current_tournament is None:
                    print("No tournament loaded.")
                    continue

                if self.current_tournament.current_round >= (
                    self.current_tournament.number_of_rounds
                ):
                    print("All rounds have already been created.")
                    continue

                players = self.current_tournament.players

                if len(players) == 0:
                    print("Add players before creating a round.")
                    continue

                if len(players) % 2 != 0:
                    print("The tournament must have an even number of players.")
                    continue

                round_ = self.tournament_controller.create_round(
                    self.current_tournament
                )
                self.tournament_controller.create_matches(
                    self.current_tournament,
                    round_,
                )
                print(f"{round_.name} created.")

            elif choice == "7":
                if self.current_tournament is None:
                    print("No tournament loaded.")
                    continue

                if not self.current_tournament.rounds:
                    print("No round available.")
                    continue

                round_ = self.current_tournament.rounds[-1]

                for match in round_.matches:
                    score_one, score_two = self.tournament_view.get_match_result(
                        match
                    )
                    self.tournament_controller.record_result(
                        self.current_tournament,
                        match,
                        score_one,
                        score_two,
                    )

            elif choice == "8":
                if self.current_tournament is None:
                    print("No tournament loaded.")
                    continue

                if not self.current_tournament.rounds:
                    print("No round available.")
                    continue

                round_ = self.current_tournament.rounds[-1]
                self.tournament_controller.close_round(
                    self.current_tournament,
                    round_,
                )
                print(f"{round_.name} closed.")

            elif choice == "9":
                break

            else:
                print("Invalid choice.")

    def display_reports(self):
        """Display players and tournaments reports."""
        players = self.player_controller.list_players()
        tournaments = self.tournament_controller.tournaments
        self.report_view.display_players(players)
        self.report_view.display_tournaments(tournaments)
