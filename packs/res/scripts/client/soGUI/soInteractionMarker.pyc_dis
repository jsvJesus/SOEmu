# Embedded file name: scripts/client/soGUI/soInteractionMarker.py
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from Avatar import PlayerAvatar

class soInteractionMarker(PyGUI.PyGUIBase):
    factoryString = 'soGUI.soInteractionMarker'
    INTERACTION_NONE = 0
    INTERACTION_USE = 1
    INTERACTION_TALK = 2
    INTERACTION_PICKUP = 3

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.iconMap = {soInteractionMarker.INTERACTION_USE: 'soGUI/maps/Icons/interaction_use.tga',
         soInteractionMarker.INTERACTION_TALK: 'soGUI/maps/Icons/interaction_talk.tga',
         soInteractionMarker.INTERACTION_PICKUP: 'soGUI/maps/Icons/interaction_pickup.tga'}
        self.setupRoot()
        self.setupBindLabel()

    def setupRoot(self):
        cmp = self.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 120
        cmp.height = 80
        cmp.position = (0.0, 0.2, 0.5)
        cmp.colour = (255, 255, 255, 125)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.textureName = ''

    def setupBindLabel(self):
        label = GUI.Text('')
        bindKey = BigWorld.keyToString(BWPersonality.gpd.keyBindings.getBindingsForAction('InteractObject')[0][0])
        cmp = label
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_calibri_Large.font'
        cmp.colour = (155, 157, 71, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = bindKey
        cmp.position = (0.0, -0.9, 0.1)
        cmp.visible = True
        self.component.addChild(cmp, 'bindLabel')

    def setInteractionMode(self, mode):
        if mode == self.INTERACTION_NONE:
            self.component.textureName = ''
            self.hide()
        else:
            self.component.textureName = self.iconMap[mode]
            self.show()

    def show(self):
        if self.component.parent is None:
            if isinstance(BigWorld.player(), PlayerAvatar):
                BigWorld.player().playerGUI.addChild(self.component)
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False