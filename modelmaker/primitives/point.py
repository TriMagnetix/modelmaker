class Point:
	def __init__(self, x, y, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z})"

	def __add__(self, other):
		return Point(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z,
		)

	def __sub__(self, other):
		return Point(
			self.x - other.x,
			self.y - other.y,
			self.z - other.z,
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
