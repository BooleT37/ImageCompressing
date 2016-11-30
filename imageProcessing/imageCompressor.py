from .rgbToYCbCrConverter import RgbToYCbCrConverter
from .medianCutQuantizer import MedianCutQuantize

METHOD_222 = "method 222"
METHOD_312 = "method 312"
METHOD_321 = "method 321"

class ImageCompressor:
	def uniformQuantizeRgb(self, pixels, depth = 2):
		if (depth > 8):
			raise ImageCompressorException("Depth can't be more than 8!")
		divisor = 8 - depth
		newPixels = list(map(lambda pixel: ((pixel[0] >> divisor << divisor) + 2**(divisor-1), (pixel[1] >> divisor << divisor) + 2**(divisor-1), (pixel[2] >> divisor << divisor) + 2**(divisor-1)), pixels))
		#print (pixels[0], newPixels[0])
		return newPixels
		
	def uniformQuantizeYCbCr(self, pixels, method):
		if method == METHOD_222:
			depths = (2, 2, 2)
		elif method == METHOD_312:
			depths = (3, 1, 2)
		elif method == METHOD_321:
			depths = (3, 2, 1)
		else:
			raise ImageCompressorException("Method number for Uniform YCbCr Quantization should be 1, 2 or 3")
		
		divisors = (8 - depths[0], 8 - depths[1], 8 - depths[2])
		
		print("===NEW STEP===")
		YCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(pixels)
		newYCbCrPixels = list(map(lambda pixel: ((pixel[0] >> divisors[0] << divisors[0]) + 2**(divisors[0]-1), (pixel[1] >> divisors[1] << divisors[1]) + 2**(divisors[1]-1), (pixel[2] >> divisors[2] << divisors[2]) + 2**(divisors[2]-1)), YCbCrPixels))
		print("YCbCr{} -> YCbCr{}".format(YCbCrPixels[0], newYCbCrPixels[0]))
		return RgbToYCbCrConverter.yCbCrToRgb(newYCbCrPixels)
		
	def medianCutQuantize(self, pixels):
		return MedianCutQuantize(pixels)
		
class ImageCompressorException(Exception):
	def __init__(self, message):
		self.message = message
		
	def __str__(self):
		return self.message