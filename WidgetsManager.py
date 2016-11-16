from tkinter import *
import tkinter as tk
from tkinter import ttk

from Constants import *
from functools import partial

class WidgetsManager:
	def __init__(self):
		self.widgets = {}
		
	def createWidgets(self, root):
		self.createHeader(root)
		self.createMainFrame(root)
		
	def createHeader(self, root):
		self.widgets["header"] = header = Frame(root, height=20, borderwidth=1, relief=RIDGE)
		header.pack(fill=X)
		
		self.createHeaderWidgets(header)
	
	def createHeaderWidgets(self, header):
		headerControlsFrames = DoubleWidget("Frame", header)
		headerControlsFrames.left.pack(fill=X, side=LEFT)
		self.widgets["psnrLabel"] = psnrLabel = Label(header, text="MSE:\nPSNR:")
		headerControlsFrames.right.pack(fill=X, side=RIGHT)
		psnrLabel.pack()
		
		self.createHeaderControls(headerControlsFrames)
		
	def createHeaderControls(self, frames):
		self.widgets["openImageButtons"] = openImageButtons = DoubleWidget("Button", frames, text="load image", width=9)
		self.widgets["saveImageButtons"] = saveImageButtons = DoubleWidget("Button", frames, text="save image", width=9, state=DISABLED)
		self.widgets["restoreImageButtons"] = restoreImageButtons = DoubleWidget("Button", frames, text="Restore image", width=11, state=DISABLED)
		
		openImageButtons.left.pack(side=LEFT, anchor = "w")
		saveImageButtons.left.pack(side=LEFT, anchor = "w")
		restoreImageButtons.left.pack(side = LEFT, anchor = "w", padx = 10)
		openImageButtons.right.pack(side=RIGHT, anchor = "e")
		saveImageButtons.right.pack(side=RIGHT, anchor = "e")
		restoreImageButtons.right.pack(side = RIGHT, anchor = "e", padx = 10)
		
	def createMainFrame(self, root):
		self.widgets["mainFrame"] = mainFrame = Frame(root)
		mainFrame.pack()
		self.createSubFrames(mainFrame)
		
	def createSubFrames(self, mainFrame):
		subFrames = self.widgets["subFrames"] = DoubleWidget("Frame", mainFrame).pack(side=LEFT, fill=Y)
		self.createSubFrameWidgets(subFrames)
		
	def createSubFrameWidgets(self, subFrames):
		controlsNotebook = self.widgets["controlsNotebook"] = Notebook(subFrames, padding = 3).pack(side=BOTTOM, fill=Y)
		#controlPanels = self.widgets["controlPanels"] = DoubleWidget("Frame", subFrames, pady=3, padx=2).pack(side=BOTTOM, fill=Y)
		self.createImageControlsTabs(controlsNotebook)
		self.widgets["imageLabels"] = DoubleWidget("Label", subFrames, width=45, height=30, relief=RIDGE).pack()
	
	def createImageControlsTabs(self, controlsNotebook):
		grayscaleControlsFrame = DoubleWidget("Frame", None, width = 45, height = 10)
		self.createGrayscaleTabControls(grayscaleControlsFrame)
		controlsNotebook.add(grayscaleControlsFrame, text = "Grayscale")
	
		YCbCrControlsFrame = DoubleWidget("Frame", None, width = 45, height = 10)
		self.createYCbCrTabControls(YCbCrControlsFrame)
		controlsNotebook.add(YCbCrControlsFrame, text = "YCbCr")
		#widgets = self.widgets
		
		compressionControlsFrame = DoubleWidget("Frame", None, width = 45, height = 10)
		self.createCompressionTabControls(compressionControlsFrame)
		controlsNotebook.add(compressionControlsFrame, text = "Compression")
		
		subsamplingControlsFrame = DoubleWidget("Frame", None, width = 45, height = 10)
		self.createSubsamplingTabControls(subsamplingControlsFrame)
		controlsNotebook.add(subsamplingControlsFrame, text = "Subsampling")
		
	def createGrayscaleTabControls(self, frame):
		DoubleWidget("Label", frame, text="Turn B&W:").pack()
		self.widgets["turnBWEwButtons"] = DoubleWidget("Button", frame, text="Eual weights", width=11, state=DISABLED).pack()
		self.widgets["turnBwCcirButtons"] = DoubleWidget("Button", frame, text="CCIR 601-1", width=11, state=DISABLED).pack()
	
	def createYCbCrTabControls(self, frame):
		DoubleWidget("Label", frame, text="YCbCr:").pack()
		YCbCrButtonsFrame = DoubleWidget("Frame", frame).pack()
		self.createYCbCrButtons(YCbCrButtonsFrame)
		self.widgets["convertFromYCbCrButtons"] = DoubleWidget("Button", frame, text="Convert from\nYCbCr", width=11, state=DISABLED).pack(pady=3)
		
	def createCompressionTabControls(self, frame):
		widgets = self.widgets
		DoubleWidget("Label", frame, text="Compression:").pack()
		widgets["uniformQuantizeRgbButtons"] = DoubleWidget("Button", frame, text="UC RGB", width=11, state=DISABLED).pack()
		widgets["uniformQuantizeYCbCr1Buttons"] = DoubleWidget("Button", frame, text="UC YCrCb 222", width=11, state=DISABLED).pack()
		widgets["uniformQuantizeYCbCr2Buttons"] = DoubleWidget("Button", frame, text="UC YCrCb 312", width=11, state=DISABLED).pack()
		widgets["uniformQuantizeYCbCr3Buttons"] = DoubleWidget("Button", frame, text="UC YCrCb 321", width=11, state=DISABLED).pack()
		widgets["mcQuantizeButtons"] = DoubleWidget("Button", frame, text="Median Cut", width=11, state=DISABLED).pack().pack(pady=5)
	
	def createSubsamplingTabControls(self, frame):
		self.widgets["subsampleButtons"] = DoubleWidget("Button", frame, text="Subsample", width=11, state=DISABLED).pack().pack(pady=5)
		DoubleWidget("Label", frame, text="Mode:").pack()
		self.subsamplingMode = (StringVar(), StringVar())
		self.subsamplingMode[0].set("2h1v")
		self.subsamplingMode[1].set("2h1v")
		DoubleWidget("Radiobutton", frame, text="2h1v", variable=self.subsamplingMode, value="2h1v").pack()
		DoubleWidget("Radiobutton", frame, text="1h2v", variable=self.subsamplingMode, value="1h2v").pack()
		DoubleWidget("Radiobutton", frame, text="2h2v", variable=self.subsamplingMode, value="2h2v").pack()
	
	def createYCbCrButtons(self, frames):
		widgets = self.widgets
		
		widgets["showYChannelButtons"] = DoubleWidget("Button", frames, text="Y", width=2, state=DISABLED).pack(side=LEFT, padx=3)
		widgets["showCbChannelButtons"] = DoubleWidget("Button", frames, text="Cb", width=2, state=DISABLED).pack(side=LEFT, padx=3)
		widgets["showCrChannelButtons"] = DoubleWidget("Button", frames, text="Cr", width=2, state=DISABLED).pack(side=LEFT, padx=3)

		
class DoubleWidget:
	def __init__(self, name, parent, **kwargs):
		leftWidgetArgs, rightWidgetArgs = self.parseKwargs(kwargs)
		leftWidgetParent = None
		rightWidgetParent = None
		if type(parent) is DoubleWidget:
			leftWidgetParent = parent.left
			rightWidgetParent = parent.right
		else:
			leftWidgetParent = parent
			rightWidgetParent = parent
		if hasattr(tk, name):
			self.left = getattr(tk, name)(leftWidgetParent, **leftWidgetArgs)
			self.right = getattr(tk, name)(rightWidgetParent, **rightWidgetArgs)
		else:
			raise Exception("Tk has no widget with name '{}'".format(name))
		
	def parseKwargs(self, kwargs):
		leftWidgetArgs = {}
		rightWidgetArgs = {}
		for key, value in kwargs.items():
			if type(value) is tuple:
				leftWidgetArgs[key] = value[0]
				rightWidgetArgs[key] = value[1]
			else:
				leftWidgetArgs[key] = value
				rightWidgetArgs[key] = value
		return leftWidgetArgs, rightWidgetArgs
		
	def pack(self, **kwargs):
		leftWidgetArgs, rightWidgetArgs = self.parseKwargs(kwargs)
		self.left.pack(**leftWidgetArgs)
		self.right.pack(**leftWidgetArgs)
		return self
		
	def configure(self, **kwargs):
		self.left.configure(**kwargs)
		self.right.configure(**kwargs)
		return self
	
	def bind(self, callback):
		self.left.configure(command = partial(callback, LEFT_SIDE))
		self.right.configure(command = partial(callback, RIGHT_SIDE))
		return self
		
class Notebook(DoubleWidget):
	def __init__(self, parent, **kwargs):
		leftWidgetArgs, rightWidgetArgs = self.parseKwargs(kwargs)
		leftWidgetParent = None
		rightWidgetParent = None
		if type(parent) is DoubleWidget:
			leftWidgetParent = parent.left
			rightWidgetParent = parent.right
		else:
			leftWidgetParent = parent
			rightWidgetParent = parent
		self.left = ttk.Notebook(leftWidgetParent, **leftWidgetArgs)
		self.right = ttk.Notebook(rightWidgetParent, **rightWidgetArgs)
	def add(self, child, **kw):
		if type(child) is DoubleWidget:
			self.left.add(child.left, **kw)
			self.right.add(child.right, **kw)
		else:
			self.left.add(child, **kw)
			self.right.add(child, **kw)