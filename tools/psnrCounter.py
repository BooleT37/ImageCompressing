import math


class PsnrCounter:
    @staticmethod
    def countMse(pixels1, pixels2, n):
        summ = 0
        for i in range(n):
            pixel1 = pixels1[i]
            pixel2 = pixels2[i]
            summ += (pixel1[0] - pixel2[0]) ** 2 + (pixel1[1] - pixel2[1]) ** 2 + (pixel1[2] - pixel2[2]) ** 2

        mse = summ / (n * 3)
        return mse

    @staticmethod
    def countPsnr(mse):
        if mse == 0:
            raise MseIsZeroException()
        return 10 * math.log10(255 * 255 / mse)


class MseIsZeroException(Exception):
    def __str__(self):
        return "MSE = 0, PSNR is undefined"
