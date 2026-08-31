# Embedded file name: scripts/client/soGUI/soProgressBars.py
import BigWorld
import GUI
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
import Localization
from soGUI.soTextField import soTextField2
from soGUI.soTextField import soTxtFieldPropsStructure
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
import ResMgr
from random import randint
EVENT_START = 0
EVENT_FINISH = 1
EVENT_CANCEL = 2
EVENT_TIMEOUT = 3
TYPE_STARTUP = 0
TYPE_SPACE = 1
TYPE_INGAME = 2
TYPE_DUMMY = 3
LOADING_SCREENS = 'scripts/client/soGUI/data/LoadingScreens.xml'

class soIProgressBar(PyGUIBase):
    factoryString = 'soGUI.soIProgressBar'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)

    def setMinMax(self, min, max):
        pass

    def setProgress(self, value):
        pass

    def reset(self, value):
        pass

    def addMessage(self, str):
        pass

    def appendMessage(self, str):
        pass


class soAppStartProgressBar(soIProgressBar):
    factoryString = 'soGUI.soAppStartProgressBar'

    def __init__(self, component):
        soIProgressBar.__init__(self, component)
        self.min = 0.0
        self.max = 1.0
        self.msgs = ''
        self.finnished = False

    def setMinMax(self, min, max):
        self.min = min
        self.max = max

    def setProgress(self, value):
        range = self.max - self.min
        value = self.min + value * range
        self.component.bar.fillbar.clipper.value = value

    def start(self):
        GUI.addRoot(self.component)

    def cancel(self):
        pass

    def stop(self):
        GUI.delRoot(self.component)

    def reset(self, value):
        self.component.bar.fillbar.clipper.reset()

    def onLoad(self, section):
        soIProgressBar.onLoad(self, section)

    def onBound(self):
        soIProgressBar.onBound(self)
        self.start()


class soSpaceProgressBar(soIProgressBar):
    factoryString = 'soGUI.soSpaceProgressBar'
    ASPECT_RATIO = 1.777777777777778

    def __init__(self, component):
        soIProgressBar.__init__(self, component)
        component.script = self
        self.min = 0.0
        self.max = 1.0
        self.msgs = ''
        self.distance = 0
        self.timeOut = 5
        self.finished = False
        self.canceled = False
        self.timedOut = False
        self.spaceTextures = {}
        self.spaceName = 'unknown'
        self.waitForReset = False
        self.initTextureMap()
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.0)
        cmp.visible = False
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.dropFocus = True
        cmp.dragFocus = True
        cmp.mouseButtonFocus = True
        BWPersonality.GUICore.generalLayer.addChild(cmp, 'spaceLoader')

    def setupContent(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (0, 0, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.6)
        self.component.addChild(cmp, 'blackStripes')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = sh * 2
        cmp.height = sh
        cmp.position = (0.0, 0.0, 0.5)
        cmp.textureName = ''
        cmp.filterType = 'LINEAR'
        self.component.addChild(cmp, 'ldrBack')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 40)
        cmp.materialFX = 'BLEND'
        cmp.width = sw
        cmp.height = sh
        cmp.position = (0.0, 0.0, 0.5)
        cmp.textureName = 'textures/misc/other/white_noise/loading_noise.texanim'
        cmp.filterType = 'LINEAR'
        self.component.addChild(cmp, 'ldrMask')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = sw
        cmp.height = sh
        cmp.position = (0.0, 0.0, 0.5)
        cmp.textureName = 'soGUI/maps/Misc/loading_screens/loading_mask.dds'
        cmp.filterType = 'LINEAR'
        self.component.addChild(cmp, 'ldrMask1')
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loadingCircle.texanim')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.height = 41
        cmp.width = 41
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (sW - 130, sH - 60, 0.0)
        self.component.addChild(cmp, 'ldrAnim')
        if Localization.Localization.globalLanguage == 'russian':
            cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loading.tga')
        else:
            cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loading_eng.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.height = 41
        cmp.width = 165
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (sW - 200, sH - 60, 0.0)
        self.component.addChild(cmp, 'ldrSign')
        hint = soTextField2(GUI.Window(), soTxtFieldPropsStructure(autoSize=True, height=200, width=375, vScroll=False, textureless=True))
        cmp = hint.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalAnchor = 'CENTER'
        cmp.position = (sW / 2.0, sH - 20, 0.2)
        hint.onBound()
        hint.setText('')
        self.component.addChild(cmp, 'hint')

    def initTextureMap(self):
        xmlData = ResMgr.openSection(LOADING_SCREENS)
        spaces = xmlData.values()
        for space in spaces:
            self.spaceTextures[space.readString('name')] = space.readStrings('path')

    def setMinMax(self, min, max):
        self.min = min
        self.max = max

    def setProgress(self, value):
        range = self.max - self.min
        value = self.min + value * range

    def reset(self, value = None):
        pass

    def addMessage(self, str):
        self.component.hint.script.setText(str)

    def appendMessage(self, str):
        pass

    def show(self):
        BigWorld.worldDrawEnabled(False)
        self.component.visible = True
        self.progressChecker().run()
        self.addMessage(BWPersonality.GUICore.hintFeeder.getHint())

    def hide(self):
        BigWorld.worldDrawEnabled(True)
        self.component.visible = False

    def setTimeout(self, timeOut):
        self.timeOut = timeOut

    def setDistance(self, dst):
        self.distance = dst

    def setWaitMode(self, doWait = False):
        self.waitForReset = doWait

    def setSpaceName(self, spaceName):
        texturePath = ''
        if not self.spaceTextures.has_key(spaceName):
            spaceName = 'unknown'
        index = randint(0, len(self.spaceTextures[spaceName]) - 1)
        texturePath = self.spaceTextures[spaceName][index]
        self.component.ldrBack.textureName = texturePath

    def cancel(self):
        self.canceled = True
        self.hide()
        BWPersonality.GUICore.loaderGUIEvent(EVENT_CANCEL, (TYPE_SPACE, self.spaceName))

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.hint.position = (sW / 2.0, sH - 20, 0.2)
        self.component.ldrAnim.position = (sW - 130, sH - 60, 0.0)
        self.component.ldrSign.position = (sW - 200, sH - 60, 0.0)
        self.component.ldrBack.width = sH * 2
        self.component.ldrBack.height = sH

    @BWMemberCoroutine
    def progressChecker(self):
        startTime = BigWorld.time()
        self.finished = False
        self.timedOut = False
        self.canceled = False
        self.reset()
        lastStatus = 0.0
        if self.waitForReset:
            while BigWorld.spaceLoadStatus(self.distance) == 1.0:
                yield BWWaitForPeriod(0.05)

        while not self.finished:
            if not self.canceled:
                if not self.timedOut:
                    yield BWWaitForPeriod(0.05)
                    status = BigWorld.spaceLoadStatus(self.distance)
                    finished = status >= 0.999
                    timedOut = BigWorld.time() - self.timeOut > startTime
                    if timedOut:
                        self.timedOut = True
                        BWPersonality.GUICore.loaderGUIEvent(EVENT_TIMEOUT, (TYPE_SPACE, self.spaceName))
                    self.finished = finished and True
                    BWPersonality.GUICore.loaderGUIEvent(EVENT_FINISH, (TYPE_SPACE, self.spaceName))
                    self.setProgress(1.0)
                lastStatus < status and self.setProgress(status)
                lastStatus = status

        self.hide()


class soIngameProgressBar(soIProgressBar):
    factoryString = 'soGUI.soIngameProgressBar'

    def __init__(self, component):
        soIProgressBar.__init__(self, component)
        component.script = self
        self.min = 0.0
        self.max = 1.0
        self.distance = 0
        self.timeOut = 5
        self.finished = False
        self.canceled = False
        self.timedOut = False
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.textureName = 'soGUI/maps/Colours/col_white.dds'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.filterType = 'LINEAR'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.25)
        cmp.visible = False
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.dropFocus = True
        cmp.dragFocus = True
        cmp.mouseButtonFocus = True
        BWPersonality.GUICore.generalLayer.addChild(cmp, 'ingameLoader')

    def setupContent(self):
        cmp = GUI.Simple('soGUI/maps/loadingScreen/gears/gears.texanim')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.height = 153
        cmp.width = 191
        cmp.colour = (255, 255, 255, 125)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.5, 0.0)
        self.component.addChild(cmp, 'ldrAnim')

    def setMinMax(self, min, max):
        self.min = min
        self.max = max

    def setProgress(self, value):
        range = self.max - self.min
        value = self.min + value * range

    def reset(self, value = None):
        pass

    def addMessage(self, str):
        pass

    def appendMessage(self, str):
        pass

    def downSampleIfNotPresent(self):
        import PostProcessing
        eC = PostProcessing.chain()
        doDS = True
        for effect in eC:
            if effect.name == 'Down Sample':
                doDS = False

        if doDS:
            dsE = PostProcessing.downSample()
            eC.append(dsE)
            PostProcessing.chain(eC)

    def show(self):
        self.component.visible = True
        self.progressChecker().run()

    def hide(self):
        self.component.visible = False

    def setTimeout(self, timeOut):
        self.timeOut = timeOut

    def setDistance(self, dst):
        self.distance = dst

    @BWMemberCoroutine
    def progressChecker(self):
        startTime = BigWorld.time()
        self.finished = False
        self.timedOut = False
        self.canceled = False
        self.reset()
        self.downSampleIfNotPresent()
        import PostProcessing
        effect = PostProcessing.blur()
        effect.name = 'Teleport Progress Bar'
        effect.phases[-1].renderTarget = BigWorld.RenderTarget('teleportGobo', -3, -3)
        effect.phases[-1].material.additionalAlpha = 1.0
        c = list(PostProcessing.chain())
        c.append(effect)
        PostProcessing.chain(c)
        self.effect = effect
        self.component.secondaryTexture = effect.phases[-1].renderTarget.texture
        self.component.freeze = effect.phases[-1].renderTarget
        yield BWWaitForPeriod(0.1)
        c = list(PostProcessing.chain())
        ch = []
        for e in c:
            if e.name != 'Teleport Progress Bar':
                ch.append(e)

        PostProcessing.chain(ch)
        while not self.finished:
            if not self.canceled:
                if not self.timedOut:
                    lastStatus = 0.0
                    yield BWWaitForPeriod(0.05)
                    status = BigWorld.spaceLoadStatus(self.distance)
                    finished = status >= 0.999
                    timedOut = BigWorld.time() - self.timeOut > startTime
                    if timedOut:
                        self.timedOut = True
                        BWPersonality.GUICore.loaderGUIEvent(EVENT_TIMEOUT, TYPE_INGAME)
                    self.finished = finished and True
                    BWPersonality.GUICore.loaderGUIEvent(EVENT_FINISH, TYPE_INGAME)
                    self.setProgress(1.0)
                lastStatus < status and self.setProgress(status)
                lastStatus = status

        self.hide()


class soDummyProgressBar(soIProgressBar):
    factoryString = 'soGUI.soDummyProgressBar'
    LOADING_SCREEN_MAP = {'unknown': 'soGUI/maps/Misc/loading_screen.jpg',
     'default': 'soGUI/maps/Misc/loading_screen.jpg',
     'random': '',
     'spaces/noob_city': 'soGUI/maps/loadingScrs/noob_city_ldr.tga',
     'spaces/vesuvius': 'soGUI/maps/loadingScrs/vesuvius_ldr.tga',
     'spaces/main': 'soGUI/maps/loadingScrs/main_ldr.tga',
     'spaces/personages_select': 'soGUI/maps/loadingScrs/charMgr_ldr.tga'}
    RANDOM_SCREEN_LIST = ['soGUI/maps/loadingScrs/noob_city_ldr.tga',
     'soGUI/maps/loadingScrs/vesuvius_ldr.tga',
     'soGUI/maps/loadingScrs/main_ldr.tga',
     'soGUI/maps/loadingScrs/charMgr_ldr.tga']
    ASPECT_RATIO = 1.777777777777778

    def __init__(self, component):
        soIProgressBar.__init__(self, component)
        component.script = self
        self.min = 0.0
        self.max = 1.0
        self.msgs = ''
        self.distance = 0
        self.timeOut = 5
        self.finished = False
        self.canceled = False
        self.timedOut = False
        self.spaceName = 'unknown'
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.0)
        cmp.visible = False
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.dropFocus = True
        cmp.dragFocus = True
        cmp.mouseButtonFocus = True
        BWPersonality.GUICore.generalLayer.addChild(cmp, 'dummyLoader')

    def setupContent(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (0, 0, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.6)
        self.component.addChild(cmp, 'blackStripes')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = sh * 2
        cmp.height = sh
        cmp.position = (0.0, 0.0, 0.5)
        cmp.textureName = ''
        self.component.addChild(cmp, 'ldrBack')
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loadingCircle.texanim')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.height = 41
        cmp.width = 41
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (sW - 130, sH - 60, 0.0)
        self.component.addChild(cmp, 'ldrAnim')
        if Localization.Localization.globalLanguage == 'russian':
            cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loading.tga')
        else:
            cmp = GUI.Simple('soGUI/maps/loadingScreen/loadingCircle/loading_eng.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.height = 41
        cmp.width = 165
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (sW - 200, sH - 60, 0.0)
        self.component.addChild(cmp, 'ldrSign')
        hint = soTextField2(GUI.Window(), soTxtFieldPropsStructure(autoSize=True, height=200, width=375, vScroll=False, textureless=True))
        cmp = hint.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalAnchor = 'CENTER'
        cmp.position = (sW / 2.0, sH - 20, 0.2)
        hint.onBound()
        hint.setText('')
        self.component.addChild(cmp, 'hint')

    def setMinMax(self, min, max):
        self.min = min
        self.max = max

    def setProgress(self, value):
        range = self.max - self.min
        value = self.min + value * range

    def reset(self, value = None):
        pass

    def addMessage(self, str):
        self.component.hint.script.setText(str)

    def appendMessage(self, str):
        pass

    def show(self):
        BigWorld.worldDrawEnabled(False)
        self.component.visible = True

    def hide(self):
        BigWorld.worldDrawEnabled(True)
        self.component.visible = False

    def setTimeout(self, timeOut):
        self.timeOut = timeOut

    def setDistance(self, dst):
        self.distance = dst

    def setSpaceName(self, spaceName):
        if spaceName == 'random':
            self.spaceName = 'random'
            index = randint(0, len(self.RANDOM_SCREEN_LIST) - 1)
            self.component.ldrBack.textureName = self.RANDOM_SCREEN_LIST[index]
            return
        if self.LOADING_SCREEN_MAP.has_key(spaceName):
            self.spaceName = spaceName
            self.component.ldrBack.textureName = self.LOADING_SCREEN_MAP[spaceName]
        else:
            self.spaceName = 'unknown'
            self.component.ldrBack.textureName = self.LOADING_SCREEN_MAP[self.spaceName]

    def cancel(self):
        self.canceled = True
        self.hide()

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.hint.position = (sW / 2.0, sH - 20, 0.2)
        self.component.ldrAnim.position = (sW - 130, sH - 60, 0.0)
        self.component.ldrSign.position = (sW - 200, sH - 60, 0.0)
        self.component.ldrBack.width = sH * 2
        self.component.ldrBack.height = sH