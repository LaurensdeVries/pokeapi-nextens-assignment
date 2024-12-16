import unittest
import sys
import logging

from TestClasses.PokemonTests import PokemonTests
from TestClasses.BerryTests import BerryTests
from TestClasses.BerryFirmnessTests import BerryFirmnessTests
from TestClasses.BerryFlavorTests import BerryFlavorTests

"""I configure the logging to only show the message. And the level to INFO, so that INFO messages are shown"""
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

if __name__ == '__main__':
    """Here I create the test loader and the test suite"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    """The loader loads the tests from the test classes"""
    suite.addTests(loader.loadTestsFromTestCase(PokemonTests))
    suite.addTests(loader.loadTestsFromTestCase(BerryTests))
    suite.addTests(loader.loadTestsFromTestCase(BerryFirmnessTests))
    suite.addTests(loader.loadTestsFromTestCase(BerryFlavorTests))
    
    """Verbosity is set to 2 to get a little extra information about the tests"""
    """I do not like it when the suite stops running after the first failure, so I set failfast to False"""
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False
    )    
    
    runner.run(suite)
