import pyray as pr

ref_point = (0, 0)


def setup():
	"""
	Sets up the camera

	returns the camera instance
	"""

	camera = pr.Camera()
	camera.position = (-7, 7, 7)
	camera.target = (0, 0, 0)
	camera.up = (0, 1, 0)
	camera.fovy = 45
	camera.projection = pr.CAMERA_PERSPECTIVE

	return camera


def is_in_dead_zone():
	dead_zone = 0.01
	move = pr.vector2_subtract(get_rel_mouse(), ref_point)

	return pr.vector2_length(move) < dead_zone


def rotate(camera):
	if is_in_dead_zone():
		return

	move = pr.vector2_subtract(get_rel_mouse(), ref_point)
	rot_speed_h = -0.1 * move.x
	rot_speed_v = -0.1 * move.y
	forward = pr.vector3_subtract(camera.target, camera.position)

	# relative right vector
	right = pr.vector3_cross_product(forward, camera.up)
	right = pr.vector3_normalize(right)

	# relative up vector
	up = pr.vector3_cross_product(right, forward)
	up = pr.vector3_normalize(up)

	# rotate horizontally
	camera.position = pr.vector3_rotate_by_axis_angle(
		camera.position,
		up,
		rot_speed_h,
	)

	# rotate vertically
	camera.position = pr.vector3_rotate_by_axis_angle(
		camera.position,
		right,
		rot_speed_v,
	)


def pan(camera):
	if is_in_dead_zone():
		return

	move = pr.vector2_subtract(get_rel_mouse(), ref_point)
	forward = pr.vector3_subtract(camera.target, camera.position)
	distance = pr.vector3_length(forward)
	pan_speed_h = distance / 10 * move.x
	pan_speed_v = distance / 10 * move.y

	# relative right vector
	right = pr.vector3_cross_product(forward, camera.up)
	right = pr.vector3_normalize(right)

	# relative up vector
	up = pr.vector3_cross_product(right, forward)
	up = pr.vector3_normalize(up)

	translation = pr.vector3_add(
		pr.vector3_scale(right, pan_speed_h), pr.vector3_scale(up, pan_speed_v)
	)

	camera.position = pr.vector3_add(camera.position, translation)
	camera.target = pr.vector3_add(camera.target, translation)


def zoom(camera):
	forward = pr.vector3_subtract(camera.position, camera.target)
	distance = pr.vector3_length(forward)
	norm = pr.vector3_normalize(forward)

	if pr.get_mouse_wheel_move() > 0:
		camera.position = pr.vector3_add(
			pr.vector3_scale(norm, 0.8 * distance), camera.target
		)
	else:
		camera.position = pr.vector3_add(
			pr.vector3_scale(norm, 1.25 * distance), camera.target
		)


def get_rel_mouse():
	rel_mouse_x = pr.get_mouse_x() / pr.get_screen_width() - 0.5
	rel_mouse_y = -pr.get_mouse_y() / pr.get_screen_height() + 0.5

	return (rel_mouse_x, rel_mouse_y)


def set_ref_point():
	if not (
		pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT)
		or pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_MIDDLE)
	):
		return

	global ref_point

	rel_mouse_x, rel_mouse_y = get_rel_mouse()

	ref_point = (
		rel_mouse_x,
		rel_mouse_y,
	)


def update(camera):
	set_ref_point()

	if pr.is_mouse_button_down(pr.MOUSE_BUTTON_LEFT):
		rotate(camera)
	elif pr.is_mouse_button_down(pr.MOUSE_BUTTON_MIDDLE):
		pan(camera)
	elif pr.get_mouse_wheel_move():
		zoom(camera)
