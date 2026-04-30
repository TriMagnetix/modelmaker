from .primitive import Primitive
from .face import Face


class Shape(Primitive):
	def __init__(self, faces):
		self.faces = self._parse_faces(faces)
		self.points = self._get_points()
		self.center = self._calc_centroid()

	def copy(self):
		return Shape([f.copy() for f in self.faces])

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
