import pyray as pr

from . import cameraops as co
from .. import utils as ut


def setup():
	"""
	Sets up the window and the camera

	returns the main camera instance
	"""

	pr.set_config_flags(pr.FLAG_MSAA_4X_HINT)
	pr.init_window(500, 500, "Model Maker")
	pr.set_window_state(pr.FLAG_WINDOW_RESIZABLE)
	pr.set_target_fps(24)
	pr.rl_disable_backface_culling()

	camera = co.setup()

	return camera


def calc_triangles(primitives):
	"""
	Triangulates all faces
	"""

	faces = []

	for p in primitives:
		if ut.is_face(p):
			faces.append(p)
		elif ut.is_shape(p) or ut.is_group(p):
			faces.extend(p.faces)

	for f in faces:
		f._calc_triangles()


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

	pr.draw_sphere(tuple(point), 0.02, pr.BLACK)


def draw_primitives(primitives):
	"""
	Renders a list of primitives to the window
	"""

	for p in primitives:
		if ut.is_group(p):
			draw_primitives(p.members)
		elif ut.is_shape(p):
			draw_3d_shape(p)
		elif ut.is_face(p):
			draw_2d_face(p)
		elif ut.is_point(p):
			draw_point(p)

def draw_grid(num, space):
	for line in range(-num, num, space):
		color = pr.BLACK if line == 0 else pr.LIGHTGRAY
		distance = num * space
		xline = (
			(-distance, line, 0),
			(distance, line, 0),
		)
		yline = (
			(line, -distance, 0),
			(line, distance, 0),
		)

		pr.draw_line_3d(*xline, color)
		pr.draw_line_3d(*yline, color)


def render(primitives):
	camera = setup()
	calc_triangles(primitives)

	while not pr.window_should_close():
		co.update(camera)
		pr.begin_drawing()
		pr.clear_background(pr.WHITE)
		pr.begin_mode_3d(camera)

		draw_primitives(primitives)
		draw_grid(100, 1)

		pr.end_mode_3d()
		pr.end_drawing()

	pr.close_window()
