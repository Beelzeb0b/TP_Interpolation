from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
from PIL import Image
import scipy.misc


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

	def __init__(self, a, b, N):
		self.a = a
		self.b = b
		self.N = N

	#-----------------------------------------
	# METHODS
	#-----------------------------------------

	def Function(self, x):
		return 1/(1+x**2) #np.sin(x) #(4*x**3-3*x-4)/(5*x**2+x+1)

	def CreatePoint(self):
		for i in np.linspace(self.a, self.b, self.N):
			self.point['x'].append(i)
			self.point['y'].append(self.Function(i))

	def DividedDifference(self, i):
		return (self.point['y'][i+1] - self.point['y'][i]) / (self.point['x'][i+1] - self.point['x'][i])

	def NewtonCoef(self, y):
		nbElement = len(y)

		# Make a copy the y point array
		dividedDiff = np.copy(y)

		# Calculate all the divided difference
		for i in range(1,nbElement):
			dividedDiff[i:nbElement] = (dividedDiff[i:] - dividedDiff[i-1])/(self.point['x'][i:] - self.point['x'][i-1])

		return dividedDiff

	@abstractmethod
	def PolynomialeInterpolation(self, x):
		pass	

	@abstractmethod
	def PiecewiseInterpolation(self, x):
		pass

	@abstractmethod
	def ClampedCubicSplineInterpolation(self, x):
		pass

	# Probably need some rework to work with all function
	def Error(self, yFunc, yCalculated):
		yError = []
		for i in range(self.N):
			yError.append(yFunc[i] - yCalculated[i])
		return yError

# OneDInterpolation
class OneDInterpolation(Interpolation):

	# FAIRE RUNGE
	def PolynomialeInterpolation(self, x):
		# y[x0]
		result = self.point['y'][0]

		# Get an array of the divided difference
		dividedDifference = self.NewtonCoef(self.point['y'])

		# Newton Formula
		for i in range(1,self.N):
			# i'th divided difference
			otherY = dividedDifference[i]

			# Generate all the (x - xN)
			for j in range(0,i):
				otherY *= (x - self.point['x'][j])

			result += otherY

		return result

	# W.I.P. working on the 2d piecewise
	def PiecewiseInterpolation(self, x, x0, x1, y0, y1):#
		x0 = int(x0)
		x1 = int(x1)
		y0 = int(y0)
		y1 = int(y1)

		#loc_dx = (x1 - x0) / ptPerCouple

		#loc_x = np.arange(x0, x1+0.1, loc_dx) #+0.1 to include the stop number

		a = (self.point['y'][i+1] - self.point['y'][i]) / (self.point['x'][i+1] - self.point['x'][i])
		b = - (self.point['x'][i]*self.point['y'][i+1] - self.point['x'][i+1] * self.point['y'][i]) / (self.point['x'][i+1] - self.point['x'][i])

		return a * x + b

	# Piecewise interpolation that take an x as param
	def PiecewiseInterpolationX(self, x):
		# Find the interval for the x param
		# i -> the index of x0/y0
		i = -1
		for e in self.point['x']:
			if e >= x:
				break
			i = i + 1

		# Get the right y
		a = (self.point['y'][i+1] - self.point['y'][i]) / (self.point['x'][i+1] - self.point['x'][i])
		b = - (self.point['x'][i]*self.point['y'][i+1] - self.point['x'][i+1] * self.point['y'][i]) / (self.point['x'][i+1] - self.point['x'][i])

		return a * x + b

	'''
	# First version of the PiecewiseInterpolation
	def PiecewiseInterpolation(self, i, ptPerCouple):
		x0 = self.point['x'][i]
		x1 = self.point['x'][i+1]
		y0 = self.point['y'][i]
		y1 = self.point['y'][i+1]

		loc_dx = (x1 - x0) / ptPerCouple

		loc_x = np.arange(x0, x1+0.1, loc_dx) #+0.1 to include the stop number

		a = (y1 - y0) / (x1 - x0)
		b = - (x0*y1 - x1 * y0) / (x1 - x0)

		return (loc_x, a * loc_x + b)'''

	# W.I.P.
	def ClampedCubicSplineInterpolation(self, ptPerCouple):
		p = []
		#p[0] = #derivé de s(self.a) -> ?
		#p[self.N] = #derivé de s(self.b) -> ?

		# Generate all the P
		for i in range(1, self.N-1):
			# HOW TO GET p[i] ?!?!
			#p[i] = ???

			#p[i] = s'[x[i]]
			#p[i+1] = s'[x[i+1]]
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
		
		return (xPoint, s)

# TwoDInterpolation
class TwoDInterpolation(OneDInterpolation):

	point = [[]]

	def loadImage(self, image):
		img = Image.open(image).convert('L')
		self.point = np.asarray(img)

	def saveImage(self, image):
		scipy.misc.imsave(image, self.point)

	#
	def PolynomialeInterpolation_2d(self, x):
		newImage = [[]]

		#for x in range(len(self.point[0])):
		#	self.PolynomialeInterpolation(self.point)

		#for y in range(len(self.point)):
		#	pass

	# Test function for PiecewiseInterpolation_2d
	def test(self, x, x0, x1, y0, y1, Q0, Q1):
		x0 = int(x0)
		x1 = int(x1)
		y0 = int(y0)
		y1 = int(y1)

		return ((x1 - x) / (x1 - x0)) * Q0 + ((x - x0) / (x1 - x0)) * Q1


	#
	def PiecewiseInterpolation_2d(self, ptPerCouple):
		newImage = []

		# Generate new X
		for y in range(len(self.point)-1):
			newImage.append([])
			newImage[y].append(self.point[y][0])
			for x in range(len(self.point[0])-1):
				#[y].append(self.test(x, x, x+1, y, y+1, self.point[y][x], self.point[y][x+1]))
				xp = self.PiecewiseInterpolation(x, x, x+1, y, y+1, ptPerCouple)
				#print(xp)
				newImage[y].append(xp*self.point[y][x])
				#newImage[y].extend(yp)
				newImage[y].append(self.point[y][x+1])
		
		#(yp, xp) = self.PiecewiseInterpolation(0, 0+1, 0, 0+1, 1)
		#print(xp)
		# Generate new Y
		'''for y in range(0, (len(newImage)*2)-2, 2):
			newImage.insert(y+1, [])
			newImage[y+1].append(newImage[y][x])
			for x in range(len(newImage[0])-2):
				#newImage[y+1].append(self.PiecewiseInterpolation(newImage[y][x], newImage[y+2][x], newImage[y][x], newImage[y][x+2], ptPerCouple))
				newImage[y+1].append(self.test(y, y, y+1, x, x+1, newImage[y][x], newImage[y+2][x]))
			newImage[y+1].append(newImage[y][x])'''

		self.point = newImage

	#
	def ClampedCubicSplineInterpolation_2d(self, x):
		pass


def main():
	nbPoint = 10

	a = -10
	b = 10

	xFunc = []
	yFunc = []

	xPoly = []
	yPoly = []

	xInterval = []
	yInterval = []

	xSpline = []
	ySpline = []

	'''Bi = TwoDInterpolation(a, b, nbPoint)
	Bi.loadImage('image.png')
	Bi.PiecewiseInterpolation_2d(2)
	Bi.saveImage('output.png')'''

	Uni = OneDInterpolation(a, b, nbPoint)
	
	Uni.CreatePoint()

	# 
	for x in np.linspace(a, b, 100):#
		xFunc.append(x)
		yFunc.append(Uni.Function(x))
		xPoly.append(x)
		yPoly.append(Uni.PolynomialeInterpolation(x))
		xInterval.append(x)
		yInterval.append(Uni.PiecewiseInterpolationX(x))

	# Spline
	#(xp, yp) = Uni.ClampedCubicSplineInterpolation(2)
	#xSpline.extend(xp)
	#ySpline.extend(yp)

	#print(yFunc)
	#print(yPoly)
	#print(yInterval)
	#print(ySpline)

	# Show the function as well as the result of all the methods
	plt.plot(xFunc,yFunc, label="Fonction")
	plt.plot(xPoly,yPoly, '-', label="Poly degré N-1")
	plt.plot(xInterval,yInterval, '-', label="Morceaux degré 1")
	#plt.plot(xSpline,ySpline, '-', label="Spline")
	plt.xlabel("$x$")
	plt.ylabel("$y$")
	plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
	plt.grid(True)
	plt.show()


if __name__ == "__main__":
	#sys.setrecursionlimit(1000)
	main()