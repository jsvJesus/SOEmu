# Embedded file name: scripts/client/soGUI/soDialogueGUI.py
QUEST_GUI_FRAME_TEXTURE = 'soGUI/maps/con_frame.tga'
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from soGUI.soTextField import soTextField, soTextField2, soTxtFieldPropsStructure
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWTT
from Helpers.PyGUI import Utils
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import Utils
from functools import partial
from Helpers import Listener

class QuestDlgPropsStructure(object):

    def __init__(self, text = u'end', caption = 'Stalker NPC', answers = {1: u'',
 2: u'',
 3: u'',
 4: u''}, icon = soGUI.QUEST_GUI_ICON_NONE):
        self.text = text
        self.answers = answers
        self.icon = icon
        self.caption = caption


class soDlgWindow(PyGUI.Window):
    factoryString = 'soGUI.soDlgWindow'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self


class soDialogueGUI(PyGUI.Window, Listener.Listenable):
    factoryString = 'soGUI.soDialogueGUI'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        Listener.Listenable.__init__(self)
        component.script = self
        self.dlg = None
        self.answerBtns = []
        self.setupRoot()
        return

    def setupRoot(self):
        self.component.horizontalAnchor = soGUI.QUEST_GUI_ROOT_HPLACEMENT
        self.component.verticalAnchor = soGUI.QUEST_GUI_ROOT_VPLACEMENT
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'CLIP'
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.materialFX = 'BLEND'
        self.component.colour = (255, 255, 255, 255)
        self.component.position = (-0.1, 0.0, 0.0)

    def showDlg(self, props = QuestDlgPropsStructure()):
        if self.dlg is not None:
            self.closeDlg()
        self.dlg = soDlgWindow(GUI.Window())
        BWPersonality.GUICore.setBestCursor()
        self.dlg.component.horizontalPositionMode = self.dlg.component.verticalPositionMode = 'CLIP'
        self.dlg.component.widthMode = self.dlg.component.heightMode = 'PIXEL'
        self.dlg.component.verticalAnchor = 'TOP'
        self.dlg.component.horizontalAnchor = 'LEFT'
        self.dlg.component.textureName = ''
        self.dlg.component.position = (-1.0, 1.0, 0.0)
        self.dlg.component.width = soGUI.QUEST_GUI_DLG_WIDTH
        self.dlg.component.height = 650

        def setupFrameTexture():
            frameComp = GUI.Frame2(QUEST_GUI_FRAME_TEXTURE)
            frameComp.horizontalPositionMode = frameComp.verticalPositionMode = 'CLIP'
            frameComp.widthMode = frameComp.heightMode = 'CLIP'
            frameComp.horizontalAnchor = 'LEFT'
            frameComp.verticalAnchor = 'TOP'
            frameComp.colour = (255, 255, 255, 255)
            frameComp.materialFX = 'BLEND'
            frameComp.width = 2.0
            frameComp.height = 2.0 - soGUI.getPixelHeight(self.dlg.component) * soGUI.QUEST_GUI_CAPTIONH
            frameComp.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.dlg.component) * soGUI.QUEST_GUI_CAPTIONH, 0.5)
            self.dlg.component.addChild(frameComp, 'frameCmp')

        def setupCaption():
            captionComp = GUI.Frame2(QUEST_GUI_FRAME_TEXTURE)
            captionComp.horizontalPositionMode = captionComp.verticalPositionMode = 'CLIP'
            captionComp.widthMode = captionComp.heightMode = 'CLIP'
            captionComp.horizontalAnchor = 'LEFT'
            captionComp.verticalAnchor = 'TOP'
            captionComp.colour = (175, 166, 112, 255)
            captionComp.materialFX = 'BLEND'
            captionComp.height = soGUI.getPixelHeight(self.dlg.component) * soGUI.QUEST_GUI_CAPTIONH
            captionComp.width = 2.0
            captionComp.position = (-1.0, 1.0, 0.5)
            self.dlg.component.addChild(captionComp, 'caption')

        def setupCloseBtn():
            btnComp = GUI.Window()
            btnComp.horizontalPositionMode = btnComp.verticalPositionMode = 'CLIP'
            btnComp.widthMode = btnComp.heightMode = 'PIXEL'
            btnComp.verticalAnchor = 'TOP'
            btnComp.horizontalAnchor = 'RIGHT'
            btnComp.colour = (255, 255, 255, 255)
            btnComp.materialFX = 'BLEND'
            btnComp.width = 18
            btnComp.height = 18
            btnComp.position = (1.0 - soGUI.getPixelWidth(self.dlg.component) * soGUI.QUEST_GUI_DLG_BORDER_OFFSET, 1.0 - soGUI.getPixelHeight(self.dlg.component) * soGUI.QUEST_GUI_DLG_BORDER_OFFSET, 0.0)
            btn = soButton(btnComp)
            btn.initVSC('soGUI/visual_styles/closeBox.xml')
            btn.setVisualState('normal')
            btn.onBound()
            btn.onClick = self.onCloseBtn
            self.dlg.component.addChild(btn.component, 'closeBox')

        def setupCaptionLabel():
            cptComp = GUI.Text('')
            cptComp.horizontalPositionMode = cptComp.verticalPositionMode = 'CLIP'
            cptComp.verticalAnchor = 'CENTER'
            cptComp.horizontalAnchor = 'LEFT'
            cptComp.colour = (175, 166, 112, 255)
            cptComp.materialFX = 'BLEND'
            cptComp.font = 'ruRU_calibri_default.font'
            cptComp.text = props.caption
            cptComp.position = (-1.0 + soGUI.getPixelWidth(self.dlg.component) * 6, 1.0 - soGUI.getPixelHeight(self.dlg.component) * (soGUI.QUEST_GUI_CAPTIONH / 2), 0.0)
            self.dlg.component.addChild(cptComp, 'captionLabel')

        def setupTextField():
            txtComp = GUI.Window()
            txtComp.horizontalPositionMode = txtComp.verticalPositionMode = 'CLIP'
            txtComp.horizontalAnchor = 'LEFT'
            txtComp.verticalAnchor = 'TOP'
            txtComp.widthMode = txtComp.heightMode = 'PIXEL'
            txtComp.width = self.dlg.component.width - soGUI.QUEST_GUI_DLG_BORDER_OFFSET * 2
            txtComp.height = self.dlg.component.height - soGUI.QUEST_GUI_DLG_BORDER_OFFSET * 2 - soGUI.QUEST_GUI_CAPTIONH - 138
            txtComp.position = (-1.0 + soGUI.getPixelWidth(self.dlg.component) * soGUI.QUEST_GUI_DLG_BORDER_OFFSET, 1.0 - soGUI.getPixelHeight(self.dlg.component) * (soGUI.QUEST_GUI_CAPTIONH + soGUI.QUEST_GUI_DLG_BORDER_OFFSET), 0.0)
            txtField = soTextField(txtComp)
            txtField.textFrame.textureName = ''
            txtField.frameTopOffset = 0
            txtField.frameLeftOffset = 0
            self.dlg.component.addChild(txtField.component, 'textField')
            txtField.doLayout()
            txtField.onBound()
            txtField.addText(props.text)

        def setupBtns():
            i = 0
            for answer in props.answers:
                btn = soButton(GUI.Window())
                btn.component.horizontalPositionMode = btn.component.verticalPositionMode = 'CLIP'
                btn.component.widthMode = btn.component.heightMode = 'PIXEL'
                btn.component.horizontalAnchor = 'LEFT'
                btn.component.verticalAnchor = 'TOP'
                btn.component.width = self.dlg.component.textField.width
                btn.component.height = soGUI.QUEST_GUI_BUTTONH
                btn.component.position = (-1.0 + soGUI.getPixelWidth(self.dlg.component) * soGUI.QUEST_GUI_DLG_BORDER_OFFSET, 1.0 - soGUI.getPixelHeight(self.dlg.component) * (self.dlg.component.textField.height + i * (soGUI.QUEST_GUI_BUTTONH + 2) + soGUI.QUEST_GUI_CAPTIONH), 0.0)
                btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
                self.dlg.component.addChild(btn.component, 'btn' + str(i))
                btn.setVisualState('normal')
                btn.onBound()
                btn.component.label.text = props.answers[answer]
                btn.onClick = partial(self.processDialogueEvent, answer)
                self.answerBtns.append(btn)
                i += 1

        setupFrameTexture()
        setupCaption()
        setupCloseBtn()
        setupCaptionLabel()
        setupTextField()
        setupBtns()
        self.dlg.onBound()
        self.component.addChild(self.dlg.component, 'dlgWindow')
        return

    def setText(self, txt = ''):
        if self.dlg is not None:
            if hasattr(self.dlg.component, 'textField'):
                self.dlg.component.textField.script.delText()
                self.dlg.component.textField.script.addText(txt)
                return True
        else:
            return False
        return

    def setAnswers(self, answers = {}):
        for btn in self.answerBtns:
            btn.component.parent.delChild(btn.component)
            btn = None

        def setupBtns():
            i = 0
            for answer in answers:
                btn = soButton(GUI.Window())
                btn.component.horizontalPositionMode = btn.component.verticalPositionMode = 'CLIP'
                btn.component.widthMode = btn.component.heightMode = 'PIXEL'
                btn.component.horizontalAnchor = 'LEFT'
                btn.component.verticalAnchor = 'TOP'
                btn.component.width = self.dlg.component.textField.width
                btn.component.height = soGUI.QUEST_GUI_BUTTONH
                btn.component.position = (-1.0 + soGUI.getPixelWidth(self.dlg.component) * soGUI.QUEST_GUI_DLG_BORDER_OFFSET, 1.0 - soGUI.getPixelHeight(self.dlg.component) * (self.dlg.component.textField.height + i * (soGUI.QUEST_GUI_BUTTONH + 2) + soGUI.QUEST_GUI_CAPTIONH), 0.0)
                btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
                self.dlg.component.addChild(btn.component, 'btn' + str(i))
                btn.setVisualState('normal')
                btn.onBound()
                btn.component.label.text = answers[answer]
                btn.onClick = partial(self.processDialogueEvent, answer)
                self.answerBtns.append(btn)
                i += 1

        setupBtns()
        return

    def closeDlg(self):
        if self.dlg is not None:
            self.component.delChild(self.dlg.component)
            self.dlg = None
            BWPersonality.GUICore.setBestCursor()
        return

    def processDialogueEvent(self, event):
        self.listeners.questGUIEvent(event)

    def wantClose(self):
        self.listeners.questCloseBtn()

    def onCloseBtn(self):
        self.wantClose()


class soDialogueGUI2(PyGUIBase):
    factoryString = 'soGUI.soDialogueGUI2'
    EVENT_ANSWER = 0
    EVENT_USERCLOSE = 1
    EVENT_CLOSE = 2

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.btns = []
        self.setupRoot()
        self.setupFrame()
        self.setupTxt()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 363
        cmp.height = 384
        cmp.position = (0.0, 0.66666666, 0.2)
        cmp.visible = False
        cmp.textureName = ''

    def setupFrame(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (335, 6, 0.4)
        btn.initVSC('soGUI/visual_styles/closeBox3D.xml')
        self.component.addChild(cmp, 'closeBox')
        btn.onBound()
        btn.setVisualState('normal')
        cmp = GUI.Text('')
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.position = (self.component.width / 2.0, 18, 0.5)
        cmp.text = u''
        self.component.addChild(cmp, 'caption')

    def setupTxt(self):
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(autoSize=False, borderWidth=0, autoScroll=False, width=333, height=290, hideScroll=True))
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (15, 56, 0.5)
        self.component.addChild(cmp, 'txt')
        txt.onBound()

    def renderAnswers(self, answerList):
        btnOrigin = self.component.txt.script.getHeight() + 54 + 15
        self.component.height = 397
        for btn in self.btns:
            self.component.delChild(btn)

        self.btns = []
        for i, answer in enumerate(answerList):
            self.component.height += 30
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.width = 347
            cmp.height = 30
            cmp.position = (self.component.width / 2.0, btnOrigin + i * 30, 0.4)
            btn.initVSC('soGUI/visual_styles/dialogueBtn.xml')
            self.component.addChild(cmp, 'answer' + str(i))
            btn.onBound()
            btn.setVisualState('normal')
            btn.onClick = partial(self.onAnswer, answer[0], answer[1])
            cmp.label.font = 'ruRU_calibri_default.font'
            cmp.label.text = answer[1]
            self.btns.append(cmp)

    def lockAnswers(self, doLock = True):
        for btn in self.btns:
            btn.script.buttonDisabled = doLock
            btn.script._updateVisualState()

    def update(self):
        data = BWPersonality.GUICore.dialogueDataSection
        if data is None:
            return
        else:
            self.component.caption.text = data[0]
            self.component.txt.script.setText(data[1])
            self.component.txt.script.scrollToTop()
            self.renderAnswers(data[2])
            return

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'dlgGUI')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        BWPersonality.GUICore.dialogueEvent(self.EVENT_CLOSE, None)
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        return

    def onAnswer(self, id, caption):
        BWPersonality.GUICore.dialogueEvent(self.EVENT_ANSWER, (id, caption))
        self.lockAnswers(True)

    def wantClose(self):
        BWPersonality.GUICore.dialogueEvent(self.EVENT_USERCLOSE, None)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.wantClose()