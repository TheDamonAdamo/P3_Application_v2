# manage_tournament.py
from commands.tournaments import load_all_tournaments, get_tournament_by_id, advance_round
from commands.create_tournaments import create_tournament, save_tournament
from screens.tournaments.create import CreateTournamentScreen
from screens.tournaments.view import ViewTournamentScreen
from screens.tournaments.register_player import RegisterPlayerScreen
from screens.tournaments.enter_results import EnterResultsScreen
from screens.tournaments.advance_round import AdvanceRoundScreen
from screens.tournaments.report import (TournamentReportScreen)

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
        current_round = tournament.current_round
        num_players = len(tournament.players)
        min_players = 2

        print("\nActions:")

        # 1. Register Player
        print("1. Register Player", end="")
        if is_completed:
            print("  (Not available: tournament completed)")
        elif current_round:
            print("  (Not available: tournament already started)")
        else:
            print()

        # 2. Enter Match Results
        print("2. Enter Match Results", end="")
        if current_round is None:
            print("  (Not available: tournament not started)")
        elif is_completed:
            print("  (Not available: tournament completed)")
        else:
            last_round = tournament.rounds[-1]
            if all(match.completed for match in last_round.matches):
                print("  (Not available: all matches entered, select Advance to Next Round)")
            else:
                print()

        # 3. Start Tournament / Advance to Next Round
        if current_round is None:
            if num_players < min_players:
                status = "Start Tournament Not available: not enough players to start"
            else:
                status = "Start Tournament"
        elif is_completed or (current_round == tournament.number_of_rounds and all(match.completed for match in tournament.rounds[-1].matches)):
            status = "Advance to Next Round (Not available: tournament completed)"
        else:
            last_round = tournament.rounds[-1]
            if any(not match.completed for match in last_round.matches):
                status = "Advance to Next Round (Not available: current round not complete)"
            else:
                status = "Advance to Next Round"

        print(f"3. {status}")

        # 4. Generate Report
        print("4. Generate Report")

        # Save & return / back
        print("S. Save & Return to Main Menu")
        print("B. Return to Main Menu (without saving)")

        choice = input("Select action: ").strip().lower()

        if choice == "1":
            if not is_completed and not current_round:
                RegisterPlayerScreen(tournament, all_players).show()
            else:
                print("Cannot register players: tournament has started or is complete.")


        elif choice == "2":
            if current_round is not None and not is_completed:
                EnterResultsScreen(tournament).show()
                # Re-evaluate last round after entering results
                last_round = tournament.rounds[-1]
                if (
                        current_round == tournament.number_of_rounds and
                        all(match.completed for match in last_round.matches)
                ):
                    tournament.completed = True
            else:
                print("Cannot enter results: tournament not started or already completed.")

        elif choice == "3":
            if is_completed:
                print("Tournament already completed.")
            elif current_round is None and num_players >= min_players:
                if AdvanceRoundScreen(tournament).show():
                    advance_round(tournament)
            elif current_round is not None:
                last_round = tournament.rounds[-1]
                if any(not match.completed for match in last_round.matches):
                    print("Cannot advance: current round is not complete.")
                else:
                    if AdvanceRoundScreen(tournament).show():
                        advance_round(tournament)
                        # Recheck if the tournament is now complete
                        if tournament.current_round == tournament.number_of_rounds:
                            final_round = tournament.rounds[-1]
                            if all(match.completed for match in final_round.matches):
                                tournament.completed = True
            else:
                print("Cannot start tournament: not enough players.")

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
            if t.completed:
                status = "Completed"
            elif t.current_round is None:
                status = "Created"
            else:
                status = "In Progress"
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
