class ViewTournamentScreen:
    def __init__(self, tournament):
        self.tournament = tournament

    def show(self):
        print("\n=== Tournament Information ===")
        print(f"Name: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Total Rounds: {self.tournament.number_of_rounds}")
        print(f"Current Round: {self.tournament.current_round or 'None'}")
        print("Registered Players:")
        for pid in self.tournament.players:
            print(f" - {pid}")