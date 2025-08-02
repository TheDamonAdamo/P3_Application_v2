class AdvanceRoundScreen:
    def __init__(self, tournament):
        self.tournament = tournament

    def show(self):
        print("\n=== Advance to Next Round ===")
        confirm = input("Advance to next round? (y/n): ")
        if confirm.lower() == 'y':
            print("Generating new round...")
            return True
        return False