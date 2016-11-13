from tkinter import *
import tkinter as tk

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
		
		self.createPsnrLabel(header)
	
	def createPsnrLabel(self, header):
		self.widgets["psnrLabel"] = psnrLabel = Label(header, text="MSE:\nPSNR:")
		psnrLabel.pack()
	
	def createMainFrame(self, root):
		self.widgets["mainFrame"] = mainFrame = Frame(root)
		mainFrame.pack()
		
		self.createSubFrames(mainFrame)
		
	def createSubFrames(self, mainFrame):
		subFrames = self.widgets["subFrames"] = DoubleWidget("Frame", mainFrame).pack(side=LEFT, fill=Y)
		
		self.createSubFrameWidgets(subFrames)
		
	def createSubFrameWidgets(self, subFrames):
		controlPanels = self.widgets["controlPanels"] = DoubleWidget("Frame", subFrames, pady=3, padx=2).pack(side=BOTTOM, fill=Y)
		
		self.createImageControls(controlPanels)
		
		self.widgets["imageLabels"] = DoubleWidget("Label", subFrames, width=40, height=30, relief=RIDGE).pack()
	
	def createImageControls(self, controlPanels):
		widgets = self.widgets
		
		widgets["openImageButtons"] = DoubleWidget("Button", controlPanels, text="load image", width=11).pack()
		widgets["saveImageButtons"] = DoubleWidget("Button", controlPanels, text="save image", width=11, state=DISABLED).pack()
		DoubleWidget("Label", controlPanels, text="Turn B&W:").pack()
		widgets["turnBWEwButtons"] = DoubleWidget("Button", controlPanels, text="Eual weights", width=11, state=DISABLED).pack()
		widgets["turnBwCcirButtons"] = DoubleWidget("Button", controlPanels, text="CCIR 601-1", width=11, state=DISABLED).pack()
		DoubleWidget("Label", controlPanels, text="YCbCr:").pack()
		YCbCrButtonsFrames = widgets["YCbCrButtonsFrames"] = DoubleWidget("Frame", controlPanels).pack()
		
		self.createYCbCrButtons(YCbCrButtonsFrames)
		
		widgets["convertFromYCbCrButtons"] = DoubleWidget("Button", controlPanels, text="Convert from\nYCbCr", width=11, state=DISABLED).pack(pady=3)
		DoubleWidget("Label", controlPanels, text="Compression:").pack()
		widgets["uniformQuantizeRgbButtons"] = DoubleWidget("Button", controlPanels, text="UC RGB", width=11, state=DISABLED).pack()
		widgets["uniformQuantizeYCbCr1Buttons"] = DoubleWidget("Button", controlPanels, text="UC YCrCb 222", width=11, state=DISABLED).pack()
		widgets["uniformQuantizeYCbCr2Buttons"] = DoubleWidget("Button", controlPanels, text="UC YCrCb 312", width=11, state=DISABLED).pack()
		widgets["uniformQuantizeYCbCr3Buttons"] = DoubleWidget("Button", controlPanels, text="UC YCrCb 321", width=11, state=DISABLED).pack()
		widgets["mcQuantizeButtons"] = DoubleWidget("Button", controlPanels, text="Median Cut", width=11, state=DISABLED).pack().pack(pady=5)
		widgets["subsampleButtons"] = DoubleWidget("Button", controlPanels, text="Subsample", width=11, state=DISABLED).pack().pack(pady=5)
		DoubleWidget("Label", controlPanels, text="Mode:").pack()
		self.subsamplingMode = (StringVar(), StringVar())
		self.subsamplingMode[0].set("2h1v")
		self.subsamplingMode[1].set("2h1v")
		DoubleWidget("Radiobutton", controlPanels, text="2h1v", variable=self.subsamplingMode, value="2h1v").pack()
		DoubleWidget("Radiobutton", controlPanels, text="1h2v", variable=self.subsamplingMode, value="1h2v").pack()
		DoubleWidget("Radiobutton", controlPanels, text="2h2v", variable=self.subsamplingMode, value="2h2v").pack()
		widgets["restoreImageButtons"] = DoubleWidget("Button", controlPanels, text="Restore image", width=11, state=DISABLED).pack(pady=20)
	
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