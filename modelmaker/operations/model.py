import modelmaker as mm

from .. import utils as ut


def extrude(face, direction):
	face._calc_triangles()

	direction = mm.Point(*direction)
	current_norm = ut.triangle_norm(face.triangles[0])
	face.flip_norms = ut.cos_similarity(current_norm, direction) > 0
	end = mm.Face([p + direction for p in face.points], not face.flip_norms)
	new_faces = []

	for i in range(len(face.points)):
		p1 = face.points[i]
		p2 = face.points[(i + 1) % len(face.points)]
		p3 = end.points[(i + 1) % len(end.points)]
		p4 = end.points[i]

		new_face = mm.Face([p1, p2, p3, p4])

		new_face._calc_triangles()

		# Get the triangle from the original face that shares an edge with the new face
		shared_triangle = next(
			t for t in face.triangles
			if tuple(p1) in t and tuple(p2) in t
		)

		# Get the point from the shared triangle that is not used in the new face
		unshared_point = mm.Point(*next(
			p for p in shared_triangle
			if p not in (tuple(p1), tuple(p2))
		))

		new_face_norm = ut.triangle_norm(new_face.triangles[0])

		# Points toward the body of the shape
		toward_body = unshared_point - face.points[i]

		# If the new face's norms are pointing inside the body, flip the norms
		new_face.flip_norms = ut.cos_similarity(new_face_norm, toward_body) > 0

		new_faces.append(new_face)

	return mm.Shape([face] + new_faces + [end])
