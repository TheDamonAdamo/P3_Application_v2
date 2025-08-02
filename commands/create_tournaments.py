import os
import json
from models.tournament import Tournament

def create_tournament(name, venue, start, end, rounds):
    tournament = Tournament(
        name=name,
        venue=venue,
        start_date=start,
        end_date=end,
        number_of_rounds=rounds,
        players=[],
        current_round=None,
        completed=False,
        rounds=[]
    )
    save_tournament(tournament)
    return tournament

def save_tournament(tournament):
    path = get_tournament_path(tournament.name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tournament.to_dict(), f, indent=4)

def get_tournament_path(name):
    safe_name = name.replace(" ", "_").lower()
    return os.path.join("data", "tournaments", f"{safe_name}.json")
