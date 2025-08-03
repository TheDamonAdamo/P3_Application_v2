from dataclasses import dataclass
from typing import List
from models.match import Match


@dataclass
class Round:
    matches: List[Match]
    round_number: int

    def to_dict(self):
        return [match.to_dict() for match in self.matches]

    @staticmethod
    def from_dict(match_list, round_number):
        matches = [Match.from_dict(m) for m in match_list]
        return Round(matches=matches, round_number=round_number)

    def is_completed(self):
        return all(match.completed for match in self.matches)
