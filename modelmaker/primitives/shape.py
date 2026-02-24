from .face import Face


class Shape:
	def __init__(self, faces):
		self.faces = self._parse_faces(faces)

	def _parse_faces(self, faces):
		"""
		Creates Face objects from tuples as needed
		"""

		return [Face(f) if type(f).__name__ != "Face" else f for f in faces]
