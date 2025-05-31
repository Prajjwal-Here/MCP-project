from flask import Blueprint, jsonify, request
from services.fetcher import get_type_data
from services.parser import parse_type_query  # NEW IMPORT
import logging

type_bp = Blueprint("type_info", __name__, url_prefix="/api/type")

@type_bp.route("/", methods=["POST"])
def get_type_info_by_query():
    """
    Fetch Pokémon type info using a query.
    Accepts JSON: {"type_name": "fire"} OR {"query": "What is fire weak against?"}
    """
    data = request.get_json()
    type_name = data.get("type_name")
    query = data.get("query")

    if query:
        logging.info(f"Parsing type info query: {query}")
        parsed = parse_type_query(query)
        if not parsed:
            return jsonify({"error": "Could not understand query"}), 400
        type_name = parsed.get("type_name")

    if not type_name:
        return jsonify({"error": "No type specified"}), 400

    logging.info(f"Fetching info for Type: {type_name}")
    data = get_type_data(type_name)
    
    if data:
        damage_relations = data.get("damage_relations", {})
        simplified_data = {
            "name": data.get("name").capitalize(),
            "double_damage_from": [t["name"].capitalize() for t in damage_relations.get("double_damage_from", [])],
            "double_damage_to": [t["name"].capitalize() for t in damage_relations.get("double_damage_to", [])],
            "half_damage_from": [t["name"].capitalize() for t in damage_relations.get("half_damage_from", [])],
            "half_damage_to": [t["name"].capitalize() for t in damage_relations.get("half_damage_to", [])],
            "no_damage_from": [t["name"].capitalize() for t in damage_relations.get("no_damage_from", [])],
            "no_damage_to": [t["name"].capitalize() for t in damage_relations.get("no_damage_to", [])]
        }
        return jsonify(simplified_data)
    
    return jsonify({"error": "Type not found or API error"}), 404
