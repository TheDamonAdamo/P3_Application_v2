from models.player_directory import PlayerDirectory

class EnterResultsScreen:
    def __init__(self, tournament):
        self.tournament = tournament

    def show(self):
        directory = PlayerDirectory()
        round_ = self.tournament.rounds[self.tournament.current_round - 1]

        print(f"\n=== Enter Results for Round {self.tournament.current_round} ===")

        for i, match in enumerate(round_.matches, start=1):
            if match.completed:
                continue  # Skip already completed matches

            p1, _ = directory.get(match.player1_id)
            p2, _ = directory.get(match.player2_id)

            name1 = f"{p1.name} ({p1.chess_id})" if p1 else match.player1_id
            name2 = f"{p2.name} ({p2.chess_id})" if p2 else match.player2_id

            print(f"\nMatch {i}: {name1} vs {name2}")
            print("1. " + name1)
            print("2. " + name2)
            print("3. Tie")
            print("4. Skip (match still in progress)")

            while True:
                choice = input("Enter result: ").strip()
                if choice == "1":
                    match.winner = match.player1_id
                    match.completed = True
                    break
                elif choice == "2":
                    match.winner = match.player2_id
                    match.completed = True
                    break
                elif choice == "3":
                    match.winner = None
                    match.completed = True
                    break
                elif choice == "4":
                    print("Match left in progress.")
                    break
                else:
                    print("Invalid input. Choose 1–4.")
