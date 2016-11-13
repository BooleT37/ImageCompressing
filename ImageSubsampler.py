from RgbToYCbCrConverter import *

class ImageSubsampler:
	def SubsampleImage(self, pixels, mode, width):
		YCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(pixels)
		
		newPixels = [None] * len(YCbCrPixels)
		
		height = int(len(YCbCrPixels) / width)
		
		#print ("Width: {}, Height: {}".format(width, height))
		
		print("mode is {}".format(mode))
		
		for i in range(int(height / 2)):
			for j in range(int(width / 2)):
				p1Index = i * 2 * width + j * 2
				p2Index = p1Index + 1
				p3Index = p1Index + width
				p4Index = p1Index + width + 1
				
				newPixels[p1Index] = YCbCrPixels[p1Index]
				#print ("i = {}, j = {}, {}, {}, {}, {}".format(i, j, p1Index, p2Index, p3Index, p4Index))
				#quarter = (YCbCrPixels[p1Index], YCbCrPixels[p2Index], YCbCrPixels[p3Index], YCbCrPixels[p4Index])
				if mode == "2h1v":
					newPixels[p3Index] = YCbCrPixels[p3Index]
					newPixels[p2Index] = (YCbCrPixels[p2Index][0], YCbCrPixels[p1Index][1], YCbCrPixels[p1Index][2])
					newPixels[p4Index] = (YCbCrPixels[p4Index][0], YCbCrPixels[p3Index][1], YCbCrPixels[p3Index][2])
				elif mode == "1h2v":
					newPixels[p2Index] = YCbCrPixels[p2Index]
					newPixels[p3Index] = (YCbCrPixels[p3Index][0], YCbCrPixels[p1Index][1], YCbCrPixels[p1Index][2])
					newPixels[p4Index] = (YCbCrPixels[p4Index][0], YCbCrPixels[p2Index][1], YCbCrPixels[p2Index][2])
				elif mode == "2h2v":
					newPixels[p2Index] = (YCbCrPixels[p2Index][0], YCbCrPixels[p1Index][1], YCbCrPixels[p1Index][2])
					newPixels[p3Index] = (YCbCrPixels[p3Index][0], YCbCrPixels[p1Index][1], YCbCrPixels[p1Index][2])
					newPixels[p4Index] = (YCbCrPixels[p4Index][0], YCbCrPixels[p1Index][1], YCbCrPixels[p1Index][2])
				else:
					raise ImageSubsamplerException("Mode number for Image thinner should be \"2h1v\", \"1h2v\" or \"2h2v\", \"{}\" given".format(mode))
				
				
		if (height % 2 == 1):
			lastRowIndex = width * (height - 1)
			for i in range(width):
				index = lastRowIndex + i
				newPixels[index] = YCbCrPixels[index]
				
		if (width % 2 == 1):
			lastColIndex = width - 1
			for i in range(height):
				index = lastColIndex + width * i
				newPixels[index] = YCbCrPixels[index]
				
		for index, pixel in enumerate(newPixels):
			if (pixel is None):
				row = int(index / width)
				col = index - row * width
				print ("Pixel {} is None ({} row, {} col)".format(index, row, col))
			
		print("\nYCbCr:\n{} {}\t=>\t{} {}\n{} {}\t\t{} {}\n".format(YCbCrPixels[0], YCbCrPixels[1], newPixels[0], newPixels[1], YCbCrPixels[width], YCbCrPixels[width + 1], newPixels[width], newPixels[width + 1]))
			
		rgbPixels = RgbToYCbCrConverter.yCbCrToRgb(newPixels)
		
		print("\nRGB:\n{} {}\t=>\t{} {}\n{} {}\t\t{} {}\n".format(pixels[0], pixels[1], rgbPixels[0], rgbPixels[1], pixels[width], pixels[width + 1], rgbPixels[width], rgbPixels[width + 1]))
		return rgbPixels
				

class ImageSubsamplerException(Exception):
	def __init__(self, message):
		self.message = message
		
	def __str__(self):
		return self.message