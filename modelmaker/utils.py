import math

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

def is_type(primitive, t):
	class_name = type(primitive).__name__
	base_names = [ b.__name__ for b in type(primitive).__mro__]

	return class_name == t or t in base_names

def is_primitive(primitive):
	return is_type(primitive, "Primitive")

def is_point(primitive):
	return is_type(primitive, "Point")

def is_face(primitive):
	return is_type(primitive, "Face")

def is_shape(primitive):
	return is_type(primitive, "Shape")

def is_group(primitive):
	return is_type(primitive, "Group")

def unpack_groups(primitives):
	unpacked = []

	for p in primitives:
		if is_group(p):
			members = unpack_groups(p.members)
			unpacked.extend(members)
		else:
			unpacked.append(p)
	
	return unpacked
