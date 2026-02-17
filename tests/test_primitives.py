import modelmaker as mm

def test_point():
	p = mm.Point(1, 2, 3)

	assert p.x == 1
	assert p.y == 2
	assert p.z == 3

def test_face():
	f = mm.Face([
		(0, 0, 0),
		(1, 0, 0),
		(0, 1, 0),
	])

	assert len(f.points) == 3

	for p in f.points:
		assert type(p).__name__ == 'Point'

def test_shape():
	s = mm.Shape([
		[
			(0, 0, 0),
			(1, 0, 0),
			(0, 1, 0),
		],
		[
			(0, 0, 0),
			(0, 0, 1),
			(0, 1, 0),
		],
		[
			(0, 0, 0),
			(0, 0, 1),
			(1, 0, 0),
		],
		[
			(0, 0, 1),
			(1, 0, 0),
			(0, 1, 0),
		],
	])

	assert len(s.faces) == 4

	for f in s.faces:
		assert type(f).__name__ == 'Face'
