import unittest
import numpy as np

from planet import Planet

class TestPlanet(unittest.TestCase):
	def test_simmetry(self):
		p1 = Planet(_id=0, mass=1, x=0.1, y=0.1)
		p2 = Planet(_id=0, mass=1, x=0.5, y=0.1)
		
		F12x, F12y = p1._get_gravitational_force(p2)

		F21x, F21y = p2._get_gravitational_force(p1)

		self.assertAlmostEqual(F12x, -F21x, places=2)
		self.assertAlmostEqual(F12y, -F21y, places=2)

	def test_tmp(self):
		p1 = Planet(_id=0, mass=1, x=0.1, y=0.1)
		p2 = Planet(_id=0, mass=1, x=0.2, y=0.2)
		
		F12x, F12y = p1._get_gravitational_force(p2)
		print(F12x, F12y)

		F21x, F21y = p2._get_gravitational_force(p1)
		print(F21x, F21y)

		self.assertAlmostEqual(F12x, -F21x, places=2)
		self.assertAlmostEqual(F12y, -F21y, places=2)

if __name__ == '__main__':
    unittest.main()