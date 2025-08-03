from dataclasses import dataclass
from typing import Optional


@dataclass
class Match:
    player1_id: str
    player2_id: str
    winner: Optional[str] = None  # None = draw
    completed: bool = False

    def to_dict(self):
        return {
            "players": [self.player1_id, self.player2_id],
            "winner": self.winner,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Match(
            player1_id=data["players"][0],
            player2_id=data["players"][1],
            winner=data.get("winner"),
            completed=data.get("completed", False)
        )

    def get_points(self):
        if not self.completed:
            return {self.player1_id: 0, self.player2_id: 0}
        if self.winner is None:
            return {self.player1_id: 0.5, self.player2_id: 0.5}
        return {
            self.winner: 1,
            self.player1_id if self.winner != self.player1_id else self.player2_id: 0
        }
