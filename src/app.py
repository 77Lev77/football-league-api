from flask import Flask, jsonify, request
from storage import (
    delete_by_id,
    find_by_id,
    get_matches,
    get_teams,
    next_id,
    save_matches,
    save_teams,
)

app = Flask(__name__)

VALID_STATUSES = {"scheduled", "live", "finished", "cancelled"}


@app.get("/")
def index():
    return jsonify({
        "service": "Football League API",
        "description": "REST API-сервис для учета футбольных команд и матчей",
        "framework": "Flask",
        "docs": {
            "teams": "/teams",
            "matches": "/matches",
            "health": "/health"
        }
    })


@app.get("/health")
def health_check():
    return jsonify({"status": "ok", "message": "Football League API is running"})


@app.get("/teams")
def list_teams():
    city = request.args.get("city", "").strip().lower()
    teams = get_teams()
    if city:
        teams = [team for team in teams if city in team.get("city", "").lower()]
    return jsonify(teams)


@app.get("/teams/<int:team_id>")
def get_team(team_id: int):
    team = find_by_id(get_teams(), team_id)
    if team is None:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team)


@app.post("/teams")
def create_team():
    payload = request.get_json(silent=True) or {}
    required_fields = ["name", "city", "coach", "founded", "stadium"]
    missing = [field for field in required_fields if field not in payload]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    teams = get_teams()
    team = {
        "id": next_id(teams),
        "name": str(payload["name"]),
        "city": str(payload["city"]),
        "coach": str(payload["coach"]),
        "founded": int(payload["founded"]),
        "stadium": str(payload["stadium"]),
    }
    teams.append(team)
    save_teams(teams)
    return jsonify(team), 201


@app.put("/teams/<int:team_id>")
def update_team(team_id: int):
    payload = request.get_json(silent=True) or {}
    teams = get_teams()
    team = find_by_id(teams, team_id)
    if team is None:
        return jsonify({"error": "Team not found"}), 404

    for field in ["name", "city", "coach", "stadium"]:
        if field in payload:
            team[field] = str(payload[field])
    if "founded" in payload:
        team["founded"] = int(payload["founded"])

    save_teams(teams)
    return jsonify(team)


@app.delete("/teams/<int:team_id>")
def delete_team(team_id: int):
    teams = get_teams()
    if not delete_by_id(teams, team_id):
        return jsonify({"error": "Team not found"}), 404
    save_teams(teams)
    return jsonify({"message": "Team deleted"})


@app.get("/matches")
def list_matches():
    status = request.args.get("status", "").strip().lower()
    team = request.args.get("team", "").strip().lower()
    matches = get_matches()

    if status:
        matches = [match for match in matches if match.get("status", "").lower() == status]
    if team:
        matches = [
            match for match in matches
            if team in match.get("home_team", "").lower() or team in match.get("away_team", "").lower()
        ]
    return jsonify(matches)


@app.get("/matches/<int:match_id>")
def get_match(match_id: int):
    match = find_by_id(get_matches(), match_id)
    if match is None:
        return jsonify({"error": "Match not found"}), 404
    return jsonify(match)


@app.get("/matches/team/<team_name>")
def matches_by_team(team_name: str):
    team_query = team_name.lower()
    matches = [
        match for match in get_matches()
        if team_query in match.get("home_team", "").lower()
        or team_query in match.get("away_team", "").lower()
    ]
    return jsonify(matches)


@app.get("/matches/status/<status>")
def matches_by_status(status: str):
    status_query = status.lower()
    matches = [match for match in get_matches() if match.get("status", "").lower() == status_query]
    return jsonify(matches)


@app.post("/matches")
def create_match():
    payload = request.get_json(silent=True) or {}
    required_fields = ["home_team", "away_team", "date", "stadium"]
    missing = [field for field in required_fields if field not in payload]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    status = str(payload.get("status", "scheduled")).lower()
    if status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status", "valid_statuses": sorted(VALID_STATUSES)}), 400

    matches = get_matches()
    match = {
        "id": next_id(matches),
        "home_team": str(payload["home_team"]),
        "away_team": str(payload["away_team"]),
        "date": str(payload["date"]),
        "stadium": str(payload["stadium"]),
        "status": status,
        "home_score": payload.get("home_score"),
        "away_score": payload.get("away_score"),
    }
    matches.append(match)
    save_matches(matches)
    return jsonify(match), 201


@app.put("/matches/<int:match_id>")
def update_match(match_id: int):
    payload = request.get_json(silent=True) or {}
    matches = get_matches()
    match = find_by_id(matches, match_id)
    if match is None:
        return jsonify({"error": "Match not found"}), 404

    for field in ["home_team", "away_team", "date", "stadium"]:
        if field in payload:
            match[field] = str(payload[field])
    if "status" in payload:
        status = str(payload["status"]).lower()
        if status not in VALID_STATUSES:
            return jsonify({"error": "Invalid status", "valid_statuses": sorted(VALID_STATUSES)}), 400
        match["status"] = status
    for field in ["home_score", "away_score"]:
        if field in payload:
            match[field] = payload[field]

    save_matches(matches)
    return jsonify(match)


@app.patch("/matches/<int:match_id>/score")
def update_score(match_id: int):
    payload = request.get_json(silent=True) or {}
    matches = get_matches()
    match = find_by_id(matches, match_id)
    if match is None:
        return jsonify({"error": "Match not found"}), 404

    if "home_score" not in payload or "away_score" not in payload:
        return jsonify({"error": "home_score and away_score are required"}), 400

    match["home_score"] = int(payload["home_score"])
    match["away_score"] = int(payload["away_score"])
    match["status"] = str(payload.get("status", "finished")).lower()
    save_matches(matches)
    return jsonify(match)


@app.delete("/matches/<int:match_id>")
def delete_match(match_id: int):
    matches = get_matches()
    if not delete_by_id(matches, match_id):
        return jsonify({"error": "Match not found"}), 404
    save_matches(matches)
    return jsonify({"message": "Match deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
