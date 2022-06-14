import unittest

class MainTest(unittest.TestCase):

    def test_hello(self):
        print("Hello from testing!")
    
    def test_breaking(self):
        print("Hello, I'm about the break the code.")
        self.assertEqual(False, True, "Uh Oh")
