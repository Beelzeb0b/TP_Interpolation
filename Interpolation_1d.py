from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import math
from PIL import Image

from Interpolation import Interpolation

class Interpolation_1d(Interpolation):

	#-----------------------------------------
	# PROPERTIES
	#-----------------------------------------

	# Number of point
	N = 0
	
	# Start of the interval
	a = 0
	
	# End of the interval
	b = 0
	
	# Array of the function point
	point = {'x':[],'y':[]}

	#-----------------------------------------
	# CONSTRUCTOR
	#-----------------------------------------

	def __init__(self, a, b, N):
		self.a = a
		self.b = b
		self.N = N
		self.point = {'x':[],'y':[]}

	#-----------------------------------------
	# METHODS
	#-----------------------------------------

	# 
	def Function(self, x):
		return 1/(1+x**2) # (4*x**3-3*x-4)/(5*x**2+x+1)

	# Use the "Function" to create new point (used to interpolate)
	def CreatePoint(self):
		for i in np.linspace(self.a, self.b, self.N):
			self.point['x'].append(i)
			self.point['y'].append(self.Function(i))

	# Calculate the error of a method over the function
	# Probably need some rework to work with all function
	# yFunc : the function value
	# yCalculated : method result to compare with
	def Error(self, yFunc, yCalculated):
		yError = []
		for i in range(self.N):
			yError.append(abs(yFunc[i] - yCalculated[i]))
		return yError

	# Polynomial interpolation
	def PolynomialInterpolation(self, x):
		return super().PolynomialInterpolation(x, self.point['x'], self.point['y'])

	# Piecewise interpolation
	def PiecewiseInterpolation(self, x0, x1, y0, y1, ptPerCouple):
		return super().PiecewiseInterpolation(x0, x1, y0, y1, ptPerCouple)

	# Piecewise interpolation that take an x as param
	def PiecewiseInterpolationX(self, x):
		return super().PiecewiseInterpolationX(x, self.point['x'], self.point['y'])

	# W.I.P.
	def ClampedCubicSplineInterpolation(self, x):
		p = super().SplineEquation(self.point['x'], self.point['y'])
		return super().ClampedCubicSplineInterpolation(x, self.point['x'], self.point['y'], p)