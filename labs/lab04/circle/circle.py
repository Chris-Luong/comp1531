import math

class Circle:
	def __init__(self, r):
		self.radius = r
	def circumference(self):
		return 2 * self.radius * math.pi
	def area(self):
		return self.radius ** 2 * math.pi
	def valid_radius(self):
		if self.radius <= 0:
			raise ValueError