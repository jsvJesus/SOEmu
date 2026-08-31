# Embedded file name: scripts/client/Helpers/ChatConsole.py
import BigWorld
import GUI
import Keys
import collections

class ChatConsole(object):
    """
    Leverages the GUI.Console object to provide a basic chat console.
    """
    sInstance = None

    def __init__(self, numVisibleLines = 4):
        """
        Create a new ChatConsole with a maximum number of visible lines.  Note
        that you cannot construct one of these things until after
        BWPersonality.init() has been called because it relies on resource stuff
        that is initialised prior to init().
        """
        self.numVisibleLines = numVisibleLines
        self.lines = collections.deque()
        self.timerID = None
        self.con = GUI.Console()
        self.con.editCallback = self.editCallback
        self.con.editPrompt = '> '
        self.con.editCol = 0
        self.con.editRow = numVisibleLines + 1
        self.con.editColour = (255, 0, 0, 255)
        self.con.colour = (128, 128, 128, 255)
        self.con.position = (-1, -1, 0)
        self.con.verticalAnchor = 'BOTTOM'
        self.con.horizontalAnchor = 'LEFT'
        self.con.cursor = (0, 0)
        GUI.addRoot(self.con)
        ChatConsole.sInstance = self
        return

    @classmethod
    def instance(cls):
        if not cls.sInstance:
            cls.sInstance = ChatConsole()
        return cls.sInstance

    def write(self, msg):
        self.lines.appen(msg)
        if len(self.lines) > self.numVisibleLines:
            self.lines.popleft()
        self.con.clear()
        for line in self.lines:
            self.con.prints(line + '\n')

        self.show()
        self.hide(10)

    def hide(self, delay = 0):
        if self.timerID is not None:
            BigWorld.cancelCallback(self.timerID)
            self.timerID = None
        if delay == 0:
            self.con.visible = False
        else:
            BigWorld.callback(delay, self.hide)
        return

    def show(self):
        self.con.visible = True

    def editing(self, val = None):
        if val is None:
            return self.con.editEnable
        else:
            self.show()
            self.con.editEnable = val
            return

    def editCallback(self, line):
        BigWorld.player().cell.say(line)
        self.write('You say: ' + line)
        self.editing(False)

    def handleKeyEvent(self, down, key, mods):
        if down and key == Keys.KEY_ESCAPE:
            if self.editing():
                self.editing(False)
            else:
                self.hide()
            return True
        else:
            return self.con.handleKeyEvent((down, key, mods))

    def handleCharEvent(self, char, key, mods):
        if self.editing():
            return self.con.handleCharEvent((char, key, mods))
        return False