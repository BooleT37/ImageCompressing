from tkinter import *
import tkinter as tk
from tkinter import ttk

from constants import *
from functools import partial


class WidgetsManager:
    def __init__(self):
        self.subsamplingMode = (StringVar(), StringVar())
        self.subsamplingModeForJpg = (StringVar(), StringVar())
        self.quantizingMode = (StringVar(), StringVar())
        self.qntNValue = (StringVar(), StringVar())
        self.qntAlphaValue = (StringVar(), StringVar())
        self.qntGammaValue = (StringVar(), StringVar())
        self.qntQValue = (StringVar(), StringVar())
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
        self.widgets["saveImageButtons"] = saveImageButtons = DoubleWidget("Button", frames, text="save image", width=9,
                                                                           state=DISABLED)
        self.widgets["restoreImageButtons"] = restoreImageButtons = DoubleWidget("Button", frames, text="Restore image",
                                                                                 width=11, state=DISABLED)

        openImageButtons.left.pack(side=LEFT, anchor="w")
        saveImageButtons.left.pack(side=LEFT, anchor="w")
        restoreImageButtons.left.pack(side=LEFT, anchor="w", padx=10)
        openImageButtons.right.pack(side=RIGHT, anchor="e")
        saveImageButtons.right.pack(side=RIGHT, anchor="e")
        restoreImageButtons.right.pack(side=RIGHT, anchor="e", padx=10)

    def createMainFrame(self, root):
        self.widgets["mainFrame"] = mainFrame = Frame(root)
        mainFrame.pack()
        self.createSubFrames(mainFrame)

    def createSubFrames(self, mainFrame):
        subFrames = self.widgets["subFrames"] = DoubleWidget("Frame", mainFrame).pack(side=LEFT, fill=Y)
        self.createSubFrameWidgets(subFrames)

    def createSubFrameWidgets(self, subFrames):
        controlsNotebook = self.widgets["controlsNotebook"] = Notebook(subFrames, padding=3).pack(side=BOTTOM, fill=Y)
        self.createImageControlsTabs(controlsNotebook)
        self.widgets["imageLabels"] = DoubleWidget("Label", subFrames, width=55, height=30, relief=RIDGE).pack()

    def createImageControlsTabs(self, controlsNotebook):
        grayscaleControlsFrame = DoubleWidget("Frame", None, width=45, height=10)
        self.createGrayscaleTabControls(grayscaleControlsFrame)
        controlsNotebook.add(grayscaleControlsFrame, text="Grayscale")

        YCbCrControlsFrame = DoubleWidget("Frame", None, width=45, height=10)
        self.createYCbCrTabControls(YCbCrControlsFrame)
        controlsNotebook.add(YCbCrControlsFrame, text="YCbCr")

        compressionControlsFrame = DoubleWidget("Frame", None, width=45, height=10)
        self.createCompressionTabControls(compressionControlsFrame)
        controlsNotebook.add(compressionControlsFrame, text="Compression")

        subsamplingControlsFrame = DoubleWidget("Frame", None, width=45, height=10)
        self.createSubsamplingTabControls(subsamplingControlsFrame)
        controlsNotebook.add(subsamplingControlsFrame, text="Subsampling")

        jpgControlsFrame = DoubleWidget("Frame", None, width=45, height=10)
        self.createJpgTabControls(jpgControlsFrame)
        controlsNotebook.add(jpgControlsFrame, text="JPG")

    def createGrayscaleTabControls(self, frame):
        DoubleWidget("Label", frame, text="Turn B&W:").pack()
        self.widgets["turnBWEwButtons"] = DoubleWidget("Button", frame, text="Equal weights", width=11,
                                                       state=DISABLED).pack()
        self.widgets["turnBwCcirButtons"] = DoubleWidget("Button", frame, text="CCIR 601-1", width=11,
                                                         state=DISABLED).pack()

    def createYCbCrTabControls(self, frame):
        DoubleWidget("Label", frame, text="YCbCr:").pack()
        YCbCrButtonsFrame = DoubleWidget("Frame", frame).pack()
        self.createYCbCrButtons(YCbCrButtonsFrame)
        self.widgets["convertFromYCbCrButtons"] = DoubleWidget("Button", frame, text="Convert from\nYCbCr", width=11,
                                                               state=DISABLED).pack(pady=3)

    def createCompressionTabControls(self, frame):
        widgets = self.widgets
        DoubleWidget("Label", frame, text="Compression:").pack()
        widgets["uniformQuantizeRgbButtons"] = DoubleWidget("Button", frame, text="UC RGB", width=11,
                                                            state=DISABLED).pack()
        widgets["uniformQuantizeYCbCr1Buttons"] = DoubleWidget("Button", frame, text="UC YCrCb 222", width=11,
                                                               state=DISABLED).pack()
        widgets["uniformQuantizeYCbCr2Buttons"] = DoubleWidget("Button", frame, text="UC YCrCb 312", width=11,
                                                               state=DISABLED).pack()
        widgets["uniformQuantizeYCbCr3Buttons"] = DoubleWidget("Button", frame, text="UC YCrCb 321", width=11,
                                                               state=DISABLED).pack()
        widgets["mcQuantizeButtons"] = DoubleWidget("Button", frame, text="Median Cut", width=11,
                                                    state=DISABLED).pack(pady=5)

    def createSubsamplingTabControls(self, frame):
        self.widgets["subsampleButtons"] = DoubleWidget("Button", frame, text="Subsample", width=11,
                                                        state=DISABLED).pack(pady=5)
        DoubleWidget("Label", frame, text="Mode:").pack()
        self.subsamplingMode[0].set("2h1v")
        self.subsamplingMode[1].set("2h1v")
        DoubleWidget("Radiobutton", frame, text="2h1v", variable=self.subsamplingMode, value="2h1v").pack()
        DoubleWidget("Radiobutton", frame, text="1h2v", variable=self.subsamplingMode, value="1h2v").pack()
        DoubleWidget("Radiobutton", frame, text="2h2v", variable=self.subsamplingMode, value="2h2v").pack()

    def createJpgTabControls(self, frames):
        # self.widgets["dctLabel"] = DoubleWidget("Label", frames, text="DCT widgets").pack()
        mainButtonsFrame = DoubleWidget("Frame", frames).pack()
        self.createJpgMainButtons(mainButtonsFrame)

        optionsFrame = DoubleWidget("Frame", frames).pack()
        self.createJpgOptionsWidgets(optionsFrame)

    def createJpgMainButtons(self, frames):
        self.widgets["jpgCompressButtons"] = DoubleWidget("Button", frames, text="Save image", state=DISABLED) \
            .pack(side=LEFT)
        self.widgets["jpgUncompressButtons"] = DoubleWidget("Button", frames, text="Open image") \
            .pack(side=LEFT)
        self.widgets["jpgImitateCompressionButtons"] = DoubleWidget("Button", frames, text="Imitate", state=DISABLED) \
            .pack(side=LEFT)

    def createJpgOptionsWidgets(self, frames):
        subsamplingFrames = DoubleWidget("Frame", frames, relief=RIDGE, borderwidth=2).pack(side=LEFT, anchor="nw")
        self.createJpgSubsamplingWidgets(subsamplingFrames)
        quantizingFrames = DoubleWidget("Frame", frames, relief=RIDGE, borderwidth=2).pack(side=LEFT, anchor="nw")
        self.createJpgQuantizingWidgets(quantizingFrames)

    def createJpgSubsamplingWidgets(self, frames):
        self.subsamplingModeForJpg[0].set("2h2v")
        self.subsamplingModeForJpg[1].set("2h2v")
        DoubleWidget("Label", frames, text="Subsampling mode:").pack(anchor="nw")
        DoubleWidget("Radiobutton", frames, text="2h2v", variable=self.subsamplingModeForJpg, value="2h2v").pack(
            anchor="nw")
        DoubleWidget("Radiobutton", frames, text="1h2v", variable=self.subsamplingModeForJpg, value="1h2v").pack(
            anchor="nw")
        DoubleWidget("Radiobutton", frames, text="2h1v", variable=self.subsamplingModeForJpg, value="2h1v").pack(
            anchor="nw")
        DoubleWidget("Radiobutton", frames, text="No subsampling", variable=self.subsamplingModeForJpg,
                     value="no_subsampling").pack(anchor="nw")

    def createJpgQuantizingWidgets(self, frames):
        self.quantizingMode[0].set("qfactor")
        self.quantizingMode[1].set("qfactor")
        DoubleWidget("Label", frames, text="Quantizing mode:").pack(anchor="nw")
        qntModeFrame1 = DoubleWidget("Frame", frames).pack(anchor="nw")
        DoubleWidget("Radiobutton", qntModeFrame1, text="First N,", variable=self.quantizingMode, value="firstn").pack(
            side=LEFT)
        DoubleWidget("Label", qntModeFrame1, text="N = ").pack(side=LEFT)

        nEntry = DoubleWidget("Entry", qntModeFrame1, textvariable=self.qntNValue, validate="all",
                              width=2, state=DISABLED).pack(side=LEFT)
        self.configureEntryValidator(nEntry, self.qntNValue, 0, 64, "64")

        DoubleWidget("Radiobutton", frames, text="Custom matrix", variable=self.quantizingMode, value="custom").pack(
            anchor="nw")
        qntModeFrame2 = DoubleWidget("Frame", frames).pack(anchor="nw")

        DoubleWidget("Label", qntModeFrame2, text="α = ").pack(side=LEFT)
        alphaEntry = DoubleWidget("Entry", qntModeFrame2, textvariable=self.qntAlphaValue, validate="all",
                                  width=2, state=DISABLED).pack(side=LEFT)
        self.configureEntryValidator(alphaEntry, self.qntAlphaValue, 0, 10, "3")

        DoubleWidget("Label", qntModeFrame2, text="γ = ").pack(side=LEFT)
        gammaEntry = DoubleWidget("Entry", qntModeFrame2, textvariable=self.qntGammaValue,
                                  validate="all", width=2, state=DISABLED).pack(side=LEFT)
        self.configureEntryValidator(gammaEntry, self.qntGammaValue, 0, 10, "2")

        DoubleWidget("Radiobutton", frames, text="Quality factor", variable=self.quantizingMode, value="qfactor").pack(
            anchor="nw")

        qntModeFrame3 = DoubleWidget("Frame", frames).pack(anchor="nw")
        DoubleWidget("Label", qntModeFrame3, text="Q = ").pack(side=LEFT)
        self.qntQValue[0].set("50")
        self.qntQValue[1].set("50")

        qEntry = DoubleWidget("Entry", qntModeFrame3, textvariable=self.qntQValue,
                              validate="all", width=2).pack(side=LEFT)
        self.configureEntryValidator(qEntry, self.qntQValue, 0, 100, "50")

        def onQuantizingModeChange(*args):
            value = args[0].get()
            if value == "firstn":
                nEntry.configure(state=NORMAL)
                alphaEntry.configure(state=DISABLED)
                gammaEntry.configure(state=DISABLED)
                qEntry.configure(state=DISABLED)
            elif value == "custom":
                nEntry.configure(state=DISABLED)
                alphaEntry.configure(state=NORMAL)
                gammaEntry.configure(state=NORMAL)
                qEntry.configure(state=DISABLED)
            elif value == "qfactor":
                nEntry.configure(state=DISABLED)
                alphaEntry.configure(state=DISABLED)
                gammaEntry.configure(state=DISABLED)
                qEntry.configure(state=NORMAL)

        self.quantizingMode[0].trace("w", partial(onQuantizingModeChange, self.quantizingMode[0]))
        self.quantizingMode[1].trace("w", partial(onQuantizingModeChange, self.quantizingMode[1]))


    @staticmethod
    def configureEntryValidator(entry, variable, startValue, endValue, defaultValue):
        def validateEntry(_, strVal, startVal, endVal):
            startVal = int(startVal)
            endVal = int(endVal)
            if strVal == "":
                return True
            try:
                intVal = int(strVal)
            except ValueError:
                return False
            if startVal <= intVal <= endVal:
                return True
            return False

        validator1 = entry.left.register(validateEntry)
        validator2 = entry.right.register(validateEntry)

        entry.left.configure(validatecommand=(validator1, '%P', '%P', startValue, endValue))
        entry.right.configure(validatecommand=(validator2, '%P', '%P', startValue, endValue))

        variable[0].set(defaultValue)
        variable[1].set(defaultValue)


    def createYCbCrButtons(self, frames):
        widgets = self.widgets

        widgets["showYChannelButtons"] = DoubleWidget("Button", frames, text="Y", width=2, state=DISABLED).pack(
            side=LEFT, padx=3)
        widgets["showCbChannelButtons"] = DoubleWidget("Button", frames, text="Cb", width=2, state=DISABLED).pack(
            side=LEFT, padx=3)
        widgets["showCrChannelButtons"] = DoubleWidget("Button", frames, text="Cr", width=2, state=DISABLED).pack(
            side=LEFT, padx=3)


class DoubleWidget:
    def __init__(self, name, parent, isTtkWidget=False, **kwargs):
        tkModule = ttk if isTtkWidget else tk
        leftWidgetArgs, rightWidgetArgs = self.parseKwargs(kwargs)
        if type(parent) is DoubleWidget:
            leftWidgetParent = parent.left
            rightWidgetParent = parent.right
        else:
            leftWidgetParent = parent
            rightWidgetParent = parent
        if hasattr(tkModule, name):
            self.left = getattr(tkModule, name)(leftWidgetParent, **leftWidgetArgs)
            self.right = getattr(tkModule, name)(rightWidgetParent, **rightWidgetArgs)
        else:
            raise Exception(("Ttk" if isTtkWidget else "Tk") + " has no widget with name '{}'".format(name))

    @staticmethod
    def parseKwargs(kwargs):
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
        self.left.configure(command=partial(callback, LEFT_SIDE))
        self.right.configure(command=partial(callback, RIGHT_SIDE))
        return self


class Notebook(DoubleWidget):
    def __init__(self, parent, **kwargs):
        super().__init__("Notebook", parent, True, **kwargs)

    def add(self, child, **kw):
        if type(child) is DoubleWidget:
            self.left.add(child.left, **kw)
            self.right.add(child.right, **kw)
        else:
            self.left.add(child, **kw)
            self.right.add(child, **kw)
