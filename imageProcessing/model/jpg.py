# width and height - we can count that from yLayer but better to pass explicitly
# subsamplingMode
# full yLayer
# subsampled Cb layer
# subsampled Cr layer


class Jpg:
    def __init__(self, width, height, yLayer, cbLayer, crLayer, subsamplingMode):
        self.width = width
        self.height = height
        self.yLayer = yLayer
        self.cbLayer = cbLayer
        self.crLayer = crLayer
        self.subsamplingMode = subsamplingMode
