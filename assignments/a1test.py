# Name : 
# Roll No : 
# Group : 

import unittest
from a1 import changeBase

# TEST cases should cover the different boundary cases.

class testpoint(unittest.TestCase):
	
	def test_change_base(self):
		self.assertEqual(changeBase(1, "INR", "GBP", "2010-10-25"), 2.57)
		self.assertAlmostEqual(changeBase(1, "INR", "GBP", "2010-10-25"), 2.57, delta = 0.1)
		# these are just sample values. You have to add testcases (and edit these) for various dates.
		# (don't use the current date as the json would keep changing every 4 minutes)
		# you have to hard-code the 2nd parameter of assertEquals by calculating it manually
		# on a particular date and checking whether your changeBase function returns the same
		# value or not.




if __name__=='__main__':
	unittest.main()