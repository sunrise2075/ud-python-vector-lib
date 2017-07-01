from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 15

class Vector():

	def __init__(self, coordinates):

		self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'cannot normalize the zero vector'

		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple([ Decimal(x) for x in coordinates])
			self.dimension = len(coordinates)
		except ValueError:
			raise ValueError('The coordinates must not be empty')

		except TypeError:
			raise TypeError('The coordinates must not be an iterable')


	def plus(self, v):
		new_coordinates = [x+y for x,y in zip(self.coordinates,v.coordinates)]
		return Vector(new_coordinates)

	def minus(self, v):
		new_coordinates = [x-y for x,y in zip(self.coordinates,v.coordinates)]
		return Vector(new_coordinates)

	def times_scalar(self, c):
		new_coordinates = [Decimal(c)*x for x in self.coordinates]
		return Vector(new_coordinates)

	def magnitude(self):
		coordinates_squared = [x**2 for x in self.coordinates]
		return Decimal(sqrt(sum(coordinates_squared)))

	def normalized(self):
		try:
			magnitude = self.magnitude()
			return self.times_scalar(Decimal('1.0')/magnitude)

		except ZeroDivisionError:
			raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

	def dot(self, v):
		result = sum([ x*y for x,y in zip(self.coordinates, v.coordinates)])
		return Decimal(result)

	def angle_with(self, v, in_degrees = False):
		try:
			u1 = self.normalized()
			u2 = v.normalized()

			angle_in_radians = acos(u1.dot(u2))

			if in_degrees:
				degrees_per_radian = 180./pi;
				return angle_in_radians * degrees_per_radian
			else:
				return angle_in_radians

		except Exception as e:
			if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception('cannot compute an angle with the zero vector')
			else:
				raise e

	def is_orthogonal_to(self, v, tolerance=1e-10):
		return abs(self.dot(v))<tolerance

	def is_zero(self, tolerance=1e-10):
		return self.magnitude() < tolerance


	def is_parallel_to(self, v):
		return (self.is_zero() or
				v.is_zero() or
				self.angle_with(v) ==0 or
				self.angle_with(v) == pi
				)

	def __str__(self):
		return "Vector: {}".format(self.coordinates)

	def __eq__(self, vector):
		return self.coordinates == vector.coordinates



# print "addition"

# v = Vector([8.218, -9.341]);
# w = Vector([-1.129, 2.111]);

# print v.plus(w)

# print "============"

# print "substraction"

# v = Vector([7.119, 8.215])
# w = Vector([-8.223, 0.878])

# print v.minus(w)

# print "============"

# print "scalar-multiply"

# v = Vector([1.671,-1.012, -0.318])
# c = 7.41

# print v.times_scalar(c)


# v = Vector([-0.221, 7.437])
# print v.magnitude();

# v = Vector([8.813, -1.331, -6.247])
# print v.magnitude();

# v = Vector([5.581, -2.136])
# v.normalized()



# v = Vector([1.996, 3.108, -4.554])
# v.normalized()

# v = Vector([7.887, 4.138])
# w = Vector([-8.802, 6.776])
# print v.dot(w)

# v= Vector([-5.955, -4.904, -1.874])
# w = Vector([-4.496, -8.755, 7.103])
# print v.dot(w)

# v= Vector([3.183, -7.627])
# w = Vector([-2.668, 5.319])
# print v.angle_with(w)

# v= Vector([7.35, 0.221, 5.188])
# w= Vector([2.751, 8.259, 3.985])
# print v.angle_with(w, True)
# 

# v = Vector([-7.579, -7.88])
# w = Vector([22.737, 23.64])
# print v.is_parallel_to(w)
# print v.is_orthogonal_to(w)

v = Vector([-2.029, 9.97, 4.172])
w = Vector([-9.231, -6.639, -7.245])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)


v = Vector([-2.328, -7.284, -1.214])
w = Vector([-1.821, 1.072, -2.94])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)

v = Vector([2.118, 4.827])
w = Vector([0,0])
print v.is_parallel_to(w)
print v.is_orthogonal_to(w)