# Embedded file name: scripts/client/Helpers/PyGUI/EditField.py
import BigWorld, GUI, Keys
from PyGUIBase import PyGUIBase
CHARS_TO_IGNORE = [u'\r', u'\x08', u'\x1b']

class EditField(PyGUIBase):
    factoryString = 'PyGUI.EditField'
    CURSOR_CHAR = '|'

    def __init__(self, component = None):
        PyGUIBase.__init__(self, component)
        if self.component == None:
            self.component = GUI.Text('')
            self.component.text = self.CURSOR_CHAR
            self.component.position = (0, 0, 0.5)
            self.component.colour = (92, 92, 92, 128)
            self.component.width = 256
            self.component.height = 32
            self.component.script = self
        self.colour = (self.component.colour.x,
         self.component.colour.y,
         self.component.colour.z,
         self.component.colour.w)
        self.onEnter = None
        self.onEscape = None
        self.maxLength = 15
        return

    def focus(self, state):
        c = self.component
        if state:
            c.colour = self.colour
            c.text = c.text + self.CURSOR_CHAR
        else:
            c.colour = (155, 155, 155, 255)
            c.text = c.text[0:len(c.text) - 1]

    def handleCharEvent(self, character, key, mods):
        c = self.component
        if character == u'\x08':
            c.text = c.text[0:len(c.text) - 2] + self.CURSOR_CHAR
            return True
        if character not in CHARS_TO_IGNORE:
            if len(c.text) < self.maxLength:
                c.text = c.text[0:len(c.text) - 1] + character + self.CURSOR_CHAR
            return True
        return False

    def handleKeyEvent(self, event):
        key = event.key
        mods = event.modifiers
        down = event.isKeyDown()
        char = event.character
        if char is not None:
            handled = self.handleCharEvent(char, 0, mods)
            if handled:
                return True
        c = self.component
        if down:
            if key == Keys.KEY_ESCAPE:
                if self.onEscape is not None:
                    self.onEscape()
                    return True
            elif key in (Keys.KEY_RETURN, Keys.KEY_NUMPADENTER):
                if self.eventHandler != None:
                    textString = c.text
                    self.eventHandler.onClick(c.text[:-1])
                    return True
                if self.onEnter is not None:
                    self.onEnter(c.text[:-1])
                    return True
        return False

    def adjustFont(self, screenWidth):
        if screenWidth < 700:
            self.component.font = self.smallFont
        else:
            self.component.font = self.bigFont

    def onLoad(self, section):
        self.smallFont = section.readString('smallFont', 'default_small.font')
        self.bigFont = section.readString('bigFont', 'default_medium.font')