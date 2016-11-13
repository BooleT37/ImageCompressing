from tkinter import *
from constants import *

MAIN = "main"
GRAYSCALE = "grayscale"
CHANNEL_SHOWN = "channel shown"
COMPRESSED = "compressed"

class ButtonGroup:
	def __init__(self, buttons):
		self.buttons = buttons
		
	def disable(self):
		for i in range(len(self.buttons)):
			button = self.buttons[i]
			button.configure(state=DISABLED)
	def enable(self):
		for i in range(len(self.buttons)):
			self.buttons[i].configure(state=NORMAL)
				

class StateManager:
	def __init__(self, app):
		self.app = app
		self.buttonGroups = {
			LEFT_SIDE: {
				'general': ButtonGroup([app.openLeftImageButton, app.saveLeftImageButton]),
				'bw': ButtonGroup([app.turnBwEwLeftImageButton, app.turnBwCcirLeftImageButton]),
				'YCbCrChannels': ButtonGroup([app.showYChannelForLeftImageButton, app.showCbChannelForLeftImageButton, app.showCrChannelForLeftImageButton]),
				'YCbCrConvert': ButtonGroup([app.convertFromYCbCrLeftImageButton]),
				'compression': ButtonGroup([
				app.uniformQuantizeRgbLeftImageButton,
				app.uniformQuantizeYCbCr2LeftImageButton,
				app.uniformQuantizeYCbCr1LeftImageButton,
				app.uniformQuantizeYCbCr3LeftImageButton,
				app.mcQuantizeLeftImageButton,
				app.subsampleLeftImageButton]),
				'restore': ButtonGroup([app.restoreLeftImageButton])
			},
			RIGHT_SIDE: {
				'general': ButtonGroup([app.openRightImageButton, app.saveRightImageButton]),
				'bw': ButtonGroup([app.turnBwEwRightImageButton, app.turnBwCcirRightImageButton]),
				'YCbCrChannels': ButtonGroup([app.showYChannelForRightImageButton, app.showCbChannelForRightImageButton, app.showCrChannelForRightImageButton]),
				'YCbCrConvert': ButtonGroup([app.convertFromYCbCrRightImageButton]),
				'compression': ButtonGroup([
				app.uniformQuantizeRgbRightImageButton,
				app.uniformQuantizeYCbCr1RightImageButton,
				app.uniformQuantizeYCbCr2RightImageButton,
				app.uniformQuantizeYCbCr3RightImageButton,
				app.mcQuantizeRightImageButton,
				app.subsampleRightImageButton]),
				'restore': ButtonGroup([app.restoreRightImageButton])
			}
		}
		self.currentState = {
			LEFT_SIDE: MAIN,
			RIGHT_SIDE: MAIN
		}
		self.currentChannel = {
			LEFT_SIDE: None,
			RIGHT_SIDE: None
		}
				
				
	def changeState(self, state, side, channel=None):
		if (state == MAIN):
			self.enterMainState(side)
		elif (state == GRAYSCALE):
			self.enterGrayscaleState(side)
		elif (state == CHANNEL_SHOWN):
			self.enterChannedState(side, channel)
		elif (state == COMPRESSED):
			self.enterCompressedState(side)
		self.currentState[side] = state
		self.currentChannel[side] = channel
		
	def enterMainState(self, side):
		self.buttonGroups[side]['general'].enable()
		self.buttonGroups[side]['bw'].enable()
		self.buttonGroups[side]['YCbCrChannels'].enable()
		self.buttonGroups[side]['YCbCrConvert'].enable()
		self.buttonGroups[side]['compression'].enable()
		self.buttonGroups[side]['restore'].disable()
	
	def enterGrayscaleState(self, side):
		self.buttonGroups[side]['restore'].enable()
	
	def enterChannedState(self, side, channel):
		if (channel is None):
			raise Exception("channel is not defined for state change")
		self.buttonGroups[side]['general'].disable()
		self.buttonGroups[side]['bw'].disable()
		self.buttonGroups[side]['YCbCrConvert'].disable()
		
	def enterCompressedState(self, side):
		self.buttonGroups[side]['restore'].enable()