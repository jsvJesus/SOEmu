# Embedded file name: scripts/client/soGUI/data/SoundFeed.py
import ResMgr

class SoundFeeder(object):

    def __init__(self):
        self.soundCfg = ResMgr.openSection('scripts/client/soGUI/data/GUISounds.xml')

    def getSound(self, controlName, eventName):
        xmlKey = controlName + '/' + eventName
        return self.soundCfg.readString(xmlKey, '')


soundFeed = SoundFeeder()