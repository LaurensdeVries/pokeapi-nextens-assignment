from TestClasses.BasePokeAPIClass import BasePokeAPIClass
import requests
import random
import logging
from BerryModels.BerryFlavorModel import BerryFlavor

class BerryFlavorTests(BasePokeAPIClass):
    TEST_BERRY_FLAVOR_ID = 1
    TEST_BERRY_FLAVOR = "spicy"

    def test_get_berry_flavor_by_name(self):
        response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR}")
        flavor_data = response.json()
        self.assertEqual(flavor_data['name'], self.TEST_BERRY_FLAVOR)

    def test_get_berry_flavor_by_id(self):
        response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR_ID}")
        flavor_data = response.json()
        self.assertEqual(flavor_data['id'], self.TEST_BERRY_FLAVOR_ID)

    def test_get_nonexistent_berry_flavor_returns_404(self):
        response = requests.get(f"{self.BASE_URL}/berry-flavor/999")
        self.assertEqual(response.status_code, 404)

    def test_get_berry_flavor_against_berryflavorclass(self):
        try:
            response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR_ID}")
            flavor_data = response.json()
            self.assertIsNotNone(flavor_data, "Received empty berry flavor data from API")
            berry_flavor = BerryFlavor(**flavor_data)
            logging.info(f"Berry flavor data: {berry_flavor}")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e

    def test_get_limit_berry_flavor_length(self):
        random_id = random.randint(1, 5)
        response = requests.get(f"{self.BASE_URL}/berry-flavor/?limit={random_id}")
        flavor_data = response.json()
        self.assertEqual(len(flavor_data['results']), random_id)

    def test_get_berry_flavor_response_time_under_500ms(self):
        response = requests.get(f"{self.BASE_URL}/berry-flavor/{self.TEST_BERRY_FLAVOR}")
        self.assertLess(response.elapsed.total_seconds() * 1000, 500)