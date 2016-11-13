from RgbToYCbCrConverter import *
import numpy as np

class DCT:
	def __init__(self):
		self.M = np.zeros((8,8))
		for j in range(8):
			self.M[0, j] = 1 / Math.sqrt(8)
		for i in range(1, 8):
			for j in range(8):
				self.M[i, j] = Math.cos((2 * j + 1) * i * Math.Pi / 16) / 2
		
		self.MT = self.M.transpose()
		
	def CountForMatrix(matrix):
		return dot(dot(M, D), MT)
		
	def Count(pixels, width):
	
		nPixels = np.array(pixels)
		height = int(len(YCbCrPixels) / width)
		
		for i in range(int(height / 8)):
			for j in range(int(width / 8)):
				martix = nPixels[i * 8, i * 8 + 7, j * 8, j * 8 + 7]
				newMatrix = CountForMatrix(matrix)
				