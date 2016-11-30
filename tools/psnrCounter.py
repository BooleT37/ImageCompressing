import math

class PsnrCounter:
	def countMse(self, pixels1, pixels2, n):
		sum = 0
		for i in range(n):
			pixel1 = pixels1[i]
			pixel2 = pixels2[i]
			sum += (pixel1[0] - pixel2[0])**2 + (pixel1[1] - pixel2[1])**2 + (pixel1[2] - pixel2[2])**2
	
		mse = sum / (n * 3)
		return mse
		
	def countPsnr(self, mse):
		if (mse == 0):
			raise MseIsZeroException()
		return 10 * math.log10(255 * 255 / mse)
	
class MseIsZeroException(Exception):
     def __str__(self):
         return "MSE = 0, PSNR is undefined"