import numpy as np
# import time
from .rgbToYCbCrConverter import RgbToYCbCrConverter


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

    def SubsampleImage(self, rgbPixels, mode, shrinkImage=False):
        # start_time1 = time.time()
        yCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(rgbPixels)
        # print("1. Converting pixels from YCbCr to RGB: %s seconds" % (time.time() - start_time1))
        # start_time2 = time.time()

        newYCbCrPixels = np.ndarray(yCbCrPixels.shape, yCbCrPixels.dtype)

        height = yCbCrPixels.shape[0]
        width = yCbCrPixels.shape[1]
        for i in range(0, height, 2):
            lastRow = (i == height - 1)
            for j in range(0, width, 2):
                lastCol = (j == width - 1)
                pixQuad = [
                    yCbCrPixels[i][j], None, None, None
                ]
                if lastCol:
                    pixQuad[1] = yCbCrPixels[i][j]
                    if lastRow:
                        pixQuad[2] = pixQuad[3] = yCbCrPixels[i][j]
                    else:
                        pixQuad[2] = pixQuad[3] = yCbCrPixels[i + 1][j]
                else:
                    pixQuad[1] = yCbCrPixels[i][j + 1]
                    if lastRow:
                        pixQuad[2] = yCbCrPixels[i][j]
                        pixQuad[3] = yCbCrPixels[i][j + 1]
                    else:
                        pixQuad[2] = yCbCrPixels[i + 1][j]
                        pixQuad[3] = yCbCrPixels[i + 1][j + 1]

                newPixQuad = [None, None, None, None]
                for k in range(4):
                    newPixQuad[k] = (
                        pixQuad[k][0],
                        pixQuad[self.pixelTransitions[mode][k]][1],
                        pixQuad[self.pixelTransitions[mode][k]][2]
                    )

                newYCbCrPixels[i][j] = newPixQuad[0]
                if not lastCol:
                    newYCbCrPixels[i][j + 1] = newPixQuad[1]
                if not lastRow:
                    newYCbCrPixels[i + 1][j] = newPixQuad[2]
                if not lastCol and not lastRow:
                    newYCbCrPixels[i + 1][j + 1] = newPixQuad[3]

        # print("2. Filling the matrix: %s seconds" % (time.time() - start_time2))
        # start_time3 = time.time()

        newRgbPixels = RgbToYCbCrConverter.yCbCrToRgb(newYCbCrPixels)
        # endTime = time.time()
        # print("3. Converting pixels back from RGB to YCbCr: %s seconds" % (endTime - start_time3))
        # print("Total time: %s seconds" % (endTime - start_time1))
        # print("\nYCbCr:\n{0} {1}\t=>\t{4} {5}\n{2} {3}\t\t{6} {7}\n".format(
        #     yCbCrPixels[0][0], yCbCrPixels[0][1], yCbCrPixels[1][0], yCbCrPixels[1][1],
        #     newYCbCrPixels[0][0], newYCbCrPixels[0][1], newYCbCrPixels[1][0], newYCbCrPixels[1][1]
        # ))
    #
    #
        # print("\nRGB:\n{0} {1}\t=>\t{4} {5}\n{2} {3}\t\t{6} {7}\n".format(
        #     rgbPixels[0][0], rgbPixels[0][1], rgbPixels[1][0], rgbPixels[1][1],
        #     newRgbPixels[0][0], newRgbPixels[0][1], newRgbPixels[1][0], newRgbPixels[1][1]
        # ))

        return newRgbPixels


class ImageSubsamplerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
