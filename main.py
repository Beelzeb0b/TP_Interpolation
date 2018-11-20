from abc import ABCMeta, abstractmethod, abstractproperty

# Interpolation
class Interpolation:
	__metaclass__ = ABCMeta

	#-----------------------------------------
	# PROPERTIES
	#-----------------------------------------

	#
	N = 0
	
	#
	a = 0
	
	#
	b = 0

	#-----------------------------------------
	# CONSTRUCTOR
	#-----------------------------------------

	@abstractmethod
	def __init__(self, N, a, b):
		self.N = N
		self.a = a
		self.b = b

	#-----------------------------------------
	# METHODS
	#-----------------------------------------

	@abstractmethod
	def Function(self, x):
		return (4*x**3-3*x-4)/(5*x**2+x+1);

	@abstractmethod
	def InterpolationPolynomiale(self):
		pass

	@abstractmethod
	def InterpolationContinue(self):
		pass

	@abstractmethod
	def InterpolationSpline(self):
		pass

	@abstractmethod
	def CalculErreur(self):
		pass

# InterpolationUnidimensionnele
class InterpolationUnidimensionnele(Interpolation):

	def InterpolationPolynomiale(self):
		pass

	def InterpolationContinue(self):
		pass

	def InterpolationSpline(self):
		pass

# InterpolationBidimensionnele
class InterpolationBidimensionnele(Interpolation):

	def InterpolationPolynomiale(self):
		pass

	def InterpolationContinue(self):
		pass

	def InterpolationSpline(self):
		pass


def main():
	test = InterpolationUnidimensionnele(10, 10, 1)
	print(test.N)


if __name__ == "__main__":
	main()