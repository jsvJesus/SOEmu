# Embedded file name: scripts/client/soGUI/soScreen.py
from Localization import lc
import BigWorld
import FMOD
import GUI
import Helpers.PyGUI as PyGUI
import BWPersonality
import soGUI
from soGUI.soButton import soButton
from soGUI.soTextField import soTextField
from soGUI.soList import soList
from soGUI.soCheckBox import soCheckBox
from soGUI.soRadioButton import soRadioButton
from soGUI.soDropDownList import soDropDownList
from soGUI.soDialogueGUI import soDialogueGUI
from soGUI.soItemMods import soItemMods
from soGUI.soEditField import soEditField
from Helpers import Listener
from functools import partial
import GraphicsPresets
from soGUI.soEditField import soEditField2
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import Utils

class soScreen(PyGUI.Window, Listener.Listenable):
    factoryString = 'soGUI.soScreen'
    BTN_OK = 0
    BTN_CANCEL = 1
    BTN_YES = 2
    BTN_NO = 3
    BTN_APPLY = 4
    BTN_RESET = 5
    BTN_UNDO = 6
    LABEL_DEFAULT_OK = u'Ok'
    LABEL_DEFAULT_CANCEL = lc('soScreen.soGUI.STRING_41_24')
    LABEL_DEFAULT_YES = lc('soScreen.soGUI.STRING_42_21')
    LABEL_DEFAULT_NO = lc('soScreen.soGUI.STRING_43_20')
    LABEL_DEFAULT_APPLY = lc('soScreen.soGUI.STRING_44_23')
    LABEL_DEFAULT_RESET = lc('soScreen.soGUI.STRING_45_23')
    LABEL_DEFAULT_UNDO = u'Undo'
    GLYPH_TEXTURE = 'soGUI/maps/Icons/glyph_dlgBoxes.tga'
    GLYPH_NONE = ('', (0.0, 0.0, 0.0, 0.0))
    GLYPH_INFO = (GLYPH_TEXTURE, (0.0, 0.0, 0.0, 0.0))
    GLYPH_QUESTION = (GLYPH_TEXTURE, (0.0, 0.0, 0.0, 0.0))
    GLYPH_WARNING = (GLYPH_TEXTURE, (0.0, 0.0, 0.0, 0.0))
    GLYPH_ERROR = (GLYPH_TEXTURE, (0.0, 0.0, 0.0, 0.0))
    CAPTION_TEXTURE = ('soGUI/maps/Controls/window.tga', (0.0, 0.0, 600.0, 41.0))
    WRKAREA_TEXTURE = ('soGUI/maps/Controls/window.tga', (0.0, 41.0, 600.0, 450.0))
    DLGBOX_DEFAULT_WIDTH = 400
    DLGBOX_DEFAULT_HEIGHT = 200
    DLGBOX_DEFAULT_POSITION = (-0.5, 0.5)
    DLGBOX_EVENT_CLOSE = 0
    DLGBOX_EVENT_OK = 1
    DLGBOX_EVENT_CANCEL = 2
    DLGBOX_EVENT_YES = 3
    DLGBOX_EVENT_NO = 4
    DLGBOX_EVENT_APPLY = 5
    DLGBOX_EVENT_RESET = 6
    DLGBOX_EVENT_UNDO = 7
    DLGBOX_EDITFIELD_HEIGHT = 25
    dlgBoxes = {}
    buttonHeight = 30
    buttonWidth = 70
    modalState = None
    cascadeStep = 0
    radios = {}

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        Listener.Listenable.__init__(self)
        component.script = self
        BWPersonality.gpd.guiScreen = self

    def wantCharacterFocus(self, component):
        pass

    def wantKeyEventsFocus(self, component):
        pass

    def registerRadioBtn(self, btnCmp, group):
        if not self.radios.has_key(group):
            self.radios[group] = []
        self.radios[group].append(btnCmp)

    def radioSelect(self, btnCmp):
        if hasattr(btnCmp, 'script'):
            if hasattr(btnCmp.script, 'group'):
                for radio in self.radios[btnCmp.script.group]:
                    radio.script.selection(False)

                btnCmp.script.selection(True)

    def getBestCursor(self):
        """
        \xd0\xb2\xd0\xbe\xd0\xb7\xd0\xb2\xd1\x80\xd0\xb0\xd1\x89\xd0\xb0\xd0\xb5\xd1\x82 true \xd0\xb5\xd1\x81\xd0\xbb\xd0\xb8 \xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd1\x83\xd0\xb5\xd1\x82 \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd1\x8c mouse cursor
        false \xd0\xb5\xd1\x81\xd0\xbb\xd0\xb8 direction
        """
        for dlgBox in self.dlgBoxes:
            if self.dlgBoxes[dlgBox] is not None:
                return True

        if isinstance(BigWorld.player(), PlayerAvatar):
            return False
        else:
            return True

    def processDlgBoxEvent(self, event, dlgBox, text = ''):
        if hasattr(self.dlgBoxes[dlgBox].workArea, 'edit'):
            self.listeners.dlgBoxEvent(dlgBox, event, self.dlgBoxes[dlgBox].workArea.edit.script.getValue())
            self.dlgBoxes[dlgBox].workArea.edit.script.setActive(False)
        else:
            self.listeners.dlgBoxEvent(dlgBox, event)
        if event == soScreen.DLGBOX_EVENT_CLOSE or event == soScreen.DLGBOX_EVENT_OK or event == soScreen.DLGBOX_EVENT_CANCEL or event == soScreen.DLGBOX_EVENT_YES or event == soScreen.DLGBOX_EVENT_NO:
            if self.modalState == self.dlgBoxes[dlgBox]:
                self.goModal(None)
            if True:
                BWPersonality.GUICore.generalLayer.delChild(self.dlgBoxes[dlgBox])
                self.dlgBoxes[dlgBox] = None
            BWPersonality.GUICore.setBestCursor()
        return

    def showDialogueBox(self, dlgBoxProps, text = '', btnSet = None, isModal = False):
        print 'showDialogueBox is deprecated'
        print 'use soGUICore::showMessageBox instead'
        return
        if self.modalState is not None:
            return -1
        else:
            dlgBox = GUI.Window()
            dlgBox.widthMode = 'PIXEL'
            dlgBox.heightMode = 'PIXEL'
            dlgBox.horizontalPositionMode = 'CLIP'
            dlgBox.verticalPositionMode = 'CLIP'
            dlgBox.horizontalAnchor = 'LEFT'
            dlgBox.verticalAnchor = 'TOP'
            dlgBox.materialFX = 'BLEND'
            dlgBox.colour = (255, 255, 255, 255)
            dlgBox.width = dlgBoxProps.dlgBoxWidth
            dlgBox.height = dlgBoxProps.dlgBoxHeight
            dlgBox.position = (dlgBoxProps.dlgBoxPosition[0] + soGUI.getPixelWidth(self.component) * self.cascadeStep * 3, dlgBoxProps.dlgBoxPosition[1] - soGUI.getPixelHeight(self.component) * self.cascadeStep * 3, 0.0)
            dlgBox.visible = True
            index = len(self.dlgBoxes)
            self.dlgBoxes[index] = dlgBox
            BWPersonality.GUICore.generalLayer.addChild(self.dlgBoxes[index], 'dlgBox' + str(index))
            dlgBoxCaption = GUI.Window()
            dlgBoxWorkArea = GUI.Window()
            dlgBoxCaption.textureName = ''
            dlgBoxCaption.materialFX = 'BLEND'
            dlgBoxCaption.widthMode = 'PIXEL'
            dlgBoxCaption.heightMode = 'PIXEL'
            dlgBoxCaption.width = self.dlgBoxes[index].width
            dlgBoxCaption.height = 26
            dlgBoxCaption.verticalAnchor = 'TOP'
            dlgBoxCaption.horizontalAnchor = 'LEFT'
            dlgBoxCaption.horizontalPositionMode = 'CLIP'
            dlgBoxCaption.verticalPositionMode = 'CLIP'
            dlgBoxCaption.position = (-1.0, 1.0, 0.0)
            dlgBoxCaptionFrame = GUI.Frame2('soGUI/maps/con_frame.tga')
            dlgBoxCaptionFrame.horizontalPositionMode = dlgBoxCaptionFrame.verticalPositionMode = 'CLIP'
            dlgBoxCaptionFrame.widthMode = dlgBoxCaptionFrame.heightMode = 'CLIP'
            dlgBoxCaptionFrame.horizontalAnchor = 'CENTER'
            dlgBoxCaptionFrame.verticalAnchor = 'CENTER'
            dlgBoxCaptionFrame.colour = (255, 255, 255, 255)
            dlgBoxCaptionFrame.materialFX = 'BLEND'
            dlgBoxCaptionFrame.width = 2.0
            dlgBoxCaptionFrame.height = 2.0
            dlgBoxCaptionFrame.position = (0.0, 0.0, 0.5)
            dlgBoxCaption.addChild(dlgBoxCaptionFrame, 'dlgBoxCaptionFrame')
            dlgBoxWorkArea.textureName = ''
            dlgBoxWorkArea.materialFX = 'BLEND'
            dlgBoxWorkArea.widthMode = 'PIXEL'
            dlgBoxWorkArea.heightMode = 'PIXEL'
            dlgBoxWorkArea.width = self.dlgBoxes[index].width
            dlgBoxWorkArea.height = self.dlgBoxes[index].height - 26
            dlgBoxWorkArea.verticalAnchor = 'TOP'
            dlgBoxWorkArea.horizontalAnchor = 'LEFT'
            dlgBoxWorkArea.horizontalPositionMode = 'CLIP'
            dlgBoxWorkArea.verticalPositionMode = 'CLIP'
            dlgBoxWorkArea.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.dlgBoxes[index]) * dlgBoxCaption.height, 0.0)
            dlgBoxWAFrame = GUI.Frame2('soGUI/maps/con_frame.tga')
            dlgBoxWAFrame.horizontalPositionMode = dlgBoxWAFrame.verticalPositionMode = 'CLIP'
            dlgBoxWAFrame.widthMode = dlgBoxWAFrame.heightMode = 'CLIP'
            dlgBoxWAFrame.horizontalAnchor = 'CENTER'
            dlgBoxWAFrame.verticalAnchor = 'CENTER'
            dlgBoxWAFrame.colour = (255, 255, 255, 255)
            dlgBoxWAFrame.materialFX = 'BLEND'
            dlgBoxWAFrame.width = 2.0
            dlgBoxWAFrame.height = 2.0
            dlgBoxWAFrame.position = (0.0, 0.0, 0.5)
            dlgBoxWorkArea.addChild(dlgBoxWAFrame, 'dlgBoxWAFrame')
            self.dlgBoxes[index].addChild(dlgBoxCaption, 'caption')
            self.dlgBoxes[index].addChild(dlgBoxWorkArea, 'workArea')
            closeBtn = soButton(GUI.Window())
            closeBtn.component.visible = True
            closeBtn.component.widthMode = 'PIXEL'
            closeBtn.component.heightMode = 'PIXEL'
            closeBtn.component.verticalPositionMode = 'CLIP'
            closeBtn.component.horizontalPositionMode = 'CLIP'
            closeBtn.component.verticalAnchor = 'CENTER'
            closeBtn.component.horizontalAnchor = 'RIGHT'
            closeBtn.component.width = 18
            closeBtn.component.height = 18
            closeBtn.component.position = (1.0 - soGUI.getPixelWidth(self.dlgBoxes[index].caption) * 4, 0.0, 0.0)
            closeBtn.initVSC('soGUI/visual_styles/closeBox.xml')
            closeBtn.onBound()
            closeBtn.onClick = partial(self.processDlgBoxEvent, event=soScreen.DLGBOX_EVENT_CLOSE, dlgBox=index)
            closeBtn.setVisualState('normal')
            self.dlgBoxes[index].caption.addChild(closeBtn.component, 'closeBtn')
            captionLabel = GUI.Text('')
            captionLabel.font = 'ruRU_calibri_default.font'
            captionLabel.verticalAnchor = 'CENTER'
            captionLabel.horizontalAnchor = 'LEFT'
            captionLabel.horizontalPositionMode = 'CLIP'
            captionLabel.verticalPositionMode = 'CLIP'
            captionLabel.colour = (255, 255, 255, 255)
            captionLabel.visible = True
            captionLabel.position = (-1.0 + soGUI.getPixelWidth(self.dlgBoxes[index].caption) * 5, 0.0, 0.0)
            captionLabel.text = dlgBoxProps.dlgBoxCaption
            self.dlgBoxes[index].caption.addChild(captionLabel, 'captionLabel')
            textFieldComp = GUI.Window()
            textFieldComp.widthMode = 'PIXEL'
            textFieldComp.heightMode = 'PIXEL'
            textFieldComp.horizontalPositionMode = 'CLIP'
            textFieldComp.verticalPositionMode = 'CLIP'
            textFieldComp.horizontalAnchor = 'LEFT'
            textFieldComp.verticalAnchor = 'TOP'
            textFieldComp.height = self.dlgBoxes[index].workArea.height - self.buttonHeight - 10
            if dlgBoxProps.editField:
                textFieldComp.height -= soScreen.DLGBOX_EDITFIELD_HEIGHT
            textFieldComp.width = self.dlgBoxes[index].width - 10
            textFieldComp.position = (-1.0 + soGUI.getPixelWidth(self.dlgBoxes[index].workArea) * 5, 1.0 - soGUI.getPixelHeight(self.dlgBoxes[index].workArea) * 5, 0.0)
            textField = soTextField(textFieldComp)
            textField.textFrame.textureName = ''
            textField.frameTopOffset = 0
            textField.frameLeftOffset = 0
            textField.doLayout()
            textField.onBound()
            self.dlgBoxes[index].workArea.addChild(textField.component, 'textField')
            self.dlgBoxes[index].workArea.textField.script.addText(text)
            if dlgBoxProps.editField:
                editField = soEditField2(GUI.Window(), width=textFieldComp.width, height=soScreen.DLGBOX_EDITFIELD_HEIGHT, font='ruRU_calibri_small.font')
                cmp = editField.component
                cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
                cmp.verticalAnchor = 'TOP'
                cmp.horizontalAnchor = 'CENTER'
                cmp.position = (0.0, 1.0 - soGUI.getPixelHeight(self.dlgBoxes[index].workArea) * (textFieldComp.height + 5), 0.0)
                editField.setActive()
                self.dlgBoxes[index].workArea.addChild(cmp, 'edit')
            buttons = []
            if btnSet is not None:
                for i in xrange(len(btnSet)):
                    button = soButton(GUI.Window())
                    button.component.visible = True
                    button.component.widthMode = 'PIXEL'
                    button.component.heightMode = 'PIXEL'
                    button.component.verticalPositionMode = 'CLIP'
                    button.component.horizontalPositionMode = 'CLIP'
                    button.component.verticalAnchor = 'BOTTOM'
                    button.component.horizontalAnchor = 'CENTER'
                    button.component.width = self.buttonWidth
                    button.component.height = self.buttonHeight
                    button.component.position = (-1.0 + 2.0 / len(btnSet) * i + 2.0 / len(btnSet) / 2, -1.0 + soGUI.getPixelHeight(self.dlgBoxes[index]) * 5, 0.0)
                    button.initVSC('soGUI/visual_styles/defaultBtnSmall.xml')
                    button.onBound()
                    button.setVisualState('normal')
                    buttons.append(button)
                    if btnSet[i] == soScreen.BTN_OK:
                        if dlgBoxProps.editField:
                            button.onClick = partial(self.processDlgBoxEvent, event=soScreen.DLGBOX_EVENT_OK, dlgBox=index, text=self.dlgBoxes[index].workArea.edit.script.getValue())
                        else:
                            button.onClick = partial(self.processDlgBoxEvent, event=soScreen.DLGBOX_EVENT_OK, dlgBox=index, text='')
                        button.component.label.text = soScreen.LABEL_DEFAULT_OK
                    elif btnSet[i] == soScreen.BTN_CANCEL:
                        button.onClick = partial(self.processDlgBoxEvent, event=soScreen.DLGBOX_EVENT_CANCEL, dlgBox=index)
                        button.component.label.text = soScreen.LABEL_DEFAULT_CANCEL

            for button in buttons:
                self.dlgBoxes[index].addChild(button.component)

            BWPersonality.GUICore.setBestCursor()
            if isModal and self.modalState is None:
                self.goModal(self.dlgBoxes[index])
            self.doCascadeStep()
            return index

    def closeDialogueBox(self, dlgBox):
        if self.dlgBoxes.has_key(dlgBox):
            BWPersonality.GUICore.generalLayer.delChild(self.dlgBoxes[dlgBox])
            self.dlgBoxes[dlgBox] = None
            return True
        else:
            return False
            return

    def goModal(self, component):
        self.modalState = component

    def doCascadeStep(self):
        self.cascadeStep += 1
        if self.cascadeStep >= 30:
            self.cascadeStep = 0

    def processScreenEvent(self, event):
        self.listeners.GUIEvent(event)


class DlgBoxPropsStructure(object):

    def __init__(self, txtFont = 'ruRU_calibri_default.font', btnFont = 'ruRU_default.font', txtFontColour = 4294967295L, btnFontColour = 4294967295L, dlgBoxColour = 4294967295L, dlgGlyph = soScreen.GLYPH_NONE, dlgBoxWidth = soScreen.DLGBOX_DEFAULT_WIDTH, dlgBoxHeight = soScreen.DLGBOX_DEFAULT_HEIGHT, dlgBoxPos = soScreen.DLGBOX_DEFAULT_POSITION, dlgBoxCaption = '', inputField = False, maxChars = 256):
        self.textFont = txtFont
        self.buttonFont = btnFont
        self.textColour = txtFontColour
        self.buttonLabelColour = btnFontColour
        self.dlgBoxColour = dlgBoxColour
        self.dlgGlyph = dlgGlyph
        self.dlgBoxWidth = dlgBoxWidth
        self.dlgBoxHeight = dlgBoxHeight
        self.dlgBoxPosition = dlgBoxPos
        self.dlgBoxCaption = dlgBoxCaption
        self.editField = inputField
        self.maxChars = maxChars


class soPlayerGUI(soScreen):
    factoryString = 'soGUI.soPlayerGUI'

    def __init__(self, component):
        soScreen.__init__(self, component)
        BWPersonality.gpd.updateWeaponData = self.updateWeaponData
        component.script = self
        questCmp = GUI.Window()
        questCmp.widthMode = questCmp.heightMode = 'PIXEL'
        questCmp.width = 650
        questCmp.height = 650
        questCmp.position = (0.0, 0.0, 0.0)
        questCmp.materialFX = 'BLEND'
        questCmp.colour = (255, 255, 255, 255)
        questGUI = soDialogueGUI(questCmp)
        questGUI.onBound()
        self.component.addChild(questGUI.component, 'questGUI')
        helpGUI = GUI.Simple('')
        helpGUI.visible = False
        helpGUI.textureName = 'soGUI/maps/Misc/helpScreen.jpg'
        helpGUI.horizontalPositionMode = helpGUI.verticalPositionMode = 'LEGACY'
        helpGUI.widthMode = helpGUI.heightMode = 'PIXEL'
        helpGUI.horizontalAnchor = 'CENTER'
        helpGUI.verticalAnchor = 'CENTER'
        helpGUI.width = 1024
        helpGUI.height = 768
        helpGUI.colour = (255, 255, 255, 255)
        helpGUI.materialFX = 'BLEND'
        helpGUI.position = (0.0, 0.0, 0.0)
        self.component.addChild(helpGUI, 'helpGUI')
        self.setupAuxiliaryGUI()
        GUI.reSort()

    def setupRoot(self):
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'LEGACY'
        self.component.widthMode = self.component.height

    def setupAuxiliaryGUI(self):
        munitions = GUI.Window()
        munitions.horizontalPositionMode = munitions.verticalPositionMode = 'PIXEL'
        munitions.widthMode = munitions.heightMode = 'PIXEL'
        munitions.verticalAnchor = 'BOTTOM'
        munitions.horizontalAnchor = 'RIGHT'
        munitions.position = (BigWorld.screenWidth(), BigWorld.screenHeight() - 72, 0.0)
        munitions.width = 128
        munitions.height = 82
        munitions.colour = (255, 255, 255, 255)
        munitions.materialFX = 'BLEND'
        munitions.textureName = ''
        self.component.addChild(munitions, 'munitions')
        munitionsFrame = GUI.Frame2('')
        munitionsFrame.verticalPositionMode = munitionsFrame.horizontalPositionMode = 'CLIP'
        munitionsFrame.widthMode = munitionsFrame.heightMode = 'PIXEL'
        munitionsFrame.horizontalAnchor = 'CENTER'
        munitionsFrame.verticalAnchor = 'CENTER'
        munitionsFrame.width = 128
        munitionsFrame.height = 82
        munitionsFrame.position = (0.0, 0.0, 0.0)
        munitionsFrame.colour = (255, 255, 255, 255)
        munitionsFrame.materialFX = 'BLEND'
        self.component.munitions.addChild(munitionsFrame, 'frame')
        shellsIcon = GUI.Window()
        shellsIcon.verticalPositionMode = shellsIcon.horizontalPositionMode = 'CLIP'
        shellsIcon.widthMode = shellsIcon.heightMode = 'PIXEL'
        shellsIcon.horizontalAnchor = 'LEFT'
        shellsIcon.verticalAnchor = 'TOP'
        shellsIcon.width = 64
        shellsIcon.height = 64
        shellsIcon.position = (-1.0, 1.0, 0.0)
        shellsIcon.textureName = ''
        shellsIcon.colour = (255, 255, 255, 255)
        shellsIcon.materialFX = 'BLEND'
        self.component.munitions.addChild(shellsIcon, 'shells')
        shellsLabel = GUI.Text('')
        shellsLabel.verticalPositionMode = shellsLabel.horizontalPositionMode = 'CLIP'
        shellsLabel.horizontalAnchor = 'CENTER'
        shellsLabel.verticalAnchor = 'BOTTOM'
        shellsLabel.font = 'ruRU_calibri_default.font'
        shellsLabel.colour = (255, 65, 65, 255)
        shellsLabel.position = (-0.5, -1.0 + soGUI.getPixelHeight(self.component.munitions) * 2, 0.0)
        self.component.munitions.addChild(shellsLabel, 'shLabel')
        grenadeIcon = GUI.Window()
        grenadeIcon.verticalPositionMode = grenadeIcon.horizontalPositionMode = 'CLIP'
        grenadeIcon.widthMode = grenadeIcon.heightMode = 'PIXEL'
        grenadeIcon.horizontalAnchor = 'RIGHT'
        grenadeIcon.verticalAnchor = 'TOP'
        grenadeIcon.width = 64
        grenadeIcon.height = 64
        grenadeIcon.position = (1.0, 1.0, 0.0)
        grenadeIcon.textureName = ''
        grenadeIcon.mapping = ((0.25, 0.0),
         (0.25, 1.0),
         (0.75, 1.0),
         (0.75, 0.0))
        grenadeIcon.colour = (255, 255, 255, 255)
        grenadeIcon.materialFX = 'BLEND'
        self.component.munitions.addChild(grenadeIcon, 'grenades')
        grenadeLabel = GUI.Text('')
        grenadeLabel.verticalPositionMode = grenadeLabel.horizontalPositionMode = 'CLIP'
        grenadeLabel.horizontalAnchor = 'CENTER'
        grenadeLabel.verticalAnchor = 'BOTTOM'
        grenadeLabel.font = 'ruRU_calibri_default.font'
        grenadeLabel.colour = (255, 65, 65, 255)
        grenadeLabel.position = (0.5, -1.0 + soGUI.getPixelHeight(self.component.munitions) * 2, 0.0)
        self.component.munitions.addChild(grenadeLabel, 'grLabel')

    def updateWeaponData(self, newVal):
        self.component.munitions.shells.textureName = newVal['munitionIcon']
        m = str(newVal['currMunition']) + '/' + str(newVal['maxMunition'])
        self.component.munitions.shLabel.text = m
        self.component.munitions.grenades.textureName = newVal['grenadeIcon']
        self.component.munitions.grLabel.text = str(newVal['grenadeQuantity'])
        if self.component.munitions.grLabel.text == '0':
            self.component.munitions.grLabel.text = ''

    def updateActionBar(self, newVal):
        self.component.actionBar.script.setItems(newVal)

    def switchToSnipe(self, action = True, tex = None):
        self.component.crosshair.visible = not action
        self.component.snipeCrosshair.visible = action
        if tex:
            self.component.snipeCrosshair.textureName = tex


class soLogin_toplevel(soScreen, Listener.Listenable):
    factoryString = 'soGUI.soLogin_toplevel'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        BWPersonality.gpd.guiScreen = self
        self.miscFrame = None
        self.optionsBtn = None
        self.creditsBtn = None
        self.setupMiscFrame()
        self.setupOptions()
        self.setupCredits()
        self.setupHyperLinks()
        return

    def setupRoot(self):
        pass

    def setupMiscFrame(self):
        if self.miscFrame is None:
            self.miscFrame = GUI.Window()
        self.miscFrame.horizontalPositionMode = self.miscFrame.verticalPositionMode = 'CLIP'
        self.miscFrame.widthMode = self.miscFrame.heightMode = 'CLIP'
        self.miscFrame.horizontalAnchor = 'RIGHT'
        self.miscFrame.verticalAnchor = 'BOTTOM'
        self.miscFrame.materialFX = 'BLEND'
        self.miscFrame.colour = (255, 255, 255, 255)
        self.miscFrame.textureName = ''
        self.miscFrame.visible = True
        self.miscFrame.width = soGUI.getPixelWidth(self.component) * 150
        self.miscFrame.height = soGUI.getPixelHeight(self.component) * 200
        self.miscFrame.position = (1.0, -1.0, 0.0)
        frameCmp = GUI.Frame2('soGUI/maps/con_frame.tga')
        frameCmp.horizontalPositionMode = frameCmp.verticalPositionMode = 'CLIP'
        frameCmp.widthMode = frameCmp.heightMode = 'CLIP'
        frameCmp.horizontalAnchor = 'CENTER'
        frameCmp.verticalAnchor = 'CENTER'
        frameCmp.colour = (255, 255, 255, 255)
        frameCmp.materialFX = 'BLEND'
        frameCmp.width = 2.0
        frameCmp.height = 2.0
        frameCmp.position = (0.0, 0.0, 0.5)
        self.miscFrame.addChild(frameCmp, 'frameCmp')
        if not hasattr(self.component, 'miscFrame'):
            self.component.addChild(self.miscFrame, 'miscFrame')
        return

    def setupOptions(self):
        if self.optionsBtn is None:
            self.optionsBtn = soButton(GUI.Window())
        self.optionsBtn.component.horizontalPositionMode = self.optionsBtn.component.verticalPositionMode = 'CLIP'
        self.optionsBtn.component.widthMode = self.optionsBtn.component.heightMode = 'CLIP'
        self.optionsBtn.component.horizontalAnchor = 'CENTER'
        self.optionsBtn.component.verticalAnchor = 'TOP'
        self.optionsBtn.component.materialFX = 'BLEND'
        self.optionsBtn.component.colour = (255, 255, 255, 255)
        self.optionsBtn.component.visible = True
        self.optionsBtn.component.width = soGUI.getPixelWidth(self.miscFrame) * 130
        self.optionsBtn.component.height = soGUI.getPixelHeight(self.miscFrame) * 25
        self.optionsBtn.component.position = (0.0, 1.0 - soGUI.getPixelWidth(self.miscFrame) * 5, 0.0)
        self.miscFrame.addChild(self.optionsBtn.component, 'optBtn')
        self.optionsBtn.initVSC('soGUI/visual_styles/defaultBtnLarge.xml')
        self.optionsBtn.onBound()
        if hasattr(self.optionsBtn.component, 'label'):
            self.optionsBtn.component.label.font = 'ruRU_calibri_default.font'
            self.optionsBtn.component.label.text = lc('soScreen.soGUI.STRING_694_42')
        return

    def setupCredits(self):
        if self.creditsBtn is None:
            self.creditsBtn = soButton(GUI.Window())
        self.creditsBtn.component.horizontalPositionMode = self.creditsBtn.component.verticalPositionMode = 'CLIP'
        self.creditsBtn.component.widthMode = self.creditsBtn.component.heightMode = 'CLIP'
        self.creditsBtn.component.horizontalAnchor = 'CENTER'
        self.creditsBtn.component.verticalAnchor = 'TOP'
        self.creditsBtn.component.colour = (255, 255, 255, 255)
        self.creditsBtn.component.visible = True
        self.creditsBtn.component.materialFX = 'BLEND'
        self.creditsBtn.component.width = soGUI.getPixelWidth(self.miscFrame) * 130
        self.creditsBtn.component.height = soGUI.getPixelHeight(self.miscFrame) * 25
        self.creditsBtn.component.position = (0.0, 1.0 - soGUI.getPixelWidth(self.miscFrame) * 35, 0.0)
        self.miscFrame.addChild(self.creditsBtn.component, 'creditsBtn')
        self.creditsBtn.initVSC('soGUI/visual_styles/defaultBtnLarge.xml')
        self.creditsBtn.onBound()
        if hasattr(self.creditsBtn.component, 'label'):
            self.creditsBtn.component.label.font = 'ruRU_calibri_default.font'
            self.creditsBtn.component.label.text = lc('soScreen.soGUI.STRING_718_42')
        return

    def setupHyperLinks(self):
        pass

    @PyGUIEvent('loginFrame.quitBtn', 'onClick')
    def quitBtnClicked(self):
        BigWorld.playSound('ui/boop')
        BWPersonality.closeGame()

    @PyGUIEvent('miscFrame.optBtn', 'onClick')
    def optsBtnClicked(self):
        GUI.addRoot(BWPersonality.gpd.optsGUI.component)
        BWPersonality.gpd.optsGUI.component.visible = True

    def hide(self):
        self.component.visible = False


class soCharacterCreationScreen(soScreen, Listener.Listenable):
    factoryString = 'soGUI.soCharacterCreationScreen'

    def __init__(self, component):
        soScreen.__init__(self, component)
        Listener.Listenable.__init__(self)
        component.script = self
        self.editField = None
        self.setupRoot()
        self.setupFrame()
        self.setupNameInput()
        self.setupOkCancel()
        return

    def setupRoot(self):
        self.component.verticalPositionMode = self.component.horizontalPositionMode = 'LEGACY'
        self.component.widthMode = self.component.heightMode = 'CLIP'
        self.component.width = 2.0
        self.component.height = 2.0
        self.component.colour = (255, 255, 255, 255)
        self.component.position = (0.0, 0.0, 0.0)
        self.component.materialFX = 'BLEND'

    def setupFrame(self):

        def setupFrameHolder():
            wnd = GUI.Window()
            wnd.verticalPositionMode = wnd.horizontalPositionMode = 'CLIP'
            wnd.widthMode = wnd.heightMode = 'PIXEL'
            wnd.verticalAnchor = 'CENTER'
            wnd.horizontalAnchor = 'CENTER'
            wnd.width = 230
            wnd.height = 150
            wnd.textureName = ''
            wnd.position = (0.0, 0.0, 0.0)
            self.component.addChild(wnd, 'frame')

        def setupFrameTexture():
            frame = GUI.Frame2('soGUI/maps/Controls/window_frame/genericWindowFrame.tga')
            frame.verticalPositionMode = frame.horizontalPositionMode = 'CLIP'
            frame.widthMode = frame.heightMode = 'CLIP'
            frame.verticalAnchor = 'CENTER'
            frame.horizontalAnchor = 'CENTER'
            frame.width = 2.0
            frame.height = 2.0
            frame.position = (0.0, 0.0, 0.1)
            frame.colour = (255, 255, 255, 255)
            frame.materialFX = 'BLEND'
            self.component.frame.addChild(frame, 'border')

        def setupLabel():
            label = GUI.Text('')
            label.verticalPositionMode = label.horizontalPositionMode = 'CLIP'
            label.horizontalAnchor = 'LEFT'
            label.verticalAnchor = 'TOP'
            label.font = 'ruRU_calibri_default.font'
            label.colour = (255, 255, 255, 255)
            label.text = lc('soScreen.soGUI.STRING_801_16')
            label.position = (-1.0 + soGUI.getPixelWidth(self.component.frame) * 3, 1.0 - soGUI.getPixelHeight(self.component.frame) * 3, 0.0)
            self.component.frame.addChild(label, 'label')

        setupFrameHolder()
        setupFrameTexture()
        setupLabel()

    def setupNameInput(self):
        self.editField = soEditField(GUI.Window())
        self.editField.component.position = (0.0, 0.0, 0.0)
        self.editField.component.verticalAnchor = 'CENTER'
        self.editField.component.horizontalAnchor = 'CENTER'
        self.editField.component.horizontalPositionMode = 'CLIP'
        self.editField.component.verticalPositionMode = 'CLIP'
        self.editField.component.widthMode = 'PIXEL'
        self.editField.component.heightMode = 'PIXEL'
        self.editField.component.width = 200
        self.editField.maxWidth = 180
        self.editField.component.height = 30
        self.editField.component.edit.font = 'ruRU_calibri_default.font'
        self.editField.CHARS_TO_IGNORE = [u'\r',
         u'\x08',
         u'\x1b',
         u'\t']
        self.editField.onBound()
        self.component.frame.addChild(self.editField.component, 'edit')
        self.editField.component.focus = True
        self.editField.maxLength = 32

    def setupOkCancel(self):
        okBtn = soButton(GUI.Window())
        okcmp = okBtn.component
        okcmp.verticalPositionMode = okcmp.horizontalPositionMode = 'CLIP'
        okcmp.widthMode = okcmp.heightMode = 'PIXEL'
        okcmp.horizontalAnchor = 'CENTER'
        okcmp.verticalAnchor = 'BOTTOM'
        okcmp.width = 70
        okcmp.height = 30
        okcmp.position = (-0.5, -1.0 + soGUI.getPixelHeight(self.component.frame) * 3, 0.0)
        self.component.frame.addChild(okcmp, 'okBtn')
        okBtn.initVSC('soGUI/visual_styles/defaultBtnSmall.xml')
        okBtn.onBound()
        okBtn.setVisualState('normal')
        okcmp.label.text = 'Ok'
        cancelBtn = soButton(GUI.Window())
        cancelcmp = cancelBtn.component
        cancelcmp.verticalPositionMode = cancelcmp.horizontalPositionMode = 'CLIP'
        cancelcmp.widthMode = cancelcmp.heightMode = 'PIXEL'
        cancelcmp.horizontalAnchor = 'CENTER'
        cancelcmp.verticalAnchor = 'BOTTOM'
        cancelcmp.width = 70
        cancelcmp.height = 30
        cancelcmp.position = (0.5, -1.0 + soGUI.getPixelHeight(self.component.frame) * 3, 0.0)
        self.component.frame.addChild(cancelcmp, 'cancelBtn')
        cancelBtn.initVSC('soGUI/visual_styles/defaultBtnSmall.xml')
        cancelBtn.onBound()
        cancelBtn.setVisualState('normal')
        cancelcmp.label.text = lc('soScreen.soGUI.STRING_874_25')

    @PyGUIEvent('frame.okBtn', 'onClick')
    def onOk(self):
        self.listeners.characterCreationEvent(self.editField.value())

    @PyGUIEvent('frame.cancelBtn', 'onClick')
    def onCancel(self):
        self.editField.empty(True)


class soOptions(soScreen):
    factoryString = 'soGUI.soOptions'
    TAB_GRAPHICS = 0
    TAB_SOUNDS = 1
    TAB_CONTROLS = 2

    def __init__(self, component):
        soScreen.__init__(self, component)
        component.script = self
        self.graphicsBtn = None
        self.currTab = soOptions.TAB_GRAPHICS
        self.graphPresets = None
        self.graphFrame = None
        self.setupRoot()
        self.setupMainFrame()
        self.setupGraphicsPresets()
        self.setupGraphicsOpts()
        self.setupOkCancelApply()
        self.onBound()
        return

    def setupGraphicsPresets(self):
        if self.graphPresets is None:
            self.graphPresets = GraphicsPresets.GraphicsPresets()
        return

    def setupRoot(self):
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.width = 504
        self.component.height = 400
        self.horizontalAnchor = 'CENTER'
        self.verticalAnchor = 'CENTER'
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'LEGACY'
        self.component.position = (0.0, 0.0, 0.2)
        self.component.colour = (255, 255, 255, 255)
        self.component.materialFX = 'BLEND'
        self.component.textureName = ''
        self.component.focus = True
        self.component.crossFocus = True
        self.component.moveFocus = True

    def setupMainFrame(self):
        frameComp = GUI.Frame2('soGUI/maps/con_frame.tga')
        frameComp.horizontalPositionMode = frameComp.verticalPositionMode = 'CLIP'
        frameComp.widthMode = frameComp.heightMode = 'CLIP'
        frameComp.horizontalAnchor = 'LEFT'
        frameComp.verticalAnchor = 'TOP'
        frameComp.colour = (255, 255, 255, 255)
        frameComp.materialFX = 'BLEND'
        frameComp.width = 2.0
        frameComp.height = 2.0
        frameComp.position = (-1.0, 1.0, 0.5)
        self.component.addChild(frameComp, 'frameCmp')

    def setupGraphicsOpts(self):
        GRAPH_FRAME_WIDTH = 500
        GRAPH_FRAME_HEIGHT = 340
        GRAPH_FRAME_CAPTIONH = 25
        GRAPH_RESOLUTION_CAPTIONH = 20
        GRAPH_DETAIL_CAPTIONH = 20
        if self.graphFrame is None:
            self.graphFrame = GUI.Window()
        self.graphFrame.textureName = ''
        self.graphFrame.horizontalPositionMode = self.graphFrame.verticalPositionMode = 'CLIP'
        self.graphFrame.widthMode = self.graphFrame.heightMode = 'PIXEL'
        self.graphFrame.horizontalAnchor = 'LEFT'
        self.graphFrame.verticalAnchor = 'TOP'
        self.graphFrame.colour = (255, 255, 255, 255)
        self.graphFrame.materialFX = 'BLEND'
        self.graphFrame.width = GRAPH_FRAME_WIDTH
        self.graphFrame.height = GRAPH_FRAME_HEIGHT
        self.graphFrame.position = (-1.0 + soGUI.getPixelWidth(self.component) * 2, 1.0, 0.0)
        frameBorder = GUI.Frame2('soGUI/maps/con_frame.tga')
        frameBorder.verticalPositionMode = frameBorder.horizontalPositionMode = 'CLIP'
        frameBorder.widthMode = frameBorder.heightMode = 'CLIP'
        frameBorder.horizontalAnchor = 'LEFT'
        frameBorder.verticalAnchor = 'TOP'
        frameBorder.tiled = True
        frameBorder.tileHeight = 32
        frameBorder.tileWidth = 32
        frameBorder.colour = (255, 255, 255, 255)
        frameBorder.materialFX = 'BLEND'
        frameBorder.width = soGUI.getPixelWidth(self.graphFrame) * GRAPH_FRAME_WIDTH
        frameBorder.height = soGUI.getPixelHeight(self.graphFrame) * (GRAPH_FRAME_HEIGHT - GRAPH_FRAME_CAPTIONH)
        frameBorder.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.graphFrame) * GRAPH_FRAME_CAPTIONH, 0.3)
        self.graphFrame.addChild(frameBorder, 'frameBorder')
        label = GUI.Text(lc('soScreen.soGUI.STRING_987_19'))
        label.horizontalPositionMode = label.verticalPositionMode = 'CLIP'
        label.horizontalAnchor = 'LEFT'
        label.verticalAnchor = 'TOP'
        label.font = 'ruRU_calibri_default.font'
        label.colour = (255, 255, 255, 255)
        label.materialFX = 'BLEND'
        label.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 2, 1.0 - soGUI.getPixelHeight(self.graphFrame) * 2, 0.0)
        self.graphFrame.addChild(label, 'label')
        self.component.addChild(self.graphFrame, 'graphFrame')

        def setupResolutionList():
            resLabel = GUI.Text(lc('soScreen.soGUI.STRING_1003_23'))
            resLabel.horizontalPositionMode = resLabel.verticalPositionMode = 'CLIP'
            resLabel.horizontalAnchor = 'LEFT'
            resLabel.verticalAnchor = 'TOP'
            resLabel.font = 'ruRU_calibri_default.font'
            resLabel.colour = (255, 255, 255, 255)
            resLabel.materialFX = 'BLEND'
            resLabel.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 2, 1.0 - soGUI.getPixelHeight(self.graphFrame) * (2 + GRAPH_FRAME_CAPTIONH + 5), 0.0)
            self.graphFrame.addChild(resLabel, 'resLabel')
            resolutionCmp = GUI.Window()
            resolutionCmp.verticalPositionMode = resolutionCmp.horizontalPositionMode = 'CLIP'
            resolutionCmp.widthMode = resolutionCmp.heightMode = 'PIXEL'
            resolutionCmp.horizontalAnchor = 'LEFT'
            resolutionCmp.verticalAnchor = 'TOP'
            resolutionCmp.colour = (255, 255, 255, 255)
            resolutionCmp.materialFX = 'BLEND'
            resolutionCmp.visible = True
            resolutionCmp.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 5, self.graphFrame.resLabel.position.y - soGUI.getPixelHeight(self.graphFrame) * (GRAPH_RESOLUTION_CAPTIONH + 5), 0.0)
            resolutionCmp.width = GRAPH_FRAME_WIDTH - 10
            resDDL = soDropDownList(resolutionCmp, soGUI.DropDownListPropsStructure(DDLWidth=GRAPH_FRAME_WIDTH - 10, DDLHeight=250))
            resDDL.onBound()
            for entry in BigWorld.listVideoModes():
                resDDL.addElement(entry[4])

            self.graphFrame.addChild(resDDL.component, 'resolutionDDL')
            resDDL.setSelection(str(int(BigWorld.screenWidth())) + 'x' + str(int(BigWorld.screenHeight())))

        def setupFScheckBox():
            checkComp = GUI.Window()
            checkComp.horizontalPositionMode = checkComp.verticalPositionMode = 'CLIP'
            checkComp.widthMode = checkComp.heightMode = 'PIXEL'
            checkComp.horizontalAnchor = 'LEFT'
            checkComp.verticalAnchor = 'TOP'
            checkComp.colour = (255, 255, 255, 255)
            checkComp.materialFX = 'BLEND'
            checkComp.visible = True
            checkComp.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 5, self.graphFrame.resolutionDDL.position.y - soGUI.getPixelHeight(self.graphFrame) * (self.graphFrame.resolutionDDL.selectionView.height + 5), 0.0001)
            FScheckBox = soCheckBox(checkComp, soGUI.CheckBoxPropsStructure(labelText=lc('soScreen.soGUI.STRING_1047_79')))
            self.graphFrame.addChild(FScheckBox.component, 'FScheckBox')
            FScheckBox.onBound()
            if BigWorld.isVideoWindowed():
                FScheckBox.box.buttonActive = True
                FScheckBox.setVisualState('active')
            else:
                FScheckBox.box.buttonActive = False
                FScheckBox.setVisualState('normal')

        def setupMusicCheckBox():
            checkComp = GUI.Window()
            checkComp.horizontalPositionMode = checkComp.verticalPositionMode = 'CLIP'
            checkComp.widthMode = checkComp.heightMode = 'PIXEL'
            checkComp.horizontalAnchor = 'LEFT'
            checkComp.verticalAnchor = 'TOP'
            checkComp.colour = (255, 255, 255, 255)
            checkComp.materialFX = 'BLEND'
            checkComp.visible = True
            checkComp.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 5, self.graphFrame.resolutionDDL.position.y - soGUI.getPixelHeight(self.graphFrame) * (self.graphFrame.resolutionDDL.selectionView.height + 95), 0.0001)
            musicCheckBox = soCheckBox(checkComp, soGUI.CheckBoxPropsStructure(labelText=lc('soScreen.soGUI.STRING_1072_82')))
            self.graphFrame.addChild(musicCheckBox.component, 'musicCheckBox')
            musicCheckBox.onBound()

        def setupDetailList():
            detailLabel = GUI.Text(lc('soScreen.soGUI.STRING_1085_26'))
            detailLabel.horizontalPositionMode = detailLabel.verticalPositionMode = 'CLIP'
            detailLabel.horizontalAnchor = 'LEFT'
            detailLabel.verticalAnchor = 'TOP'
            detailLabel.font = 'ruRU_calibri_default.font'
            detailLabel.colour = (255, 255, 255, 255)
            detailLabel.materialFX = 'BLEND'
            detailLabel.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 2, self.graphFrame.FScheckBox.position.y - soGUI.getPixelHeight(self.graphFrame) * (self.graphFrame.FScheckBox.height + 5), 0.01)
            self.graphFrame.addChild(detailLabel, 'detailLabel')
            detailCmp = GUI.Window()
            detailCmp.verticalPositionMode = detailCmp.horizontalPositionMode = 'CLIP'
            detailCmp.widthMode = detailCmp.heightMode = 'PIXEL'
            detailCmp.horizontalAnchor = 'LEFT'
            detailCmp.verticalAnchor = 'TOP'
            detailCmp.colour = (255, 255, 255, 255)
            detailCmp.materialFX = 'BLEND'
            detailCmp.visible = True
            detailCmp.position = (-1.0 + soGUI.getPixelWidth(self.graphFrame) * 5, self.graphFrame.detailLabel.position.y - soGUI.getPixelHeight(self.graphFrame) * (GRAPH_DETAIL_CAPTIONH + 5), 0.01)
            detailCmp.width = GRAPH_FRAME_WIDTH - 10
            detailDDL = soDropDownList(detailCmp, soGUI.DropDownListPropsStructure(DDLWidth=GRAPH_FRAME_WIDTH - 10, DDLHeight=150))
            detailDDL.onBound()
            for entry in self.graphPresets.entries:
                detailDDL.addElement(entry)

            self.graphFrame.addChild(detailDDL.component, 'detailDDL')
            detailDDL.setSelection(self.graphPresets.entryNames[self.graphPresets.selectedOption])

        setupResolutionList()
        setupFScheckBox()
        setupMusicCheckBox()
        setupDetailList()
        GUI.reSort()
        return

    def setupOkCancelApply(self):
        okBtn = soButton(GUI.Window())
        cancelBtn = soButton(GUI.Window())
        applyBtn = soButton(GUI.Window())
        okBtn.component.verticalPositionMode = okBtn.component.horizontalPositionMode = 'CLIP'
        okBtn.component.widthMode = okBtn.component.heightMode = 'PIXEL'
        okBtn.component.horizontalAnchor = 'LEFT'
        okBtn.component.verticalAnchor = 'BOTTOM'
        okBtn.component.colour = (255, 255, 255, 255)
        okBtn.component.materialFX = 'BLEND'
        okBtn.component.width = soGUI.OPTS_GUI_BTN_WIDTH
        okBtn.component.height = soGUI.OPTS_GUI_BTN_HEIGHT
        okBtn.component.position = (-1.0 + soGUI.getPixelWidth(self.component) * 5, -1.0 + soGUI.getPixelHeight(self.component) * 5, 0.0)
        okBtn.initVSC('soGUI/visual_styles/defaultBtnLarge.xml')
        okBtn.setVisualState('normal')
        okBtn.onBound()
        okBtn.component.label.text = 'Ok'
        self.component.addChild(okBtn.component, 'okBtn')
        cancelBtn.component.verticalPositionMode = cancelBtn.component.horizontalPositionMode = 'CLIP'
        cancelBtn.component.widthMode = cancelBtn.component.heightMode = 'PIXEL'
        cancelBtn.component.horizontalAnchor = 'CENTER'
        cancelBtn.component.verticalAnchor = 'BOTTOM'
        cancelBtn.component.colour = (255, 255, 255, 255)
        cancelBtn.component.materialFX = 'BLEND'
        cancelBtn.component.width = soGUI.OPTS_GUI_BTN_WIDTH
        cancelBtn.component.height = soGUI.OPTS_GUI_BTN_HEIGHT
        cancelBtn.component.position = (0.0, -1.0 + soGUI.getPixelHeight(self.component) * 5, 0.0)
        cancelBtn.initVSC('soGUI/visual_styles/defaultBtnLarge.xml')
        cancelBtn.setVisualState('normal')
        cancelBtn.onBound()
        cancelBtn.component.label.text = lc('soScreen.soGUI.STRING_1164_35')
        self.component.addChild(cancelBtn.component, 'cancelBtn')
        applyBtn.component.verticalPositionMode = applyBtn.component.horizontalPositionMode = 'CLIP'
        applyBtn.component.widthMode = applyBtn.component.heightMode = 'PIXEL'
        applyBtn.component.horizontalAnchor = 'RIGHT'
        applyBtn.component.verticalAnchor = 'BOTTOM'
        applyBtn.component.colour = (255, 255, 255, 255)
        applyBtn.component.materialFX = 'BLEND'
        applyBtn.component.width = soGUI.OPTS_GUI_BTN_WIDTH
        applyBtn.component.height = soGUI.OPTS_GUI_BTN_HEIGHT
        applyBtn.component.position = (1.0 - soGUI.getPixelWidth(self.component) * 5, -1.0 + soGUI.getPixelHeight(self.component) * 5, 0.0)
        applyBtn.initVSC('soGUI/visual_styles/defaultBtnLarge.xml')
        applyBtn.setVisualState('normal')
        applyBtn.onBound()
        applyBtn.component.label.text = lc('soScreen.soGUI.STRING_1181_34')
        self.component.addChild(applyBtn.component, 'applyBtn')

    def applySettings(self):
        if not self.graphFrame.FScheckBox.script.box.buttonActive:
            videoModes = BigWorld.listVideoModes()
            for i in xrange(len(videoModes)):
                if videoModes[i][4] == self.graphFrame.resolutionDDL.script.getSelection():
                    BigWorld.changeVideoMode(videoModes[i][0], False)

        else:
            if not BigWorld.isVideoWindowed():
                BigWorld.changeVideoMode(1, True)
            w = self.graphFrame.resolutionDDL.script.getSelection().split('x')[0]
            h = self.graphFrame.resolutionDDL.script.getSelection().split('x')[1]
            BigWorld.resizeWindow(int(w), int(h))
        if not self.graphPresets.entryNames[self.graphPresets.selectedOption] == self.graphFrame.detailDDL.script.getSelection():
            for i in xrange(len(self.graphPresets.entryNames)):
                if self.graphPresets.entryNames[i] == self.graphFrame.detailDDL.script.getSelection():
                    self.graphPresets.selectGraphicsOptions(i)

        if not self.graphFrame.musicCheckBox.script.box.buttonActive:
            BWPersonality.GUICore.soundOptsEvent(0, False)
        else:
            BWPersonality.GUICore.soundOptsEvent(0, True)
        BigWorld.savePreferences()

    def handleMouseButtonEvent(self, comp, event):
        return True

    def closeOptions(self):
        GUI.delRoot(self.component)
        BWPersonality.GUICore.checkAllTopmostComponents()

    @PyGUIEvent('okBtn', 'onClick')
    def onOk(self):
        self.applySettings()
        self.closeOptions()

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancel(self):
        self.closeOptions()

    @PyGUIEvent('applyBtn', 'onClick')
    def onApply(self):
        self.applySettings()