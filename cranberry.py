# Imaginary number.
nan = float("nan")

# Absolutely.
def abs(i):
	return i < 0 and -i or i

# Floor to integer.
def floor(i):
	return (i - i%1) - (i%1 < 0 and 1 or 0)

# Ceil to integer.
def ceil(i):
	return (i - i%1) + (i%1 > 0 and 1 or 0)

# Square root with precision of 7.
def sqrt(i):
	if i <= 1:
		return i
	elif i < 0:
		return nan # Imaginary.

	a = i/2
	b = a + (i/a)/2

	while abs(a - b) >= 0.0000001: # Precision.
		a = b
		b = (a + (i/a))/2

	return b

# Check if it's a python number.
def isnum(i):
	return type(i) == int or type(i) == float or type(i) == complex

# Flattens a multi-dimensional array into a 1D array. Neat stuff yo.
def flat(l):
	r = []

	for x in range(len(l)):
		if type(l[x]) == list:
			l[x] = flat(l[x])

			for y in range(len(l[x])):
				r.append(l[x][y])
		else:
			r.append(l[x])

	return r

''' Vectors.

	Property
		Number v[n]
			Number assigned to the vector. These are proportional from
			what you've inputted upon creating the object.
			Index it via `Vector.v0, Vector.v1, Vector.v2, ...`

		Integer length (read-only)
			Total number of dimensions of the vector.

	Method
		.__init__(v0, v1, ...)
			Create a vector. The length is fixed as soon as you create
			it.

		.Guass_Jordan(matrix, dimensions, constant)
			Guass-Jordan Elimination (or Guassian Elimination).
			Matrices can be of any size, but some of them will be
			unused (matrix too big, etc).

		.magnitude()
			Returns the total width of the vector from it's origin.

		.unit()
			The equivalent of the vector if it has a magnitude of 1.

	Arithmetic
		Addition, Subtraction, Multiplication, Division, Floor Division
'''
class Vector:
	def __init__(self, *tuple):
		self(*tuple) # Redirect.

	def __call__(self, *tuple):
		# Setup keys similarly to an array for easier manipulation.
		if not tuple or not len(tuple):
			raise ValueError(
				"Attempted to create a vector with no dimensions!"
			)
		elif type(tuple[0]) == tuple or type(tuple[0]) == list:
			if len(tuple) > 2:
				raise ValueError(
					"Invalid 'vector.init' parameters!"
				)
			elif len(tuple) == 1 or not isnum(tuple[1]):
				self.length = len(tuple[0])
			elif len(tuple[0]) < tuple[1]:
				raise ValueError(
					"Vector dimension larger than given list/tuple!"
				)
			else:
				self.length = tuple[1]

			tuple = tuple[0]
		else:
			self.length = len(tuple)

		for i in range(0, self.length):
			if not isnum(tuple[i]):
				raise ValueError("Non-number in vector!")

			setattr(self, "v" + str(i), tuple[i])

		return self

	def Gauss_Jordan(self, matrix, dim, con):
		d = [] # All the relevant rows. Ignore excess rows.
		c = [] # The vector's numbers.
		l = [] # A copy of the matrix.
		h, w = len(matrix), 0

		# Copy the matrix vectors into raw numbers.
		for i in range(h):
			temp = []
			w = max(w, matrix[i].length)

			for n in range(matrix[i].length):
				temp.append(getattr(matrix[i], "v" + str(n)))

			l.append(temp)
		
		# Copy the vector's numbers.
		for i in range(dim):
			c.append(getattr(con, "v" + str(i)))

		# Base it on which one is shorter.
		for i in range(min(dim, h)):
			d.append(i)

		print(matrix, h, w, c)

		# Exhaust all rows (make them mostly 0).
		while len(d):
			x = 0 # Start at the first element of the row.
			y = d[0] # Grab a row.

			# Make sure the element isn't 0, otherwise find a non-zero
			# inside the row.
			while x not in d and l[y][x] == 0 and x < w:
				x += 1

			# Make sure that all the elements aren't all 0's.
			if l[y][x] != 0:
				i = y # Counter.

				# Make the entire column 0s except the currently
				# selected row.
				for _ in range(h-1):
					i = (i + 1)%h # Don't change the current row.
					n = l[i][x] # The value that we'll turn into 0.
					c[i] -= n * c[y]/l[y][x] # Change the vector too.

					# Affect the entire row.
					for r in range(w):
						l[i][r] -= n * l[y][r]/l[y][x]

				# Flatten/Normalize values.
				n = l[y][x]
				c[y] /= n

				for r in range(w):
					l[y][r] /= n

			# This dimension is done. Remove it from the array.
			del d[0]

		# Modify the input.
		for i in range(h):
			matrix[i](l[i])

		# Return the new vector and matrix.
		return con(c)

	def span(self, matrix, dim):
		self.Gauss_Jordan(matrix, dim, Vector([0]*dim))

		i = 0

		for v in matrix:
			if v.magnitude() > 0:
				i += 1

		return i

	def magnitude(self):
		v = 0

		for i in range(self.length):
			i = getattr(self, "v" + str(i))
			v += i*i

		return sqrt(v)

	def unit(self):
		m = self.magnitude()
		l = []

		for i in range(self.length):
			l.append(getattr(self, "v" + str(i))/m)

		return Vector(*tuple(l))

	def __proof(self, that):
		if type(that) != Vector or self.length != that.length:
			raise Exception(
				"You can only do arithmetics " +
				"with vectors of the same length!"
			)

	def scale(self, that):
		self.__proof(that)

		for i in range(self.length):
			setattr(
				self,
				"v" + str(i),
				getattr(self, "v" + str(i)) *
				getattr(that, "v" + str(i))
			)

		return self;

	def add(self, that):
		self.__proof(that)

		for i in range(self.length):
			setattr(
				self,
				"v" + str(i),
				getattr(self, "v" + str(i)) +
				getattr(that, "v" + str(i))
			)

		return self;

	def __add__(self, that):
		self.__proof(that)

		l = []

		for i in range(self.length):
			l.append(
				getattr(self, "v" + str(i)) +
				getattr(that, "v" + str(i))
			)

		return Vector(*tuple(l))

	def __sub__(self, that):
		self.__proof(that, flag)

		l = []

		for i in range(self.length):
			l.append(
				getattr(self, "v" + str(i)) -
				getattr(that, "v" + str(i))
			)

		return Vector(*tuple(l))

	def __mul__(self, that):
		l = []
		r = range(self.length)

		if type(that) == int:
			for i in r:
				l.append(getattr(self, "v" + str(i)) * that)

			return Vector(*tuple(l))

		self.__proof(that)

		for i in r:
			l.append(
				getattr(self, "v" + str(i)) *
				getattr(that, "v" + str(i))
			)

		return Vector(*tuple(l))

	def __truediv__(self, that):
		l = []
		r = range(self.length)

		if type(that) == int:
			for i in r:
				l.append(getattr(self, "v" + str(i)) / that)

			return Vector(*tuple(l))

		self.__proof(that)

		for i in r:
			l.append(
				getattr(self, "v" + str(i)) /
				getattr(that, "v" + str(i))
			)

		return Vector(*tuple(l))

	def __floordiv__(self, that):
		l = []
		r = range(self.length)

		if type(that) == int:
			for i in r:
				l.append(getattr(self, "v" + str(i)) // that)

			return Vector(*tuple(l))

		self.__proof(that)

		for i in r:
			l.append(
				getattr(self, "v" + str(i)) //
				getattr(that, "v" + str(i))
			)

		return Vector(*tuple(l))

	def __repr__(self):
		s = "("

		for i in range(self.length):
			s += str(getattr(self, "v" + str(i))) + ", "

		return s[:-2] + ")"

	def __str__(self):
		s = "("

		for i in range(self.length):
			s += str(getattr(self, "v" + str(i))) + ", "

		return s[:-2] + ")"

mat = [
	Vector(1, -3),
	Vector(4, -12),
]

print(Vector(5,7,8).Gauss_Jordan(
	mat,
	2,
	Vector(7, 6)
), mat)

mat = [
	Vector(1, -3),
	Vector(4, -12),
]

print(Vector(5,7,8).span(
	mat,
	2
))

print(abs)