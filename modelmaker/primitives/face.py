from scipy.spatial import Delaunay

from .point import Point


class Face:
	def __init__(self, points):
		self.points = self._parse_points(points)
		self.triangles = []
		self.outline = []

	def translate(self, x, y, z):
		pass

	def rotate(self, radians):
		pass

	def reflect(self, line):
		pass

	def scale(self, factor):
		pass

	def _parse_points(self, points):
		"""
		Creates Point objects from tuples as needed
		"""

		return [Point(*p) if type(p).__name__ != "Point" else p for p in points]

	def _calculate_triangles(self):
		"""
		Triangulates the face
		"""

		def dedupe(points):
			return list(set(points))

		# select a reference plane where there are no overlapping points
		points_xy = [(p.x, p.y) for p in self.points]
		points_xz = [(p.x, p.z) for p in self.points]
		points_yz = [(p.y, p.z) for p in self.points]
		points_2d = (
			points_xy
			if len(points_xy) == len(dedupe(points_xy))
			else points_xz
			if len(points_xz) == len(dedupe(points_xz))
			else points_yz
		)

		# raise an error if the face cannot be expressed in 2 dimensions
		if len(points_2d) != len(dedupe(self.points)):
			raise Exception(
				"The face cannot be expressed in 2 dimensions."
				+ "Please split it into separate faces."
			)

		# triangulate the face
		self.triangles = [
			(
				tuple(self.points[s[0]]),
				tuple(self.points[s[1]]),
				tuple(self.points[s[2]]),
			)
			for s in Delaunay(points_2d).simplices
		]

	def _calculate_outline(self):
		"""
		Creates the outline using non-shared edges in the triangulation
		"""

		tally = {}

		def count_edge(s, d):
			key = tuple(set([s, d]))
			tally[key] = tally.get(key, 0) + 1

		for t in self.triangles:
			count_edge(t[0], t[1])
			count_edge(t[0], t[2])
			count_edge(t[1], t[2])

		self.outline = [k for k, v in tally.items() if v == 1]
