# Embedded file name: scripts/client/soGUI/soHelpGUI.py
import BigWorld
import BWPersonality
import GUI
from soGUI.soTextField import soTextField3
import traceback
from Localization import lc
from Helpers.PyGUI.PyGUIBase import PyGUIBase

class soHelpGUI(PyGUIBase):
    factoryString = 'soGUI.soHelpGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()
        self.setupTxt()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        sW, sH = BigWorld.screenSize()
        cmp.width = sW
        cmp.height = sH
        cmp.position = (0, 0, 0.0)

    def setupContent(self):
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Simple('textures/default/black.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 190)
        cmp.materialFX = 'BLEND'
        cmp.width = sW
        cmp.height = sH
        cmp.position = (0, 0, 1)
        self.component.addChild(cmp, 'frame1')

    def setupTxt(self):
        sW, sH = BigWorld.screenSize()
        txt = soTextField3(GUI.Window(), width=sW - 10, height=sH - 20, textWidth=-1, hScroll=False, vScroll=True, hideScroll=1, borderWidth=0, vOffset=5, hOffset=5, textureless=1, autosize=0)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (1, 8, 0.2)
        txt.onBound()
        self.component.addChild(cmp, 'ctext')
        try:
            self.component.ctext.script.component.vScroll.script.component.backFrame.colour = (0, 0, 0, 255)
        except:
            print 'help vScroll black frame problem'
            traceback.print_exc()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'helpGUI')
        self.component.visible = True
        self.updateText()
        self.component.crossFocus = True
        self.component.moveFocus = True
        return

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False

    def handleMouseLeaveEvent(self, cmp):
        return True

    def handleMouseEnterEvent(self, cmp):
        return True

    def handleMouseEvent(self, cmp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.component.ctext.script.scrolledUP()
            return True
        if dz < 0:
            self.component.ctext.script.scrolledDOWN()
            return True
        return False

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.width = sW
        self.component.height = sH
        self.component.frame1.width = sW
        self.component.frame1.height = sH
        self.component.delChild('ctext')
        self.setupTxt()

    def updateText(self):
        binds = BWPersonality.GUICore.optionsDataSection['keybinds']
        bindingkeys = u''
        for action, bkey, str1, str2, flag in binds:
            bindingkeys += '%s    [ %s ] \n' % (str2, bkey)

        tmpHelpText = lc('soHelpGUI.helpText')
        tmpHelpText = tmpHelpText.replace('[', '<').replace(']', '>')
        text = tmpHelpText.replace('<bindingkeys>', bindingkeys)
        self.component.ctext.script.setText(text)