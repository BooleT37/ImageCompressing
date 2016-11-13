import math

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
		newPixels = list(map(lambda pixel: (rgbToY(pixel), rgbToCb(pixel), rgbToCr(pixel)), pixels))
		
		#print("RGB{} -> YCbCr{}".format(pixels[0], newPixels[0]))
		return newPixels
	
	def yCbCrToRgb(pixels):
		newPixels = list(map(lambda pixel: (bound(pixel[0]), bound(pixel[1]), bound(pixel[2])) ,(map(lambda pixel: (yCbCrToR(pixel), yCbCrToG(pixel), yCbCrToB(pixel)), pixels))))
		
		#print("YCbCr{} -> RGB{}".format(pixels[0], newPixels[0]))
		return newPixels