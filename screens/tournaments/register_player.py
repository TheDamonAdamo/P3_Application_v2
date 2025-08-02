class RegisterPlayerScreen:
    def __init__(self, tournament, all_players):
        self.tournament = tournament
        self.all_players = all_players

    def show(self):
        print("\n=== Register a Player ===")
        query = input("Enter name or chess ID: ").lower()
        matches = [p for p in self.all_players if query in p.chess_id.lower() or query in p.name.lower()]
        for idx, p in enumerate(matches):
            print(f"[{idx}] {p.chess_id} - {p.name}")
        choice = int(input("Select a player to register (number): "))
        selected = matches[choice]
        if selected.chess_id not in self.tournament.players:
            self.tournament.players.append(selected.chess_id)
            print(f"Player {selected.name} registered.")
        else:
            print("Player already registered.")