import os
import json
import random
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from models.player_directory import PlayerDirectory

def load_all_tournaments():
    tournaments = []
    folder = os.path.join("data", "tournaments")
    if not os.path.exists(folder):
        return tournaments
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                tournaments.append(Tournament.from_dict(data))
    return tournaments

def get_tournament_by_id(tournaments, selection):
    if 0 <= selection < len(tournaments):
        return tournaments[selection]
    return None

def generate_next_round(tournament):
    scores = tournament.get_scores()
    sorted_players = sorted(tournament.players, key=lambda pid: (-scores.get(pid, 0), pid))
    random.shuffle(sorted_players)  # break ties randomly

    previous_pairs = set()
    for round_ in tournament.rounds:
        for match in round_.matches:
            pair = frozenset([match.player1_id, match.player2_id])
            previous_pairs.add(pair)

    matches = []
    while len(sorted_players) >= 2:
        p1 = sorted_players.pop(0)
        opponent = None
        for i, p2 in enumerate(sorted_players):
            if frozenset([p1, p2]) not in previous_pairs:
                opponent = sorted_players.pop(i)
                break
        if opponent is None:
            opponent = sorted_players.pop(0)
        matches.append(Match(player1_id=p1, player2_id=opponent))

    round_number = len(tournament.rounds) + 1
    new_round = Round(matches=matches, round_number=round_number)
    tournament.rounds.append(new_round)
    tournament.current_round = round_number

def enter_match_results(tournament, match_results):
    if not tournament.rounds:
        return
    current_round = tournament.rounds[-1]
    for i, result in enumerate(match_results):
        match = current_round.matches[i]
        if result == '1':
            match.winner = match.player1_id
        elif result == '2':
            match.winner = match.player2_id
        else:
            match.winner = None
        match.completed = True
"""
def advance_round(tournament):
    if tournament.current_round is not None:
        current = tournament.rounds[-1]
        if not current.is_completed():
            return False  # Cannot advance until current round is done
    if len(tournament.rounds) >= tournament.number_of_rounds:
        tournament.completed = True
        tournament.current_round = None
    else:
        generate_next_round(tournament)
    return True
"""
def advance_round(tournament):
    directory = PlayerDirectory()

    # Prevent advancing if current round has incomplete matches
    if tournament.rounds:
        last_round = tournament.rounds[-1]
        if any(not match.completed for match in last_round.matches):
            print("Cannot advance: not all matches in the current round are completed.")
            return

    if tournament.current_round is None:
        # --- First round: random pairing across clubs ---
        club_map = {}
        for pid in tournament.players:
            _, club = directory.get(pid)
            club_map.setdefault(club, []).append(pid)

        all_players = [(club, pid) for club, pids in club_map.items() for pid in pids]
        random.shuffle(all_players)
        matches = []
        used = set()

        while len(used) < len(tournament.players):
            for i in range(len(all_players)):
                if all_players[i][1] in used:
                    continue
                for j in range(i + 1, len(all_players)):
                    if all_players[j][1] in used:
                        continue
                    if all_players[i][0] != all_players[j][0]:
                        p1 = all_players[i][1]
                        p2 = all_players[j][1]
                        matches.append(Match(player1_id=p1, player2_id=p2))
                        used.update({p1, p2})
                        break
                break  # outer loop restart

        new_round = Round(matches=matches, round_number=1)
        tournament.rounds.append(new_round)
        tournament.current_round = 1

    else:
        # --- Later rounds: score-based Swiss pairing ---
        # Calculate current points
        points = {pid: 0 for pid in tournament.players}
        played_matches = set()

        for rnd in tournament.rounds:
            for match in rnd.matches:
                played_matches.add(frozenset([match.player1_id, match.player2_id]))
                for pid, pts in match.get_points().items():
                    points[pid] += pts

        # Sort by points (break ties randomly)
        players = list(tournament.players)
        random.shuffle(players)
        players.sort(key=lambda pid: points[pid], reverse=True)

        matches = []
        used = set()
        while players:
            p1 = players.pop(0)
            if p1 in used:
                continue

            for i, p2 in enumerate(players):
                if frozenset([p1, p2]) not in played_matches:
                    matches.append(Match(player1_id=p1, player2_id=p2))
                    used.update({p1, p2})
                    players.pop(i)
                    break

        new_round = Round(matches=matches, round_number=tournament.current_round + 1)
        tournament.rounds.append(new_round)
        tournament.current_round += 1

    if tournament.current_round >= tournament.number_of_rounds:
        tournament.completed = True
