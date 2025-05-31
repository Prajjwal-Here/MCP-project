from flask import Blueprint, jsonify, request
from services.fetcher import get_pokemon_data, get_type_data
from services.parser import parse_strategy_query  # NEW IMPORT
import logging

strategy_bp = Blueprint("strategy", __name__, url_prefix="/api/strategy")

@strategy_bp.route("/type-matchup", methods=["POST"])
def get_type_matchup_strategy():
    """
    Suggest counters based on Pokémon or type name.
    Accepts:
      - JSON: {"pokemon_name": "charizard"} or {"type_name": "fire"}
      - OR:   {"query": "How do I counter Charizard?"}
    """
    data = request.get_json()
    pokemon_name = data.get("pokemon_name")
    type_name = data.get("type_name")
    query = data.get("query")

    if query:
        # NLP mode
        logging.info(f"NLP strategy query: {query}")
        parsed = parse_strategy_query(query)
        if not parsed:
            return jsonify({"error": "Could not parse query"}), 400
        if parsed.get("pokemon_name"):
            pokemon_name = parsed["pokemon_name"]
        elif parsed.get("type_name"):
            type_name = parsed["type_name"]

    if not pokemon_name and not type_name:
        return jsonify({"error": "Provide either a Pokémon, type name, or natural language query"}), 400

    target_types = []
    if pokemon_name:
        logging.info(f"Getting type matchup for Pokémon: {pokemon_name}")
        poke_data = get_pokemon_data(pokemon_name)
        if not poke_data:
            return jsonify({"error": "Pokémon not found"}), 404
        target_types = [t["type"]["name"] for t in poke_data["types"]]
    elif type_name:
        logging.info(f"Getting type matchup for Type: {type_name}")
        target_types = [type_name.lower()]

    weaknesses = set()
    resistances = set()
    immunities = set()

    for t in target_types:
        type_info = get_type_data(t)
        if type_info:
            dmg = type_info["damage_relations"]
            weaknesses.update([i["name"].capitalize() for i in dmg.get("double_damage_from", [])])
            resistances.update([i["name"].capitalize() for i in dmg.get("half_damage_from", [])])
            immunities.update([i["name"].capitalize() for i in dmg.get("no_damage_from", [])])

    result = {
        "target": pokemon_name.capitalize() if pokemon_name else type_name.capitalize(),
        "types": [t.capitalize() for t in target_types],
        "weak_to": sorted(list(weaknesses)),
        "resists": sorted(list(resistances)),
        "immune_to": sorted(list(immunities)),
        "suggested_counter_types": sorted(list(weaknesses))
    }

    return jsonify(result)
