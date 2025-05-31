from flask import Blueprint, jsonify, request
from services.fetcher import get_pokemon_data, get_all_pokemon
from services.parser import parse_team_query
import random
import logging

team_bp = Blueprint("team", __name__, url_prefix="/api/team")

@team_bp.route("/generate", methods=["POST"])
def generate_team():
    """
    Generate a natural language description of a team of 6 Pokémon.
    Accepts:
      - {"preferred_types": ["fire", "water"], "avoid_duplicates": true}
      - OR: {"query": "Make a team with fire and water types"}
    """
    data = request.get_json()
    preferred_types = data.get("preferred_types", [])
    avoid_duplicates = data.get("avoid_duplicates", True)
    query = data.get("query")

    if query:
        logging.info(f"Parsing team generation query: {query}")
        parsed = parse_team_query(query)
        if not parsed:
            return jsonify({"response": "Sorry, I couldn't understand your team request."}), 400
        preferred_types = parsed.get("preferred_types", preferred_types)
        avoid_duplicates = parsed.get("avoid_duplicates", avoid_duplicates)

    all_pokemon = get_all_pokemon()
    if not all_pokemon:
        return jsonify({"response": "Failed to fetch Pokémon list. Please try again."}), 500

    selected_team = []
    used_types = set()
    attempts = 0
    max_attempts = 1000

    while len(selected_team) < 6 and attempts < max_attempts:
        attempts += 1
        poke_entry = random.choice(all_pokemon)
        poke_data = get_pokemon_data(poke_entry["name"])
        if not poke_data:
            continue

        poke_types = [t["type"]["name"] for t in poke_data["types"]]
        if avoid_duplicates and used_types.intersection(poke_types):
            continue
        if preferred_types and not any(pt in poke_types for pt in preferred_types):
            continue

        selected_team.append(poke_data)
        used_types.update(poke_types)

    if len(selected_team) < 6:
        return jsonify({"response": "I couldn't form a complete team. Try again with fewer constraints."}), 400

    # Build a natural language response
    response = "Here's your custom Pokémon team:\n\n"
    for i, poke in enumerate(selected_team, 1):
        name = poke.get("name", "Unknown").capitalize()
        height = poke.get("height", 0)
        weight = poke.get("weight", 0)
        types = [t["type"]["name"].capitalize() for t in poke.get("types", [])]
        abilities = [a["ability"]["name"].replace('-', ' ').title() for a in poke.get("abilities", [])]
        stats = {s["stat"]["name"].replace('-', ' ').title(): s["base_stat"] for s in poke.get("stats", [])}

        response += (
            f"{i}. {name}:\n"
            f"   - Type: {' and '.join(types)}\n"
            f"   - Height: {height} dm, Weight: {weight} hg\n"
            f"   - Abilities: {', '.join(abilities)}\n"
            f"   - Base Stats:\n"
            f"       • HP: {stats.get('Hp', 'N/A')}\n"
            f"       • Attack: {stats.get('Attack', 'N/A')}\n"
            f"       • Defense: {stats.get('Defense', 'N/A')}\n"
            f"       • Special Attack: {stats.get('Special Attack', 'N/A')}\n"
            f"       • Special Defense: {stats.get('Special Defense', 'N/A')}\n"
            f"       • Speed: {stats.get('Speed', 'N/A')}\n\n"
        )

    return jsonify({"response": response})
