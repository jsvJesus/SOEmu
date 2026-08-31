# Embedded file name: scripts/client/__debug/gui/Label.py
import numbers
from BWPersonality import GUICore
from __debug.gui.Widget import Widget

class Label(Widget):
    last_id = -1
    height = 21

    def __init__(self, text, x = 0, y = 0, hAnchor = 'LEFT', vAnchor = 'TOP'):
        Widget.__init__(self, x, y)
        Label.last_id += 1
        self.id = Label.last_id
        self.is_visible = True
        self.x, self.y = x, y
        self.hAnchor, self.vAnchor = hAnchor, vAnchor
        self.set_text(text)
        self.reinit()

    def reinit(self):
        self.is_visible = True
        GUICore.drawLabel(id=self.id, text=self.text, x=self.x, y=self.y, hAnchor=self.hAnchor, vAnchor=self.vAnchor)

    def destroy(self):
        self.is_visible = False
        GUICore.delLabel(self.id)

    def set_visible(self, visible):
        if visible and not self.is_visible:
            self.reinit()
        elif not visible and self.is_visible:
            self.destroy()

    def set_x(self, x):
        self.x = x
        self.reinit()

    def set_y(self, y):
        self.y = y
        self.reinit()

    def get_text(self):
        return self._text

    def set_text(self, text):
        if isinstance(text, numbers.Number):
            text = str(text)
        elif isinstance(text, bool):
            text = 'True' if text else 'False'
        self._text = text
        if self.is_visible:
            self.reinit()

    text = property(get_text, set_text)