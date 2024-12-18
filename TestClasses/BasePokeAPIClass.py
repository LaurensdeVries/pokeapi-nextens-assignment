import unittest
import requests

class BasePokeAPIClass(unittest.TestCase):
    BASE_URL = "https://pokeapi.co/api/v2"
    AUTH_TOKEN = "auth_token_that_will_not_work"

    """This class is inherited by all the test classes, and so is run before each suite."""

    @classmethod
    def setUpClass(cls):
        """This is where I check if the PokeAPI is responding correctly"""
        try:
            response = requests.get(cls.BASE_URL)
            if response.status_code != 200:
                raise unittest.SkipTest(f"PokeAPI is not responding correctly: {response.status_code}")
        except requests.RequestException as e:
            raise unittest.SkipTest(f"Could not connect to PokeAPI: {str(e)}")

    def _check_response_headers(self, response):
        """Some headers that I expect to be present in the response"""
        if response.status_code == 200: 
            self.assertEqual(response.headers['content-type'], 'application/json; charset=utf-8', "Expected JSON content type")
            self.assertEqual(response.headers['Content-Encoding'], 'gzip', "Expected content encoding to be gzip")
            self.assertEqual(response.headers['server'], 'cloudflare', "Expected server to be cloudflare")
        else:
            self.assertEqual(response.headers['Content-Type'], 'text/plain; charset=utf-8', "Expected Content-Type to be text/plain") 