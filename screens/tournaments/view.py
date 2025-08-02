from models.player_directory import PlayerDirectory

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

        directory = PlayerDirectory()

        print("Registered Players:")
        print(f"   {'Chess ID':<10} {'Name':<25} {'Club'}")
        print("-" * 60)
        for i, pid in enumerate(self.tournament.players, start=1):
            player, club = directory.get(pid)
            name = player.name if player else "Unknown"
            club_name = club if club else "Unknown Club"
            print(f"   {pid:<10} {name:<25} {club_name}")