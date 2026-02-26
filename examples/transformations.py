import math
import modelmaker as mm

# create a triangle
triangle = mm.Face([
	(0, 0, 0),
	(1, 0, 0),
	(0, 1, 0),
])

# translate the triangle 10 units in the +x direction
triangle.translate(10, 0, 0)

# rotate the triangle pi radians around its y axis
triangle.rotate((0, 1, 0), math.pi / 2)

# scale the triangle by a factor of 2
triangle.scale(2)

# extrude the triangle to create a triangular prism
prism = mm.extrude(triangle, (0, 0, 1))

# render the scene
mm.render([prism])
