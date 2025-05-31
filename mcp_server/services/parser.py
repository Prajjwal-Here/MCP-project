import re

def parse_description(text):
    text = text.lower()

    types = []
    roles = []
    actions = []
    pokemon = []

    type_keywords = [
        "fire", "water", "grass", "electric", "psychic", "ice",
        "dragon", "fairy", "fighting", "flying", "ghost", "ground",
        "rock", "steel", "bug", "dark", "poison", "normal"
    ]
    
    role_keywords = {
        "tank": "defensive",
        "defense": "defensive",
        "attacker": "offensive",
        "sweeper": "offensive",
        "support": "support",
        "fast": "speed",
        "speed": "speed"
    }

    # 🛠️ Extended with extra keywords that users might naturally use
    action_keywords = [
    "compare", "team", "build", "strategy", "info", "analysis", "type",
    "details", "counter", "generate", "suggest", "recommend", "show", "help",
    "versus", "vs", "weakness", "resistance", "strong", "against","counter"
    ]

    stop_words = {
    "a", "an", "the", "and", "or", "but", "if", "while", "with", "to", "for", "from", "of", "on", "in", "at", "by", "about",
    "as", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "can", "could",
    "will", "would", "shall", "should", "may", "might", "must", "this", "that", "these", "those", "there", "here",
    "then", "than", "so", "because", "since", "just", "also", "too", "very", "more", "most", "some", "any", "each",
    "every", "all", "no", "not", "nor", "only", "own", "same", "such", "again", "further", "yet", "ever", "even", 
    "though", "although", "before", "after", "once", "when", "where", "why", "how", "tell", "me", "give", "show", 
    "want", "need", "get", "see", "say", "ask", "like", "look", "use", "make", "help", "know", "think", "let", "go",
    "into", "out", "up", "down", "over", "under", "off", "around", "through", "between", "during", "without", "within","I", "what"
    }



    for word in type_keywords:
        if word in text:
            types.append(word)

    for key, value in role_keywords.items():
        if key in text:
            roles.append(value)

    for word in action_keywords:
        if word in text:
            actions.append(word)

    possible_names = re.findall(r"\b[a-zA-Z]{3,}\b", text)
    for name in possible_names:
        if (
            name not in type_keywords
            and name not in role_keywords
            and name not in action_keywords
            and name not in stop_words
        ):
            pokemon.append(name)

    return {
        "types": list(set(types)),
        "roles": list(set(roles)),
        "actions": list(set(actions)),
        "pokemon": list(set(pokemon))
    }

# --- Compare ---
def parse_compare_query(query):
    parsed = parse_description(query)
    names = parsed["pokemon"]
    if len(names) >= 2:
        return {
            "pokemon1": names[0].capitalize(),
            "pokemon2": names[1].capitalize()
        }
    return None

# --- Team ---
def parse_team_query(query):
    parsed = parse_description(query)
    return {
        "preferred_types": [t.capitalize() for t in parsed["types"]],
        "avoid_duplicates": True
    }

# --- Info ---
def parse_pokemon_query(query):
    match = re.search(r"info about (\w+)", query.lower())
    if match:
        return {"pokemon_name": match.group(1).capitalize()}
    return None

def parse_strategy_query(query):
    parsed = parse_description(query)
    print("DEBUG - Parsed result:", parsed)  # <--- Add this

    if parsed["pokemon"]:
        return {"pokemon_name": parsed["pokemon"][0].capitalize()}

    if parsed["types"]:
        return {"type_name": parsed["types"][0].capitalize()}
    return None

# --- Type Analysis ---
def parse_type_query(query):
    parsed = parse_description(query)
    if parsed["types"]:
        return {"type_name": parsed["types"][0].capitalize()}
    return None
