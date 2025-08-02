from dataclasses import dataclass, field
from typing import List, Optional
from models.round import Round
import json

@dataclass
class Tournament:
    name: str
    venue: str
    start_date: str
    end_date: str
    number_of_rounds: int
    players: List[str] = field(default_factory=list)
    current_round: Optional[int] = None
    completed: bool = False
    rounds: List[Round] = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "venue": self.venue,
            "dates": {
                "from": self.start_date,
                "to": self.end_date
            },
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": self.players,
            "rounds": [round_.to_dict() for round_ in self.rounds]
        }

    @staticmethod
    def from_dict(data):
        rounds = [Round.from_dict(r, i + 1) for i, r in enumerate(data.get("rounds", []))]
        return Tournament(
            name=data["name"],
            venue=data["venue"],
            start_date=data["dates"]["from"],
            end_date=data["dates"]["to"],
            number_of_rounds=data["number_of_rounds"],
            current_round=data.get("current_round"),
            completed=data.get("completed", False),
            players=data.get("players", []),
            rounds=rounds
        )

    def get_scores(self):
        scores = {pid: 0 for pid in self.players}
        for round_ in self.rounds:
            for match in round_.matches:
                for pid, pts in match.get_points().items():
                    scores[pid] += pts
        return scores
