import pyray as pr
import numpy as np
from scipy.spatial import Delaunay

triangle_cache = []


def setup():
	"""
	Sets up the window and the camera

	returns the main camera instance
	"""

	pr.init_window(500, 500, "Model Maker")
	pr.set_target_fps(60)

	camera = pr.Camera()
	camera.position = pr.Vector3(4, 4, 4)
	camera.target = pr.Vector3(0.0, 0.0, 0.0)
	camera.up = pr.Vector3(0.0, 1.0, 0.0)
	camera.fovy = 45.0
	camera.projection = pr.CAMERA_PERSPECTIVE

	return camera


def draw_3d_shape(shape):
	"""
	Renders 3d shapes to the window
	"""

	for f in shape.faces:
		draw_2d_face(f)


def draw_2d_face(face, triangles=None):
	"""
	Renders 2d faces to the window

	Triangles can be passed to the function to avoid recalculating them
	"""

	# Only triangulate the face once
	if not triangles:
		points = np.array([tuple(p) for p in face.points])
		triangles = Delaunay(points[:, :2])
		triangle_cache.push(triangles)

	# Render triangles
	for s in triangles.simplices:
		p1 = tuple(face.points[s[0]])
		p2 = tuple(face.points[s[1]])
		p3 = tuple(face.points[s[2]])

		pr.draw_triangle(p1, p2, p3, pr.GREEN)


def draw_point(point):
	"""
	Renders individual points to the window
	"""

	pr.draw_point_3d(tuple(point), pr.DARKGREY)


def draw_primitives(primitives):
	"""
	Renders a list of primitives to the window
	"""
	i = 0

	for p in primitives:
		class_name = type(p).__name__

		if class_name == "Shape":
			draw_3d_shape(p)
		elif class_name == "Face":
			triangles = (
				triangle_cache[i]
				if i < len(triangle_cache)
				else None
			)
			draw_2d_face(p, triangles)
			i += 1
		elif class_name == "Point":
			draw_point(p)


def render(primitives):
	setup()

	while not pr.window_should_close():
		pr.begin_drawing()
		pr.clear_background(pr.WHITE)

		draw_primitives(primitives)

		pr.end_drawing()

	pr.close_window()
