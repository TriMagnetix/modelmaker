import math

class Point:
	def __init__(self, x, y, z=0):
		self.x = x
		self.y = y
		self.z = z
	
	def copy(self):
		return Point(*tuple(self))

	def dot(self, other):
		'''
		Takes the dot product between this point and another point
		'''

		other = self._coerce_other(other)
		
		return self.x * other.x + self.y * other.y + self.z * other.z

	def magnitude(self):
		'''
		Returns the magnitude of the point
		'''

		squared = self * self

		return math.sqrt(squared.x + squared.y + squared.z)

	def _coerce_other(self, other):
		'''
		Converts the given value to a Point
		'''

		if type(other) == int or type(other) == float:
			other = (other, other, other)

		other = tuple(other)

		return Point(*other)

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z})"

	def __add__(self, other):
		other = self._coerce_other(other)

		return Point(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z,
		)

	def __sub__(self, other):
		other = self._coerce_other(other)

		return Point(
			self.x - other.x,
			self.y - other.y,
			self.z - other.z,
		)

	def __mul__(self, other):
		other = self._coerce_other(other)

		return Point(
			self.x * other.x,
			self.y * other.y,
			self.z * other.z,
		)

	def __pow__(self, other):
		other = self._coerce_other(other)

		return Point(
			self.x ** other.x,
			self.y ** other.y,
			self.z ** other.z,
		)

	def __round__(self, n):
		return Point(
			round(self.x, n),
			round(self.y, n),
			round(self.z, n),
		)

	def __iter__(self):
		for n in (self.x, self.y, self.z):
			yield n
