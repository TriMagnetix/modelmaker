import modelmaker as mm

# create a single point
origin = mm.Point(0, 0, 0)

# create a 2d face from a list of tuples, or a group of points
triangle = mm.Face([
	(0, 0, 0),
	(1, 0, 0),
	(0, 1, 0),
])

# create a 3d shape from a group of tuples, or a group of faces
tetrahedron = mm.Shape([
	[
		(0, 0, 0),
		(1, 0, 0),
		(0, 1, 0),
	],
	[
		(0, 0, 0),
		(0, 0, 1),
		(1, 0, 0),
	],
	[
		(0, 0, 0),
		(0, 0, 1),
		(0, 1, 0),
	],
	[
		(0, 0, 1),
		(1, 0, 0),
		(0, 1, 0),
	],
])

# render a group of primitives to the screen, and navigate the scene via mouse
mm.render([
	origin,
	triangle,
	tetrahedron
])
