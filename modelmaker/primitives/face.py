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

		def dedupe(points):
			rounded = [
				tuple(round(p, 6))
				for p in points
			]
			deduped = [
				Point(*p)
				for p in list(dict.fromkeys(rounded))
			]

			return deduped

		raw_points = [Point(*p) if type(p).__name__ != "Point" else p for p in points]

		return dedupe(raw_points)

	def _calc_triangles(self):
		"""
		Triangulates the face
		"""

		points_xy = [(p.x, p.y) for p in self.points]
		points_xz = [(p.x, p.z) for p in self.points]
		points_yz = [(p.y, p.z) for p in self.points]

		# Try to triangulate the face in each plane before failing
		try:
			triangulation = Delaunay(points_xy)
		except:
			try:
				triangulation = Delaunay(points_xz)
			except:
				triangulation = Delaunay(points_yz)

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

		# Returns a list of unique edges
		def get_unique_edges():
			edge_tally = {}

			def tally(p1, p2):
				if (p1, p2) in edge_tally:
					edge_tally[(p1, p2)] += 1
				elif (p2, p1) in edge_tally:
					edge_tally[(p2, p1)] += 1
				else:
					edge_tally[(p1, p2)] = 1

			for t in self.triangles:
				p1, p2, p3 = t

				tally(p1, p2)
				tally(p1, p3)
				tally(p2, p3)

			return [ e for e, tally in edge_tally.items() if tally == 1 ]

		# Remove triangles that interfere with intended concavity
		def is_good_triangle(triangle):
			def is_bad_edge(e):
				p1, p2 = e
				is_unique = (p1, p2) in self.unique_edges or (p2, p1) in self.unique_edges
				is_in_outline = (p1, p2) in self.outline or (p2, p1) in self.outline

				return is_unique and not is_in_outline

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
				if not is_bad_edge(e): continue
				self.bad_edges += [e]

			self.bad_edges += bad_edges

			return False

		# Cull the triangles until there are no bad triangles left
		self.unique_edges = get_unique_edges()
		while True:
			updated_triangles = list(filter(is_good_triangle, self.triangles))

			if len(updated_triangles) == len(self.triangles): break

			self.triangles = updated_triangles
			self.unique_edges = get_unique_edges()

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
