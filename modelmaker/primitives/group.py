from .. import utils as ut
from .primitive import Primitive

class Group(Primitive):
	def __init__(self, members):
		print('here')
		self.members = self._filter_members(members)
		self.faces = self._get_faces()
		self.points = self._get_points()
		self.center = self._calc_centroid()
	
	def copy(self):
		return Group([m.copy() for m in self.memebers])

	def _filter_members(self, members):
		return [m for m in members if ut.is_primitive(m)]

	def _get_points(self):
		points = []

		for m in self.members:
			points.extend(m.points)

		return points

	def _get_faces(self):
		faces = []

		for m in self.members:
			if ut.is_face(m):
				faces.append(face)
			else:
				faces.extend(m.faces)

		return faces
