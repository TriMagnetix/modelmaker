from .point import Point

class Face:
	def __init__(self, points):
		self.points = self._parse_points(points)

	def _parse_points(self, points):
		return [
			Point(*p) if type(p).__name__ != 'Point' else p
			for p in points
		]
