import math
import pyray as pr

def setup():
	'''
	Sets up the camera

	returns the camera instance
	'''

	camera = pr.Camera()
	camera.position = (-7, 7, 7)
	camera.target = (0, 0, 0)
	camera.up = (0, 1, 0)
	camera.fovy = 45
	camera.projection = pr.CAMERA_PERSPECTIVE

	return camera

def rotate(camera):
	rot_speed_h = 0.1 * (pr.get_mouse_x() / pr.get_screen_width() - 0.5)
	rot_speed_v = 0.1 * (-pr.get_mouse_y() / pr.get_screen_height() + 0.5)
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
	pan_speed_h = 2 * (pr.get_mouse_x() / pr.get_screen_width() - 0.5)
	pan_speed_v = 2 * (-pr.get_mouse_y() / pr.get_screen_height() + 0.5)
	forward = pr.vector3_subtract(camera.target, camera.position)

	# relative right vector
	right = pr.vector3_cross_product(forward, camera.up)
	right = pr.vector3_normalize(right)

	# relative up vector
	up = pr.vector3_cross_product(right, forward)
	up = pr.vector3_normalize(up)

	translation = pr.vector3_add(
		pr.vector3_scale(right, pan_speed_h),
		pr.vector3_scale(up, pan_speed_v)
	)

	camera.position = pr.vector3_add(camera.position, translation)
	camera.target = pr.vector3_add(camera.target, translation)


def zoom(camera):
	forward = pr.vector3_subtract(camera.position, camera.target)
	length = pr.vector3_length(forward) 
	norm = pr.vector3_normalize(forward)

	if pr.get_mouse_wheel_move() > 0:
		camera.position = pr.vector3_add(
			pr.vector3_scale(norm, 0.9 * length),
			camera.target
		)
	else:
		camera.position = pr.vector3_add(
			pr.vector3_scale(norm, 1.1 * length),
			camera.target
		)

def update(camera):
	if pr.is_mouse_button_down(pr.MOUSE_BUTTON_LEFT):
		rotate(camera)
	elif pr.is_mouse_button_down(pr.MOUSE_BUTTON_MIDDLE):
		pan(camera)
	elif pr.get_mouse_wheel_move():
		zoom(camera)
