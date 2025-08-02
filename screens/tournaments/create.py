class CreateTournamentScreen:
    def show(self):
        print("\n=== Create a New Tournament ===")
        name = input("Enter tournament name: ")
        venue = input("Enter venue: ")
        start = input("Start date (DD-MM-YYYY): ")
        end = input("End date (DD-MM-YYYY): ")
        rounds = int(input("Number of rounds: "))
        return {
            "name": name,
            "venue": venue,
            "start": start,
            "end": end,
            "rounds": rounds
        }
