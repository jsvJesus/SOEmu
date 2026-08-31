# Embedded file name: scripts/client/__debug/gui/Button.py
import numbers
from BWPersonality import GUICore
from __debug.gui.Widget import Widget

class Button(Widget):
    last_btn_id = -1

    def __init__(self, text, x = 0, y = 0, w = None, h = 21, hAnchor = 'LEFT', vAnchor = 'TOP', callback = lambda : None):
        Widget.__init__(self, x, y)
        Button.last_btn_id += 1
        self.id = Button.last_btn_id
        self.adjust_width = w is None
        self.is_visible = True
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.hAnchor, self.vAnchor = hAnchor, vAnchor
        self.callback = callback
        self.set_text(text)
        self.reinit()
        return

    def reinit(self):
        self.is_visible = True
        GUICore.setDebugBtn(id=self.id, text=self.text, x=self.x, y=self.y, w=self.width, h=self.height, hAnchor=self.hAnchor, vAnchor=self.vAnchor, callBack=self.callback)

    def destroy(self):
        self.is_visible = False
        GUICore.delDebugBtn(self.id)

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
        if self.adjust_width:
            self.width = len(text) * 7.5 + 13
        if self.is_visible:
            self.reinit()

    text = property(get_text, set_text)


class Menu(Widget):
    dx, dy = (5, 5)

    def __init__(self, x = 0, y = 0, text = 'X'):
        self.x = x
        self.y = y
        self.is_visible = True
        self.is_opened = True
        self.children = []
        self.open_btn = Button(text, self.x, self.y, callback=self.open_btn_click)
        self.width = self.open_btn.width
        self.height = self.open_btn.height
        self.next_x = self.x + self.open_btn.width + self.dx
        self.next_y = self.y

    def add_widget(self, widget):
        self.children.append(widget)
        widget.set_visible(self.is_opened)
        self.set_x(self.x)
        self.set_y(self.y)

    def set_visible(self, visible):
        if self.is_visible != visible:
            self.is_visible = visible
            self.open_btn.set_visible(self.is_visible)
            if self.is_visible and self.is_opened:
                for child in self.children:
                    child.set_visible(True)

            elif not self.is_visible:
                for child in self.children:
                    child.set_visible(False)

    def set_opened(self, is_opened):
        if self.is_opened != is_opened:
            self.is_opened = is_opened
            if self.is_opened and self.is_visible:
                for child in self.children:
                    child.set_visible(True)

            elif not self.is_opened:
                for child in self.children:
                    child.set_visible(False)

    def set_x(self, x):
        self.x = x
        self.open_btn.set_x(self.x)
        self.next_x = self.x + self.open_btn.width + self.dx
        for child in self.children:
            child.set_x(self.next_x)

    def set_y(self, y):
        self.y = y
        self.open_btn.set_y(self.y)
        self.next_y = self.y
        for child in self.children:
            child.set_y(self.next_y)
            self.next_y += child.height + self.dy

        if self.children:
            self.height = child.y + child.height - self.y

    def open_btn_click(self):
        self.set_opened(not self.is_opened)