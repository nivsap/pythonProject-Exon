import requests
import pytest
import random
#we can use logging.basicConfig(level=logging.INFO)

BASE_URL = "https://pokeapi.co/api/v2/"


def test_get_pokemon_types_success():
    try:
        response = requests.get(BASE_URL + "type")
        assert response.status_code == 200
        return response.json()["results"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve pokemon types: {e}")


def test_get_pokemon_types_no_data():
    try:
        response = requests.get(BASE_URL + "type/non_existent_type")
        assert response.status_code == 404
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve pokemon types: {e}")


def test_get_pokemon_types_server_error():
    try:
        response = requests.get(BASE_URL + "non_existent_endpoint")
        assert response.status_code == 404
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve pokemon types: {e}")


def get_pokemon_name(pokemon_id):
    try:
        pokemon_response = requests.get(BASE_URL + f"pokemon/{pokemon_id}")
        return pokemon_response.json()["name"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve pokemon name: {e}")


def get_pokemon_name_match(pokemon_id):
    try:
        pokemon_name = get_pokemon_name(pokemon_id)
        types = test_get_pokemon_types_success()

        for type_info in types:
            type_name = type_info["name"]
            pokemon_with_type_response = requests.get(BASE_URL + f"type/{type_name}")
            pokemon_with_type = pokemon_with_type_response.json()["pokemon"]

            for pokemon in pokemon_with_type:
                if pokemon["pokemon"]["name"] == pokemon_name:
                    return type_name
        print(f"No! No type found for Pokemon with ID {pokemon_id}")
        pytest.fail(f"No type found for Pokemon with ID {pokemon_id}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve pokemon type: {e}")


def test_get_pokemon_name_match():
    try:
#bonus
        pokemon_ids = random.sample(range(1, 899), 10)
        for pokemon_id in pokemon_ids:
            pokemon_type = get_pokemon_name_match(pokemon_id)
            assert pokemon_type is not None, f"Yes! type found for Pokemon with ID {pokemon_id}"
            print(f"Yes! type found for Pokemon with ID {pokemon_id}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve pokemon type: {e}")
