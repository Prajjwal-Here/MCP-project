import requests
import logging

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

def fetch_from_pokeapi(endpoint):
    """Fetches data from the Open Pokémon API."""
    url = f"{POKEAPI_BASE_URL}{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"[PokeAPI ERROR] Failed to fetch {url}: {e}")
        return None

def get_pokemon_data(pokemon_name):
    return fetch_from_pokeapi(f"pokemon/{pokemon_name.lower()}")

def get_type_data(type_name):
    return fetch_from_pokeapi(f"type/{type_name.lower()}")

def get_ability_data(ability_name):
    return fetch_from_pokeapi(f"ability/{ability_name.lower()}")

def get_all_pokemon():
    """Returns a list of all Pokémon (limited to 1000)."""
    url = f"{POKEAPI_BASE_URL}pokemon?limit=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching all Pokémon: {e}")
        return []
