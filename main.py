import re
import math
import numpy as np

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

import inspect

from gui.stateManager import *
from gui import WidgetsManager

from imageProcessing import RgbToYCbCrConverter
from imageProcessing.imageCompressor import *
from imageProcessing import ImageSubsampler
from imageProcessing import Dct

from tools import PsnrCounter
from tools import MseIsZeroException
from constants import *

from PIL import Image, ImageTk


class Main:
    def __init__(self, master):
        self.initializeWidgets(master)

        self.image = {
            LEFT_SIDE: None,
            RIGHT_SIDE: None
        }

        self.originalImage = {
            LEFT_SIDE: None,
            RIGHT_SIDE: None
        }

        self.yCbCrData = {
            LEFT_SIDE: None,
            RIGHT_SIDE: None
        }

        self.stateManager = StateManager(self.widgets)
        self.psnrCounter = PsnrCounter()
        self.imageCompressor = ImageCompressor()
        self.ImageSubsampler = ImageSubsampler()

    def initializeWidgets(self, master):
        self.widgetsManager = widgetsManager = WidgetsManager()
        widgetsManager.createWidgets(master)
        self.widgets = self.widgetsManager.widgets

        self.bindButtons()

    def bindButtons(self):
        widgets = self.widgets

        widgets["openImageButtons"].bind(self.openImageDialog)
        widgets["saveImageButtons"].bind(self.saveImageDialog)
        widgets["turnBWEwButtons"].bind(self.turnBWEw)
        widgets["turnBwCcirButtons"].bind(self.turnBWCcir)
        widgets["showYChannelButtons"].bind(self.showYChannel)
        widgets["showCbChannelButtons"].bind(self.showCbChannel)
        widgets["showCrChannelButtons"].bind(self.showCrChannel)
        widgets["uniformQuantizeRgbButtons"].bind(self.uniformQuantizeRgb)
        widgets["uniformQuantizeYCbCr1Buttons"].bind(self.uniformQuantizeYCbCr1)
        widgets["uniformQuantizeYCbCr2Buttons"].bind(self.uniformQuantizeYCbCr2)
        widgets["uniformQuantizeYCbCr3Buttons"].bind(self.uniformQuantizeYCbCr3)
        widgets["mcQuantizeButtons"].bind(self.mcQuantize)
        widgets["subsampleButtons"].bind(self.subsample)
        widgets["restoreImageButtons"].bind(self.restoreImage)

    def getImageLabel(self, side):
        return self.widgets["imageLabels"].left if side == LEFT_SIDE else self.widgets["imageLabels"].right

    def getImagePixels(self, side):
        pixels = list(self.image[side].getdata())
        if (self.image[side].mode == 'L' or self.image[side].mode == '1'):
            pixels = list(map(lambda pixel: (pixel, pixel, pixel), pixels))
        return pixels

    def replaceImage(self, side, mode, pixels):
        image = self.image[side]
        label = self.getImageLabel(side)
        newImage = Image.new(mode, image.size)
        newImage.putdata(pixels)
        photo = ImageTk.PhotoImage(newImage)
        label.configure(image=photo)
        label.image = photo
        self.image[side] = newImage
        self.countPsnr()

    def openImageDialog(self, side):
        fname = askopenfilename(filetypes=(("JPEG", "*.jpg;*.jpeg"),
                                           ("PNG", "*.png"),
                                           ("BMP", "*.bmp"),
                                           ("TIFF,", "*.tiff"),
                                           ("All files", "*.*")), initialdir="Jpg_samples")
        if fname:
            self.loadImage(fname, side)

    def loadImage(self, fname, side):
        self.image[side] = Image.open(fname)
        photo = ImageTk.PhotoImage(self.image[side])
        width = 512 if photo.width() > 512 else 0
        height = 512 if photo.height() > 512 else 0

        imageLabels = self.widgets["imageLabels"]
        imageLabel = imageLabels.left if side == LEFT_SIDE else imageLabels.right
        imageLabel.configure(image=photo, width=width, height=height)
        imageLabel.image = photo
        self.countPsnr()
        self.yCbCrData[side] = None
        self.stateManager.changeState(state=MAIN, side=side)

    def saveImageDialog(self, side):
        fname = asksaveasfilename(filetypes=(("BMP", "*.bmp"),
                                             ("PNG", "*.png"),
                                             ("TIFF,", "*.tiff")), initialdir="Test_Images", defaultextension=".bmp")
        if fname:
            self.saveImage(fname, side)

    def saveImage(self, fname, side):
        m = re.search('\.(\w+)$', fname)
        extension = m.group(1)
        self.image[side].save(fname, extension)

    def countPsnr(self):
        leftImage = self.image[LEFT_SIDE]
        rightImage = self.image[RIGHT_SIDE]
        if (leftImage is None or rightImage is None):
            return
        if (leftImage.size != rightImage.size):
            self.widgets["psnrLabel"].configure(text="MSE is undefined\nPSNR is undefined, Image sizes are not equal")
            return;
        leftImagePixels = self.getImagePixels(side=LEFT_SIDE)
        rightImagePixels = self.getImagePixels(side=RIGHT_SIDE)
        n = leftImage.size[0] * leftImage.size[1]  # width * height
        leftImageMode = leftImage.mode
        rightImageMode = rightImage.mode

        ##print("left image pixels:\n{}".format(leftImagePixels[:30]))
        # if (leftImageMode == 'L' or leftImageMode == '1'):
        #	leftImagePixels = list(map((lambda pixel: (pixel, pixel, pixel)), leftImagePixels))
        ##print("left image pixels:\n{}".format(leftImagePixels[:30]))
        #
        # print("right image pixels:\n{}".format(rightImagePixels[:30]))
        # if (rightImageMode == 'L' or rightImageMode == '1'):
        #	#print("mode is {}, converting...".format(rightImageMode))
        #	rightImagePixels = list(map((lambda pixel: (pixel, pixel, pixel)), rightImagePixels))
        ##print("right image pixels:\n{}".format(rightImagePixels[:30]))

        mse = self.psnrCounter.countMse(leftImagePixels, rightImagePixels, n)
        try:
            psnr = self.psnrCounter.countPsnr(mse)
            self.widgets["psnrLabel"].configure(text="MSE = {:.4f}\nPSNR = {:.4f}".format(mse, psnr))
        except MseIsZeroException:
            self.widgets["psnrLabel"].configure(text="MSE = 0\nPSNR is undefined")

    def turnBWEw(self, side):
        self.turnBlackAndWhite('ew', side)

    def turnBWCcir(self, side):
        self.turnBlackAndWhite('ccir', side)

    def equalWeightsMethod(self, pixel):
        return round((pixel[0] + pixel[1] + pixel[2]) / 3)

    def ccirWeightsMethod(self, pixel):
        return ((77 * pixel[0]) >> 8) + ((150 * pixel[1]) >> 8) + ((29 * pixel[2]) >> 8)

    def turnBlackAndWhite(self, mode, side):
        image = self.image[side]
        if image.mode == 'L':
            return
        self.originalImage[side] = image  # saving the link to be able to restore image later
        label = self.getImageLabel(side)
        pixels = list(image.getdata())
        newPixels = list(map((self.equalWeightsMethod) if mode == 'ew' else (self.ccirWeightsMethod), pixels))

        self.replaceImage(side, "L", newPixels)

        self.stateManager.changeState(state=GRAYSCALE, side=side)

    def showYChannel(self, side):
        self.showYCbCrChannel('Y', side)

    def showCbChannel(self, side):
        self.showYCbCrChannel('Cb', side)

    def showCrChannel(self, side):
        self.showYCbCrChannel('Cr', side)

    def showYCbCrChannel(self, channel, side):
        widgets = self.widgets
        yButtons = widgets["showYChannelButtons"]
        cbButtons = widgets["showCbChannelButtons"]
        crButtons = widgets["showCrChannelButtons"]

        if (self.stateManager.currentState[side] == GRAYSCALE):
            self.restoreImage(side)
        image = self.image[side]
        label = self.getImageLabel(side)
        if (side == LEFT_SIDE):
            yButton = yButtons.left
            cbButton = cbButtons.left
            crButton = crButtons.left
            yButton.configure(font="SegoeUI 9 normal")
            cbButton.configure(font="SegoeUI 9 normal")
            crButton.configure(font="SegoeUI 9 normal")
            button = yButton if channel == 'Y' else cbButton if channel == 'Cb' else crButton
        else:
            yButton = yButtons.right
            cbButton = cbButtons.right
            crButton = crButtons.right
            yButton.configure(font="SegoeUI 9 normal")
            cbButton.configure(font="SegoeUI 9 normal")
            crButton.configure(font="SegoeUI 9 normal")
            button = yButton if channel == 'Y' else cbButton if channel == 'Cb' else crButton

        if (self.stateManager.currentState[side] == CHANNEL_SHOWN):
            if (self.stateManager.currentChannel[side] == channel):
                self.stateManager.changeState(state=MAIN, side=side)
                originalImage = self.originalImage[side]
                photo = ImageTk.PhotoImage(originalImage)
                label.configure(image=photo)
                label.image = photo
                self.image[side] = originalImage
                return
        else:
            self.originalImage[side] = image

            self.stateManager.changeState(state=MAIN, side=side)
        self.stateManager.changeState(state=CHANNEL_SHOWN, side=side, channel=channel)

        channelIndex = 0 if channel == 'Y' else 1 if channel == 'Cb' else 2

        button.configure(font="SegoeUI 9 bold")

        YCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(self.getImagePixels(side))
        newPixels = list(map(lambda pixel: pixel[channelIndex], YCbCrPixels))

        self.replaceImage(side, "L", newPixels)

    def convertFromYCbCrLeftImage(self):
        self.convertFromYCbCr(side=LEFT_SIDE)

    def convertFromYCbCrRightImage(self):
        self.convertFromYCbCr(side=RIGHT_SIDE)

    def convertFromYCbCr(self, side):
        newPixels = RgbToYCbCrConverter.yCbCrToRgb(RgbToYCbCrConverter.rgbToYCbCr(self.getImagePixels(side)))

        self.stateManager.changeState(state=MAIN, side=side)

        self.replaceImage(side, "RGB", newPixels)

    def uniformQuantizeRgb(self, side):
        self.originalImage[side] = self.image[side]
        pixels = self.getImagePixels(side)
        newPixels = self.imageCompressor.uniformQuantizeRgb(pixels, 2)
        self.replaceImage(side, "RGB", newPixels)
        self.stateManager.changeState(state=COMPRESSED, side=side)

    def uniformQuantizeYCbCr1(self, side):
        self.uniformQuantizeYCbCr(METHOD_222, side)

    def uniformQuantizeYCbCr2(self, side):
        self.uniformQuantizeYCbCr(METHOD_312, side)

    def uniformQuantizeYCbCr3(self, side):
        self.uniformQuantizeYCbCr(METHOD_321, side)

    def uniformQuantizeYCbCr(self, method, side):
        self.originalImage[side] = self.image[side]
        pixels = self.getImagePixels(side)
        newPixels = self.imageCompressor.uniformQuantizeYCbCr(pixels, method)
        self.replaceImage(side, "RGB", newPixels)
        self.stateManager.changeState(state=COMPRESSED, side=side)

    def mcQuantize(self, side):
        self.originalImage[side] = self.image[side]
        pixels = self.getImagePixels(side)
        newPixels = self.imageCompressor.medianCutQuantize(pixels)
        self.replaceImage(side, "RGB", newPixels)
        self.stateManager.changeState(state=COMPRESSED, side=side)

    def subsample(self, side):
        mode = self.widgetsManager.subsamplingMode[0].get() if side == LEFT_SIDE else \
        self.widgetsManager.subsamplingMode[1].get()
        self.originalImage[side] = self.image[side]
        pixelsArray = self.getImagePixels(side)
        pixels = np.ndarray((self.image[side].width, self.image[side].height), buffer=np.array(pixelsArray))
        newPixels = self.ImageSubsampler.SubsampleImage(pixels, mode).ravel()
        self.replaceImage(side, "RGB", newPixels)
        self.stateManager.changeState(state=COMPRESSED, side=side)

    def restoreImage(self, side):
        image = self.image[side]
        originalImage = self.originalImage[side]
        label = self.getImageLabel(side)
        self.image[side] = originalImage
        photo = ImageTk.PhotoImage(originalImage)
        label.configure(image=photo)
        label.image = photo

        self.stateManager.changeState(state=MAIN, side=side)
        self.countPsnr()


root = Tk()
root.wm_title("IC task 1")

app = Main(root)

root.mainloop()
