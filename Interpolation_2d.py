from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import math
from PIL import Image
import scipy.misc

from Interpolation import Interpolation

class Interpolation_2d(Interpolation):

	#-----------------------------------------
	# PROPERTIES
	#-----------------------------------------

	#
	inputImage = ""

	#
	outputImage = ""

	#
	point = [[]]

	#-----------------------------------------
	# CONSTRUCTOR
	#-----------------------------------------

	def __init__(self, input, output):
		self.point = [[]]
		self.inputImage = input
		self.outputImage = output

	#-----------------------------------------
	# METHODS
	#-----------------------------------------

	#
	def loadImage(self):
		img = Image.open(self.inputImage).convert('L')
		self.point = np.asarray(img)

	#
	def saveImage(self):
		scipy.misc.imsave(self.outputImage, self.point)

	# Used to generate new row in polynomiale interpolation
	# Get the y row
	def colArrayValue(self, array, col):
		result = []
		for i in range(len(array)):
			if len(array[i]) <= col:
				result.append(0)
			else:
				result.append(array[i][col])
		return result

	#
	def getIndexs(self, arraySize, index, space):
		startIndex = 0
		stopIndex = 0

		if arraySize > (space*2):
			startIndex = index - space
			stopIndex = index + space
			
			if (index-space) < 0:
				startIndex = 0
				stopIndex = (space*2)
			elif (index+space) > arraySize:
				startIndex = arraySize - (space*2)
				stopIndex = arraySize

		return (int(startIndex), int(stopIndex))

	#
	def PolynomialeInterpolation(self, nbPoint):
		newImage = []

		space = nbPoint / 2

		# Generate new line
		for y in range(len(self.point)):

			newImage.append([])

			for x in range(len(self.point[0])):
				newImage[y].append(self.point[y][x])

				# Array of X
				(start, stop) = self.getIndexs(len(self.point[y]), x, space)
				xPoint = np.arange(start, stop)

				# Array of Pixels
				(start, stop) = self.getIndexs(len(self.point[y]), x, space)
				yPoint = self.point[y][start:stop]

				# Create new X
				xp = super().PolynomialeInterpolation(x, xPoint, yPoint)
				newImage[y].append(xp)

		# Generate new row
		for y in range(0, (len(newImage))*2-2, 2):

			newImage.insert(y+1, [])

			for x in range(len(newImage[0])):

				# Array of X
				(start, stop) = self.getIndexs(len(newImage[y]), x, space)
				xPoint = np.arange(start, stop)

				# Get the n column
				array = self.colArrayValue(newImage, x)

				# Array of Pixels
				(start, stop) = self.getIndexs(len(array), y, space)
				yPoint = array[start:stop]

				# Create new X
				xp = super().PolynomialeInterpolation(x, xPoint, yPoint)
				newImage[y+1].append(xp)

		# Generate last row
		newImage.append([])
		for x in range(len(newImage[0])):
			array = self.colArrayValue(newImage, x)

			# Array of X
			(start, stop) = self.getIndexs(len(newImage[y]), x, space)
			xPoint = np.arange(start, stop)

			# Array of Pixels
			(start, stop) = self.getIndexs(len(array), x, space)
			yPoint = array[start:stop]

			# Create new X
			xp = super().PolynomialeInterpolation(x, xPoint, yPoint)
			newImage[-1].append(xp)

		# Replace the old image with the new one
		self.point = newImage


	#
	def PiecewiseInterpolation(self):
		newImage = []

		# Generate new line
		for y in range(len(self.point)):
			newImage.append([])
			newImage[y].append(self.point[y][0])
			for x in range(len(self.point[0])-1):
				xp = super().PiecewiseInterpolation(x, x+1, self.point[y][x], self.point[y][x+1], 2)
				newImage[y].extend(xp)
			newImage[y].append(self.point[y][-1])

		# Generate new row
		for y in range(0, (len(newImage))*2-2, 2):
			newImage.insert(y+1, [])
			for x in range(len(newImage[0])):
				xp = super().PiecewiseInterpolation(y, y+1, newImage[y][x], newImage[y+2][x], 1)
				newImage[y+1].extend(xp)

		# Generate last row
		newImage.append([])
		for x in range(len(newImage[0])):
			xp = super().PiecewiseInterpolation(0, 1, newImage[-2][x], newImage[-2][x], 1)
			newImage[-1].append(xp)

		# Replace the old image with the new one
		self.point = newImage

	#
	def ClampedCubicSplineInterpolation(self):
		pass