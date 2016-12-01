import numpy as np
import time


def bound(byte):
    return min(255, max(0, byte))


def rgbToY(pixel):
    return int(((77 * pixel[0]) >> 8) + ((150 * pixel[1]) >> 8) + ((29 * pixel[2]) >> 8))


def rgbToCb(pixel):
    return int(-((43 * pixel[0]) >> 8) - ((85 * pixel[1]) >> 8) + ((128 * pixel[2]) >> 8) + 128)


def rgbToCr(pixel):
    return int((pixel[0] >> 1) - ((107 * pixel[1]) >> 8) - ((21 * pixel[2]) >> 8) + 128)


def yCbCrToR(pixel):
    return int(pixel[0] + round(((pixel[2] - 128) << 8) / 183))


def yCbCrToG(pixel):
    return int(pixel[0] - round(5329 * (pixel[1] - 128) / 15481) - round(11103 * (pixel[2] - 128) / 15481))


def yCbCrToB(pixel):
    return int(pixel[0] + round(((pixel[1] - 128) << 8) / 144))


class RgbToYCbCrConverter:
    @staticmethod
    def rgbToYCbCr(pixels):
        start_time = time.time()

        def convertPixel(pixel):
            return rgbToY(pixel), rgbToCb(pixel), rgbToCr(pixel)

        if type(pixels) == list:
            newPixels = list(map(convertPixel, pixels))
        elif type(pixels) == np.ndarray:
            # newPixels = np.zeros(pixels.shape, dtype=np.int32)
            shape = pixels.shape
            newPixels = np.array(list(map(convertPixel, pixels.reshape(-1,3).tolist()))).reshape(shape)
        else:
            raise Exception("Expected type 'list' or 'numpy.ndarray' for conversion, got '{}'".format(type(pixels)))

        print("Converting %d pixels from RGB to YCbCr: %s seconds" % (pixels.size, time.time() - start_time))
        return newPixels

    @staticmethod
    def yCbCrToRgb(pixels):
        start_time = time.time()

        def convertPixel(pixel):
            pixel = (bound(pixel[0]), bound(pixel[1]), bound(pixel[2]))
            newPixel = (yCbCrToR(pixel), yCbCrToG(pixel), yCbCrToB(pixel))
            return newPixel

        if type(pixels) == list:
            newPixels = list(map(convertPixel, pixels))
        elif type(pixels) == np.ndarray:
            shape = pixels.shape
            newPixels = np.array(list(map(convertPixel, pixels.reshape(-1, 3).tolist()))).reshape(shape)
        else:
            raise Exception("Expected type 'list' or 'numpy.ndarray' for conversion, got '{}'".format(type(pixels)))

        print("Converting %d pixels from YCbCr to RGB: %s seconds" % (pixels.size, time.time() - start_time))
        return newPixels
