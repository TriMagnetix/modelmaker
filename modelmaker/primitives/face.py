import math
from scipy.spatial import Delaunay

from .point import Point


class Face:
	def __init__(self, points):
		self.points = self._parse_points(points)
		self.triangles = []
		self.outline = []
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

	def rotate(self, rot_vect, rad):
		ux, uy, uz = self._vect_norm(rot_vect)
		q = (
			math.cos(rad / 2),
			ux * math.sin(rad / 2),
			uy * math.sin(rad / 2),
			uz * math.sin(rad / 2),
		)
		q_conj = (
			math.cos(rad / 2),
			-ux * math.sin(rad / 2),
			-uy * math.sin(rad / 2),
			-uz * math.sin(rad / 2),
		)

		x, y, z = self.center
		self.move_to(0, 0, 0)

		for p in self.points:
			p_quat = (0, p.x, p.y, p.z)
			_, p.x, p.y, p.z = self._quatmul(
				self._quatmul(q, p_quat),
				q_conj,
			)

		self.center = self._calc_centroid()
		self.move_to(x, y, z)

	def scale(self, factor):
		x, y, z = self.center

		self.move_to(0, 0, 0)

		for p in self.points:
			p.x = factor * p.x
			p.y = factor * p.y
			p.z = factor * p.z

		self.center = self._calc_centroid()

		self.move_to(x, y, z)

	def _vect_norm(self, vect):
		magnitude = math.sqrt(sum([n**2 for n in vect]))

		return (n / magnitude for n in vect)

	def _quatmul(self, q1, q2):
		w1, x1, y1, z1 = q1
		w2, x2, y2, z2 = q2

		return (
			w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
			w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
			w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
			w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
		)

	def _parse_points(self, points):
		"""
		Creates Point objects from tuples as needed
		"""

		return [Point(*p) if type(p).__name__ != "Point" else p for p in points]

	def _calc_centroid(self):
		x = sum(p.x / len(self.points) for p in self.points)
		y = sum(p.y / len(self.points) for p in self.points)
		z = sum(p.z / len(self.points) for p in self.points)

		return Point(x, y, z)

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
			key = tuple(set([s, d]))
			tally[key] = tally.get(key, 0) + 1

		for t in self.triangles:
			count_edge(t[0], t[1])
			count_edge(t[0], t[2])
			count_edge(t[1], t[2])

		self.outline = [k for k, v in tally.items() if v == 1]
