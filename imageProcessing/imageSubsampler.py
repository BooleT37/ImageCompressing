import numpy as np
import math
import time

from .rgbToYCbCrConverter import RgbToYCbCrConverter

DEBUG = False


class ImageSubsampler:
    pixelTransitions = {
        "2h1v": [
            0, 0,
            3, 3
        ],
        "1h2v": [
            0, 1,
            0, 1
        ],
        "2h2v": [
            0, 0,
            0, 0
        ]
    }

    def imitateForImage(self, rgbPixels, mode):
        start_time1 = start_time2 = start_time3 = 0
        if DEBUG:
            start_time1 = time.time()

        yCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(rgbPixels)

        if DEBUG:
            print("1. Converting pixels from YCbCr to RGB: %s seconds" % (time.time() - start_time1))
            start_time2 = time.time()

        layers = yCbCrPixels.transpose(2, 0, 1)

        if DEBUG:
            print("2. Filling the matrix: %s seconds" % (time.time() - start_time2))
            start_time3 = time.time()

        newLayers = np.array([layers[0], self.imitateForLayer(layers[1], mode), self.imitateForLayer(layers[2], mode)])
        newYCbCrPixels = newLayers.transpose(1, 2, 0)

        newRgbPixels = RgbToYCbCrConverter.yCbCrToRgb(newYCbCrPixels)

        if DEBUG:
            endTime = time.time()
            print("3. Converting pixels back from RGB to YCbCr: %s seconds" % (endTime - start_time3))
            print("Total time: %s seconds" % (endTime - start_time1))
            print("\nYCbCr:\n{0} {1}\t=>\t{4} {5}\n{2} {3}\t\t{6} {7}\n".format(
                yCbCrPixels[0][0], yCbCrPixels[0][1], yCbCrPixels[1][0], yCbCrPixels[1][1],
                newYCbCrPixels[0][0], newYCbCrPixels[0][1], newYCbCrPixels[1][0], newYCbCrPixels[1][1]
            ))
            print("\nRGB:\n{0} {1}\t=>\t{4} {5}\n{2} {3}\t\t{6} {7}\n".format(
                rgbPixels[0][0], rgbPixels[0][1], rgbPixels[1][0], rgbPixels[1][1],
                newRgbPixels[0][0], newRgbPixels[0][1], newRgbPixels[1][0], newRgbPixels[1][1]
            ))

        return newRgbPixels

    @staticmethod
    def subsampleLayer(matrix, mode):
        height = matrix.shape[0]
        width = matrix.shape[1]

        halfHeight = int(math.ceil(height / 2))
        halfWidth = int(math.ceil(width / 2))
        if mode == "2h1v":
            newMatrix = np.ndarray((height, halfWidth), matrix.dtype)
            for i in range(0, height):
                for j in range(0, halfWidth):
                    newMatrix[i][j] = matrix[i][j * 2]
        elif mode == "1h2v":
            newMatrix = np.ndarray((halfHeight, width), matrix.dtype)
            for i in range(0, halfHeight):
                for j in range(0, width):
                    newMatrix[i][j] = matrix[i * 2][j]
        elif mode == "2h2v":
            newMatrix = np.ndarray((halfHeight, halfWidth), matrix.dtype)
            for i in range(0, halfHeight):
                for j in range(0, halfWidth):
                    newMatrix[i][j] = matrix[i * 2][j * 2]
        else:
            raise ImageSubsamplerException(
                "Subsampling mode should be \"2h1v\", \"1h2v\" or \"2h2v\", \"{}\" given".format(mode))
        return newMatrix

    @staticmethod
    def unSubsampleLayer(matrix, mode, oddHeight=False, oddWidth=False):
        height = matrix.shape[0]
        width = matrix.shape[1]

        doubleHeight = height * 2 - 1 if oddHeight else height * 2
        doubleWidth = width * 2 - 1 if oddWidth else width * 2

        if mode == "2h1v":
            newMatrix = np.zeros((height, doubleWidth), matrix.dtype)
            for i in range(0, height):
                for j in range(0, width):
                    clippedLastRow = oddWidth and j == width - 1
                    newMatrix[i][j * 2] = matrix[i][j]
                    if not clippedLastRow:
                        newMatrix[i][j * 2 + 1] = matrix[i][j]
        elif mode == "1h2v":
            newMatrix = np.zeros((doubleHeight, width), matrix.dtype)
            for i in range(0, height):
                for j in range(0, width):
                    clippedLastColumn = oddHeight and i == height - 1
                    newMatrix[i * 2][j] = matrix[i][j]
                    if not clippedLastColumn:
                        newMatrix[i * 2 + 1][j] = matrix[i][j]
        elif mode == "2h2v":
            newMatrix = np.zeros((doubleHeight, doubleWidth), matrix.dtype)
            for i in range(0, height):
                for j in range(0, width):
                    clippedLastColumn = oddHeight and i == height - 1
                    clippedLastRow = oddWidth and j == width - 1
                    newMatrix[i * 2][j * 2] = matrix[i][j]
                    if not clippedLastRow:
                        newMatrix[i * 2][j * 2 + 1] = matrix[i][j]
                    if not clippedLastColumn:
                        newMatrix[i * 2 + 1][j * 2] = matrix[i][j]
                    if not clippedLastRow and not clippedLastColumn:
                        newMatrix[i * 2 + 1][j * 2 + 1] = matrix[i][j]
        else:
            raise ImageSubsamplerException(
                "Subsampling mode should be \"2h1v\", \"1h2v\" or \"2h2v\", \"{}\" given".format(mode))
        return newMatrix

    def imitateForLayer(self, matrix, mode):
        height = matrix.shape[0]
        width = matrix.shape[1]
        newMatrix = np.ndarray(matrix.shape, matrix.dtype)
        for i in range(0, height, 2):
            lastRow = (i == height - 1)
            for j in range(0, width, 2):
                lastCol = (j == width - 1)
                # taking original pixels quad
                quad = [
                    matrix[i][j], None, None, None
                ]
                if lastCol:
                    quad[1] = matrix[i][j]
                    if lastRow:
                        quad[2] = quad[3] = matrix[i][j]
                    else:
                        quad[2] = quad[3] = matrix[i + 1][j]
                else:
                    quad[1] = matrix[i][j + 1]
                    if lastRow:
                        quad[2] = matrix[i][j]
                        quad[3] = matrix[i][j + 1]
                    else:
                        quad[2] = matrix[i + 1][j]
                        quad[3] = matrix[i + 1][j + 1]
                # transforming it into new quad
                newQuad = [None, None, None, None]
                for k in range(4):
                    newQuad[k] = quad[self.pixelTransitions[mode][k]]
                newMatrix[i][j] = newQuad[0]
                if not lastCol:
                    newMatrix[i][j + 1] = newQuad[1]
                if not lastRow:
                    newMatrix[i + 1][j] = newQuad[2]
                if not lastCol and not lastRow:
                    newMatrix[i + 1][j + 1] = newQuad[3]
        return newMatrix

class ImageSubsamplerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
