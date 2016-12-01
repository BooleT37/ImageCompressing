import math

from .rgbToYCbCrConverter import RgbToYCbCrConverter
from .imageSubsampler import ImageSubsampler, ImageSubsamplerException
from .quantizeMatrices import QuantizeMatrices
from .model.jpg import Jpg

import numpy as np


class Dct:
    def __init__(self):

        self.M = np.zeros((8, 8))
        i0 = round(1 / math.sqrt(8), 2)
        for j in range(8):
            self.M[0, j] = i0
        for i in range(1, 8):
            for j in range(8):
                self.M[i, j] = math.cos((2 * j + 1) * i * math.pi / 16) / 2

        self.MT = self.M.transpose()

    def compressImage(self, pixels, subsamplingMode="2h2v"):
        yCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(pixels)

        layers = yCbCrPixels.transpose(2, 0, 1)

        yLayer = layers[0]
        cbLayerOddHeight = layers[1].shape[0] % 2 == 1
        cbLayerOddWidth = layers[1].shape[1] % 2 == 1
        crLayerOddHeight = layers[2].shape[0] % 2 == 1
        crLayerOddWidth = layers[2].shape[1] % 2 == 1

        # subsampling
        subsampler = ImageSubsampler()
        subsampledCbLayer = subsampler.subsampleLayer(layers[1], subsamplingMode)
        subsampledCrLayer = subsampler.subsampleLayer(layers[2], subsamplingMode)

        # DCT and quantizing
        newYLayer = self.dctLayer(yLayer, QuantizeMatrices.defaultY)
        newCbLayer = self.dctLayer(subsampledCbLayer, QuantizeMatrices.defaultCrCb)
        newCrLayer = self.dctLayer(subsampledCrLayer, QuantizeMatrices.defaultCrCb)

        # unsubsampling
        # newCbLayer = subsampler.unSubsampleLayer(newCbLayer, subsamplingMode, cbLayerOddHeight, cbLayerOddWidth)
        # newCrLayer = subsampler.unSubsampleLayer(newCrLayer, subsamplingMode, crLayerOddHeight, crLayerOddWidth)

        # newYCbCrPixels = np.array([newYLayer, newCbLayer, newCrLayer]).transpose(1, 2, 0)
        #
        # newRgbPixels = RgbToYCbCrConverter.yCbCrToRgb(newYCbCrPixels)
        # return newRgbPixels
        return Jpg(pixels.shape[0], pixels.shape[1], newYLayer.flatten().tolist(), newCbLayer.flatten().tolist(),
                   newCrLayer.flatten().tolist(), subsamplingMode)

    def dctLayer(self, matrix, quantizeMatrix):
        newMatrix = matrix.copy()
        height = matrix.shape[0]
        width = matrix.shape[1]
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                # block = np.array(matrix[i:i+8, j:j+8])
                block = newMatrix[i:i+8, j:j+8]
                blockShape = block.shape
                if block.shape[0] < 8:
                    lastColumn = block[-1]
                    while block.shape[0] < 8:
                        block = np.concatenate((block, [lastColumn]))
                if block.shape[1] < 8:
                    lastRow = block.transpose()[-1].reshape(-1, 1)
                    while block.shape[1] < 8:
                        block = np.hstack((block, lastRow))
                block = self.dctBlock(block)
                block = self.quantizeBlock(block, quantizeMatrix)

                if blockShape[0] < 8 or blockShape[1] < 8:
                    block = block[0:blockShape[0], 0:blockShape[1]]
                newMatrix[i:i + 8, j:j + 8] = block
        return newMatrix

    def dctBlock(self, block):
        return np.dot(np.dot(self.M, block), self.MT)

    @staticmethod
    def quantizeBlock(block, quantizeMatrix):
        divide = np.vectorize(lambda a, b: int(a / b))
        return divide(block, np.array(quantizeMatrix).reshape(8,8))

if __name__ == "__main__":
    np.set_printoptions(suppress=True, precision=2)
    dct = Dct()
