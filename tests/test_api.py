import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from app import app


def test_health_check():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_teams():
    client = app.test_client()
    response = client.get("/teams")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_matches():
    client = app.test_client()
    response = client.get("/matches")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
