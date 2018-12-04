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
		for i in range(0,self.N-2):
			self.point[1][i] + (x - self.point[0][i]) * self.Derivative(i)

	@abstractmethod
	def Derivative(index):
		return (self.point[1][index+1] - self.point[1][index]) / (self.point[0][index+1] - self.point[0][index])

	@abstractmethod
	def InterpolationContinue(self):
		pass

	@abstractmethod
	def InterpolationSpline(self):
		pass

	@abstractmethod
	def CalculErreur(self):
		pass
		
	@abstractmethod
	def b2(self,x, index):
		return (Derivative(self.point[0][index+2] - Derivative(self.point[0][index])/(self.point[0][index+2]- self.point[0][index])
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
	test = InterpolationUnidimensionnele(1, 10, 10)
	test.CreatePoint()
	print(test.point)


if __name__ == "__main__":
	main()