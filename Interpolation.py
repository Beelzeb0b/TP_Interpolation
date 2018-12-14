from abc import ABC, abstractmethod, abstractproperty
import numpy as np
import math
from PIL import Image

# Interpolation
class Interpolation(ABC):

	#-----------------------------------------
	# PROPERTIES
	#-----------------------------------------



	#-----------------------------------------
	# CONSTRUCTOR
	#-----------------------------------------

	def __init__(self):
		pass

	#-----------------------------------------
	# METHODS
	#-----------------------------------------

	# Calculate the divided difference
	def DividedDifference(self, x0, x1, y0, y1):
		return (y1 - y0) / (x1 - x0)

	# Calculate the coef for the polynomial interpolation
	def NewtonCoef(self, xPoint, yPoint):
		nbElement = len(xPoint)

		coef = np.copy(yPoint)

		for j in range(1, nbElement):

			for i in range(nbElement-1, j-1, -1):
				coef[i] = self.DividedDifference(xPoint[i-j], xPoint[i], coef[i-1], coef[i])

		return coef

	# Polynomial interpolation
	@abstractmethod
	def PolynomialInterpolation(self, x, xPoint, yPoint):
		# y[x0]
		result = yPoint[0]

		# Get an array of the divided difference
		dividedDifference = self.NewtonCoef(xPoint, yPoint)

		# Newton Formula
		for i in range(1,len(xPoint)):#self.N
			# delta y
			otherY = dividedDifference[i]

			# Generate all the (x - xN)
			for j in range(0,i):
				otherY *= (x - xPoint[j])

			result += otherY

		return result

	# Piecewise interpolation
	@abstractmethod
	def PiecewiseInterpolation(self, x0, x1, y0, y1, ptPerCouple):
		x0 = int(x0)
		x1 = int(x1)
		y0 = int(y0)
		y1 = int(y1)

		# delta X
		dx = (x1 - x0) / ptPerCouple

		# Array of X
		x = np.arange(x0, x1, dx)

		# Piecewise formula
		a = self.DividedDifference(x0, x1, y0, y1)
		b = - (x0 * y1 - x1 * y0) / (x1 - x0)

		return a * x + b

	# Piecewise interpolation that take an x as param
	def PiecewiseInterpolationX(self, x, xPoint, yPoint):
		# Find the interval for the x param
		# i -> the index of x0/y0
		i = -1
		for e in xPoint:
			if e >= x:
				break
			i = i + 1

		# Get the right y
		a = self.DividedDifference(xPoint[i], xPoint[i+1], yPoint[i], yPoint[i+1])
		b = - (xPoint[i]*yPoint[i+1] - xPoint[i+1] * yPoint[i]) / (xPoint[i+1] - xPoint[i])

		return a * x + b


	# W.I.P.
	@abstractmethod
	def ClampedCubicSplineInterpolation(self, ptPerCouple):
		p = []
		#p[0] = #derivé de s(self.a) -> ?
		#p[self.N] = #derivé de s(self.b) -> ?

		# Generate all the P
		for i in range(1, self.N-1):
			# HOW TO GET p[i] ?!?!
			#p[i] = ???

			# Plusieurs équations :
			# pi-1 + 4*pi + pi+1 = 3 * (self.DividedDifference(i) + self.DividedDifference(i-1))
			pass

		s = []
		xPoint = []

		# Generate all the S
		for i in range(self.N-1):
			for x in range(self.point['x'][i], self.point['x'][i+1], ptPerCouple):
				xPoint[i].append(x)
				result = self.point['y'][i] + self.DividedDifference(i) * (x - self.point['x'][i])
				result += (1 / (2 * (self.point['x'][i+1] - self.point['x'][i]))) * (p[i+1] - p[i]) * (x - self.point['x'][i]) * (x - self.point['x'][i+1])
				result += (1 / (2 * (self.point['x'][i+1] - self.point['x'][i])**2)) * (p[i+1] + p[i] - 2 * self.DividedDifference(i))
				result *= (((x - self.point['x'][i])**2 * (x - self.point['x'][i+1])) + (x - self.point['x'][i]) * (x - self.point['x'][i+1])**2)
				s[i].append(result)

		# si(x) = ai + bi*(x-xi) + ci*(x-xi)**2 + di*(x-xi)**3
		# si'(x) = bi + 2*ci*(x-xi) + 3*di*(x-xi)**2
		# si''(x) = 2*ci + 6*di*(x-xi)
		
		return (xPoint, s)