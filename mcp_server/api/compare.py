from flask import Blueprint, jsonify, request
from services.fetcher import get_pokemon_data
from services.parser import parse_compare_query
import logging

compare_bp = Blueprint("compare", __name__, url_prefix="/api/compare")

@compare_bp.route("/pokemon", methods=["POST"])
def compare_two_pokemon():
    """
    Compare two Pokémon and return a natural language sentence.
    Expects:
        - JSON: {"pokemon1": "pikachu", "pokemon2": "charmander"}
        - or JSON: {"query": "Compare Pikachu with Charmander"}
    """
    data = request.get_json()
    
    pokemon1_name = None
    pokemon2_name = None

    if "query" in data:
        parsed_names = parse_compare_query(data["query"])
        if parsed_names:
            pokemon1_name, pokemon2_name = parsed_names
    else:
        pokemon1_name = data.get("pokemon1")
        pokemon2_name = data.get("pokemon2")

    if not pokemon1_name or not pokemon2_name:
        return jsonify({"error": "Please provide two Pokémon names for comparison"}), 400

    logging.info(f"Comparing: {pokemon1_name} vs {pokemon2_name}")

    poke1_data = get_pokemon_data(pokemon1_name)
    poke2_data = get_pokemon_data(pokemon2_name)

    if not poke1_data:
        return jsonify({"error": f"Pokémon '{pokemon1_name}' not found"}), 404
    if not poke2_data:
        return jsonify({"error": f"Pokémon '{pokemon2_name}' not found"}), 404

    def extract_relevant_info(pokemon_data):
        stats = {s["stat"]["name"].replace("-", " ").title(): s["base_stat"] for s in pokemon_data["stats"]}
        return {
            "name": pokemon_data["name"].capitalize(),
            "types": [t["type"]["name"].capitalize() for t in pokemon_data["types"]],
            "hp": stats.get("Hp", 0),
            "attack": stats.get("Attack", 0),
            "defense": stats.get("Defense", 0),
            "speed": stats.get("Speed", 0)
        }

    p1 = extract_relevant_info(poke1_data)
    p2 = extract_relevant_info(poke2_data)

    p1_types_str = " and ".join(p1["types"]) if p1["types"] else "no known"
    p1_num_types = len(p1["types"])

    p2_types_str = " and ".join(p2["types"]) if p2["types"] else "no known"
    p2_num_types = len(p2["types"])

    sentence = (
        f"{p1['name']} is a {p1_types_str} type Pokémon with {p1_num_types} type(s), "
        f"while {p2['name']} is a {p2_types_str} type Pokémon with {p2_num_types} type(s). "
        f"In terms of stats, {p1['name']} has {p1['hp']} HP, {p1['attack']} Attack, and {p1['speed']} Speed. "
        f"On the other hand, {p2['name']} has {p2['hp']} HP, {p2['attack']} Attack, and {p2['speed']} Speed."
    )

    return jsonify({"sentence": sentence})

