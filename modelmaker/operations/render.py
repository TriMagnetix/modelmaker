import pyray as pr


def setup():
	"""
	Sets up the window and the camera

	returns the main camera instance
	"""

	pr.init_window(500, 500, "Model Maker")
	pr.set_target_fps(60)
	pr.rl_disable_backface_culling()

	camera = pr.Camera()
	camera.position = (-7, 7, 7)
	camera.target = (0, 0, 0)
	camera.up = (0, 1, 0)
	camera.fovy = 45
	camera.projection = pr.CAMERA_PERSPECTIVE

	return camera


def calculate_triangles(primitives):
	"""
	Triangulates all faces
	"""

	faces = []

	for p in primitives:
		if type(p).__name__ == "Face":
			faces.append(p)
		elif type(p).__name__ == "Shape":
			faces.extend(p.faces)

	for f in faces:
		f._calculate_triangles()
		f._calculate_outline()


def draw_3d_shape(shape):
	"""
	Renders 3d shapes to the window
	"""

	for f in shape.faces:
		draw_2d_face(f)


def draw_2d_face(face):
	"""
	Renders 2d faces to the window

	Triangles can be passed to the function to avoid recalculating them
	"""

	for t in face.triangles:
		pr.draw_triangle_3d(*t, pr.GREEN)

	for o in face.outline:
		pr.draw_line_3d(*o, pr.DARKGREEN)


def draw_point(point):
	"""
	Renders individual points to the window
	"""

	pr.draw_sphere(tuple(point), 0.05, pr.BLACK)


def draw_primitives(primitives):
	"""
	Renders a list of primitives to the window
	"""

	for p in primitives:
		class_name = type(p).__name__

		if class_name == "Shape":
			draw_3d_shape(p)
		elif class_name == "Face":
			draw_2d_face(p)
		elif class_name == "Point":
			draw_point(p)


def render(primitives):
	camera = setup()
	calculate_triangles(primitives)

	while not pr.window_should_close():
		pr.begin_drawing()
		pr.clear_background(pr.WHITE)
		pr.begin_mode_3d(camera)

		draw_primitives(primitives)
		pr.draw_grid(100, 1)

		pr.end_mode_3d()
		pr.end_drawing()

	pr.close_window()
