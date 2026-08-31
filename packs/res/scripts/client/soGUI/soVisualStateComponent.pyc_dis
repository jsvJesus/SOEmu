# Embedded file name: scripts/client/soGUI/soVisualStateComponent.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import ResMgr
from bwdebug import ERROR_MSG
from Helpers.PyGUI.VisualStateComponent import VisualStateComponent, VisualState

class soVisualState(VisualState):
    pass


class soVisualStateComponent(VisualStateComponent):

    def initVSC(self, xmlPath):
        extName = xmlPath
        ext = ResMgr.openSection(extName)
        if ext is not None:
            visualStatesSection = ext
            self.visualStateClassName = visualStatesSection.asString
            components = self.visualStateClassName.strip('"').split('.')
            module = __import__('__main__')
            for comp in components[:-1]:
                module = getattr(module, comp)

            visualStateClass = getattr(module, components[-1])
            for stateName, stateSection in visualStatesSection.items():
                visualState = visualStateClass()
                visualState.onLoad(stateSection)
                self._visualStates[stateName] = visualState

        else:
            ERROR_MSG("Failed to open external visual state '%s'." % extName)
        return