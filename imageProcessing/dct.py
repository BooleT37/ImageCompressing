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

        self.subsampler = ImageSubsampler()
        self.quantizeMatrices = QuantizeMatrices()

    def compressImage(self, pixels, options):
        quantizingMode = options["quantizingMode"]
        subsamplingMode = options["subsamplingMode"]

        if quantizingMode == "firstn":
            yLayerQuantizeOptions = {
                "quantizeMatrix": self.quantizeMatrices.NO_COMPRESSION,
                "n": options["n"]
            }
            crCbLayerQuantizeOptions = {
                "quantizeMatrix": self.quantizeMatrices.NO_COMPRESSION,
                "n": options["n"]
            }
        elif quantizingMode == "custom":
            yLayerQuantizeOptions = {
                "quantizeMatrix": self.quantizeMatrices.getCustom(options["alpha"], options["gamma"])
            }
            crCbLayerQuantizeOptions = {
                "quantizeMatrix": self.quantizeMatrices.getCustom(options["alpha"], options["gamma"])
            }
        elif quantizingMode == "qfactor":
            yLayerQuantizeOptions = {
                "quantizeMatrix": self.quantizeMatrices.getForQualityFactor(options["q"], "Y")
            }
            crCbLayerQuantizeOptions = {
                "quantizeMatrix": self.quantizeMatrices.getForQualityFactor(options["q"], "CrCb")
            }
        else:
            raise Exception("quantizingMode has to be 'firstn', 'custom' or 'qfactor', {} given".format(quantizingMode))

        # print("RGB pixels: ")
        # print(pixels[0:10,0:10])

        yCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(pixels)

        layers = yCbCrPixels.transpose(2, 0, 1)

        # print("YCbCr layers: ")
        # print("Y:")
        # print(layers[0][0:10, 0:10])
        # print("Cb:")
        # print(layers[1][0:10, 0:10])
        # print("Cr:")
        # print(layers[2][0:10, 0:10])
        yLayer = layers[0]

        # subsampling
        subsampledCbLayer = self.subsampler.subsampleLayer(layers[1], subsamplingMode)
        subsampledCrLayer = self.subsampler.subsampleLayer(layers[2], subsamplingMode)

        # print("Subsampled Cb:")
        # print(subsampledCbLayer[0:10, 0:10])
        # print("Subsampled Cr:")
        # print(subsampledCrLayer[0:10, 0:10])

        # DCT and quantizing
        newYLayer = self.dctLayer(yLayer, quantizingMode, yLayerQuantizeOptions)
        newCbLayer = self.dctLayer(subsampledCbLayer, quantizingMode, crCbLayerQuantizeOptions)
        newCrLayer = self.dctLayer(subsampledCrLayer, quantizingMode, crCbLayerQuantizeOptions)

        # print("Y layer after DCT:")
        # print(newYLayer[0:10, 0:10])
        # print("Cb layer after DCT:")
        # print(newCbLayer[0:10, 0:10])
        # print("Cr layer after DCT:")
        # print(newCrLayer[0:10, 0:10])

        return Jpg(pixels.shape[0], pixels.shape[1], newYLayer.flatten().tolist(),
                   newCbLayer.flatten().tolist(), newCrLayer.flatten().tolist(), subsamplingMode,
                   quantizingMode, yLayerQuantizeOptions["quantizeMatrix"], crCbLayerQuantizeOptions["quantizeMatrix"])

    @staticmethod
    def processForEveryBlock(matrix, function, functionArgs, fillGapsWithZeros=False):
        newMatrix = matrix.copy()
        height = matrix.shape[0]
        width = matrix.shape[1]
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block = newMatrix[i:i + 8, j:j + 8]
                blockShape = block.shape
                if block.shape[0] < 8:
                    if fillGapsWithZeros:
                        lastColumn = np.zeros(block.shape[1], dtype=int)
                    else:
                        lastColumn = block[-1]
                    while block.shape[0] < 8:
                        block = np.concatenate((block, [lastColumn]))
                if block.shape[1] < 8:
                    if fillGapsWithZeros:
                        lastRow = np.zeros(block.shape[0], dtype=int).transpose().reshape(-1, 1)
                    else:
                        lastRow = block.transpose()[-1].reshape(-1, 1)
                    while block.shape[1] < 8:
                        block = np.hstack((block, lastRow))

                block = function(block, *functionArgs)

                if blockShape[0] < 8 or blockShape[1] < 8:
                    block = block[0:blockShape[0], 0:blockShape[1]]
                newMatrix[i:i + 8, j:j + 8] = block
        return newMatrix

    def dctAndQuantize(self, block, quantizingMode, quantizeOptions):
        block = self.dctBlock(block)
        block = self.quantizeBlock(block, quantizingMode, quantizeOptions)
        return block

    def dctLayer(self, matrix, quantizingMode, quantizeOptions):
        return self.processForEveryBlock(matrix, self.dctAndQuantize, [quantizingMode, quantizeOptions])

    def dctBlock(self, block):
        newBlock = np.dot(np.dot(self.M, block), self.MT)
        # newBlock[0, 0] -= 1024
        return newBlock

    @staticmethod
    def quantizeBlock(block, quantizingMode, options):
        if quantizingMode == "firstn":
            newBlock = block.copy()
            indexes = np.argsort(block)
            indexes[:] = indexes[::-1]  # reversing sort
            for i in range(63, options["n"], -1):
                newBlock[int(i / 8), i % 8] = 0
            return newBlock
        if quantizingMode != "custom" and quantizingMode != "qfactor":
            raise Exception("quantizingMode has to be 'firstn', 'custom' or 'qfactor', {} given".format(quantizingMode))

        quantizeMatrix = options["quantizeMatrix"]
        divide = np.vectorize(lambda a, b: int(a / b))
        return divide(block, np.array(quantizeMatrix).reshape(8,8))

    def uncompressImage(self, jpgObject):
        subsampledShape = self.subsampler.getShapeFromMode((jpgObject.height, jpgObject.width), jpgObject.subsamplingMode)

        subsampledHeight = subsampledShape[0]
        subsampledWidth = subsampledShape[1]

        oddHeight = jpgObject.height % 2 == 1
        oddWidth = jpgObject.width % 2 == 1

        # print("jpg object:")
        # print("Y layer:")
        # for i in range(10):
        #     start = i * jpgObject.width
        #     print(jpgObject.yLayer[start:start + 10])
        # print("Cb layer:")
        # for i in range(10):
        #     start = i * subsampledWidth
        #     print(jpgObject.cbLayer[start:start + 10])
        # print("Cr layer:")
        # for i in range(10):
        #     start = i * subsampledWidth
        #     print(jpgObject.crLayer[start:start + 10])

        yLayer = np.array(jpgObject.yLayer).reshape(jpgObject.height, jpgObject.width)
        cbLayer = np.array(jpgObject.cbLayer).reshape(subsampledHeight, subsampledWidth)
        crLayer = np.array(jpgObject.crLayer).reshape(subsampledHeight, subsampledWidth)

        # print("Y layer after reshaping:")
        # print(yLayer[0:10, 0:10])
        # print("Cb layer after reshaping:")
        # print(cbLayer[0:10, 0:10])
        # print("Cr layer after reshaping:")
        # print(crLayer[0:10, 0:10])

        yLayer = self.unDctLayer(yLayer, jpgObject.quantizeMatrixY)
        cbLayer = self.unDctLayer(cbLayer, jpgObject.quantizeMatrixCrCb)
        crLayer = self.unDctLayer(crLayer, jpgObject.quantizeMatrixCrCb)

        # print("Y layer after reversing DCT:")
        # print(yLayer[0:10, 0:10])
        # print("Cb layer after reversing DCT:")
        # print(cbLayer[0:10, 0:10])
        # print("Cr layer after reversing DCT:")
        # print(crLayer[0:10, 0:10])

        cbLayer = self.subsampler.unSubsampleLayer(cbLayer, jpgObject.subsamplingMode, oddHeight, oddWidth)
        crLayer = self.subsampler.unSubsampleLayer(crLayer, jpgObject.subsamplingMode, oddHeight, oddWidth)

        # print("Cb layer after unsabsampling")
        # print(cbLayer[0:10, 0:10])
        # print("Cr layer after unsabsampling")
        # print(crLayer[0:10, 0:10])

        yCbCrMatrix = np.concatenate(([yLayer], [cbLayer], [crLayer])).transpose(1, 2, 0)
        rgbMatrix = RgbToYCbCrConverter.yCbCrToRgb(yCbCrMatrix)
        # print("RGB pixels:")
        # print(rgbMatrix[0:10, 0:10])
        return rgbMatrix

    def unDctAndQuantize(self, block, quantizeMatrix):
        block = self.unquantizeBlock(block, quantizeMatrix)
        block = self.unDctBlock(block)
        return block

    def unDctLayer(self, matrix, quantizeMatrix):
        return self.processForEveryBlock(matrix, self.unDctAndQuantize, [quantizeMatrix], True)

    def unDctBlock(self, block):
        newBlock = np.dot(np.dot(self.MT, block), self.M)
        #newBlock[0, 0] += 1024
        return newBlock

    @staticmethod
    def unquantizeBlock(block, quantizeMatrix):
        multiply = np.vectorize(lambda a, b: a * b)
        return multiply(block, np.array(quantizeMatrix).reshape(8,8))

if __name__ == "__main__":
    np.set_printoptions(suppress=True, precision=2)
    dct = Dct()
