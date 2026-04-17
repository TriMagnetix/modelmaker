import modelmaker as mm


def extrude(face, direction):
	end = [p + mm.Point(*direction) for p in face.points]
	new_faces = []

	for i in range(len(face.points)):
		new_face = mm.Face(
			[
				face.points[i],
				face.points[(i + 1) % len(face.points)],
				end[(i + 1) % len(end)],
				end[i],
			]
		)

		new_faces.append(new_face)

	return mm.Shape([face.points] + new_faces + [end])
