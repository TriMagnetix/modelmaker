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
		new_face = mm.Face([
			face.points[i],
			face.points[(i + 1) % len(face.points)],
			end.points[(i + 1) % len(end.points)],
			end.points[i],
		])

		new_face._calc_triangles()

		new_face_norm = ut.triangle_norm(new_face.triangles[0])
		toward_center = new_face.center - face.center
		new_face.flip_norms = ut.cos_similarity(new_face_norm, toward_center) < 0

		new_faces.append(new_face)

	return mm.Shape([face] + new_faces + [end])
