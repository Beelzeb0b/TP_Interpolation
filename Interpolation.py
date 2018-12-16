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
		
	def gauss(self, A):
		n = len(A)
	
		for i in range(0, n):
			# Search for maximum in this column
			maxEl = abs(A[i][i])
			maxRow = i
			for k in range(i+1, n):
				if abs(A[k][i]) > maxEl:
					maxEl = abs(A[k][i])
					maxRow = k
	
			# Swap maximum row with current row (column by column)
			for k in range(i, n+1):
				tmp = A[maxRow][k]
				A[maxRow][k] = A[i][k]
				A[i][k] = tmp
	
			# Make all rows below this one 0 in current column
			for k in range(i+1, n):
				c = -A[k][i]/A[i][i]
				for j in range(i, n+1):
					if i == j:
						A[k][j] = 0
					else:
						A[k][j] += c * A[i][j]
				
		# Solve equation Ax=b for an upper triangular matrix A
		x = [0 for i in range(n)]
		for i in range(n-1, -1, -1):
			x[i] = A[i][n]/A[i][i]
			for k in range(i-1, -1, -1):
				A[k][n] -= A[k][i] * x[i]
		return x
		

	def SplineEquation(self, xPoint, yPoint):
		nbElement = len(xPoint)
	
		p = []
		for i in range(0, nbElement):
			p.append(0)
		
		for i in range(1, nbElement-1):
			p[i] = 3 * (self.DividedDifference(xPoint[i+1], xPoint[i], yPoint[i+1], yPoint[i]) +  self.DividedDifference(xPoint[i], xPoint[i-1], yPoint[i], yPoint[i-1]))
			
		# init matrix as for equation system
		m=[]
		for i in range(nbElement+1):
			m.append([])
			for j in range(nbElement+2):
				m[i].append(0)
				
		# set value in equation system
		m[0][0]=1
		m[nbElement][nbElement]=1
		for i in range(1, nbElement):
			m[i][i-1] = 1
			m[i][i] = 4
			m[i][i+1] = 1
			m[i][nbElement+1] = p[i]
			
		
		
		#print(self.gauss(m))
		'''# Generate all the P[i] , i = 1..N-1
		for i in range(1, nbElement-1):
			p.append(3 * (self.DividedDifference(xPoint[i+1], xPoint[i], yPoint[i+1], yPoint[i]) +  self.DividedDifference(xPoint[i], xPoint[i-1], yPoint[i], yPoint[i-1])))
			p[i] -= p[i-1]
		
		
		#p.append(yPoint[nbElement-1]) # p[N]
		p.append(0) # p[N]
			
		for i in range(nbElement - 1, 1):
			p[i] -= p[i+1]
			p[i] /= 4'''
			
		return self.gauss(m)		

	# W.I.P.
	@abstractmethod
	def ClampedCubicSplineInterpolation(self, x, xPoint, yPoint, p):
		# Find the interval for the x param
		# i -> the index of x0/y0
		i = -1
		for e in xPoint:
			if e >= x:
				break
			i = i + 1
			
		x0 = xPoint[i]
		x1 = xPoint[i+1]
		y0 = yPoint[i]
		y1 = yPoint[i+1]
	
		dy = self.DividedDifference(x1, x0, y1, y0)
		
		#Genere S
		s = yPoint[i] + (dy * (x-x0))
		s += (1 / 2 * (x1-x0)) * (p[i+1] - p[i]) * (x-x0) * (x-x1)
		s += (1 / 2 * (x1-x0)**2) * (p[i+1] + p[i] - 2 * dy) * ((x-x0)**2 * (x-x1) + (x-x0 )*(x-x1)**2)
		
		return s
		
		'''N = len(xPoint)
		p = []
		
		p.append(yPoint[0]) # p[0]
		
		# Generate all the P[i] , i = 1..N-1
		for i in range(1, N-2):
			p.append(3 * (self.DividedDifference(xPoint[i+1], xPoint[i], yPoint[i+1], yPoint[i]) +  self.DividedDifference(xPoint[i], xPoint[i-1], yPoint[i], yPoint[i-1])))
			p[i] -= p[i-1]
		
		
		p.append(yPoint[N-1]) # p[N]
			
		for i in range(N, 1):
			p[i] -= p[i+1]
			p[i] /= 4

		s = []
		xs = []

		# Generate all the S
		for i in range(N-1):
			for x in range(xPoint[i], xPoint[i+1], ptPerCouple):
				deltaY = self.DividedDifference(xPoint[i+1], xPoint[i], yPoint[i+1], yPoint[i])
				xs[i].append(x)
				result = yPoint[i] + deltaY * (x - xPoint[i])
				result += (1 / (2 * (xPoint[i+1] - xPoint[i]))) * (p[i+1] - p[i]) * (x - xPoint[i]) * (x - xPoint[i+1])
				result += (1 / (2 * (xPoint[i+1] - xPoint[i])**2)) * (p[i+1] + p[i] - 2 * deltaY)
				result *= (((x - xPoint[i])**2 * (x - xPoint[i+1])) + (x - xPoint[i]) * (x - xPoint[i+1])**2)
				s[i].append(result)

		# si(x) = ai + bi*(x-xi) + ci*(x-xi)**2 + di*(x-xi)**3
		# si'(x) = bi + 2*ci*(x-xi) + 3*di*(x-xi)**2
		# si''(x) = 2*ci + 6*di*(x-xi)
		
		return (xs, s)'''