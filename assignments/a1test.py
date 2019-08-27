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
		self.assertEqual(changeBase(1, "INR", "INR", "2019-01-01"), 1)
		self.assertEqual(changeBase(0, "INR", "USD", "2019-01-01"), 0)

if __name__=='__main__':
	unittest.main()