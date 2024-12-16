import requests
import unittest
import random
import logging
import sys
from BerryTestClass import Berry
from BerryFirmnessTestClass import BerryFirmnessTest
from BerryFlavorTestClass import BerryFlavor

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

class PokeAPITests(unittest.TestCase):
    BASE_URL = "https://pokeapi.co/api/v2"
    AUTH_TOKEN = "auth_token_that_will_not_work"

    TEST_POKEMON = "pikachu"
    TEST_BERRY_ID = 2
    TEST_BERRY = "cheri"
    TEST_BERRY_FIRMNESS_ID = 5
    TEST_BERRY_FIRMNESS = "soft"
    TEST_BERRY_FLAVOR_ID = 1
    TEST_BERRY_FLAVOR = "spicy"

    @classmethod
    def setUpClass(self):
        """Check if PokeAPI is accessible before running any tests"""
        try:
            response = requests.get(self.BASE_URL)
            if response.status_code != 200:
                raise unittest.SkipTest(f"PokeAPI is not responding correctly: {response.status_code}")
        except requests.RequestException as e:
            raise unittest.SkipTest(f"Could not connect to PokeAPI: {str(e)}")

    def test_get_hardcoded_pokemon_returns_200_status_code(self):
        """Testing if GET request for a valid hardcoded Pokemon returns 200 status code"""
        response = requests.get(f"{self.BASE_URL}/pokemon/pikachu")
        self.assertEqual(response.status_code, 200)
        self._check_response_headers(response)

    def test_get_parameterized_pokemon_returns_200_status_code(self, pokemon_name=TEST_POKEMON):
        """Testing if GET request for a parameterized Pokemon returns 200 status code"""
        response = requests.get(f"{self.BASE_URL}/pokemon/{pokemon_name}")
        self.assertEqual(response.status_code, 200)
        self._check_response_headers(response)
        
    def test_get_nonexistent_pokemon_returns_404(self):
        """Testing if GET request for a nonexistent Pokemon returns 404 status code"""
        response = requests.get(f"{self.BASE_URL}/pokemon/charifart")
        self.assertEqual(response.status_code, 404, "Expected status code 404 for fake pokemon")
        self._check_response_headers(response)

    def test_get_pokemon_and_verify_existence_of_abilities_and_cries(self):
        """Testing if Pokemon API response contains all required headers with correct values"""
        response = requests.get(f"{self.BASE_URL}/pokemon/{self.TEST_POKEMON}")
        self.assertIn('abilities', response.json())
        self.assertIn('cries', response.json())
        ability_array = (response.json().get('abilities'))
        latest_cry = (response.json().get('cries')["latest"])

        logging.info(f"Ability array: {ability_array}")

        """While it has no actual name to each cry, it does give a URL to the soundfile"""
        logging.info(f"Latest cry: {latest_cry}")      

    #Berry tests
    def test_get_single_berry_by_name(self):
        response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY}")
        berry_data = response.json()
        self.assertEqual(berry_data['name'], self.TEST_BERRY, f"Expected berry name to be {self.TEST_BERRY} but got {berry_data['name']}")
    
    def test_get_single_berry_by_id(self):
        response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY_ID}")
        berry_data = response.json()
        self.assertEqual(berry_data['id'], self.TEST_BERRY_ID, f"Expected berry id to be {self.TEST_BERRY_ID} but got {berry_data['id']}")

    def test_get_single_berry_against_berrytestclass(self):
        """Test if the berry data can be parsed into the BerryTestClass"""
        """Because we are only asserting that it's not none - some extra errorhandling is needed while parsing the data onto the berry class"""
        """https://bulbapedia.bulbagarden.net/wiki/Category:Berries"""
        try:
            response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY_ID}")
            berry_data = response.json()
            """Check if the berry data is not empty"""
            self.assertIsNotNone(berry_data, "Received empty berry data from API")
            berry = Berry(**berry_data)
            logging.info(f"Berry data: {berry}")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
    
    def test_get_x_limit_berries_length(self):
        """Get a random number of berries and check if the length of the berry array is equal to the random number"""
        random_id = random.randint(1, 64)
        response = requests.get(f"{self.BASE_URL}/berry/?limit={random_id}")
        berry_data = response.json()
        self.assertEqual(len(berry_data['results']), random_id, f"Expected {random_id} berries but got {len(berry_data['results'])}")   
    
    def test_get_nonexistent_berry_returns_404(self):
        """Test non-existent berry response"""
        response = requests.get(f"{self.BASE_URL}/berry/9000")
        self.assertEqual(response.status_code, 404, "Expected status code 404 for fake berry")

    def test_get_berry_response_time_under_500ms(self):
        """Test if the response time of the berry endpoint is under 500ms"""
        response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY}")
        self.assertLess(response.elapsed.total_seconds() * 1000, 500, "Expected response time to be under 500ms")

    #Berry firmness tests
    def test_get_single_berry_firmness_by_name(self):
        response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS}")
        berry_firmness_data = response.json()
        self.assertEqual(berry_firmness_data['name'], self.TEST_BERRY_FIRMNESS, f"Expected berry firmness name to be {self.TEST_BERRY_FIRMNESS} but got {berry_firmness_data['name']}")

    def test_get_single_berry_firmness_by_id(self):
        response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS_ID}")
        berry_firmness_data = response.json()
        self.assertEqual(berry_firmness_data['id'], self.TEST_BERRY_FIRMNESS_ID, f"Expected berry firmness id to be {self.TEST_BERRY_FIRMNESS_ID} but got {berry_firmness_data['id']}")

    def test_get_single_berry_firmness_against_berryfirmnesstestclass(self):
        """Test if the berry firmness data can be parsed into the BerryFirmnessTestClass"""
        """https://bulbapedia.bulbagarden.net/wiki/Category:Berries_by_firmness"""
        """Because we are only asserting that it's not none - some extra errorhandling is needed while parsing the data onto the berry class"""
        try:
            response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS_ID}")
            berry_firmness_data = response.json()
            """Check if the berry firmness data is not empty"""
            self.assertIsNotNone(berry_firmness_data, "Received empty berry firmness data from API")
            berry_firmness = BerryFirmnessTest(**berry_firmness_data)
            logging.info(f"Berry firmness data: {berry_firmness}")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
    
    def test_get_x_limit_berry_firmnesses_length(self):
        """Get a random number of berry firmnesses and check if the length of the berry firmness array is equal to the random number"""
        random_id = random.randint(1, 5)
        response = requests.get(f"{self.BASE_URL}/berry-firmness/?limit={random_id}")
        berry_firmness_data = response.json()
        self.assertEqual(len(berry_firmness_data['results']), random_id, f"Expected {random_id} berry firmnesses but got {len(berry_firmness_data['results'])}")

    def test_get_nonexistent_berry_firmness_returns_404(self):
        """Test non-existent berry firmness response"""
        response = requests.get(f"{self.BASE_URL}/berry-firmness/9000")
        self.assertEqual(response.status_code, 404, "Expected status code 404 for fake berry firmness")
    
    def test_get_berry_firmness_response_time_under_500ms(self):
        """Test if the response time of the berry firmness endpoint is under 500ms"""
        response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS}")
        self.assertLess(response.elapsed.total_seconds() * 1000, 500, "Expected response time to be under 500ms")
    
    #Berry flavor tests
    def test_get_single_berry_flavor_by_name(self):
        response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR}")
        berry_flavor_data = response.json()
        self.assertEqual(berry_flavor_data['name'], self.TEST_BERRY_FLAVOR, f"Expected berry flavor name to be {self.TEST_BERRY_FLAVOR} but got {berry_flavor_data['name']}")

    def test_get_single_berry_flavor_by_id(self):
        response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR_ID}")
        berry_flavor_data = response.json()
        self.assertEqual(berry_flavor_data['id'], self.TEST_BERRY_FLAVOR_ID, f"Expected berry flavor id to be {self.TEST_BERRY_FLAVOR_ID} but got {berry_flavor_data['id']}")

    def test_get_single_berry_flavor_against_berryflavorstestclass(self):
        """Test if the berry flavor data can be parsed into the BerryFlavorTestClass"""
        """https://bulbapedia.bulbagarden.net/wiki/Flavor"""
        """Because we are only asserting that it's not none - some extra errorhandling is needed while parsing the data onto the berry class"""
        try:
            response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR_ID}")
            berry_flavor_data = response.json()
            """Check if the berry flavor data is not empty"""
            self.assertIsNotNone(berry_flavor_data, "Received empty berry flavor data from API")
            berry_flavor = BerryFlavor(**berry_flavor_data)
            logging.info(f"Berry flavor data: {berry_flavor}")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e

    def test_get_x_limit_berry_flavors_length(self):
        """Get a random number of berry flavors and check if the length of the berry flavor array is equal to the random number"""
        random_id = random.randint(1, 5)
        response = requests.get(f"{self.BASE_URL}/berry-flavor/?limit={random_id}")
        berry_flavor_data = response.json()
        self.assertEqual(len(berry_flavor_data['results']), random_id, f"Expected {random_id} berry flavors but got {len(berry_flavor_data['results'])}")

    def test_get_nonexistent_berry_flavor_returns_404(self):
        """Test non-existent berry flavor response"""
        response = requests.get(f"{self.BASE_URL}/berry-flavor/9000")
        self.assertEqual(response.status_code, 404, "Expected status code 404 for fake berry flavor")

    def test_get_berry_flavor_response_time_under_500ms(self):
        """Test if the response time of the berry flavor endpoint is under 500ms"""
        response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR}")
        self.assertLess(response.elapsed.total_seconds() * 1000, 500, "Expected response time to be under 500ms")

    #Skipped tests
    @unittest.skip("Skipping this test because auth is not actually supported")
    def test_get_pokemon_with_auth_returns_401(self):
        headers = {
            "Authorization": f"Basic {self.AUTH_TOKEN}"
        }
        response = requests.get(
            f"{self.BASE_URL}/pokemon/{self.TEST_POKEMON}",
            headers=headers
        )
        self.assertEqual(response.status_code, 401, "Expected unauthorized status code 401 since auth is not actually supported")
        self._check_response_headers(response)

        
    @unittest.skip("Skipping this test because /NewPokemon is not actually supported")
    def test_post_create_pokemon_and_verify_success(self):
        """Testing if POST request for a Pokemon returns 200 status code"""
        response = requests.post(f"{self.BASE_URL}/NewPokemon", json={"name": "Laurenvris", 
                                                                      "id": 9000, 
                                                                      "abilities": [{"1": {"ability": "waterbolt x3", "url": f"https://pokeapi.co/api/v2/ability/{random.randint(9000, 9010)}/"}}, 
                                                                                    {"3": {"ability": "freeze", "url": f"https://pokeapi.co/api/v2/ability/{random.randint(10000, 10010)}/"}}]})
        self.assertEqual(response.status_code, 200)

        """Doublecheck if new pokemon is created"""
        response_2 = self.test_get_parameterized_pokemon_returns_200_status_code(pokemon_name="Laurenvris")
        self.assertEqual(response_2.status_code, 200)

    #Helper functions
    def _check_response_headers(self, response):
        if response.status_code == 200: 
            """Check the certain headers of a successful he response"""
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8', "Expected JSON content type")
            self.assertEqual(response.headers['Content-Encoding'], 'gzip', "Expected content encoding to be gzip")
            self.assertEqual(response.headers['server'], 'cloudflare', "Expected server to be cloudflare")
        else:
            """Check the content-type of a failed response"""
            self.assertEqual(response.headers['Content-Type'], 'text/plain; charset=utf-8', "Expected Content-Type to be text/plain")

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(PokeAPITests)
    
    # Create and configure the runner
    runner = unittest.TextTestRunner(
        verbosity=2,  # Detailed output
        stream=sys.stdout,  # Uses sys.stderr by default
        descriptions=True,
        failfast=False
    )
    
    # Run the tests
    runner.run(suite)
