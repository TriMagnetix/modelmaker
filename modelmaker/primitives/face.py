from scipy.spatial import Delaunay

from .point import Point
from . import utils as ut


class Face:
	def __init__(self, points):
		self.points = self._parse_points(points)
		self.triangles = []
		self.outline = []
		self.center = ut.calc_centroid(self.points)

	def copy(self):
		return Face([Point(p.x, p.y, p.z) for p in self.points])

	def move_to(self, x, y, z):
		ut.move_to(self, (x, y, z))

	def translate(self, x, y, z):
		ut.translate(self, (x, y, z))

	def scale(self, factor):
		ut.scale(self, factor)

	def rotate(self, rot_vect, rad):
		ut.rotate(self, rot_vect, rad)

	def _parse_points(self, points):
		"""
		Creates Point objects from tuples as needed
		"""

		return ut.reorder_points(
			[Point(*p) if type(p).__name__ != "Point" else p for p in points]
		)

	def _calc_triangles(self):
		"""
		Triangulates the face
		"""

		def dedupe(points):
			return list(set(points))

		# select a reference plane where there are no overlapping points
		points_xy = [(round(p.x, 3), round(p.y, 3)) for p in self.points]
		points_xz = [(round(p.x, 3), round(p.z, 3)) for p in self.points]
		points_yz = [(round(p.y, 3), round(p.z, 3)) for p in self.points]
		points_2d = (
			points_xy
			if len(points_xy) == len(dedupe(points_xy))
			else points_xz
			if len(points_xz) == len(dedupe(points_xz))
			else points_yz
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

	def _calc_outline(self):
		"""
		Creates the outline using non-shared edges in the triangulation
		"""

		tally = {}

		def count_edge(s, d):
			key = tuple(sorted([s, d], key=lambda p: str(p)))
			tally[key] = tally.get(key, 0) + 1

		for t in self.triangles:
			count_edge(t[0], t[1])
			count_edge(t[0], t[2])
			count_edge(t[1], t[2])

		self.outline = [k for k, v in tally.items() if v == 1]
