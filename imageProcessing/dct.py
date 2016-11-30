from .rgbToYCbCrConverter import RgbToYCbCrConverter
from .imageSubsampler import ImageSubsampler, ImageSubsamplerException
import numpy as np
import math

class Dct:
	def __init__(self):
		
		self.M = np.zeros((8,8))
		i0 = round(1 / math.sqrt(8), 2)
		for j in range(8):
			self.M[0, j] = i0
		for i in range(1, 8):
			for j in range(8):
				self.M[i, j] = math.cos((2 * j + 1) * i * math.pi / 16) / 2
		
		self.MT = self.M.transpose()
		
		#print(self.M)
		D = np.array([
			[52, 55, 61, 66, 70, 61, 64, 73],
			[63, 59, 55, 90, 109, 85, 69, 72],
			[62, 59, 68, 113, 144, 104, 66, 73],
			[63, 58, 71, 122, 154, 106, 70, 69],
			[67, 61, 68, 104, 126, 88, 68, 70],
			[79, 65, 60, 70, 77, 68, 58, 75],
			[85, 71, 64, 59, 55, 61, 65, 83],
			[87, 79, 69, 68, 65, 76, 78, 94]
		], np.int32)
		print(D)
		result = np.dot(np.dot(self.M, D), self.MT)
		result[0, 0] = result[0, 0] - 1024
		print(result)
		
	#def CountForMatrix(matrix):
	#	return dot(dot(M, D), MT)
	#	
	#def Count(pixels, width):
	#
	#	nPixels = np.array(pixels)
	#	height = int(len(YCbCrPixels) / width)
	#	
	#	for i in range(int(height / 8)):
	#		for j in range(int(width / 8)):
	#			martix = nPixels[i * 8, i * 8 + 7, j * 8, j * 8 + 7]
	#			newMatrix = CountForMatrix(matrix)
	
	def compressImage(self, pixels):
		yCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(pixels);
		#subsample 2 layers
		#split to 8x8 blocks
		#DCT all blocks
		#quantize all blocks
		
				
if __name__ == "__main__":
	np.set_printoptions(suppress=True, precision=2)
	dct = Dct()
