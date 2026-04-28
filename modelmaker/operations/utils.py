def is_type(primitive, t):
	class_name = type(primitive).__name__
	base_names = [ b.__name__ for b in type(primitive).__bases__ ]

	return class_name == t or t in base_names

def is_point(primitive):
	return is_type(primitive, "Point")

def is_face(primitive):
	return is_type(primitive, "Face")

def is_shape(primitive):
	return is_type(primitive, "Shape")
