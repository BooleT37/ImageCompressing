import re
import math

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import font
from PIL import Image, ImageTk

from stateManager import *
from RgbToYCbCrConverter import *
from PsnrCounter import *
from ImageCompressor import *
from ImageSubsampler import *
from DCT import *
from constants import *

class App:
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
		
		self.stateManager = StateManager(self)
		self.psnrCounter = PsnrCounter()
		self.imageCompressor = ImageCompressor()
		self.ImageSubsampler = ImageSubsampler()
		
	def initializeWidgets(self, master):
		self.commandsFrame = Frame(master, height=20, borderwidth=1, relief=RIDGE)
		self.commandsFrame.pack(fill=X)
		
		self.psnrLabel = Label(self.commandsFrame, text="MSE:\nPSNR:")
		self.psnrLabel.pack()
		
		self.mainFrame = Frame(master)
		self.mainFrame.pack()
		
		#left frame
		self.leftFrame = Frame(self.mainFrame)
		self.leftFrame.pack(side=LEFT, fill=Y)
		
		self.leftImageButtonsFrame = Frame(self.leftFrame, pady=3, padx=2)
		self.leftImageButtonsFrame.pack(side=LEFT, fill=Y)
		
		self.openLeftImageButton = Button(
			self.leftImageButtonsFrame, text="load image", width=11, command=self.openLeftImageDialog
			)
		self.openLeftImageButton.pack()
		
		self.saveLeftImageButton = Button(
			self.leftImageButtonsFrame, text="save image", width=11, command=self.saveLeftImageDialog, state=DISABLED
			)
		self.saveLeftImageButton.pack()
		
		Label(self.leftImageButtonsFrame, text="Turn B&W:").pack()
		
		self.turnBwEwLeftImageButton = Button(
			self.leftImageButtonsFrame, text="Eual weights", width=11, command=self.turnBwEwLeftImage, state=DISABLED
			)
		self.turnBwEwLeftImageButton.pack()
		
		self.turnBwCcirLeftImageButton = Button(
			self.leftImageButtonsFrame, text="CCIR 601-1", width=11, command=self.turnBwCcirLeftImage, state=DISABLED
			)
		self.turnBwCcirLeftImageButton.pack()
		
		Label(self.leftImageButtonsFrame, text="YCbCr:").pack()
		
		self.YCbCrButtonsFrame = Frame(self.leftImageButtonsFrame)
		self.YCbCrButtonsFrame.pack()
		
		self.showYChannelForLeftImageButton = Button(
			self.YCbCrButtonsFrame, text="Y", width=2, command=self.showYChannelForLeftImage, state=DISABLED
			)
		self.showYChannelForLeftImageButton.pack(side=LEFT, padx=3)
		
		self.showCbChannelForLeftImageButton = Button(
			self.YCbCrButtonsFrame, text="Cb", width=2, command=self.showCbChannelForLeftImage, state=DISABLED
			)
		self.showCbChannelForLeftImageButton.pack(side=LEFT, padx=3)
		
		self.showCrChannelForLeftImageButton = Button(
			self.YCbCrButtonsFrame, text="Cr", width=2, command=self.showCrChannelForLeftImage, state=DISABLED
			)
		self.showCrChannelForLeftImageButton.pack(side=LEFT, padx=3)
		
		self.convertFromYCbCrLeftImageButton = Button(
			self.leftImageButtonsFrame, text="Convert from\nYCbCr", width=11, command=self.convertFromYCbCrLeftImage, state=DISABLED
			)
		self.convertFromYCbCrLeftImageButton.pack(pady=3)
		
		Label(self.leftImageButtonsFrame, text="Compression:").pack()
		
		self.uniformQuantizeRgbLeftImageButton = Button(
			self.leftImageButtonsFrame, text="UC RGB", width=11, command=self.uniformQuantizeRgbLeftImage, state=DISABLED
			)
		self.uniformQuantizeRgbLeftImageButton.pack()
		
		self.uniformQuantizeYCbCr1LeftImageButton = Button(
			self.leftImageButtonsFrame, text="UC YCrCb 222", width=11, command=self.uniformQuantizeYCbCr1LeftImage, state=DISABLED
			)
		self.uniformQuantizeYCbCr1LeftImageButton.pack()
		
		self.uniformQuantizeYCbCr2LeftImageButton = Button(
			self.leftImageButtonsFrame, text="UC YCrCb 312", width=11, command=self.uniformQuantizeYCbCr2LeftImage, state=DISABLED
			)
		self.uniformQuantizeYCbCr2LeftImageButton.pack()
		
		self.uniformQuantizeYCbCr3LeftImageButton = Button(
			self.leftImageButtonsFrame, text="UC YCrCb 321", width=11, command=self.uniformQuantizeYCbCr3LeftImage, state=DISABLED
			)
		self.uniformQuantizeYCbCr3LeftImageButton.pack()
		
		self.mcQuantizeLeftImageButton = Button(
			self.leftImageButtonsFrame, text="Median Cut", width=11, command=self.mcQuantizeLeftImage, state=DISABLED
			)
		self.mcQuantizeLeftImageButton.pack(pady=5)
		
		self.subsampleLeftImageButton = Button(
			self.leftImageButtonsFrame, text="Subsample", width=11, command=self.subsampleLeftImage, state=DISABLED
			)
		self.subsampleLeftImageButton.pack(pady=5)
		
		Label(self.leftImageButtonsFrame, text="Mode:").pack()
		
		self.leftImageSubsamplingMode = StringVar()
		self.leftImageSubsamplingMode.set("2h1v")
		
		Radiobutton(self.leftImageButtonsFrame, text="2h1v", variable=self.leftImageSubsamplingMode, value="2h1v").pack()
		Radiobutton(self.leftImageButtonsFrame, text="1h2v", variable=self.leftImageSubsamplingMode, value="1h2v").pack()
		Radiobutton(self.leftImageButtonsFrame, text="2h2v", variable=self.leftImageSubsamplingMode, value="2h2v").pack()
		
		self.restoreLeftImageButton = Button(
			self.leftImageButtonsFrame, text="Restore image", width=11, command=self.restoreLeftImage, state=DISABLED
			)
		self.restoreLeftImageButton.pack(pady=20)
		
		self.leftImageLabel = Label(self.leftFrame, width=40, height=30, relief=RIDGE)
		self.leftImageLabel.pack()
		
		#right frame
		self.rightFrame = Frame(self.mainFrame)
		self.rightFrame.pack(side=LEFT, fill=Y)
		
		self.rightImageButtonsFrame = Frame(self.rightFrame, pady=3, padx=2)
		self.rightImageButtonsFrame.pack(side=RIGHT, fill=Y);
		
		self.openRightImageButton = Button(
			self.rightImageButtonsFrame, text="load image", width=11, command=self.openRightImageDialog
			)
		self.openRightImageButton.pack()
		
		self.saveRightImageButton = Button(
			self.rightImageButtonsFrame, text="save image", width=11, command=self.saveRightImageDialog, state=DISABLED
			)
		self.saveRightImageButton.pack()
		
		Label(self.rightImageButtonsFrame, text="Turn B&W:").pack()
		
		self.turnBwEwRightImageButton = Button(
			self.rightImageButtonsFrame, text="Eual weights", width=11, command=self.turnBwEwRightImage, state=DISABLED
			)
		self.turnBwEwRightImageButton.pack()
		
		self.turnBwCcirRightImageButton = Button(
			self.rightImageButtonsFrame, text="CCIR 601-1", width=11, command=self.turnBwCcirRightImage, state=DISABLED
			)
		self.turnBwCcirRightImageButton.pack()
		
		Label(self.rightImageButtonsFrame, text="YCbCr:").pack()
		
		self.YCbCrButtonsFrame = Frame(self.rightImageButtonsFrame)
		self.YCbCrButtonsFrame.pack()
		
		self.showYChannelForRightImageButton = Button(
			self.YCbCrButtonsFrame, text="Y", width=2, command=self.showYChannelForRightImage, state=DISABLED
			)
		self.showYChannelForRightImageButton.pack(side=LEFT, padx=3)
		
		self.showCbChannelForRightImageButton = Button(
			self.YCbCrButtonsFrame, text="Cb", width=2, command=self.showCbChannelForRightImage, state=DISABLED
			)
		self.showCbChannelForRightImageButton.pack(side=LEFT, padx=3)
		
		self.showCrChannelForRightImageButton = Button(
			self.YCbCrButtonsFrame, text="Cr", width=2, command=self.showCrChannelForRightImage, state=DISABLED
			)
		self.showCrChannelForRightImageButton.pack(side=LEFT, padx=3)
		
		self.convertFromYCbCrRightImageButton = Button(
			self.rightImageButtonsFrame, text="Convert from\nYCbCr", width=11, command=self.convertFromYCbCrRightImage, state=DISABLED
			)
		self.convertFromYCbCrRightImageButton.pack(pady=3)
		
		Label(self.rightImageButtonsFrame, text="Compression:").pack()
		
		self.uniformQuantizeRgbRightImageButton = Button(
			self.rightImageButtonsFrame, text="UC RGB", width=11, command=self.uniformQuantizeRgbRightImage, state=DISABLED
			)
		self.uniformQuantizeRgbRightImageButton.pack()
		
		self.uniformQuantizeYCbCr1RightImageButton = Button(
			self.rightImageButtonsFrame, text="UC YCrCb 222", width=11, command=self.uniformQuantizeYCbCr1RightImage, state=DISABLED
			)
		self.uniformQuantizeYCbCr1RightImageButton.pack()
		
		self.uniformQuantizeYCbCr2RightImageButton = Button(
			self.rightImageButtonsFrame, text="UC YCrCb 312", width=11, command=self.uniformQuantizeYCbCr2RightImage, state=DISABLED
			)
		self.uniformQuantizeYCbCr2RightImageButton.pack()
		
		self.uniformQuantizeYCbCr3RightImageButton = Button(
			self.rightImageButtonsFrame, text="UC YCrCb 321", width=11, command=self.uniformQuantizeYCbCr3RightImage, state=DISABLED
			)
		self.uniformQuantizeYCbCr3RightImageButton.pack()
		
		self.mcQuantizeRightImageButton = Button(
			self.rightImageButtonsFrame, text="Median Cut", width=11, command=self.mcQuantizeRightImage, state=DISABLED
			)
		self.mcQuantizeRightImageButton.pack(pady=5)
		
		self.subsampleRightImageButton = Button(
			self.rightImageButtonsFrame, text="Subsample", width=11, command=self.subsampleRightImage, state=DISABLED
			)
		self.subsampleRightImageButton.pack(pady=5)
		
		Label(self.rightImageButtonsFrame, text="Mode:").pack()
		
		self.rightImageSubsamplingMode = StringVar()
		self.rightImageSubsamplingMode.set("2h1v")
		
		Radiobutton(self.rightImageButtonsFrame, text="2h1v", variable=self.rightImageSubsamplingMode, value="2h1v").pack()
		Radiobutton(self.rightImageButtonsFrame, text="1h2v", variable=self.rightImageSubsamplingMode, value="1h2v").pack()
		Radiobutton(self.rightImageButtonsFrame, text="2h2v", variable=self.rightImageSubsamplingMode, value="2h2v").pack()
		
		self.restoreRightImageButton = Button(
			self.rightImageButtonsFrame, text="Restore image", width=11, command=self.restoreRightImage, state=DISABLED
			)
		self.restoreRightImageButton.pack(pady=20)
		
		self.rightImageLabel = Label(self.rightFrame, width=40, height=30, relief=RIDGE)
		self.rightImageLabel.pack()
		
	def	getImagePixels(self, side):
		pixels = list(self.image[side].getdata())
		if (self.image[side].mode == 'L' or self.image[side].mode == '1'):
			pixels = list(map(lambda pixel: (pixel, pixel, pixel), pixels))
		return pixels
	
	def replaceImage(self, side, mode, pixels):
		image = self.image[side]
		label = self.leftImageLabel if side == LEFT_SIDE else self.rightImageLabel
		newImage = Image.new(mode, image.size)
		newImage.putdata(pixels)
		photo = ImageTk.PhotoImage(newImage)
		label.configure(image=photo)
		label.image = photo
		self.image[side] = newImage
		self.countPsnr()
	
	def openLeftImageDialog(self):
		self.openImageDialog(side=LEFT_SIDE)
	
	def openRightImageDialog(self):
		self.openImageDialog(side=RIGHT_SIDE)
	
	def openImageDialog(self, side):
		fname = askopenfilename(filetypes=(("JPEG", "*.jpg;*.jpeg"),
										   ("PNG", "*.png"),
										   ("BMP", "*.bmp"),
										   ("TIFF,", "*.tiff"),
										   ("All files", "*.*") ), initialdir="Jpg_samples")
		if fname:
			self.loadImage(fname, side)
	
	def loadImage(self, fname, side):
		self.image[side] = Image.open(fname)
		photo = ImageTk.PhotoImage(self.image[side])
		width = 512 if photo.width() > 512 else 0
		height = 512 if photo.height() > 512 else 0
		if side == LEFT_SIDE:
			self.leftImageLabel.configure(image=photo, width=width, height=height)
			self.leftImageLabel.image = photo
		else:
			self.rightImageLabel.configure(image=photo, width=width, height=height)
			self.rightImageLabel.image = photo
		self.countPsnr()
		self.yCbCrData[side] = None
		self.stateManager.changeState(state=MAIN, side=side)
			
	def saveLeftImageDialog(self):
		self.saveImageDialog(side=LEFT_SIDE)
		
	def saveRightImageDialog(self):
		self.saveImageDialog(side=RIGHT_SIDE)
		
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
			self.psnrLabel.configure("MSE is undefined\nPSNR is undefined, Image sizes are not equal")
			return;
		leftImagePixels = self.getImagePixels(side = LEFT_SIDE)
		rightImagePixels = self.getImagePixels(side = RIGHT_SIDE)
		n = leftImage.size[0] * leftImage.size[1] #width * height
		leftImageMode = leftImage.mode
		rightImageMode = rightImage.mode
		
		##print("left image pixels:\n{}".format(leftImagePixels[:30]))
		#if (leftImageMode == 'L' or leftImageMode == '1'):
		#	leftImagePixels = list(map((lambda pixel: (pixel, pixel, pixel)), leftImagePixels))
		##print("left image pixels:\n{}".format(leftImagePixels[:30]))
		#	
		#print("right image pixels:\n{}".format(rightImagePixels[:30]))
		#if (rightImageMode == 'L' or rightImageMode == '1'):
		#	#print("mode is {}, converting...".format(rightImageMode))
		#	rightImagePixels = list(map((lambda pixel: (pixel, pixel, pixel)), rightImagePixels))
		##print("right image pixels:\n{}".format(rightImagePixels[:30]))
		
		mse = self.psnrCounter.countMse(leftImagePixels, rightImagePixels, n)
		try:
			psnr = self.psnrCounter.countPsnr(mse)
			self.psnrLabel.configure(text = "MSE = {}\nPSNR = {}".format(mse, psnr))
		except MseIsZeroException:
			self.psnrLabel.configure(text = "MSE = 0\nPSNR is undefined")
			
	def turnBwEwLeftImage(self):
		self.turnBlackAndWhite(mode = 'ew', side = LEFT_SIDE)
		
	def turnBwEwRightImage(self):
		self.turnBlackAndWhite(mode = 'ew', side = RIGHT_SIDE)
		
	def turnBwCcirLeftImage(self):
		self.turnBlackAndWhite(mode = 'ccir', side = LEFT_SIDE)
		
	def turnBwCcirRightImage(self):
		self.turnBlackAndWhite(mode = 'ccir', side = RIGHT_SIDE)
		
	def equalWeightsMethod(self, pixel):
		return round((pixel[0] + pixel[1] + pixel[2]) / 3)
		
	def ccirWeightsMethod(self, pixel):
		return ((77 * pixel[0]) >> 8) + ((150 * pixel[1]) >> 8) + ((29 * pixel[2]) >> 8)
	
	def turnBlackAndWhite(self, mode, side):
		image = self.image[side]
		if image.mode == 'L':
			return
		self.originalImage[side] = image #saving the link to be able to restore image later
		label = self.leftImageLabel if side == LEFT_SIDE else self.rightImageLabel
		pixels = list(image.getdata())
		newPixels = list(map((self.equalWeightsMethod) if mode == 'ew' else (self.ccirWeightsMethod), pixels))
		
		self.replaceImage(side, "L", newPixels)
			
		self.stateManager.changeState(state = GRAYSCALE, side = side)
		
	def restoreLeftImage(self):
		self.restoreImage(side = LEFT_SIDE)
	
	def restoreRightImage(self):
		self.restoreImage(side = RIGHT_SIDE)
	
	def restoreImage(self, side):
		image = self.image[side]
		originalImage = self.originalImage[side]
		if (side == LEFT_SIDE):
			label = self.leftImageLabel
		else:
			label = self.rightImageLabel
		self.image[side] = originalImage
		photo = ImageTk.PhotoImage(originalImage)
		label.configure(image=photo)
		label.image = photo
		
		self.stateManager.changeState(state = MAIN, side = side)
		self.countPsnr()
	
	def showYChannelForLeftImage(self):
		self.showYCbCrChannel(channel = 'Y', side = LEFT_SIDE)
	
	def showCbChannelForLeftImage(self):
		self.showYCbCrChannel(channel = 'Cb', side = LEFT_SIDE)
	
	def showCrChannelForLeftImage(self):
		self.showYCbCrChannel(channel = 'Cr', side = LEFT_SIDE)
	
	def showYChannelForRightImage(self):
		self.showYCbCrChannel(channel = 'Y', side = RIGHT_SIDE)
	
	def showCbChannelForRightImage(self):
		self.showYCbCrChannel(channel = 'Cb', side = RIGHT_SIDE)
	
	def showCrChannelForRightImage(self):
		self.showYCbCrChannel(channel = 'Cr', side = RIGHT_SIDE)
		
	def showYCbCrChannel(self, channel, side):
		if (self.stateManager.currentState[side] == GRAYSCALE):
			self.restoreImage(side)
		image = self.image[side]
		if (side == LEFT_SIDE):
			label = self.leftImageLabel
			self.showYChannelForLeftImageButton.configure(font = "SegoeUI 9 normal")
			self.showCbChannelForLeftImageButton.configure(font = "SegoeUI 9 normal")
			self.showCrChannelForLeftImageButton.configure(font = "SegoeUI 9 normal")
			button = self.showYChannelForLeftImageButton if channel == 'Y' else self.showCbChannelForLeftImageButton if channel == 'Cb' else self.showCrChannelForLeftImageButton
		else:
			label = self.rightImageLabel
			self.showYChannelForRightImageButton.configure(font = "SegoeUI 9 normal")
			self.showCbChannelForRightImageButton.configure(font = "SegoeUI 9 normal")
			self.showCrChannelForRightImageButton.configure(font = "SegoeUI 9 normal")
			button = self.showYChannelForRightImageButton if channel == 'Y' else self.showCbChannelForRightImageButton if channel == 'Cb' else self.showCrChannelForRightImageButton
	
		if (self.stateManager.currentState[side] == CHANNEL_SHOWN):
			if (self.stateManager.currentChannel[side] == channel):
				self.stateManager.changeState(state = MAIN, side = side)
				originalImage = self.originalImage[side]
				photo = ImageTk.PhotoImage(originalImage)
				label.configure(image=photo)
				label.image = photo
				self.image[side] = originalImage
				return
		else:
			self.originalImage[side] = image
			
			self.stateManager.changeState(state = MAIN, side = side)
		self.stateManager.changeState(state = CHANNEL_SHOWN, side = side, channel = channel)
		
		channelIndex = 0 if channel == 'Y' else 1 if channel == 'Cb' else 2
		
		button.configure(font = "SegoeUI 9 bold")
			
		YCbCrPixels = RgbToYCbCrConverter.rgbToYCbCr(self.getImagePixels(side))
		newPixels = list(map(lambda pixel: pixel[channelIndex], YCbCrPixels))
		
		self.replaceImage(side, "L", newPixels)
		
	def convertFromYCbCrLeftImage(self):
		self.convertFromYCbCr(side = LEFT_SIDE)
		
	def convertFromYCbCrRightImage(self):
		self.convertFromYCbCr(side = RIGHT_SIDE)
		
	def convertFromYCbCr(self, side):		
		newPixels = RgbToYCbCrConverter.yCbCrToRgb(RgbToYCbCrConverter.rgbToYCbCr(self.getImagePixels(side)))
			
		self.stateManager.changeState(state = MAIN, side = side)
		
		self.replaceImage(side, "RGB", newPixels)
	
	def uniformQuantizeRgbLeftImage(self):
		self.uniformQuantizeRgb(side = LEFT_SIDE)
		
	def uniformQuantizeRgbRightImage(self):
		self.uniformQuantizeRgb(side = RIGHT_SIDE)
	
	def uniformQuantizeRgb(self, side):
		self.originalImage[side] = self.image[side]
		pixels = self.getImagePixels(side)
		newPixels = self.imageCompressor.uniformQuantizeRgb(pixels, 2)
		self.replaceImage(side, "RGB", newPixels)
		self.stateManager.changeState(state = COMPRESSED, side = side)
		
		
	def uniformQuantizeYCbCr1LeftImage(self):
		self.uniformQuantizeYCbCr(side = LEFT_SIDE, method = METHOD_222)
		
	def uniformQuantizeYCbCr1RightImage(self):
		self.uniformQuantizeYCbCr(side = RIGHT_SIDE, method = METHOD_222)
	
	def uniformQuantizeYCbCr2LeftImage(self):
		self.uniformQuantizeYCbCr(side = LEFT_SIDE, method = METHOD_312)
	
	def uniformQuantizeYCbCr2RightImage(self):
		self.uniformQuantizeYCbCr(side = RIGHT_SIDE, method = METHOD_312)
		
	def uniformQuantizeYCbCr3LeftImage(self):
		self.uniformQuantizeYCbCr(side = LEFT_SIDE, method = METHOD_321)
		
	def uniformQuantizeYCbCr3RightImage(self):
		self.uniformQuantizeYCbCr(side = RIGHT_SIDE, method = METHOD_321)
		
	
	def uniformQuantizeYCbCr(self, side, method):
		self.originalImage[side] = self.image[side]
		pixels = self.getImagePixels(side)
		newPixels = self.imageCompressor.uniformQuantizeYCbCr(pixels, method)
		self.replaceImage(side, "RGB", newPixels)
		self.stateManager.changeState(state = COMPRESSED, side = side)
		
	def mcQuantizeLeftImage(self):
		self.mcQuantizeImage(side = LEFT_SIDE)
		
	def mcQuantizeRightImage(self):
		self.mcQuantizeImage(side = RIGHT_SIDE)
		
	def mcQuantizeImage(self, side):
		self.originalImage[side] = self.image[side]
		pixels = self.getImagePixels(side)
		newPixels = self.imageCompressor.medianCutQuantize(pixels)
		self.replaceImage(side, "RGB", newPixels)
		self.stateManager.changeState(state = COMPRESSED, side = side)
		
	def subsampleLeftImage(self):
		self.subsampleImage(side = LEFT_SIDE, mode = self.leftImageSubsamplingMode.get())
	
	def subsampleRightImage(self):
		self.subsampleImage(side = RIGHT_SIDE, mode = self.rightImageSubsamplingMode.get())
	
	def subsampleImage(self, side, mode):
		#print("{}, {}".format(side, mode))
		self.originalImage[side] = self.image[side]
		pixels = self.getImagePixels(side)
		width = self.image[side].width
		newPixels = self.ImageSubsampler.SubsampleImage(pixels, mode, width)
		self.replaceImage(side, "RGB", newPixels)
		self.stateManager.changeState(state = COMPRESSED, side = side)
		
	
root = Tk()
root.wm_title("IC task 1")

app = App(root)

root.mainloop()