# Model Maker

This is a python library used for creating and visualizing 3d models. Model Maker was created with small precise model creation in mind, and it is not intended for CAD or 3d art.

## Initialize development environment

1. Create a virual environment (optional)

```bash
python -m venv ./venv
```
2. Activate the virtual environment (optional)

```bash
source ./venv/bin/activate
```
3. Install package

```bash
pip install .[test]
```
## Running tests

Tests are defined in the `tests` directory, and they can be run using pytest.

```bash
pytest
```

## Overview

### Create and render a model

The only primitives in this library are points, 2d faces, and 3d shapes. A list of points defines a 2d face, and a list of faces defines a 3d shape.

```python
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

# render a group of primitives to the screen, and navigate the scene using the mouse
mm.render([
	origin,
	triangle,
	tetrahedron
])
```

### Transformations

You can extrude faces to make a 3d shape, and you can perform transformations on a point, 2d face, or 3d shape.

```python
import math
import modelmaker as mm

# create a triangle
triangle = mm.Face([
	(0, 0, 0),
	(1, 0, 0),
	(0, 0, 1),
])

# move the triangle to the center
triangle.move_to(0, 0, 0)

# translate the triangle 10 units in the +x direction
triangle.translate(10, 0, 0)

# rotate the triangle pi radians around its y axis
triangle.rotate((0, 1, 0), math.pi / 2)

# scale the triangle by a factor of 2
triangle.scale(2)

# extrude the triangle to create a triangular prism
prism = mm.extrude(triangle, (0, 1, 0))

# render the scene
mm.render([prism])
```

### Composite Geometry

For more complex geometry, you can combine pair of 2d faces or a pair of 3d shapes.

```python
import math
import modelmaker as mm

# create a triangle
t1 = mm.Face([
	(0, 0, 0),
	(1, 0, 0),
	(0, 1, 0),
])

# create three other triangles based on t1
t2, t3, t4 = (t1.copy(), t1.copy(), t1.copy())
t2.translate(-0.5, 0, 0)
t3.scale(0.5)
t4.rotate(0.25 * math.pi)

# add t2 to t1
t1.add(t2)

# subtract t3 from t1
t1.subtract(t3)

# intersect t4 with t1
t1.instersect(t4)

# render the scene
mm.render([ t1 ])
```
