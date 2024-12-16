from TestClasses.BasePokeAPIClass import BasePokeAPIClass
import requests
import random
import logging
from BerryModels.BerryFirmnessModel import BerryFirmness

class BerryFirmnessTests(BasePokeAPIClass):
    TEST_BERRY_FIRMNESS_ID = 1
    TEST_BERRY_FIRMNESS = "very-soft"

    def test_get_berry_firmness_by_name(self):
        response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS}")
        firmness_data = response.json()
        self.assertEqual(firmness_data['name'], self.TEST_BERRY_FIRMNESS)

    def test_get_berry_firmness_by_id(self):
        response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS_ID}")
        firmness_data = response.json()
        self.assertEqual(firmness_data['id'], self.TEST_BERRY_FIRMNESS_ID)

    def test_get_nonexistent_berry_firmness_returns_404(self):
        response = requests.get(f"{self.BASE_URL}/berry-firmness/999")
        self.assertEqual(response.status_code, 404)

    def test_get_berry_firmness_against_berryfirmnessclass(self):
        try:
            response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS_ID}")
            firmness_data = response.json()
            self.assertIsNotNone(firmness_data, "Received empty berry firmness data from API")
            berry_firmness = BerryFirmness(**firmness_data)
            logging.info(f"Berry firmness data: {berry_firmness}")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e

    def test_get_limit_berry_firmness_length(self):
        random_id = random.randint(1, 5)
        response = requests.get(f"{self.BASE_URL}/berry-firmness/?limit={random_id}")
        firmness_data = response.json()
        self.assertEqual(len(firmness_data['results']), random_id)

    def test_get_berry_firmness_response_time_under_500ms(self):
        response = requests.get(f"{self.BASE_URL}/berry-firmness/{self.TEST_BERRY_FIRMNESS}")
        self.assertLess(response.elapsed.total_seconds() * 1000, 500)
