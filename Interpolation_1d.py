from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import math
from PIL import Image

from Interpolation import Interpolation

class Interpolation_1d(Interpolation):

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
		return 1/(1+x**2) #np.sin(x) #(4*x**3-3*x-4)/(5*x**2+x+1)

	#
	def CreatePoint(self):
		for i in np.linspace(self.a, self.b, self.N):
			self.point['x'].append(i)
			self.point['y'].append(self.Function(i))

	# Probably need some rework to work with all function
	def Error(self, yFunc, yCalculated):
		yError = []
		for i in range(self.N):
			yError.append(yFunc[i] - yCalculated[i])
		return yError

	#
	def PolynomialeInterpolation(self, x):
		return super().PolynomialeInterpolation(x, self.point['x'], self.point['y'])

	# Piecewise interpolation
	def PiecewiseInterpolation(self, x0, x1, y0, y1, ptPerCouple):
		return super().PiecewiseInterpolation(x0, x1, y0, y1, ptPerCouple)

	# Piecewise interpolation that take an x as param
	def PiecewiseInterpolationX(self, x):
		return super().PiecewiseInterpolationX(x, self.point['x'], self.point['y'])

	# W.I.P.
	def ClampedCubicSplineInterpolation(self, ptPerCouple):
		return super().ClampedCubicSplineInterpolation(ptPerCouple)