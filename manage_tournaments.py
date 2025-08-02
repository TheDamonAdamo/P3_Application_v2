# manage_tournament.py
from commands.tournaments import load_all_tournaments, get_tournament_by_id, advance_round
from commands.create_tournaments import create_tournament, save_tournament
from screens.tournaments.create import CreateTournamentScreen
from screens.tournaments.view import ViewTournamentScreen
from screens.tournaments.register_player import RegisterPlayerScreen
from screens.tournaments.enter_results import EnterResultsScreen
from screens.tournaments.advance_round import AdvanceRoundScreen
from screens.tournaments.report3 import TournamentReportScreen

from models.club_manager import ClubManager


def load_all_players():
    manager = ClubManager()
    all_players = []
    for club in manager.clubs:
        for p in club.players:
            all_players.append(p)
    return all_players


def tournament_menu(tournament, all_players):
    while True:
        ViewTournamentScreen(tournament).show()
        is_completed = tournament.completed
        print("\nActions:")
        if not is_completed and tournament.current_round is None:
            print("1. Register Player")
        if not is_completed:
            print("2. Enter Match Results")
        if not is_completed:
            print("3. Advance to Next Round")
        print("4. Generate Report")
        if not is_completed:
            print("S. Save & Return to Main Menu")
        print("B. Return to Main Menu (without saving)")
        choice = input("Select action: ").strip().lower()

        if choice == "1" and not tournament.completed and tournament.current_round is None:
            RegisterPlayerScreen(tournament, all_players).show()
        elif choice == "2" and not tournament.completed:
            EnterResultsScreen(tournament).show()
        elif choice == "3" and not tournament.completed:
            if AdvanceRoundScreen(tournament).show():
                advance_round(tournament)
        elif choice == "4":
            TournamentReportScreen(tournament).show()
        elif choice == "s":
            save_tournament(tournament)
            break
        elif choice == "b":
            print("Returning to main menu without saving...")
            break
        else:
            print("Invalid choice.")


def main():
    print("=== Chess Tournament Manager ===")
    tournaments = load_all_tournaments()
    all_players = load_all_players()

    while True:
        print("\nTournaments:")
        in_progress = sorted([t for t in tournaments if not t.completed], key=lambda t: t.start_date, reverse=True)
        completed = sorted([t for t in tournaments if t.completed], key=lambda t: t.start_date, reverse=True)
        sorted_tournaments = in_progress + completed
        for i, t in enumerate(sorted_tournaments, start=1):
            status = "In Progress" if not t.completed else "Completed"
            print(f"[{i}] {t.name} ({t.start_date} - {t.end_date}) [{status}]")
        print("[N] New Tournament")
        print("[Q] Quit")

        choice = input("Select a tournament or action: ").strip().lower()

        if choice == "q":
            break
        elif choice == "n":
            form = CreateTournamentScreen().show()
            new_tournament = create_tournament(
                name=form["name"],
                venue=form["venue"],
                start=form["start"],
                end=form["end"],
                rounds=form["rounds"]
            )
            tournament_menu(new_tournament, all_players)
        elif choice.isdigit():
            tid = int(choice)
            selected = get_tournament_by_id(sorted_tournaments, tid - 1)
            if selected:
                tournament_menu(selected, all_players)
        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()
