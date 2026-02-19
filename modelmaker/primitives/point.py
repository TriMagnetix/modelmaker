class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __iter__(self):
		for n in (self.x, self.y, self.z):
			yield n
