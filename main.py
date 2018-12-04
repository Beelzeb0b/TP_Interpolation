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
		result = self.point[1][0] + (x - self.point[0][0]) * self.Derivative(0) #P1
		for i in range(1,self.N): # All the B
			print(self.B(x, 0))
		#	result += self.B(x, 0)
		#	for j in range(0,i):
		#		result *= (x - self.point[0][j])
		return result
		
	@abstractmethod
	def B(self, x, index):
		return (self.Derivative(index+2) - self.Derivative(index)) / (self.point[0][index+2]- self.point[0][index])

	@abstractmethod
	def Derivative(self, index):
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