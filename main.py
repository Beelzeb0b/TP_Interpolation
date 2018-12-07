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
	point = {'x':[],'y':[]}

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
		return np.sin(x)#(4*x**3-3*x-4)/(5*x**2+x+1)

	@abstractmethod
	def CreatePoint(self):
		for i in np.linspace(self.a, self.b, self.N):
			self.point['x'].append(i)
			self.point['y'].append(self.Function(i))

	@abstractmethod
	def DividedDifference(self):
		nbElement = len(self.point['y'])

		# Make a copy the y point array
		dividedDiff = np.copy(self.point['y'])

		# Calculate all the divided difference)
		for i in range(1,nbElement):
			dividedDiff[i:nbElement] = (dividedDiff[i:nbElement] - dividedDiff[i-1])/(self.point['x'][i:nbElement] - self.point['x'][i-1])

		return dividedDiff

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

		# Get an array of the divided difference
		dividedDifference = self.DividedDifference()

		# Newton Formula
		for i in range(1,self.N):
			# i'th divided difference
			otherY = dividedDifference[i]

			# Generate all the (x - xN)
			for j in range(0,i):
				otherY *= (x - self.point['x'][j])

			result += otherY

		return result

	#
	def InterpolationContinue(self, x):
		#h = (b - a) / n
		#xi = a + h * i
		#f(xi) = yi

		# i = {0...N-1}
		#for i in np.linspace(self.a, self.b, self.N):
		i = 0
		ai = (self.point['y'][i + 1] - self.point['y'][i]) / (self.point['x'][i + 1] - self.point['x'][i])
		bi = -((self.point['x'][i] * self.point['y'][i + 1] - self.point['x'][i] + self.point['y'][i]) / (self.point['x'][i + 1] - self.point['x'][i]))

		return ai * x + bi

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
	nbPoint = 7

	Uni = InterpolationUnidimensionnele(1, 10, nbPoint)
	
	Uni.CreatePoint()

	''' EXEMPLE OF PLOT
	t = np.arange(0., 5., 0.2)
	plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
	plt.show()
	'''

	x = 3

	print("Fonction             : {}".format(Uni.Function(x)))
	print("Polynomiale          : {}".format(Uni.InterpolationPolynomiale(x)))
	print("Interval de degré 1  : {}".format(Uni.InterpolationContinue(x)))

	xPoint = []
	yFunc = []
	yPoly = []
	yInterval = []

	for x in np.linspace(1, 10, 100):
		xPoint.append(x)
		yFunc.append(Uni.Function(x))
		yPoly.append(Uni.InterpolationPolynomiale(x))
		yInterval.append(Uni.InterpolationContinue(x))

	#print(yFunc)
	#print(yPoly)
	#print(yInterval)

	plt.plot(xPoint,yFunc, xPoint,yPoly, xPoint,yInterval)
	plt.xlabel("$x$")
	plt.ylabel("$y$")
	plt.grid(True)
	plt.show()
	

if __name__ == "__main__":
	#sys.setrecursionlimit(1000)
	main()