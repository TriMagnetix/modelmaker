from .face import Face
from .point import Point


class Shape:
	def __init__(self, faces):
		self.faces = self._parse_faces(faces)
		self.points = self._get_points()
		self.center = self._calc_centroid()

	def move_to(self, x, y, z):
		dx, dy, dz = tuple(self.center)

		for p in self.points:
			p.x += x - dx
			p.y += y - dy
			p.z += z - dz

		self.center = self._calc_centroid()

	def translate(self, x, y, z):
		for p in self.points:
			p.x += x
			p.y += y
			p.z += z

		self.center = self._calc_centroid()

	def _parse_faces(self, faces):
		"""
		Creates Face objects from tuples as needed
		"""

		return [Face(f) if type(f).__name__ != "Face" else f for f in faces]

	def _get_points(self):
		points = set()

		for f in self.faces:
			for p in f.points:
				points.add(p)

		return points

	def _calc_centroid(self):
		points = []

		for f in self.faces:
			points.extend(f.points)

		x = sum(p.x / len(points) for p in points)
		y = sum(p.y / len(points) for p in points)
		z = sum(p.z / len(points) for p in points)

		return Point(x, y, z)
