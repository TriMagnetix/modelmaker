from scipy.spatial import Delaunay, ConvexHull

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

		return [Point(*p) if type(p).__name__ != "Point" else p for p in points]

	def _calc_triangles(self):
		"""
		Triangulates the face
		"""

		def dedupe(points):
			return list(set(points))

		points_xy = [(round(p.x, 3), round(p.y, 3)) for p in self.points]
		points_xz = [(round(p.x, 3), round(p.z, 3)) for p in self.points]
		points_yz = [(round(p.y, 3), round(p.z, 3)) for p in self.points]

		# Try to triangulate the face in each plane before failing
		try:
			triangulation = Delaunay(points_xy)
			hull = ConvexHull(points_xy)
		except:
			try:
				triangulation = Delaunay(points_xz)
				hull = ConvexHull(points_xz)
			except:
				triangulation = Delaunay(points_yz)
				hull = ConvexHull(points_yz)

		# Define edges in the convex hull
		self._calc_outline()
		hull_edges = [
			(
				tuple(self.points[s[0]]),
				tuple(self.points[s[1]]),
			)
			for s in hull.simplices
		]

		# Construct the triangles
		self.triangles = [
			(
				tuple(self.points[s[0]]),
				tuple(self.points[s[1]]),
				tuple(self.points[s[2]]),
			)
			for s in triangulation.simplices
		]

		# Remove triangles that interfere with intended concavity
		def is_good_triangle(triangle):
			p1, p2, p3 = triangle

			def in_outline(p1, p2):
				return (p1, p2) in self.outline or (p2, p1) in self.outline

			def in_hull(p1, p2):
				return (p1, p2) in hull_edges or (p2, p1) in hull_edges

			return not (
				(in_outline(p1, p2) and in_outline(p2, p3) and in_hull(p3, p1))
				or (in_outline(p1, p2) and in_outline(p3, p1) and in_hull(p2, p3))
				or (in_outline(p2, p3) and in_outline(p3, p1) and in_hull(p1, p2))
			)

		self.triangles = list(filter(is_good_triangle, self.triangles))

	def _calc_outline(self):
		"""
		Creates the outline using non-shared edges in the triangulation
		"""

		self.outline = []

		for i in range(len(self.points)):
			edge = (
				tuple(self.points[i]),
				tuple(self.points[(i + 1) % len(self.points)]),
			)
			self.outline.append(edge)
