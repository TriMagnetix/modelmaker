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

		for t in triangles:
			p1, p2, p3 = t
			norm = ut.triangle_norm(t)

			write_data(norm)
			write_data(p1)
			write_data(p2)
			write_data(p3)
			file.write(struct.pack('<h', 0)) # attribute byte count (unspecified)
