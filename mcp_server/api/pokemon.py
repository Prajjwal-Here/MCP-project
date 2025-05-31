from flask import Blueprint, jsonify, request
from services.fetcher import get_pokemon_data
from services.parser import parse_pokemon_query
import logging

pokemon_bp = Blueprint("pokemon", __name__, url_prefix="/api/pokemon")

@pokemon_bp.route("/<string:pokemon_name>", methods=["GET"])
def get_pokemon_info(pokemon_name):
    logging.info(f"Fetching info for Pokémon: {pokemon_name}")
    return _get_pokemon_response(pokemon_name)

@pokemon_bp.route("", methods=["POST"])
def get_pokemon_info_from_query():
    """
    Expects JSON: { "query": "Tell me about Pikachu" }
    """
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"response": "Missing query input."}), 400
    
    pokemon_name = parse_pokemon_query(data["query"])
    if not pokemon_name:
        return jsonify({"response": "Could not parse Pokémon name from query."}), 400

    logging.info(f"NLP request - Pokémon info: {pokemon_name}")
    return _get_pokemon_response(pokemon_name)

def _get_pokemon_response(pokemon_name):
    data = get_pokemon_data(pokemon_name)
    if data:
        name = data.get("name", "Unknown").capitalize()
        height = data.get("height", 0)
        weight = data.get("weight", 0)
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        abilities = [a["ability"]["name"].replace('-', ' ').title() for a in data["abilities"]]
        stats = {s["stat"]["name"].replace('-', ' ').title(): s["base_stat"] for s in data["stats"]}

        response = (
            f"Here's what I found about {name}:\n\n"
            f"• Type: {' and '.join(types)}\n"
            f"• Height: {height} decimetres, Weight: {weight} hectograms\n"
            f"• Abilities: {', '.join(abilities)}\n"
            f"• Base Stats:\n"
            f"   - HP: {stats.get('Hp', 'N/A')}\n"
            f"   - Attack: {stats.get('Attack', 'N/A')}\n"
            f"   - Defense: {stats.get('Defense', 'N/A')}\n"
            f"   - Special Attack: {stats.get('Special Attack', 'N/A')}\n"
            f"   - Special Defense: {stats.get('Special Defense', 'N/A')}\n"
            f"   - Speed: {stats.get('Speed', 'N/A')}"
        )
        return jsonify({"response": response})
    
    return jsonify({"response": "Pokémon not found or API error."}), 404
