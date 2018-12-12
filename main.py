from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt
import sys
import scipy.misc

from Interpolation_1d import Interpolation_1d
from Interpolation_2d import Interpolation_2d

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

	#
	Inter1d = Interpolation_1d(a, b, nbPoint)

	#
	Inter2d = Interpolation_2d("image.png", "output.png")
	
	#
	Inter1d.CreatePoint()
	
	'''
	# 
	for x in np.linspace(a, b, 100):#
		xFunc.append(x)
		yFunc.append(Inter1d.Function(x))
		xPoly.append(x)
		yPoly.append(Inter1d.PolynomialeInterpolation(x, Inter1d.point['x'], Inter1d.point['y']))
		xInterval.append(x)
		yInterval.append(Inter1d.PiecewiseInterpolationX(x, Inter1d.point['x'], Inter1d.point['y']))

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
	'''

	#
	Inter2d.loadImage()
	#Inter2d.PiecewiseInterpolation_2d()
	Inter2d.PolynomialeInterpolation_2d()
	Inter2d.saveImage()
	


if __name__ == "__main__":
	#sys.setrecursionlimit(1000)
	main()