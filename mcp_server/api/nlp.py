from flask import Blueprint, request, jsonify
import requests
from services.parser import (
    parse_description,
    parse_compare_query,
    parse_strategy_query,
    parse_team_query,
    parse_pokemon_query,
    parse_type_query
)

nlp_bp = Blueprint("nlp", __name__, url_prefix="/api/nlp")

@nlp_bp.route("/process", methods=["POST"])
def process_nlp():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Missing 'query' in request"}), 400

    try:
        parsed = parse_description(query)
        actions = parsed.get("actions", [])

        # COMPARISON
        if "compare" in actions:
            payload = parse_compare_query(query)
            if payload:
                response = requests.post("http://localhost:5000/api/compare/pokemon", json=payload)
                return jsonify(response.json()), response.status_code
            return jsonify({"error": "Need two Pokémon to compare"}), 400

        # STRATEGY
        # --- STRATEGY ---
        # STRATEGY
        if "strategy" in actions:
            payload = parse_strategy_query(query)
            if payload:
                response = requests.post("http://localhost:5000/api/strategy/type-matchup", json=payload)
                return jsonify(response.json()), response.status_code
            return jsonify({"error": "Need Pokémon name or type"}), 400


# --- TYPE INFO / ANALYSIS ---
        if "analysis" in actions or "type" in actions:
            payload = parse_type_query(query)
            if payload:
                response = requests.post("http://localhost:5000/api/type/", json=payload)
                return jsonify(response.json()), response.status_code
            return jsonify({"error": "Need type name for type info"}), 400


        # TEAM BUILDING
        if "team" in actions or "build" in actions:
            payload = parse_team_query(query)
            if payload:
                response = requests.post("http://localhost:5000/api/team/generate", json=payload)
                return jsonify(response.json()), response.status_code
            return jsonify({"error": "Invalid team generation query"}), 400

        # POKÉMON INFO
        if "info" in actions:
            payload = parse_pokemon_query(query)
            if payload:
                name = payload["pokemon_name"]
                response = requests.get(f"http://localhost:5000/api/pokemon/{name.lower()}")
                if response.status_code == 200:
                    return jsonify(response.json()), 200
                return jsonify({"error": "Pokémon not found or API error"}), 404
            return jsonify({"error": "Need Pokémon name"}), 400



        # DEFAULT FALLBACK
        return jsonify({"error": "Could not understand the intent"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
