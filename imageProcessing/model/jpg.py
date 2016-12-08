# width and height - we can count that from yLayer but better to pass explicitly
# subsamplingMode
# full yLayer
# subsampled Cb layer
# subsampled Cr layer


class Jpg:
    def __init__(self, height, width, yLayer, cbLayer, crLayer, subsamplingMode, quantizingMode, quantizeMatrixY, quantizeMatrixCrCb):
        self.height = height
        self.width = width
        self.yLayer = yLayer
        self.cbLayer = cbLayer
        self.crLayer = crLayer
        self.subsamplingMode = subsamplingMode
        self.quantizingMode = quantizingMode
        self.quantizeMatrixY = quantizeMatrixY
        self.quantizeMatrixCrCb = quantizeMatrixCrCb
