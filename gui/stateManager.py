from tkinter import *
from constants import *

MAIN = "main"
GRAYSCALE = "grayscale"
CHANNEL_SHOWN = "channel shown"
COMPRESSED = "compressed"


class ButtonGroup:
    def __init__(self, buttons):
        self.buttons = buttons

    def disable(self, side):
        for i in range(len(self.buttons)):
            button = self.buttons[i].left if (side == LEFT_SIDE) else self.buttons[i].right
            button.configure(state=DISABLED)

    def enable(self, side):
        for i in range(len(self.buttons)):
            button = self.buttons[i].left if (side == LEFT_SIDE) else self.buttons[i].right
            button.configure(state=NORMAL)


class StateManager:
    def __init__(self, widgets):
        self.widgets = widgets
        self.buttonGroups = {
            'general': ButtonGroup([widgets["openImageButtons"], widgets["saveImageButtons"]]),
            'bw': ButtonGroup([widgets["turnBWEwButtons"], widgets["turnBwCcirButtons"]]),
            'YCbCrChannels': ButtonGroup(
                [widgets["showYChannelButtons"], widgets["showCbChannelButtons"], widgets["showCrChannelButtons"]]),
            'YCbCrConvert': ButtonGroup([widgets["convertFromYCbCrButtons"]]),
            'compression': ButtonGroup([
                widgets["uniformQuantizeRgbButtons"],
                widgets["uniformQuantizeYCbCr1Buttons"],
                widgets["uniformQuantizeYCbCr2Buttons"],
                widgets["uniformQuantizeYCbCr3Buttons"],
                widgets["mcQuantizeButtons"],
                widgets["subsampleButtons"]]),
            'restore': ButtonGroup([widgets["restoreImageButtons"]])
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
        if state == MAIN:
            self.enterMainState(side)
        elif state == GRAYSCALE:
            self.enterGrayscaleState(side)
        elif state == CHANNEL_SHOWN:
            self.enterChannelState(side, channel)
        elif state == COMPRESSED:
            self.enterCompressedState(side)
        self.currentState[side] = state
        self.currentChannel[side] = channel

    def enterMainState(self, side):
        self.buttonGroups['general'].enable(side)
        self.buttonGroups['bw'].enable(side)
        self.buttonGroups['YCbCrChannels'].enable(side)
        self.buttonGroups['YCbCrConvert'].enable(side)
        self.buttonGroups['compression'].enable(side)
        self.buttonGroups['restore'].disable(side)

    def enterGrayscaleState(self, side):
        self.buttonGroups['restore'].enable(side)

    def enterChannelState(self, side, channel):
        if channel is None:
            raise Exception("channel is not defined for state change")
        self.buttonGroups['general'].disable(side)
        self.buttonGroups['bw'].disable(side)
        self.buttonGroups['YCbCrConvert'].disable(side)

    def enterCompressedState(self, side):
        self.buttonGroups['restore'].enable(side)
