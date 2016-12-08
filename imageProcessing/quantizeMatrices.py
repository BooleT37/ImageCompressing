import numpy as np


class QuantizeMatrices:
    DEFAULT_Y_MATRIX = [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]
    DEFAULT_CRCB_MATRIX = [
        [17, 18, 24, 47, 99, 99, 99, 99],
        [18, 21, 26, 66, 99, 99, 99, 99],
        [24, 26, 56, 99, 99, 99, 99, 99],
        [47, 66, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99]
    ]
    NO_COMPRESSION = np.ones(64, dtype=int).reshape(8, 8)

    @staticmethod
    def getCustom(alpha, gamma):
        matrix = np.zeros(64, dtype=int).reshape(8, 8)
        for i in range(8):
            for j in range(8):
                matrix[i, j] = int(alpha * (1 + gamma * (i + j + 2)))
        return matrix

    def getForQualityFactor(self, q, layer):
        defaultMatrix = self.DEFAULT_Y_MATRIX if layer == "Y" else self.DEFAULT_CRCB_MATRIX
        s = 5000 / q if q < 50 else 200 - 2 * q

        def changeQuality(value):
            newVal = int((s * value + 50) / 100)
            return 1 if newVal == 0 else newVal

        changeQualityVector = np.vectorize(changeQuality)

        return changeQualityVector(defaultMatrix)
