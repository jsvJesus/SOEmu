# Embedded file name: scripts/client/soGUI/soGUILayer.py
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soInventoryScreen import soInventoryScreen, soInventoryScreen2, soInventorySlot2
from soPCTradeScreen import soPCTradeSlot
from soGUI.soCraftGUI import soCraftGUI
from soGUI.soPCTradeScreen import soPCTradeScreen
from soGUI.soCharacterScreen import soCharacterSlot
from soGUI.soQuickSlotsBar import soActionSlot

class soGUILayer(PyGUIBase):
    factoryString = 'soGUI.soGUILayer'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.dropFocus = True

    def handleDropEvent(self, component, dropped):
        if hasattr(dropped, 'script'):
            if not hasattr(dropped.script, 'factoryString'):
                return False
        fStr = dropped.script.factoryString
        if isinstance(dropped.script, soInventorySlot2):
            dropped.script.wannaDrop()
        if isinstance(dropped.script, soPCTradeSlot):
            dropped.script.cancelItem()
        if isinstance(dropped.script, soCharacterSlot):
            dropped.script.unequip()
        if isinstance(dropped.script, soActionSlot):
            dropped.script.remove()
        if fStr == 'soGUI.soPartSlot':
            BWPersonality.GUICore.craftEvent(soCraftGUI.EVENT_DELITEM, dropped.script.slotInfo)
        if fStr == 'soGUI.soTradeSlot':
            dropped.script.returnToParent()
        if fStr == 'soGUI.soEquipSlot':
            dropped.script.unEquiped()
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleMouseEvent(self, cmp, event):
        BWPersonality.GUICore.mouseMovementEvent([event.dx,
         event.dy,
         event.dz,
         (event.cursorPosition.x, event.cursorPosition.y)])
        return False