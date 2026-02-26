import modelmaker as mm


def extrude(face, direction):
	x, y, z = direction

	end = tuple((p.x + x, p.y + y, p.z + z) for p in face.points)

	new_faces = []

	face_points = tuple(face.points)

	for i in range(len(face_points)):
		new_face = mm.Face(
			[
				face_points[i],
				end[i],
				face_points[(i + 1) % len(face_points)],
				end[(i + 1) % len(end)],
			]
		)

		new_faces.append(new_face)

	return mm.Shape([face_points] + new_faces + [end])
