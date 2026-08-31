# Embedded file name: scripts/client/Helpers/PyGUI/Console.py
import BigWorld, GUI
import math
from PyGUIBase import PyGUIBase

class Console(PyGUIBase):
    factoryString = 'PyGUI.Console'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.maxLines = 255
        self.lines = []
        self.displayLines = []
        self.lineLength = component.visibleWidth()
        self.numOfLines = component.visibleHeight()
        self.scrollIndex = 0
        self.editColour = (255, 255, 255, 255)
        self.component.cursor = (0, 0)
        self.setEditColour(self.editColour)
        self.setEditCursor((0, 0))
        self.setPosition(self.component.position)

    def onSave(self, dataSection):
        PyGUIBase.onSave(self, dataSection)

    def onLoad(self, dataSection):
        PyGUIBase.onLoad(self, dataSection)

    def onRecreateDevice(self):
        self.displayLines = []
        for line in self.lines:
            self._addDisplayLine(line[0], line[1])

        self.redraw()

    @staticmethod
    def create():
        c = GUI.Console()
        return Console(c).component

    def getMaxLines(self):
        return self.maxLines

    def setMaxLines(self, maxLines):
        if self.maxLines > 0:
            self.clear()
            self.maxLines = maxLines
            self.redraw()

    def addLine(self, str, colour = (255, 255, 255, 255)):
        if len(self.lines) == self.maxLines:
            line, colour = self.lines[0]
            n = int(math.ceil(len(line) / self.lineLength)) + 1
            self.displayLines = self.displayLines[n:]
            self.lines = self.lines[1:]
        self.lines.append((str, colour))
        self._addDisplayLine(str, colour)
        self.redraw()

    def appendLine(self, str, colour = (255, 255, 255, 255)):
        line, colour = self.lines.pop()
        n = int(math.ceil(len(line) / self.lineLength))
        self.displayLines = self.displayLines[0:int(len(self.displayLines) - n) - 1]
        self.addLine(line + str, colour)

    def _addDisplayLine(self, str, colour):
        if len(str) <= self.lineLength:
            self.displayLines.append((str, colour))
        else:
            while len(str) > self.lineLength:
                line = str[:self.lineLength]
                idx = line.rfind(' ')
                if idx == -1:
                    line = str[:self.lineLength]
                    str = str[self.lineLength:]
                else:
                    line = str[:idx]
                    str = str[idx + 1:]
                self.displayLines.append((line, colour))

            if len(str) > 0:
                self.displayLines.append((str, colour))
        self.scrollIndex = len(self.displayLines) - self.numOfLines
        if self.scrollIndex < 0:
            self.scrollIndex = 0

    def clear(self):
        self.lines = []
        self.displayLines = []
        self.scrollIndex = 0
        self.redraw()

    def scrollUp(self):
        if self.scrollIndex > 0:
            self.scrollIndex -= 1
            self.redraw()

    def scrollDown(self):
        if self.scrollIndex < len(self.displayLines) - self.numOfLines:
            self.scrollIndex += 1
            self.redraw()

    def getScrollIndex(self):
        return self.scrollIndex

    def setScrollIndex(self, index):
        if index < 0:
            self.scrollIndex = 0
        elif index > len(self.displayLines) - self.numOfLines:
            self.scrollIndex = len(self.displayLines) - self.numOfLines
        else:
            self.scrollIndex = index
        self.redraw()

    def getLineLength(self):
        return self.lineLength

    def setLineLength(self, length):
        lineLength = length
        if lineLength > self.component.visibleWidth():
            lineLength = self.component.visibleWidth()
        self.lineLength = lineLength
        self.component.editLineLength = lineLength
        self.redraw()

    def getNumberOfLines(self):
        return self.numOfLines

    def setNumberOfLines(self, numOfLines):
        self.numOfLines = numOfLines
        if self.numOfLines > self.component.visibleHeight():
            self.numOfLines = self.component.visibleHeight()
        self.redraw()

    def getPosition(self):
        return self.component.position

    def setPosition(self, position):
        self.component.position = position
        self.redraw()

    def getEditCursor(self):
        return (self.component.editCol, self.component.editRow)

    def setEditCursor(self, cursorPos):
        self.component.editCol = cursorPos[0]
        self.component.editRow = cursorPos[1]
        self.setEditColour(self.editColour)
        self.redraw()

    def enableEdit(self):
        self.component.editEnable = True

    def disableEdit(self):
        self.component.editEnable = False

    def getEditPrompt(self):
        return self.component.editPrompt

    def setEditPrompt(self, prompt):
        self.component.editPrompt = prompt

    def getEditText(self):
        return self.component.editText

    def setEditText(self, text):
        self.component.editText = text[0:self.lineLength]

    def editCallback(self, callback):
        self.component.editCallback = callback

    def setEditColour(self, colour):
        self.editColour = colour
        self.component.editColour = colour

    def consolePixelSize(self):
        widthMode = self.component.widthMode
        self.component.widthMode = 'PIXEL'
        heightMode = self.component.heightMode
        self.component.heightMode = 'PIXEL'
        width = self.component.width
        height = self.component.height
        self.component.widthMode = widthMode
        self.component.heightMode = heightMode
        return (width, height)

    def redraw(self):
        console = self.component
        console.clear()
        startIndex = self.scrollIndex
        endIndex = startIndex + self.numOfLines
        displayLines = self.displayLines[startIndex:endIndex]
        if len(displayLines) < self.numOfLines:
            row = self.numOfLines - len(displayLines)
        else:
            row = 0
        for line in displayLines:
            str = line[0]
            colour = line[1]
            console.cursor = (0, row)
            console.lineColour = colour
            console.prints(str)
            row += 1

        if self.component.editEnable:
            self.setEditColour(self.editColour)