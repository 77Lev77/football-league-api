import json
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEAMS_FILE = DATA_DIR / "teams.json"
MATCHES_FILE = DATA_DIR / "matches.json"


def read_json(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, data: List[Dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def next_id(items: List[Dict[str, Any]]) -> int:
    if not items:
        return 1
    return max(int(item.get("id", 0)) for item in items) + 1


def get_teams() -> List[Dict[str, Any]]:
    return read_json(TEAMS_FILE)


def save_teams(teams: List[Dict[str, Any]]) -> None:
    write_json(TEAMS_FILE, teams)


def get_matches() -> List[Dict[str, Any]]:
    return read_json(MATCHES_FILE)


def save_matches(matches: List[Dict[str, Any]]) -> None:
    write_json(MATCHES_FILE, matches)


def find_by_id(items: List[Dict[str, Any]], item_id: int) -> Optional[Dict[str, Any]]:
    for item in items:
        if int(item.get("id", 0)) == item_id:
            return item
    return None


def delete_by_id(items: List[Dict[str, Any]], item_id: int) -> bool:
    initial_length = len(items)
    items[:] = [item for item in items if int(item.get("id", 0)) != item_id]
    return len(items) != initial_length
