# Embedded file name: scripts/client/Helpers/PyGUI/__init__.py
from PyGUIBase import PyGUIBase
from Button import Button, ButtonVisualState
from CheckBox import CheckBox
from RadioButton import RadioButton
from EditField import EditField
from Grid import Grid
from Slider import Slider, SliderThumb, SliderVisualState
from ScrollingList import ScrollingList
from ScrollWindow import ScrollWindow
from SmoothMover import SmoothMover
from TextField import TextField
from ToolTip import ToolTip
from ToolTip import ToolTipInfo
from ToolTip import ToolTipManager
from Window import Window
from Window import DraggableWindow
from Window import EscapableWindow
from Console import Console
import EditUtils
import Test
import TextStyles
import Utils
import VisualStateComponent
from Helpers.videoFeeds import s_videoFeeds
from Helpers.videoFeeds import VideoFeed
from Helpers.ProgressBar import IProgressBar
from Helpers.ProgressBar import ProgressBar
from Helpers.ProgressBar import ChunkLoadingProgressBar
from Helpers.ProgressBar import TeleportProgressBar

def handleKeyEvent(event):
    key = event.key
    mods = event.modifiers
    down = event.isKeyDown()
    import DraggableComponent
    return DraggableComponent.dragManager.handleKeyEvent(down, key, mods)


def handleMouseEvent(event):
    dx = event.dx
    dy = event.dy
    dz = event.dz
    position = event.cursorPosition
    import DraggableComponent
    return DraggableComponent.dragManager.handleMouseEvent(event)


def PyGUIEvent(componentName, eventName, *args, **kargs):
    """
            @PyGUIEvent decorator.
            
            Note: If you override a function that is marked with this decorator
            in the base class, the derived class function is not required to be
            decorated. If you do decorate both, the event handler will be called
            twice.
    """
    from functools import partial

    def addEvent(componentName, eventName, args, kargs, eventFunction):
        if not hasattr(eventFunction, '_PyGUIEventHandler'):
            eventFunction._PyGUIEventHandler = []
        eventFunction._PyGUIEventHandler += [(componentName,
          eventName,
          args,
          kargs)]
        return eventFunction

    return partial(addEvent, componentName, eventName, args, kargs)