from abc import ABCMeta, abstractmethod, abstractproperty
import numpy

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
	
	#
	point = [[],[]] # faire en sorte que point[y][index] et point[x][index]

	#-----------------------------------------
	# CONSTRUCTOR
	#-----------------------------------------

	@abstractmethod
	def __init__(self, a, b, N):
		self.a = a
		self.b = b
		self.N = N

	#-----------------------------------------
	# METHODS
	#-----------------------------------------

	@abstractmethod
	def CreatePoint(self):
		self.point = []
		self.point.append([])
		self.point.append([])
		for i in numpy.linspace(self.a, self.b, self.N):
			self.point[0].append(i)
			self.point[1].append(self.Function(i))

	@abstractmethod
	def Function(self, x):
		return (4*x**3-3*x-4)/(5*x**2+x+1);

	@abstractmethod
	def InterpolationPolynomiale(self, x):
		# y[x0]
		result = self.point[1][0]

		# Newton Formula
		for i in range(1,self.N):
			# Yeme différence divisé
			param = self.point[:i]
			otherY = self.Derivative(param)

			# Generate all the (x - xN)
			for j in range(0,i):
				otherY *= (x - self.point[0][j])

			# Add the current B to the final result
			result += otherY

		return result
		
	#@abstractmethod
	#def B(self, index):
	#	return (self.Derivative(index+2) - self.Derivative(index)) / (self.point[0][index+2]- self.point[0][index])

	def DividedDifference(self, param):
		nbElement = len(array)
		for i in range(0,nbElement):
			self.DividedDifference(self, param)

	#indexs = array of index
	@abstractmethod
	def Derivative(self, indexs):
		nbIndex = len(indexs)
		result = 0.0;
		#if nbIndex == 1:
		#	result = self.point[1][index[0]]
		#else:
		# CERTAINEMENT PROBLEME DANS LES INDEX : indexs[1:]
		result = (((nbIndex-1)**self.Derivative(indexs[1:])) - ((nbIndex-1)**self.Derivative(nbIndex[:-1]))) / (self.point[0][index[nbIndex-1]] - self.point[0][0])

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

	#def InterpolationPolynomiale(self):
	#	pass

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
	test = InterpolationUnidimensionnele(1, 10, 10)
	test.CreatePoint()

	x = 5

	#print(test.Function(x))
	print(test.InterpolationPolynomiale(x))
	
	#print(test.CreatePoint)


if __name__ == "__main__":
	main()