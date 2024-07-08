import numpy as np
import math

G = 3e-8

class Planet:
	def __init__(self, _id, mass, color, x , y):
		self.id = _id
		self.mass = mass
		self.color = color

		self.x = x
		self.y = y

		self.xspeed = 0
		self.yspeed = 0

	def init_random_speed(self):
		r = np.random.rand()*0.05
		angle = math.radians(np.random.rand()*360)
		self.xspeed = r*math.sin(angle)
		self.yspeed = r*math.cos(angle)

	def _get_gravitational_force(self, planet):
		d = ((self.x - planet.x)**2 + (self.y - planet.y)**2)**0.5
		d = max(d, 0.1)
		# print(d)
		unit_v = ((planet.x - self.x) / d, (planet.y - self.y) / d)

		F = G * self.mass * planet.mass / d**2

		Fx, Fy = F * unit_v[0], F * unit_v[1]

		return Fx, Fy

	def _update_xy(self):
		self.x += self.xspeed
		self.y += self.yspeed

	def update(self, planets):
		tot_Fx = 0
		tot_Fy = 0

		for planet in planets:
			if planet.id == self.id:
				continue
			Fx, Fy = self._get_gravitational_force(planet)
			tot_Fx += Fx
			tot_Fy += Fy

		self.xspeed += tot_Fx/self.mass
		self.yspeed += tot_Fy/self.mass
		# print(f"id = {self.id}: ({self.xspeed} , {self.yspeed})")
		self._update_xy()