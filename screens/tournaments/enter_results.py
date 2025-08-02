class EnterResultsScreen:
    def __init__(self, tournament):
        self.tournament = tournament

    def show(self):
        print("\n=== Enter Match Results ===")
        if not self.tournament.rounds:
            print("No rounds available.")
            return
        round_ = self.tournament.rounds[-1]
        for i, match in enumerate(round_.matches):
            print(f"[{i}] {match.player1_id} vs {match.player2_id}")
            res = input("Enter result (1 = player1, 2 = player2, D = draw): ")
            if res == '1':
                match.winner = match.player1_id
            elif res == '2':
                match.winner = match.player2_id
            else:
                match.winner = None
            match.completed = True