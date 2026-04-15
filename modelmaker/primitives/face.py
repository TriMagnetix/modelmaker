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

		points_xy = [(p.x, p.y) for p in self.points]
		points_xz = [(p.x, p.z) for p in self.points]
		points_yz = [(p.y, p.z) for p in self.points]

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
		hull_edges = {
			tuple({
				tuple(self.points[s[0]]),
				tuple(self.points[s[1]]),
			})
			for s in hull.simplices
		}

		self._calc_outline()

		# Construct the triangles
		self.triangles = [
			(
				tuple(self.points[s[0]]),
				tuple(self.points[s[1]]),
				tuple(self.points[s[2]]),
			)
			for s in triangulation.simplices
		]
		self.bad_edges = []

		# Remove triangles that interfere with intended concavity
		def is_good_triangle(triangle):
			def is_bad_edge(e):
				return e in hull_edges and e not in self.outline

			result = True
			p1, p2, p3 = triangle
			edges = {
				tuple({p1, p2}),
				tuple({p1, p3}),
				tuple({p2, p3}),
			}
			bad_edges = set(filter(is_bad_edge, edges))
			good_edges = edges.difference(bad_edges)

			if len(bad_edges) == 0: return True

			for e in good_edges:
				hull_edges.add(e)
				if not is_bad_edge(e): continue
				self.bad_edges += [e]

			self.bad_edges += bad_edges

			return False

		# Cull the triangles until there are no bad triangles left
		i = 0
		while True:
			if i == 3: break
			i += 1
			updated_triangles = list(filter(is_good_triangle, self.triangles))

			if len(updated_triangles) == len(self.triangles): break

			self.triangles = updated_triangles

	def _calc_outline(self):
		"""
		Creates the outline using non-shared edges in the triangulation
		"""

		self.outline = set()

		for i in range(len(self.points)):
			edge = tuple({
				tuple(self.points[i]),
				tuple(self.points[(i + 1) % len(self.points)]),
			})

			if len(edge) == 1:
				edge = (edge[0], edge[0])

			self.outline.add(edge)
