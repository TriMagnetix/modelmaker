from .face import Face
from . import utils as ut


class Shape:
	def __init__(self, faces):
		self.faces = self._parse_faces(faces)
		self.points = self._get_points()
		self.center = ut.calc_centroid(self.points)

	def copy(self):

		return Shape([f.copy() for f in self.faces])

	def move_to(self, x, y, z):
		ut.move_to(self, (x, y, z))

	def translate(self, x, y, z):
		ut.translate(self, (x, y, z))

	def scale(self, factor):
		ut.scale(self, factor)

	def rotate(self, rot_vect, rad):
		ut.rotate(self, rot_vect, rad)

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
