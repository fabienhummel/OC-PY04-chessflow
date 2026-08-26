"""Manage JSON data for players and tournaments."""

import json
import os

from models.player import Player
from models.tournament import Tournament


PLAYERS_FILE = "data/players.json"
TOURNAMENTS_FOLDER = "data/tournaments"


def load_players():
    """Load all players."""
    if not os.path.exists(PLAYERS_FILE):
        return []

    with open(PLAYERS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Player.from_dict(player) for player in data]


def save_players(players):
    """Save all players."""
    data = [player.to_dict() for player in players]

    with open(PLAYERS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_tournament(filename):
    """Load one tournament."""
    path = os.path.join(TOURNAMENTS_FOLDER, filename)

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return Tournament.from_dict(data)


def save_tournament(tournament, filename):
    """Save one tournament."""
    os.makedirs(TOURNAMENTS_FOLDER, exist_ok=True)
    path = os.path.join(TOURNAMENTS_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(tournament.to_dict(), file, indent=4, ensure_ascii=False)


def delete_tournament(filename):
    """Delete one tournament file."""
    path = os.path.join(TOURNAMENTS_FOLDER, filename)

    if os.path.exists(path):
        os.remove(path)
