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

	#
	def PolynomialeInterpolation_2d(self, x):
		pass


	#
	def PiecewiseInterpolation_2d(self):
		newImage = []

		# Generate new line
		for y in range(len(self.point)):
			newImage.append([])
			newImage[y].append(self.point[y][0])
			for x in range(len(self.point[0])-1):
				xp = self.PiecewiseInterpolation(x, x+1, self.point[y][x], self.point[y][x+1], 2)
				newImage[y].extend(xp)
			newImage[y].append(self.point[y][-1])

		# Generate new row
		for y in range(0, (len(newImage))*2-2, 2):
			newImage.insert(y+1, [])
			for x in range(len(newImage[0])):
				xp = self.PiecewiseInterpolation(y, y+1, newImage[y][x], newImage[y+2][x], 1)
				newImage[y+1].extend(xp)

		# Generate last row
		newImage.append([])
		for x in range(len(newImage[0])):
			xp = self.PiecewiseInterpolation(0, 1, newImage[-2][x], newImage[-2][x], 1)
			newImage[-1].append(xp)

		# Replace the old image with the new one
		self.point = newImage

	#
	def ClampedCubicSplineInterpolation_2d(self, x):
		pass