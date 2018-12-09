from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import enum


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
	def CalculErreur(self, yFunc, yInterpol):
		yErreur = []
		for i in range(self.N):
			yErreur.append(yFunc[i] - yInterpol[i])
		return yErreur

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
	def InterpolationContinue(self, i):
		dx = (self.b - self.a) / self.N

		x = self.point['x'][i]
		x1 = self.point['x'][i+1]

		loc_dx = (self.point['x'][i+1] - self.point['x'][i]) / self.N

		a = (self.point['y'][i+1] - self.point['y'][i]) / (self.point['x'][i+1] - self.point['x'][i])
		b = - (self.point['x'][i]*self.point['y'][i+1] - self.point['x'][i+1] * self.point['y'][i]) / (self.point['x'][i+1]-self.point['x'][i])

		loc_x = np.arange(self.point['x'][i], self.point['x'][i+1], loc_dx)

		return (loc_x, loc_x * a + b)

	#
	def InterpolationSpline(self, x):
		pass

# InterpolationBidimensionnele
class InterpolationBidimensionnele(InterpolationUnidimensionnele):

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

	a = 1
	b = 10

	#POLYNOMIAL BUG SI b > nbPoint

	Uni = InterpolationUnidimensionnele(a, b, nbPoint)
	
	Uni.CreatePoint()

	x = 19

	xPoint = []
	yFunc = []
	yPoly = []

	xInterval = []
	yInterval = []
	for i in range(nbPoint-1):
		(xp, yp) = Uni.InterpolationContinue(i)
		xInterval.extend(xp)
		yInterval.extend(yp)

	#print("Fonction             : {}".format(Uni.Function(x)))
	#print("Polynomiale          : {}".format(Uni.InterpolationPolynomiale(x)))
	#print("Interval de degré 1  : {}".format(Uni.InterpolationContinue(x)))

	
	# calcul y de la fonction selon x
	# determine y avec interpolation polynomial selon x
	for x in np.linspace(a, b, 100):
		xPoint.append(x)
		yFunc.append(Uni.Function(x))
		yPoly.append(Uni.InterpolationPolynomiale(x))
		#yInterval.append(Uni.InterpolationContinue(x))
		
	print(Uni.CalculErreur(yFunc, yPoly))
	#print(Uni.point['y'][1])
	#print(yFunc[1])
	#print(yPoly[1])
	

	#print(yFunc)
	#print(yPoly)
	#print(yInterval)

	# Affich la fonction, le resultat de l'interpolation poly
	plt.plot(xPoint,yFunc, label="Fonction")
	plt.plot(xPoint,yPoly, label="Poly degré N-1")
	plt.plot(xInterval,yInterval, label="Morceaux degré 1")
	plt.xlabel("$x$")
	plt.ylabel("$y$")
	plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
	plt.grid(True)
	plt.show()


if __name__ == "__main__":
	#sys.setrecursionlimit(1000)
	main()