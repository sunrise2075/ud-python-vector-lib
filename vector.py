class Vector():

	def __init__(self, coordinates):
		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple(coordinates)
			self.dimension = len(coordinates)
		except ValueError:
			new ValueError('The coordinates must not be empty')

		except TypeError:
			new TypeError('The coordinates must not be an iterable')

	def __str__(self):
		return "Vector: {}".format(self.coordinates)

	def __eq__(self, vector):
		return self.coordinates == vector.coordinates