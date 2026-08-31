# Embedded file name: scripts/client/msgbox_templates.py
from Localization import lc
import BWPersonality
from gui_const import MESSAGEBOX

def text_and_ok(id, title, text, callback = lambda event, data: None):
    BWPersonality.GUICore.showMsgBox(id, isModal=False, x=0.0, y=0.0, width=600, caption=title, forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_OK,
      'width': 80}], timeout=-1, closeBox=True, defaultAction=MESSAGEBOX.BTN_OK, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
      'ID': 'main_txt_field',
      'text': text,
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER,
      'autosize': False,
      'height': 500}], callback=callback)
    return


def ask_yes_no(id, title, text, callback = lambda event, data: None, isSystem = False):
    BWPersonality.GUICore.showMsgBox(id, isModal=False, x=0.0, y=0.0, width=300, caption=title, forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_YES,
      'width': 80}, {'type': MESSAGEBOX.BTN_NO,
      'width': 80}], timeout=-1, closeBox=True, defaultAction=MESSAGEBOX.BTN_YES, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
      'ID': 'main_txt_field',
      'text': text,
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=callback, isSystem=isSystem)
    return


def input_box_ok_cancel(id, title, text, callback = lambda event, data: None, default = None, input_validator = lambda newStr, wholeText, offset: True):
    BWPersonality.GUICore.showMsgBox(id, isModal=False, x=0.0, y=0.0, width=300, caption=title, forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_OK,
      'width': 80}, {'type': MESSAGEBOX.BTN_CANCEL,
      'width': 80}], timeout=-1, closeBox=True, defaultAction=MESSAGEBOX.BTN_YES, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
      'ID': 'main_txt_field',
      'text': text,
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER}, {'type': MESSAGEBOX.ADDCONTROL_EDIT,
      'ID': 'edit_box',
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER,
      'active': True,
      'default': default,
      'input_validator': input_validator}], callback=callback)
    return


def clan_invite(inviter, clan, callback = lambda event, data: None):
    BWPersonality.GUICore.showMsgBox(id='clan_invite', isModal=False, x=0.0, y=0.0, width=300, caption=lc('msgbox_templates.INVITE_TITTLE').format(inviter), forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_YES,
      'width': 80}, {'type': MESSAGEBOX.BTN_NO,
      'width': 80}], timeout=10, closeBox=True, defaultAction=MESSAGEBOX.BTN_NO, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
      'ID': 'main_txt_field',
      'text': lc('msgbox_templates.INVITE_QUESTION').format(inviter, clan),
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=callback)
    return


def text_and_ok_timeout(id, title, text, timeout, callback = lambda event, data: None):
    BWPersonality.GUICore.showMsgBox(id, isModal=False, x=0.0, y=0.0, width=300, caption=title, forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_OK,
      'width': 80}], timeout=timeout, closeBox=True, defaultAction=MESSAGEBOX.BTN_OK, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
      'ID': 'main_txt_field',
      'text': text,
      'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=callback)
    return