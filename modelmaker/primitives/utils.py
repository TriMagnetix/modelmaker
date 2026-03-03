import math

from .point import Point


def vect_norm(vect):
	"""
	Normalizes a vector
	"""

	magnitude = math.sqrt(sum([n**2 for n in vect]))

	return (n / magnitude for n in vect)


def quat_mul(q1, q2):
	"""
	Multiplies two quaternions
	"""

	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2

	return (
		w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
		w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
		w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
		w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
	)


def calc_centroid(points):
	"""
	Calculates the centroid for a group of points
	"""

	x = sum(p.x / len(points) for p in points)
	y = sum(p.y / len(points) for p in points)
	z = sum(p.z / len(points) for p in points)

	return Point(x, y, z)


def reorder_points(points):
	"""
	Rearranges points so that the nearest neighbors are next to each other
	"""

	if len(points) <= 1:
		return points

	def distance(p1, p2):
		return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)

	first = points[0]
	closest = points[1]
	closest_idx = 1

	for i, p in enumerate(points):
		if i <= 1:
			continue
		if distance(first, p) > distance(first, closest):
			continue

		closest = p
		closest_idx = i

	new_points = [closest] + points[1:closest_idx] + points[closest_idx + 1 :]

	return [first] + reorder_points(new_points)


def move_to(body, dest):
	"""
	Move a face or a shape to a particular destination
	"""

	x, y, z = dest
	dx, dy, dz = tuple(body.center)

	for p in body.points:
		p.x += x - dx
		p.y += y - dy
		p.z += z - dz

	body.center = calc_centroid(body.points)


def translate(body, offset):
	"""
	Move a face or a shape by an offset
	"""

	x, y, z = offset

	for p in body.points:
		p.x += x
		p.y += y
		p.z += z

	body.center = calc_centroid(body.points)


def scale(body, factor):
	"""
	Scales a face or a shape by a given factor
	"""

	x, y, z = body.center

	body.move_to(0, 0, 0)

	for p in body.points:
		p.x = factor * p.x
		p.y = factor * p.y
		p.z = factor * p.z

	body.center = calc_centroid(body.points)

	body.move_to(x, y, z)


def rotate(body, rot_vect, rad):
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

	x, y, z = body.center
	body.move_to(0, 0, 0)

	for p in body.points:
		p_quat = (0, p.x, p.y, p.z)
		_, p.x, p.y, p.z = quat_mul(
			quat_mul(q, p_quat),
			q_conj,
		)

	body.center = calc_centroid(body.points)
	body.move_to(x, y, z)
