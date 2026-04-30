from .point import Point

class Primitive:
	def copy(self):
		raise NotImplementedError()

	def move_to(self, x, y, z):
		"""
		Move a face or a shape to a particular destination
		"""

		dx, dy, dz = tuple(self.center)

		for p in self.points:
			p.x += x - dx
			p.y += y - dy
			p.z += z - dz

		self.center = self._calc_centroid()

	def translate(self, x, y, z):
		"""
		Move a face or a shape by an offset
		"""

		x, y, z = offset

		for p in self.points:
			p.x += x
			p.y += y
			p.z += z

		self.center = self._calc_centroid()

	def scale(self, factor):
		"""
		Scales a face or a shape by a given factor
		"""

		x, y, z = self.center

		self.move_to(0, 0, 0)

		for p in self.points:
			p.x = factor * p.x
			p.y = factor * p.y
			p.z = factor * p.z

		self.center = self._calc_centroid()

		self.move_to(x, y, z)

	def rotate(self, rot_vect, rad):
		"""
		Rotates a face or a given amount around a rotation vector
		"""

		ux, uy, uz = vect_norm(rot_vect)
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
			_, p.x, p.y, p.z = quat_mul(
				quat_mul(q, p_quat),
				q_conj,
			)

		self.center = self._calc_centroid()
		self.move_to(x, y, z)
	
	def _calc_centroid(self):
		"""
		Calculates the centroid for a group of points
		"""

		x = sum(p.x / len(self.points) for p in self.points)
		y = sum(p.y / len(self.points) for p in self.points)
		z = sum(p.z / len(self.points) for p in self.points)

		return Point(x, y, z)
