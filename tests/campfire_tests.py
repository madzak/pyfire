import unittest, os
from pyfire.campfire import Campfire

class TestCampfire(unittest.TestCase):
    """

    A test class for the campfire class in the pyfire module

    """

    def setUp(self):
        self.campfire = Campfire(os.environ['CAMPFIRE_SUBDOMAIN'], os.environ['CAMPFIRE_USER'],os.environ['CAMPFIRE_PASSWORD'],)

    def testSanity(self):
        self.assertEqual(0, 0)

    def testGetRooms(self):
        rooms = self.campfire.get_rooms()
        self.assertEqual(len(rooms), 2)

    def test_search(self):
        messages = self.campfire.search('Hi')
        self.assertNotEqual(len(messages), 0)

