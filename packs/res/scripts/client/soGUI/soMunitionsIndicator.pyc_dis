# Embedded file name: scripts/client/soGUI/soMunitionsIndicator.py
import BigWorld
import GUI
from Helpers.PyGUI import PyGUIBase
import BWPersonality
from Localization import lc

class soMunitionsGUI(PyGUIBase):
    factoryString = 'soGUI.soMunitionsGUI'
    UPDATE_TIME_INTERVAL = 0.5

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()
        self.doReposition()
        BigWorld.callback(self.UPDATE_TIME_INTERVAL, self.updateTime)

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 148
        cmp.height = 68
        cmp.position.z = 0.9

    def setupContent(self):
        cmp = GUI.Simple('soGUI/maps/munitionsGUI/primary.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 16
        cmp.position = (0, 20, 0.5)
        self.component.addChild(cmp, 'primaryIcon')
        cmp = GUI.Simple('soGUI/maps/munitionsGUI/primary.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 16
        cmp.position = (0, 36, 0.5)
        self.component.addChild(cmp, 'secondaryIcon')
        cmp = GUI.Simple('soGUI/maps/munitionsGUI/throw.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 16
        cmp.position = (0, 52, 0.5)
        self.component.addChild(cmp, 'throwIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (19, 28, 0.5)
        cmp.text = lc('GUI.MunitionsGUI.NO_AMMO')
        self.component.addChild(cmp, 'pLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (19, 44, 0.5)
        cmp.text = lc('GUI.MunitionsGUI.NO_AMMO')
        self.component.addChild(cmp, 'sLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (19, 60, 0.5)
        cmp.text = lc('GUI.MunitionsGUI.NO_AMMO')
        self.component.addChild(cmp, 'tLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (143, 28, 0.5)
        cmp.text = u'0'
        self.component.addChild(cmp, 'pCount')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (143, 44, 0.5)
        cmp.text = u'0'
        self.component.addChild(cmp, 'sCount')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (143, 60, 0.5)
        cmp.text = u'0'
        self.component.addChild(cmp, 'tCount')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 135, 60, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_18i.font'
        cmp.position = (136, 8, 0.5)
        cmp.text = u' '
        self.component.addChild(cmp, 'timeLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 135, 60, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (50, 5, 0.5)
        cmp.text = u' '
        cmp.visible = 0
        self.component.addChild(cmp, 'fpsLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 135, 60, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.position = (70, 14, 0.5)
        cmp.text = u' '
        cmp.visible = 0
        self.component.addChild(cmp, 'pingLabel')

    def update(self):
        data = BWPersonality.GUICore.munitionsDataSection
        if data is None:
            return
        else:
            if data.has_key('primary_name'):
                self.component.pLabel.text = data['primary_name']
            if data.has_key('secondary_name'):
                self.component.sLabel.text = data['secondary_name']
            if data.has_key('throw_name'):
                self.component.tLabel.text = data['throw_name']
            if data.has_key('primary_count'):
                self.component.pCount.text = data['primary_count']
            if data.has_key('secondary_count'):
                self.component.sCount.text = data['secondary_count']
            if data.has_key('throw_count'):
                self.component.tCount.text = data['throw_count']
            self._fitText()
            return

    def _fitText(self):

        def fitLine(leftSideCmp, rightSideCmp):
            testCmp = GUI.Text('')
            testCmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            ellipsisWidth = testCmp.stringWidth(u'...')
            if testCmp.stringWidth(leftSideCmp.text + rightSideCmp.text + u' ') > self.component.width:
                rightWidth = testCmp.stringWidth(rightSideCmp.text + u' ')
                leftWidth = self.component.width - rightWidth - ellipsisWidth
                if leftWidth > 0:
                    shortName = leftSideCmp.text
                    while testCmp.stringWidth(shortName) > leftWidth:
                        shortName = shortName[:-1]

                    shortName = shortName + u'...'
                    leftSideCmp.text = shortName
                else:
                    leftSideCmp.text = u''

        fitLine(self.component.pLabel, self.component.pCount)
        fitLine(self.component.sLabel, self.component.sCount)
        fitLine(self.component.tLabel, self.component.tCount)

    def updateTime(self):
        BigWorld.callback(self.UPDATE_TIME_INTERVAL, self.updateTime)
        pl = BigWorld.player()
        if pl and pl.__class__.__name__ != 'PlayerAvatar':
            return
        self.component.timeLabel.text = BigWorld.timeOfDay()
        if self.component.fpsLabel.visible:
            self.component.fpsLabel.text = u'FPS: %0.1f' % float(BigWorld.getWatcher('Render/FPS'))
            lp = BigWorld.LatencyInfo().value
            self.component.pingLabel.text = u'ping: %0.0fms' % (lp[3] * 1000)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'munitionsGUI')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.position.x = sW - 3
        self.component.position.y = sH - 80