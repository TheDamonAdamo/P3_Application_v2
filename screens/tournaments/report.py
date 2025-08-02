class TournamentReportScreen:
    def __init__(self, tournament):
        self.tournament = tournament

    def show(self):
        print("\n=== Tournament Report ===")
        print(f"Tournament: {self.tournament.name}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        scores = self.tournament.get_scores()
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print("\nPlayer Rankings:")
        for pid, pts in sorted_scores:
            print(f"{pid}: {pts} points")
        print("\nAll Rounds:")
        for i, r in enumerate(self.tournament.rounds):
            print(f"\nRound {i+1}:")
            for m in r.matches:
                result = m.winner if m.winner else "Draw"
                print(f"{m.player1_id} vs {m.player2_id} → {result}")
