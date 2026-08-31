# Embedded file name: scripts/client/__debug/gui/__init__.py
import os
from functools import partial
from pprint import pprint
import BigWorld
from Settings import Settings
from __debug.gui.Button import Button, Menu
from __debug.gui.Label import Label

def create_widget(data):
    type_name = data[0]
    if type_name == 'Button':
        text, func = data[1:]
        return Button(text, callback=func)
    if type_name == 'Label':
        func, dt = data[1:]
        label = Label('')

        def set_text():
            label.set_text(func())
            BigWorld.callback(dt, set_text)

        BigWorld.callback(dt, set_text)
        return label


settings = Settings()
debug_gui_path = settings.getSetting('debugGui')
if debug_gui_path is not None:
    try:
        exec 'from __debug.gui.configs import ' + debug_gui_path + ' as debug_gui'
    except ImportError:
        print "Can't import debug gui module", debug_gui_path
    else:
        try:
            gui_settings = debug_gui.settings
        except AttributeError:
            gui_settings = {}

        title = gui_settings.get('title', 'debug')
        x = gui_settings.get('x', 10)
        y = gui_settings.get('y', 100)
        root = Menu(x, y, text=title)
        for widget_data in debug_gui.gui:
            widget = create_widget(widget_data)
            root.add_widget(widget)

        root.set_opened(gui_settings.get('opened', False))