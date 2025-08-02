from commands.tournaments import load_all_tournaments, get_tournament_by_id, advance_round
from commands.create_tournaments import create_tournament, save_tournament
from screens.tournaments.create import CreateTournamentScreen
from screens.tournaments.view import ViewTournamentScreen
from screens.tournaments.register_player import RegisterPlayerScreen
from screens.tournaments.enter_results import EnterResultsScreen
from screens.tournaments.advance_round import AdvanceRoundScreen
from screens.tournaments.report import TournamentReportScreen

from models.player import Player
from screens import clubs  # use clubs.py from screens package


def load_all_players():
    all_players = []
    club_data = clubs.load_clubs()
    for club in club_data:
        for p in club["players"]:
            player = Player(
                name=p["name"],
                email=p["email"],
                chess_id=p["chess_id"],
                birthdate=p["birthdate"]
            )
            all_players.append(player)
    return all_players

def tournament_menu(tournament, all_players):
    while True:
        ViewTournamentScreen(tournament).show()
        print("\nActions:")
        print("1. Register Player")
        print("2. Enter Match Results")
        print("3. Advance to Next Round")
        print("4. Generate Report")
        print("5. Save & Return to Main Menu")
        choice = input("Select action: ")

        if choice == "1":
            RegisterPlayerScreen(tournament, all_players).show()
        elif choice == "2":
            EnterResultsScreen(tournament).show()
        elif choice == "3":
            if AdvanceRoundScreen(tournament).show():
                advance_round(tournament)
        elif choice == "4":
            TournamentReportScreen(tournament).show()
        elif choice == "5":
            save_tournament(tournament)
            break
        else:
            print("Invalid choice.")

def main():
    print("=== Chess Tournament Manager ===")
    tournaments = load_all_tournaments()
    all_players = load_all_players()

    if len(tournaments) == 1 and not tournaments[0].completed:
        tournament_menu(tournaments[0], all_players)
        return

    while True:
        print("\nTournaments:")
        for i, t in enumerate(sorted(tournaments, key=lambda t: t.start_date, reverse=True)):
            print(f"[{i}] {t.name} ({t.start_date} - {t.end_date})")
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
            selected = get_tournament_by_id(tournaments, tid)
            if selected:
                tournament_menu(selected, all_players)
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
