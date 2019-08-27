# Name : Mihir Chaturvedi
# Roll No : 2019061
# Group : A-7

import unittest
from a1 import changeBase

# TEST cases should cover the different boundary cases.

class testpoint(unittest.TestCase):
	
	def test_change_base(self):
		self.assertAlmostEqual(changeBase(1, "GBP", "INR", "2010-10-25"), 69.732, delta = 0.001)
		self.assertAlmostEqual(changeBase(-1, "GBP", "INR", "2010-10-25"), -69.732, delta = 0.001)
		self.assertAlmostEqual(changeBase(45.234, "USD", "MYR", "2018-09-09"), 187.576, delta = 0.001)
		self.assertEqual(changeBase(1, "INR", "INR", "2019-01-01"), 1)
		self.assertEqual(changeBase(0, "INR", "USD", "2019-01-01"), 0)
		self.assertEqual(changeBase(1, "USD", "ABC", "2019-01-01"), "Invalid currency code")
		self.assertEqual(changeBase(1, "USD", "INR", "2019-01-41"), "Invalid date format")

if __name__=='__main__':
	unittest.main()