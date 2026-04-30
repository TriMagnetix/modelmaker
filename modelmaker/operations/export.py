import struct
import modelmaker as mm

from .. import utils as ut

def stl(primitives, name='model'):
	primitives = ut.unpack_groups(primitives)
	faces = [ p for p in primitives if ut.is_face(p) ]
	shapes = [ p for p in primitives if ut.is_shape(p) ]
	
	for s in shapes:
		faces.extend(s.faces)

	triangles = []

	for f in faces:
		f._calc_triangles()
		triangles.extend(f.triangles)
	
	with open(f'{name}.stl', 'wb') as file:
		file.write(b'\0' * 80) # header (ignored)
		file.write(struct.pack('<i', len(triangles))) # num facets

		def write_data(data):
			for n in data:
				file.write(struct.pack('<f', n))

		for (p1, p2, p3) in triangles:
			vect1 = mm.Point(*p2) - mm.Point(*p1)
			vect2 = mm.Point(*p3) - mm.Point(*p1)
			norm = (
				vect1.y * vect2.z - vect1.z * vect2.y,
				- (vect1.x * vect2.z - vect1.z * vect2.x),
				vect1.x * vect2.y - vect1.y * vect2.x,
			)

			write_data(norm)
			write_data(p1)
			write_data(p2)
			write_data(p3)
			file.write(struct.pack('<h', 0)) # attribute byte count (unspecified)
