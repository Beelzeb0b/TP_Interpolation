from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import math
from PIL import Image

# Interpolation
class Interpolation:
	__metaclass__ = ABCMeta

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

	#
	def DividedDifference(self, x0, x1, y0, y1):
		return (y1 - y0) / (x1 - x0)

	#
	def NewtonCoef(self, xPoint, yPoint):
		nbElement = len(yPoint)

		# Make a copy the yPoint point array
		dividedDiff = np.copy(yPoint)

		# Calculate all the divided difference
		for i in range(1,nbElement):
			dividedDiff[i:nbElement] = (dividedDiff[i:] - dividedDiff[i-1])/(xPoint[i:] - xPoint[i-1])

		return dividedDiff

	#
	def PolynomialeInterpolation(self, x, xPoint, yPoint):
		# y[x0]
		result = yPoint[0]

		# Get an array of the divided difference
		dividedDifference = self.NewtonCoef(xPoint, yPoint)

		# Newton Formula
		for i in range(1,self.N):
			# i'th divided difference
			otherY = dividedDifference[i]

			# Generate all the (x - xN)
			for j in range(0,i):
				otherY *= (x - xPoint[j])

			result += otherY

		return result

	# Piecewise interpolation
	def PiecewiseInterpolation(self, x0, x1, y0, y1, ptPerCouple):#
		x0 = int(x0)
		x1 = int(x1)
		y0 = int(y0)
		y1 = int(y1)

		loc_dx = (x1 - x0) / ptPerCouple #nb point

		loc_x = np.arange(x0, x1, loc_dx) #+0.1 to include the stop number

		a = self.DividedDifference(x0, x1, y0, y1)
		b = - (x0 * y1 - x1 * y0) / (x1 - x0)

		return a * loc_x + b

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
	def ClampedCubicSplineInterpolation(self, ptPerCouple):
		p = []
		#p[0] = #derivé de s(self.a) -> ?
		#p[self.N] = #derivé de s(self.b) -> ?

		# Generate all the P
		for i in range(1, self.N-1):
			# HOW TO GET p[i] ?!?!
			#p[i] = ???

			#y[i]   = s[i](x[i])

			#p[i]   = s'[i](x[i])
			#p[i+1] = s'[i](x[i+1])

			#pi-1 + 4*pi + pi+1 = 3 * (self.DividedDifference(i) + self.DividedDifference(i-1))
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