"""Manage JSON data for players and tournaments."""

import json
from pathlib import Path

from models.player import Player
from models.tournament import Tournament


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
PLAYERS_FILE = DATA_FOLDER / "players.json"
TOURNAMENTS_FOLDER = DATA_FOLDER / "tournaments"


def load_players():
    """Load all players."""
    if not PLAYERS_FILE.exists():
        return []

    if PLAYERS_FILE.stat().st_size == 0:
        raise ValueError("The players JSON file is empty.")

    try:
        with PLAYERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("The players JSON file contains invalid JSON.") from None

    if not isinstance(data, list):
        raise ValueError("The players JSON file must contain a list.")

    try:
        return [Player.from_dict(player) for player in data]
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"The players JSON data is invalid: {error}") from None


def save_players(players):
    """Save all players."""
    data = [player.to_dict() for player in players]
    PLAYERS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with PLAYERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def list_tournament_files():
    """List saved tournament files."""
    if not TOURNAMENTS_FOLDER.exists():
        return []

    return sorted(
        path.name
        for path in TOURNAMENTS_FOLDER.iterdir()
        if path.is_file() and path.suffix == ".json"
    )


def load_tournament(filename):
    """Load one tournament."""
    path = TOURNAMENTS_FOLDER / filename

    if not path.exists():
        raise ValueError(f"Tournament file not found: {filename}")

    if path.stat().st_size == 0:
        raise ValueError(f"Tournament file is empty: {filename}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"Tournament file contains invalid JSON: {filename}") from None

    if not isinstance(data, dict):
        raise ValueError(f"Tournament JSON data is invalid: {filename}")

    try:
        return Tournament.from_dict(data)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            f"Tournament JSON data is invalid in {filename}: {error}"
        ) from None


def save_tournament(tournament, filename):
    """Save one tournament."""
    TOURNAMENTS_FOLDER.mkdir(parents=True, exist_ok=True)
    path = TOURNAMENTS_FOLDER / filename

    with path.open("w", encoding="utf-8") as file:
        json.dump(tournament.to_dict(), file, indent=4, ensure_ascii=False)


def delete_tournament(filename):
    """Delete one tournament file."""
    path = TOURNAMENTS_FOLDER / filename

    if path.exists():
        path.unlink()
