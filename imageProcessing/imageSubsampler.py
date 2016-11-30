import numpy as np
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
        pixels = RgbToYCbCrConverter.rgbToYCbCr(rgbPixels)

        newPixels = np.ndarray(pixels.shape, pixels.dtype)

        height = pixels.shape[0]
        width = pixels.shape[1]
        # print ("Width: {}, Height: {}".format(width, height))

        print("mode is {}".format(mode))

        for i in range(0, height, 2):
            lastRow = (i == height - 1)
            for j in range(0, width, 2):
                lastCol = (j == width - 1)
                pixQuad = [
                    pixels[i][j],
                    pixels[i][j] if lastCol else pixels[i][j + 1],
                    pixels[i][j] if lastRow else pixels[i + 1][j],
                    pixels[i][j] if lastCol and lastRow else pixels[i][j + 1] if lastRow else pixels[i + 1][j]
                ]
                newPixQuad = [
                    (pixQuad[k][0], pixQuad[self.pixelTransitions[mode][k]][1],
                     pixQuad[self.pixelTransitions[mode][k]][2])
                    for k in range(4)]

                newPixels[i][j] = newPixQuad[0]
                if not lastCol:
                    newPixels[i][j + 1] = newPixQuad[1]
                if not lastRow:
                    newPixels[i + 1][j] = newPixQuad[2]
                if not lastCol and not lastRow:
                    newPixels[i + 1][j + 1] = newPixQuad[3]

        # if (height % 2 == 1):
        #	lastRow = height - 1
        #	if (mode == "1h2v"):
        #		for i in range(width):
        #			newPixels[lastRow][i] = pixels[lastRow][i]
        #	else:
        #		for i in range(width, step=2):
        #			pixel1 = pixels[lastRow][i]
        #			pixel2 = pixels[lastRow][i + 1]
        #			newPixels[lastRow][i] = pixel1
        #			newPixels[lastRow][i + 1] = (pixel2[0], pixel1[1], pixel1[2])
        #
        # if (width % 2 == 1):
        #	lastCol = width - 1
        #	if (mode == "2h1v"):
        #		for i in range(height):
        #			newPixels[i][lastCol] = pixels[i][lastCol]
        #	else:
        #		for i in range(height, step=2):
        #			pixel1 = pixels[i][lastCol]
        #			pixel3 = pixels[i + 1][lastCol]
        #			newPixels[i][lastCol] = pixel1
        #			newPixels[i + 1][lastCol] = (pixel3[0], pixel1[1], pixel1[2])

        # if (height % 2 == 1 and width % 2 == 1 and mode == "2h2v"):



        # for index, pixel in enumerate(pixels):
        #	if (pixel is None):
        #		row = int(index / width)
        #		col = index - row * width
        #		print ("Pixel {} is None ({} row, {} col)".format(index, row, col))

        rgbPixels = RgbToYCbCrConverter.yCbCrToRgb(newPixels)

        return rgbPixels


class ImageSubsamplerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
