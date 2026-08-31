# Embedded file name: scripts/client/FX/Events/PlaySound.py
import traceback
from FX.Event import Event
from FX.Event import TRANSFORM_DEPENDENT_EVENT
from FX import s_sectionProcessors
from bwdebug import *

def playSound(sound, obj, volume = None):
    return obj.playSound(sound)


def set_playsound_function(new_playSound):
    global playSound
    playSound = new_playSound


class PlaySound(Event):
    """
    This class implements an event that plays a sound.  The sound may be
    associated with a particular actor to provide its 3D position; if not the
    sound will be played on the source model.
    """

    def __init__(self):
        self.tag = None
        self.attachToActor = False
        return

    def load(self, pSection, prereqs = None):
        """
        This method loads the PlaySound event via an XML data section. It
        reads the sound tag name from the section name.  It also looks for an
        "attachToActor" tag to specify whether the sound should be played at
        the given actor's position, or the effect source's position.
        """
        self.tag = pSection.asString
        if self.tag == '':
            WARNING_MSG('PlaySound had no associated tag')
        self.attachToActor = pSection.has_key('attachToActor')
        return self

    def go(self, effect, actor, source, target, **kargs):
        sound = None
        if self.tag != '':
            if kargs.has_key('suffix'):
                tag = self.tag + kargs['suffix']
            else:
                tag = self.tag
            if self.attachToActor:
                try:
                    sound = playSound(tag, actor)
                except:
                    ERROR_MSG('error playing sound on actor', self, actor, source, tag)
                    traceback.print_exc()

            else:
                try:
                    sound = playSound(tag, source.model)
                except:
                    try:
                        sound = playSound(tag, source)
                    except:
                        ERROR_MSG('error playing sound', self, actor, source, tag)
                        traceback.print_exc()

        if sound:
            return sound.duration
        else:
            return 0.0
            return

    def eventTiming(self):
        return TRANSFORM_DEPENDENT_EVENT


s_sectionProcessors['PlaySound'] = PlaySound