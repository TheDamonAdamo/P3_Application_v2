from models.club_manager import ClubManager

class TournamentReportScreen:

        def __init__(self, tournament):
            self.tournament = tournament

        def show(self):
            print("\n=== Tournament Report ===\n")
            print(f"Name: {self.tournament.name}")
            print(f"Venue: {self.tournament.venue}")
            print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
            print(f"Rounds: {self.tournament.number_of_rounds}")

            # Load players with club info
            manager = ClubManager()
            for club in manager.clubs:
                print(f"Loaded club: {club.name} with {len(club.players)} players")
            all_players = [
                (player, club.name)
                for club in manager.clubs
                for player in club.players
            ]

            def get_player_info(chess_id):
                for p, c in all_players:
                    if p.chess_id == chess_id:
                        return p.name, chess_id, c
                return "Unknown", chess_id, "Unknown Club"

            # Display player list
            print("\nPlayers:")
            for i, chess_id in enumerate(self.tournament.players, start=1):
                name, cid, club = get_player_info(chess_id)
                print(f"  {i}. {name} - {cid} - {club}")

            # Calculate and display final rankings
            if self.tournament.completed:
                points = {pid: 0 for pid in self.tournament.players}
                for round_ in self.tournament.rounds:
                    for match in round_:
                        p1, p2 = match["players"]
                        winner = match.get("winner")
                        completed = match.get("completed")
                        if not completed:
                            continue
                        if winner is None:
                            points[p1] += 0.5
                            points[p2] += 0.5
                        else:
                            points[winner] += 1.0

                print("\nFinal Rankings:")
                sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
                for rank, (cid, pts) in enumerate(sorted_points, start=1):
                    name, _, _ = get_player_info(cid)
                    print(f"  {rank}. {name} ({cid}) - {pts} pts")

            # Round-by-round match details
            print("\nMatch Results:")
            for i, round_ in enumerate(self.tournament.rounds, start=1):
                print(f"\n--- Round {i} ---")
                for j, match in enumerate(round_.matches, start=1):
                    p1, p2 = match.players
                    winner = match.winner
                    completed = match.completed

                    name1, _, _ = get_player_info(p1)
                    name2, _, _ = get_player_info(p2)

                    print(f"  Match {j}: {name1} vs. {name2}", end=" | Result: ")
                    if not completed:
                        print("In Progress")
                    elif winner is None:
                        print("Tie")
                    else:
                        win_name, _, _ = get_player_info(winner)
                        print(f"{win_name} - Winner")
