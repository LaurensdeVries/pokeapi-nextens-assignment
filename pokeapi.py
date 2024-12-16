import unittest
import sys
import logging

from TestClasses.PokemonTests import PokemonTests
from TestClasses.BerryTests import BerryTests
from TestClasses.BerryFirmnessTests import BerryFirmnessTests
from TestClasses.BerryFlavorTests import BerryFlavorTests

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

if __name__ == '__main__':
    # Create test suites for each test class
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes to the suite
    suite.addTests(loader.loadTestsFromTestCase(PokemonTests))
    suite.addTests(loader.loadTestsFromTestCase(BerryTests))
    suite.addTests(loader.loadTestsFromTestCase(BerryFirmnessTests))
    suite.addTests(loader.loadTestsFromTestCase(BerryFlavorTests))
    
    # Configure and run the test runner
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )    
    
    runner.run(suite)
