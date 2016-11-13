PARTITION_ELEMENTS_COUNT = 64
DEBUG = False

class Histogram(list):
	def __str__(self):
		MAX_LEN1 = 6
		MAX_LEN2 = 6
		firstNonZeroIndex = getFirstNonZeroElementIndex(self)
		lastNonZeroIndex = getLastNonZeroElementIndex(self)
		str = ""
		for index in range(firstNonZeroIndex, MAX_LEN1 - 1):
			str += "\t{}: {}\n".format(index, self[index])
		str+= "\t...\n"
		for index in range(lastNonZeroIndex - MAX_LEN2 + 1, lastNonZeroIndex + 1):
			str += "\t{}: {}\n".format(index, self[index])
		return str
		
	def __repr__(self):
		return self.__str__()

def createHistogramforOneColor(pixels, colorIndex):
	histogram = [0] * 256
	for pixel in pixels:
		color = pixel[colorIndex]
		histogram[color] += 1
	return Histogram(histogram)

def createHistogram(pixels):
	return [createHistogramforOneColor(pixels, 0), createHistogramforOneColor(pixels, 1), createHistogramforOneColor(pixels, 2)]
	
class PartitionElement:
	def __init__(self, dot, widths, histogram):
		self.dot = dot
		self.widths = widths
		self.histogram = histogram
		
	def __str__(self):
		return "({}, {})".format(self.dot, self.widths)
		
	def __repr__(self):
		return self.__str__()
		
	def findMedian(self, colorIndex):
		histogram = self.histogram[colorIndex]
		cumulates = []
		sum = 0
		for i in histogram:
			sum += i
			cumulates.append(sum)
		midValue = int(cumulates[-1] / 2)
		for index, item in enumerate(cumulates):
			if item >= midValue:
				return index
		return None
		
	def splitInTwo(self, median, colorIndex):
		el1Dot = self.dot
		el2DotList = list(self.dot)
		el2DotList[colorIndex] = median
		el2Dot = tuple(el2DotList)
		
		el1WidthsList = list(self.widths)
		el2WidthsList = list(self.widths)
		el1WidthsList[colorIndex] = median - el1Dot[colorIndex]
		el1Widths = tuple(el1WidthsList)
		el2WidthsList[colorIndex] -= el1Widths[colorIndex]
		el2Widths = tuple(el2WidthsList)
		
		el1Histogram = [Histogram(self.histogram[0][:]), Histogram(self.histogram[1][:]), Histogram(self.histogram[2][:])]
		el1Histogram[colorIndex] = Histogram(self.histogram[colorIndex][:])
		el1Histogram[colorIndex][median:] = [0] * (len(el1Histogram[colorIndex]) - median)
		
		el2Histogram = [Histogram(self.histogram[0][:]), Histogram(self.histogram[1][:]), Histogram(self.histogram[2][:])]
		el2Histogram[colorIndex] = Histogram(self.histogram[colorIndex][:])
		el2Histogram[colorIndex][:median] = [0] * median
		
		return [PartitionElement(el1Dot, el1Widths, el1Histogram), PartitionElement(el2Dot, el2Widths, el2Histogram)]
	
def getFirstNonZeroElementIndex(histogram):
	for index, item in enumerate(histogram):
		if item > 0:
			return index
	return None
	
def getLastNonZeroElementIndex(histogram):
	count = len(histogram)
	for index, item in enumerate(reversed(histogram)):
		if item > 0:
			return count - index - 1
	return None
	

def CreateInitialPartitionElement(histogram):
	dotR = getFirstNonZeroElementIndex(histogram[0])
	dotG = getFirstNonZeroElementIndex(histogram[1])
	dotB = getFirstNonZeroElementIndex(histogram[2])
	dot = (dotR, dotG, dotB)
	
	widthsR = getLastNonZeroElementIndex(histogram[0]) - dotR
	widthsG = getLastNonZeroElementIndex(histogram[1]) - dotG
	widthsB = getLastNonZeroElementIndex(histogram[2]) - dotB
	widths = (widthsR, widthsG, widthsB)
	
	return PartitionElement(dot, widths, histogram)

def getMaxEdge(partitions):
	maxEdge = {
		'len': 0,
		'index': None,
		'colorIndex': None
	}
	for index, prt in enumerate(partitions):
		for i in range(3):
			if prt.widths[i] > maxEdge['len']:
				maxEdge = {
					'len': prt.widths[i],
					'index': index,
					'colorIndex': i
				}
				
	return maxEdge

def createPartitions(pixels):
	histogram = createHistogram(pixels)
	print("Hystogram:\n\tRed:\n\n{}\n\tGreen:\n\n{}\n\tBlue:\n\n{}\n".format(histogram[0], histogram[1], histogram[2])) if DEBUG else 0
	partitions = [CreateInitialPartitionElement(histogram)]
	while len(partitions) < PARTITION_ELEMENTS_COUNT:
		#print("partitions:\n") if DEBUG else 0
		#if DEBUG:
		#	for partitionElem in partitions:
		#		print (partitionElem)
		maxEdge = getMaxEdge(partitions)
		prtEl = partitions[maxEdge['index']]
		median = prtEl.findMedian(maxEdge['colorIndex'])
		print("splitting {} in two by edge with index '{} 'using median of '{}':\n".format(prtEl, maxEdge['colorIndex'], median)) if DEBUG else 0
		newPartitions = prtEl.splitInTwo(median, maxEdge['colorIndex'])
		print("{} + {}\n".format(newPartitions[0], newPartitions[1])) if DEBUG else 0
		partitions[maxEdge['index']] = newPartitions[0]
		partitions.insert(maxEdge['index'] + 1, newPartitions[1])
	
	return partitions
	
def createPalette(partitions):
	palette = []
	print("Final partitions:") if DEBUG else 0
	for prtEl in partitions:
		color = (prtEl.findMedian(0), prtEl.findMedian(1), prtEl.findMedian(2))
		palette.append(color)
		print ("{} -> {}".format(prtEl, color)) if DEBUG else 0
	return palette
	
def findPartitionIndex(pixel, partitions):
	for index, prtEl in enumerate(partitions):
		if (prtEl.dot[0] <= pixel[0] and
		pixel[0] <= prtEl.dot[0] + prtEl.widths[0] and
		prtEl.dot[1] <= pixel[1] and
		pixel[1] <= prtEl.dot[1] + prtEl.widths[1] and
		prtEl.dot[2] <= pixel[2] and
		pixel[2] <= prtEl.dot[2] + prtEl.widths[2]):
			return index
			
	
def MedianCutQuantize(pixels):
	print ("MEDIAN CUT QUANTIZATION:\n") if DEBUG else 0
	partitions = createPartitions(pixels)
	palette = createPalette(partitions)
	newPixels = []
	
	FIRST_PIXELS_TO_PRINT = 30
	LAST_PIXELS_TO_PRINT = 30
	firstPixelToPrintInLastGroup = len(pixels) - LAST_PIXELS_TO_PRINT
	pixelsQuantized = 0
	print ("\nQuantization process:\n(pixels count: {})".format(len(pixels))) if DEBUG else 0
	ellipsis = False
	for pixelIndex, pixel in enumerate(pixels):
		index = findPartitionIndex(pixel, partitions)
		if (index is None):
			print ("pixel {} - can't find partition".format(pixel)) if DEBUG else 0
		else:
			newPixels.append(palette[index])
			if pixelsQuantized <= FIRST_PIXELS_TO_PRINT:
				print ("{}. {} -> partition {} -> {}".format(pixelIndex, pixel, index, palette[index])) if DEBUG else 0
			else:
				if not ellipsis:
					print("...") if DEBUG else 0
					ellipsis = True
				if (pixelsQuantized >= firstPixelToPrintInLastGroup):
					print ("{}. {} -> partition {} -> {}".format(pixelIndex, pixel, index, palette[index])) if DEBUG else 0
		pixelsQuantized += 1
	return newPixels