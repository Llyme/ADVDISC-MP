# ADVDISC S18; Michael Edmund Wong
class Vector:
	def __init__(self, *tuple):
		# User may construct via a 'list' or 'tuple' objects.
		# tuples will be converted to lists.

		# Make sure it's not an empty list.
		if not tuple or not len(tuple):
			raise ValueError(
				"Attempted to create a vector with no dimensions!"
			)

		''' See if the user is attempting to create via
			'Vector(list/tuple, int)'.
		'''
		if type(tuple[0]) == tuple or type(tuple[0]) == list:
			''' See if the the requirements are met. We only need up to
				2, a list/tuple and an integer. The integer is
				optional.
			'''
			if len(tuple) > 2:
				raise ValueError(
					"Invalid 'vector.init' parameters!"
				)
				''' See if the user only provided a list/tuple or the
					the 2nd parameter isn't an integer.
				'''
			elif len(tuple) == 1 or type(tuple[1]) == int:
				# Grab the length of the list/tuple instead.
				length = len(tuple[0])
				''' See if both are provided, but integer is smaller
					than the list/tuple's length.
				'''
			elif len(tuple[0]) < tuple[1]:
				raise ValueError(
					"Vector dimension larger than given list/tuple!"
				)
			else:
				# No errors. Neat.
				length = tuple[1]

			''' Convert to list if tuple. If list, copy it so no one
				else can modify it other than this class.
			'''
			dims = (type(tuple[0]) == tuple and
				list(tuple[0]) or tuple[0][:])
		else:
			# User is creating via 'Vector(n0, n1, n2, ...)'.
			dims = []
			length = len(tuple)

			# Make sure everything is a number.
			for i in range(0, length):
				if not Vector.__isnum(tuple[i]):
					raise ValueError("Non-number in vector!")

				dims.append(tuple[i])

		# Returns the number at the given index.
		def get(i):
			if i < 0 or i > length - 1:
				# Out of bounds.
				return None

			return dims[i]

		# Returns a copy of the list.
		def dump():
			return dims[:]

		''' Scales and directly modifies this vector to the given
			vector or number.
		'''
		def scale(v):
			if Vector.__isnum(v):
				for i in range(length):
					dims[i] *= v

				return self

			Vector.__proof(self, v)

			for i in range(length):
				dims[i] *= v(i)

			return self

		# Adds and directly modifies this vector to the given vector.
		def add(v):
			Vector.__proof(self, v)

			for i in range(length):
				dims[i] += v(i)

			return self

		# Returns the vector's distance from the origin.
		def magnitude():
			v = 0

			for n in dims:
				v += n*n

			return v**(1/2)

		# Returns a vector equivalent to this when magnitude is 1.
		def unit():
			m = magnitude()
			l = []

			for n in dims:
				l.append(n/m)

			return Vector(l)

		# Returns the total dimensions of this vector.
		def _len():
			return length

		# Hook them in the interface.
		self.get = get
		self.dump = dump
		self.scale = scale
		self.add = add
		self.magnitude = magnitude
		self.unit = unit
		self.Gauss_Jordan = Vector.Gauss_Jordan # Point to static.
		self.span = Vector.span # Point to static.
		self.len = _len

	# Return the value with the given index (Just like list[n]).
	def __call__(self, i):
		return self.get(i)

	# Guassian elimination (Gauss-Jordan elimination).
	@staticmethod
	def Gauss_Jordan(matrix, dim, con):
		# Not a list.
		if type(matrix) != list:
			return

		# Not an integer.
		if type(dim) != int:
			return

		# Not a vector.
		if type(con) != Vector:
			return

		# A sequence of numbers up to the total dimensions.
		col = []
		h = len(matrix)

		# There's nothing in the matrix.
		if not h:
			return

		w = len(matrix[0])

		# Jot down numbers up to the total dimensions.
		for i in range(h):
			# Not a vector or uneven length.
			if type(matrix[i]) != Vector or len(matrix[i]) != w:
				return

			if i < dim:
				col.append(i)

		# Matrix columns do not match with dimensions.
		if w != dim:
			return

		# Keep popping the list until there's nothing 'relevant'.
		for x in range(h):
			# Get a vector. This will be the representative.
			vec = matrix[x]
			# Counter for the selected column.
			i = 0
			# Total number of columns left.
			m = len(col)

			# Find a suitable column that doesn't have a value of 0.
			while i < m and vec(col[i]) == 0:
				i += 1

			if i < m:
				# Grab that column's number.
				i = col.pop(i)
				# Make a scalar to downscale the representative vector.
				scl = 1/vec(i)
				''' This will be the constant's value for the
					representative. It starts at 0 just in case if the
					matrix has longer columns than the constant's
					length.
				'''
				res = 0

				# Downscale to unit.
				vec.scale(scl)

				# See if there's a constant for this vector.
				if x < dim:
					# Create a mask that only affects that dimension.
					mask = [1] * dim
					mask[x] = scl

					# Downscale that as well.
					con.scale(Vector(mask))

					# Record it for future use.
					res = con(x)

				# Affect the rest of the vectors in the matrix.
				for y in range(h - 1):
					# Grab the 'true' index.
					z = (x + y + 1) % h
					# Grab the vector.
					vec2 = matrix[z]

					''' We only need to do this if the value directly
						below it isn't 0.
					'''
					if vec2(i) != 0:
						# Grab the negated value in the same column.
						scl2 = -vec2(i)

						''' Make a copy of the representative vector
							and scale it according to the value 'scl2'.
							Add that copy to the vector.
						'''
						vec2.add(vec * scl2)

						''' See if there's a constant right next to
							this vector.
						'''
						if z < dim:
							''' Create a mask that only affects that
								dimension.
							'''
							mask = [0] * dim
							mask[z] = res * scl2

							# Do the same as well.
							con.add(Vector(mask))

		# Return the constants.
		return con

	@staticmethod
	def span(matrix, dim):
		Vector.Gauss_Jordan(matrix, dim, Vector([0]*dim))

		i = 0

		for v in matrix:
			if v.magnitude() > 0:
				i += 1

		return i

	@staticmethod
	def __isnum(i):
		# Capture all possible 'number-like' classes.
		return type(i) == int or type(i) == float or type(i) == complex

	@staticmethod
	def __proof(a, b):
		# Universal argument for comparing 2 vectors.
		if type(b) != Vector or len(a) != len(b):
			raise Exception(
				"You can only do arithmetics " +
				"with vectors of the same length!"
			)

	def __add__(self, that):
		Vector.__proof(self, that)

		l = []

		for i in range(len(self)):
			l.append(self(i) + that(i))

		return Vector(l)

	def __sub__(self, that):
		Vector.__proof(self, that)

		l = []

		for i in range(len(self)):
			l.append(self(i) - that(i))

		return Vector(l)

	def __mul__(self, that):
		l = []

		if Vector.__isnum(that):
			for i in range(len(self)):
				l.append(self(i) * that)

			return Vector(l)

		Vector.__proof(self, that)

		for i in range(len(self)):
			l.append(self(i) * that(i))

		return Vector(l)

	def __truediv__(self, that):
		l = []

		if Vector.__isnum(that):
			for i in range(len(self)):
				l.append(self(i) / that)

			return Vector(l)

		Vector.__proof(self, that)

		for i in range(len(self)):
			l.append(self(i) / that(i))

		return Vector(l)

	def __floordiv__(self, that):
		l = []

		if Vector.__isnum(that):
			for i in range(len(self)):
				l.append(self(i) // that)

			return Vector(l)

		Vector.__proof(self, that)

		for i in range(len(self)):
			l.append(self(i) // that(i))

		return Vector(l)

	def __len__(self):
		return self.len()

	def __repr__(self):
		return "(" + ", ".join(str(v) for v in self.dump()) + ")"

	def __str__(self):
		return "(" + ", ".join(str(v) for v in self.dump()) + ")"