import math
import numpy as np

def bound(byte):
	return min(255, max(0, byte))

def rgbToY(pixel):
	return ((77 * pixel[0]) >> 8) + ((150 * pixel[1]) >> 8) + ((29 * pixel[2]) >> 8)
	
def rgbToCb(pixel):
	return -((43 * pixel[0]) >> 8) - ((85 * pixel[1]) >> 8) + ((128 * pixel[2]) >> 8) + 128
	
def rgbToCr(pixel):
	return (pixel[0] >> 1) - ((107 * pixel[1]) >> 8) - ((21 * pixel[2]) >> 8) + 128
	
def yCbCrToR(pixel): 
	return pixel[0] + round(((pixel[2] - 128) << 8) / 183)
	
def yCbCrToG(pixel):
	return pixel[0] - round(5329 * (pixel[1] - 128) / 15481) - round(11103 * (pixel[2] - 128) / 15481)
	
def yCbCrToB(pixel):
	return pixel[0] + round(((pixel[1] - 128) << 8) / 144)
	
class RgbToYCbCrConverter:	
	def rgbToYCbCr(pixels):
		convertPixel = lambda pixel: (rgbToY(pixel), rgbToCb(pixel), rgbToCr(pixel))
		
		if (type(pixels) == list):
			newPixels = list(map(convertPixel, pixels))
		elif (type(pixels) == np.ndarray):
			newPixels = np.vectorize(convertPixel)(pixels)
		else:
			raise Exception("Expected type 'list' or 'numpy.ndarray' for convertion, got '{}'".format(type(pixels)))
		
		#print("RGB{} -> YCbCr{}".format(pixels[0], newPixels[0]))
		return newPixels
	
	def yCbCrToRgb(pixels):
		def convertPixel(pixel):
			newPixel = (bound(pixel[0]), bound(pixel[1]), bound(pixel[2]))
			newPixel[0] = yCbCrToR(pixel)
			newPixel[1] = yCbCrToG(pixel)
			newPixel[2] = yCbCrToB(pixel)
			return newPixel
			
		if (type(pixels) == list):
			newPixels = list(map(convertPixel, pixels))
		elif (type(pixels) == np.ndarray):
			newPixels = np.vectorize(convertPixel)(pixels)
		else:
			raise Exception("Expected type 'list' or 'numpy.ndarray' for convertion, got '{}'".format(type(pixels)))
		#print("YCbCr{} -> RGB{}".format(pixels[0], newPixels[0]))
		return newPixels