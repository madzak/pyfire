import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from campfire_tests import TestCampfire

def suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCampfire))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
    
