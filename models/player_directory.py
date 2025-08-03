from models.club_manager import ClubManager


class PlayerDirectory:
    def __init__(self):
        self.directory = {}  # chess_id → (Player, club_name)
        self.build_directory()

    def build_directory(self):
        manager = ClubManager()
        for club in manager.clubs:
            club_name = club.name
            for player in club.players:
                if player.chess_id not in self.directory:
                    self.directory[player.chess_id] = (player, club_name)
                else:
                    print(f"[WARN] Duplicate chess_id detected: {player.chess_id}")

    def get(self, chess_id):
        return self.directory.get(chess_id, (None, "Unknown Club"))

    def get_player_info(self, chess_id):
        player, club = self.get(chess_id)
        if player:
            return (player.name, player.chess_id, club)
        else:
            return ("Unknown", chess_id, club)

    def all(self):
        return self.directory.values()
