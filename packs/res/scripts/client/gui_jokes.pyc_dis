# Embedded file name: scripts/client/gui_jokes.py
"""
Created on 01.03.2011

@author: muzhig
"""
import BWPersonality
import BigWorld
from gui_const import MESSAGEBOX
from soGUI.soDialogueBox import soDlgBoxPropsStructure, soDialogueBox

class GuiHandler(object):
    NEXT_ID = 0
    ACTIVE_GUI_HANDLERS = {}
    OK, CANCEL, YES, NO, APPLY = (soDialogueBox.BTN_OK,
     soDialogueBox.BTN_CANCEL,
     soDialogueBox.BTN_YES,
     soDialogueBox.BTN_NO,
     soDialogueBox.BTN_APPLY)
    CLOSED = -1

    def __init__(self, props = None, callback = None):
        self.ID = 'gui_jokes_%s_%s' % (self.__class__.__name__, self.NEXT_ID)
        GuiHandler.NEXT_ID += 1
        if callback:
            self.callback = callback
            self.registerListener()
        self.props = props
        BWPersonality.GUICore.showMessageBox(self.ID, props)

    def registerListener(self):
        if not GuiHandler.ACTIVE_GUI_HANDLERS.has_key(self.ID):
            BWPersonality.GUICore.addListener('dlgBoxEvent', self.onDlgBoxEvent)
            GuiHandler.ACTIVE_GUI_HANDLERS[self.ID] = self

    def unregisterListener(self):
        BWPersonality.GUICore.removeListener('dlgBoxEvent', self.onDlgBoxEvent)
        if GuiHandler.ACTIVE_GUI_HANDLERS.has_key(self.ID):
            del GuiHandler.ACTIVE_GUI_HANDLERS[self.ID]

    def onDlgBoxEvent(self, event, data):
        id = data[0]
        if id == self.ID:
            self.unregisterListener()
            self.processEventData(event, data)

    def processEventData(self, event, data):
        pass


def inputBox(title, subtitle = u'', callback = None, id = None, isModal = False):

    def handler(event, data):
        if event == MESSAGEBOX.EVENT_BTNPRESS and data['btn'] == MESSAGEBOX.BTN_OK:
            text = data['add_controls']['edit_box']
            if text:
                callback(text)

    BWPersonality.GUICore.showMsgBox(id or 'inputBox.default', isModal=isModal, x=0.0, y=0.0, width=300, caption=title, forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_OK,
      'width': 80}, {'type': MESSAGEBOX.BTN_CANCEL,
      'width': 80}], timeout=-1, closeBox=True, defaultAction=MESSAGEBOX.BTN_YES, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
      'ID': 'main_txt_field',
      'text': subtitle,
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER}, {'type': MESSAGEBOX.ADDCONTROL_EDIT,
      'ID': 'edit_box',
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=handler)
    return


class radioBox(GuiHandler):

    def __init__(self, title, subtitle = u'', boxes = [], callback = None):
        boxes_as_tuples = []
        for box in boxes:
            box.insert(0, 'radio')
            boxes_as_tuples.append(tuple(box))

        props = soDlgBoxPropsStructure(caption=title, msg=subtitle, modal=True, btnSet=[soDialogueBox.BTN_OK, soDialogueBox.BTN_CANCEL], additions=boxes_as_tuples)
        GuiHandler.__init__(self, props, callback)

    def processEventData(self, event, data):
        if event == soDialogueBox.EVENT_BTNPRESS:
            id, btn, adddata = data
            if btn == soDialogueBox.BTN_OK:
                for radio in adddata:
                    if radio[1]:
                        self.callback(radio[0])
                        return


class msgBox(GuiHandler):

    def __init__(self, title, subtitle = u'', large = False):
        if large:
            screen_size = BigWorld.screenSize()
            screen_size = [ size / 2 for size in screen_size ]
            props = soDlgBoxPropsStructure(width=screen_size[0], height=screen_size[1], caption=title, msg=subtitle, modal=True, btnSet=[soDialogueBox.BTN_OK])
        else:
            props = soDlgBoxPropsStructure(caption=title, msg=subtitle, modal=True, btnSet=[soDialogueBox.BTN_OK])
        GuiHandler.__init__(self, props, None)
        return


class askUser(GuiHandler):

    def __init__(self, title, subtitle = u'', callback = None, btn_set = None, default_btn = None, timeout_for_default = None):
        props = soDlgBoxPropsStructure(caption=title, msg=subtitle, modal=True, btnSet=btn_set)
        if callback and timeout_for_default and default_btn is not None:
            self.default_btn = default_btn
            self.setupTimeoutTimer(timeout_for_default)
        else:
            self.timeout_timer = None
        GuiHandler.__init__(self, props, callback)
        return

    def processEventData(self, event, data):
        if event in [soDialogueBox.EVENT_CLOSE, soDialogueBox.EVENT_BTNPRESS]:
            self.cancelTimeoutTimer()
            if event == soDialogueBox.EVENT_CLOSE:
                self.callback(askUser.CLOSED)
            elif event == soDialogueBox.EVENT_BTNPRESS:
                btn = data[1]
                self.callback(btn)

    def setupTimeoutTimer(self, t):
        self.cancelTimeoutTimer()
        self.timeout_timer = BigWorld.callback(t, self.onTimeEnd)

    def cancelTimeoutTimer(self):
        if hasattr(self, 'timeout_timer') and self.timeout_timer:
            BigWorld.cancelCallback(self.timeout_timer)
            self.timeout_timer = None
        return

    def onTimeEnd(self):
        self.timeout_timer = None
        BWPersonality.GUICore.removeListener('dlgBoxEvent', self.onDlgBoxEvent)
        BWPersonality.GUICore.closeMessageBox(self.ID)
        self.callback(self.default_btn)
        return


class askUserYesNo(askUser):

    def __init__(self, title, subtitle = u'', callback = None, default_btn = None, timeout_for_default = None):
        askUser.__init__(self, title, subtitle, callback, [soDialogueBox.BTN_YES, soDialogueBox.BTN_NO], default_btn, timeout_for_default)


class askUserYesNoDelayDeafultNo(askUserYesNo):

    def __init__(self, title, subtitle = u'', callback = None, timer = 60.0):
        askUserYesNo.__init__(self, title, subtitle, callback, askUserYesNo.NO, timer)


class askUserOk(askUser):

    def __init__(self, title, subtitle = u'', callback = None):
        askUser.__init__(self, title, subtitle, callback, [soDialogueBox.BTN_OK])

    def processEventData(self, event, data):
        askUser.processEventData(self, event, data)