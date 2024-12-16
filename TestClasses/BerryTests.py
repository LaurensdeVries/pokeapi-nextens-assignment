from TestClasses.BasePokeAPIClass import BasePokeAPIClass
import requests
import random
import logging
from BerryModels.BerryTestModel import Berry

class BerryTests(BasePokeAPIClass):
    TEST_BERRY_ID = 2
    TEST_BERRY = "cheri"

    def test_get_single_berry_by_name(self):
        response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY}")
        berry_data = response.json()
        self.assertEqual(berry_data['name'], self.TEST_BERRY)
    
    def test_get_single_berry_by_id(self):
        response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY_ID}")
        berry_data = response.json()
        self.assertEqual(berry_data['id'], self.TEST_BERRY_ID)

    def test_get_single_berry_against_berrytestclass(self):
        """This is where I test if the berry I get from the API is a valid Berry object"""
        """I got the JSON from the docs and created a class to match it"""
        """If a field is not present, or does not comply with the type specified in the class, it will raise an error, this error will be caught and logged"""
        try:
            response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY_ID}")
            berry_data = response.json()
            self.assertIsNotNone(berry_data, "Received empty berry data from API")
            berry = Berry(**berry_data)
            logging.info(f"Berry data: {berry}")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise e
    
    def test_get_x_limit_berries_length(self):
        """This is where I test if the limit parameter works"""
        """I'm using a random number between 1 and 64, because there are 64 berries"""
        random_id = random.randint(1, 64)
        response = requests.get(f"{self.BASE_URL}/berry/?limit={random_id}")
        berry_data = response.json()
        self.assertEqual(len(berry_data['results']), random_id)
    
    def test_get_nonexistent_berry_returns_404(self):
        response = requests.get(f"{self.BASE_URL}/berry/9000")
        self.assertEqual(response.status_code, 404)

    def test_get_berry_response_time_under_500ms(self):
        response = requests.get(f"{self.BASE_URL}/berry/{self.TEST_BERRY}")
        self.assertLess(response.elapsed.total_seconds() * 1000, 500)