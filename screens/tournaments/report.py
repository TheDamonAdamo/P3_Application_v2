from models.club_manager import ClubManager
from models.player_directory import PlayerDirectory

class TournamentReportScreen:
    def __init__(self, tournament):
        self.tournament = tournament

    def show(self):
        print("\n" + "="*60)
        print(f"Tournament Report: {self.tournament.name}")
        print("="*60)
        print(f"Venue: {self.tournament.venue}")
        print(f"Date(s): {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Number of Rounds: {self.tournament.number_of_rounds}")

        directory = PlayerDirectory()

        # --- Players ---
        print("\nPlayers:")
        print(f"{'No.':<4} {'Name':<25} {'Chess ID':<10} {'Club'}")
        print("-" * 60)
        for i, chess_id in enumerate(self.tournament.players, start=1):
            player, club = directory.get(chess_id)
            name = player.name if player else chess_id
            club_name = club if club else "Unknown Club"
            print(f"{i:<4} {name:<25} {chess_id:<10} {club_name}")

        # --- Final Rankings ---
        final_points = {pid: 0 for pid in self.tournament.players}
        for round_ in self.tournament.rounds:
            for match in round_.matches:
                for pid, pts in match.get_points().items():
                    final_points[pid] += pts

        label = "Final Rankings" if self.tournament.completed else "Current Rankings"
        print(f"\n{label}:")
        print(f"{'Rank':<5} {'Name':<25} {'Points'}")
        print("-" * 40)
        sorted_final = sorted(final_points.items(), key=lambda x: x[1], reverse=True)
        for rank, (cid, pts) in enumerate(sorted_final, start=1):
            player, _ = directory.get(cid)
            name = player.name if player else cid
            print(f"{rank:<5} {name:<25} {pts}")

        # --- Match Results and Standings Per Round ---
        print("\nMatch Results:")

        for i, round_ in enumerate(self.tournament.rounds, start=1):
            print(f"\n--- Round {i} ---")
            round_points = {pid: 0 for pid in self.tournament.players}
            for j, match in enumerate(round_.matches, start=1):
                p1_id = match.player1_id
                p2_id = match.player2_id
                winner_id = match.winner
                completed = match.completed

                p1, _ = directory.get(p1_id)
                p2, _ = directory.get(p2_id)

                p1_name = p1.name if p1 else p1_id
                p2_name = p2.name if p2 else p2_id

                result = "In Progress"
                if completed:
                    if winner_id is None:
                        result = "Tie"
                    elif winner_id == p1_id:
                        result = f"Winner: {p1_name}"
                    elif winner_id == p2_id:
                        result = f"Winner: {p2_name}"

                print(f"  Match {j}: {p1_name} vs. {p2_name} → {result}")

                # Calculate round-specific points
                for pid, pts in match.get_points().items():
                    round_points[pid] += pts

            # Standings after this round only
            print("\nStandings after Round {0}:".format(i))
            sorted_round = sorted(round_points.items(), key=lambda x: x[1], reverse=True)
            print(f"{'Rank':<5} {'Name':<25} {'Points'}")
            print("-" * 40)
            for rank, (cid, pts) in enumerate(sorted_round, start=1):
                player, _ = directory.get(cid)
                name = player.name if player else cid
                print(f"{rank:<5} {name:<25} {pts}")
