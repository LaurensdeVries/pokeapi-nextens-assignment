from TestClasses.BasePokeAPIClass import BasePokeAPIClass

import requests
import logging
import random
import unittest

class PokemonTests(BasePokeAPIClass):
    TEST_POKEMON = "pikachu"

    def test_get_hardcoded_pokemon_returns_200_status_code(self):
        response = requests.get(f"{self.BASE_URL}/pokemon/pikachu")
        self.assertEqual(response.status_code, 200)
        self._check_response_headers(response)

    def test_get_parameterized_pokemon_returns_200_status_code(self, pokemon_name=TEST_POKEMON):
        response = requests.get(f"{self.BASE_URL}/pokemon/{pokemon_name}")
        self.assertEqual(response.status_code, 200)
        self._check_response_headers(response)
        
    def test_get_nonexistent_pokemon_returns_404(self):
        response = requests.get(f"{self.BASE_URL}/pokemon/charifart")
        self.assertEqual(response.status_code, 404, "Expected status code 404 for fake pokemon")
        self._check_response_headers(response)

    def test_get_pokemon_and_verify_existence_of_abilities_and_cries(self):
        response = requests.get(f"{self.BASE_URL}/pokemon/{self.TEST_POKEMON}")
        self.assertIn('abilities', response.json())
        self.assertIn('cries', response.json())
        ability_array = (response.json().get('abilities'))
        latest_cry = (response.json().get('cries')["latest"])
        logging.info(f"Ability array: {ability_array}")
        logging.info(f"Latest cry: {latest_cry}")

    @unittest.skip("Skipping this test because auth is not actually supported")
    def test_get_pokemon_with_auth_returns_401(self):
        headers = {"Authorization": f"Basic {self.AUTH_TOKEN}"}
        response = requests.get(
            f"{self.BASE_URL}/pokemon/{self.TEST_POKEMON}",
            headers=headers
        )
        self.assertEqual(response.status_code, 401)
        self._check_response_headers(response)

    @unittest.skip("Skipping this test because /NewPokemon is not actually supported")
    def test_post_create_pokemon_and_verify_success(self):
        response = requests.post(f"{self.BASE_URL}/NewPokemon", 
                               json={"name": "Laurenvris", 
                                   "id": 9000, 
                                   "abilities": [
                                       {"1": {"ability": "waterbolt x3", 
                                             "url": f"https://pokeapi.co/api/v2/ability/{random.randint(9000, 9010)}/"}}, 
                                       {"3": {"ability": "freeze", 
                                             "url": f"https://pokeapi.co/api/v2/ability/{random.randint(10000, 10010)}/"}}
                                   ]})
        self.assertEqual(response.status_code, 200)
        response_2 = self.test_get_parameterized_pokemon_returns_200_status_code(pokemon_name="Laurenvris")
        self.assertEqual(response_2.status_code, 200)