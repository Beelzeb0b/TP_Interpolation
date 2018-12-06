from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

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
	point = {'x':[],'y':[]} # faire en sorte que point[y][index] et point[x][index]

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
	def Function(self, x):
		return 1/x#(4*x**3-3*x-4)/(5*x**2+x+1)

	@abstractmethod
	def CreatePoint(self):
		for i in np.linspace(self.a, self.b, self.N):
			self.point['x'].append(i)
			self.point['y'].append(self.Function(i))

	@abstractmethod
	def DividedDifference(self, yPoint):
		nbElement = len(yPoint)
		if nbElement == 2:
			return (yPoint[1] - yPoint[0]) / (self.point['x'][1] - self.point['x'][0])
		else:
			return (self.DividedDifference(yPoint[1:nbElement])) - self.DividedDifference(yPoint[0:nbElement-1]) / (self.point['x'][nbElement-1] - self.point['x'][0])

	@abstractmethod
	def InterpolationPolynomiale(self, x):
		pass	

	@abstractmethod
	def InterpolationContinue(self, x):
		pass

	@abstractmethod
	def InterpolationSpline(self, x):
		pass

	@abstractmethod
	def CalculErreur(self):
		pass

# InterpolationUnidimensionnele
class InterpolationUnidimensionnele(Interpolation):

	#
	def InterpolationPolynomiale(self, x):
		# y[x0]
		result = self.point['y'][0]

		# Newton Formula
		for i in range(1,self.N):
			# Y'th divided difference
			otherY = self.DividedDifference(self.point['y'][:i+1])

			# Generate all the (x - xN)
			for j in range(0,i):
				otherY *= (x - self.point['x'][j])

			# Add the current B to the final result
			result += otherY

		return result

	#
	def InterpolationContinue(self, x):
		for i in np.linspace(self.a, self.b, self.N):
			x = a + (b-a/N) * i

	#
	def InterpolationSpline(self, x):
		pass

# InterpolationBidimensionnele
class InterpolationBidimensionnele(Interpolation):

	#
	def InterpolationPolynomiale(self, x):
		pass

	#
	def InterpolationContinue(self, x):
		pass

	#
	def InterpolationSpline(self, x):
		pass


def main():
	test = InterpolationUnidimensionnele(1, 10, 10)
	test.CreatePoint()

	x = 5

	#print(test.point['x'])
	#print(test.point['y'])

	#plt.plot(test.point[0],test.point[1])
	#plt.xlabel("$x$")
	#plt.ylabel("$y$")
	#plt.grid(True)
	#plt.show()

	print("Function    : {}".format(test.Function(x)))
	print("Polynomiale : {}".format(test.InterpolationPolynomiale(x)))


if __name__ == "__main__":
	#sys.setrecursionlimit(100000)
	main()