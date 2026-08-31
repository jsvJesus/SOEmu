# Embedded file name: scripts/client/sounds.py
"""
Created on 12.05.2011

@author: muzhig
"""
import BigWorld
import traceback
import _FMOD
from Helpers.Listener import Listenable
playSound = _FMOD.playSound
getSound = _FMOD.getSound
if hasattr(BigWorld, 'Entity'):
    import Settings

    class Sound(object, Listenable):

        def __init__(self, fmod_sound, is_music):
            Listenable.__init__(self)
            self.fmod_sound = fmod_sound
            self.fmod_sound.setCallback('EVENTSTARTED', self.onPlayBegin)
            self.fmod_sound.setCallback('SOUNDDEF_END', self.onPlayEnd)
            self.event_started_callback = None
            self.sounddef_end_callback = None
            self.is_music = is_music
            return

        def setCallback(self, event, cb):
            if event == 'EVENTSTARTED':
                self.event_started_callback = cb
            elif event == 'SOUNDDEF_END':
                self.sounddef_end_callback = cb
            else:
                self.fmod_sound.setCallback(event, cb)

        def get_duration(self):
            return self.fmod_sound.duration

        def set_duration(self, value):
            self.fmod_sound.duration = value

        duration = property(get_duration, set_duration)

        def get_volume(self):
            if not self.muted:
                return self.fmod_sound.volume
            return self._volume

        def set_volume(self, value):
            if self.muted:
                self._volume = value
            else:
                self.fmod_sound.volume = value

        volume = property(get_volume, set_volume)

        def get_muted(self):
            return getattr(self, '_muted', False)

        def set_muted(self, value):
            if value:
                self._volume = self.volume
                self.volume = 0
                self._muted = value
            else:
                self._muted = value
                self.volume = self._volume

        muted = property(get_muted, set_muted)

        def get_paused(self):
            return self.fmod_sound.paused

        def set_paused(self, value):
            self.fmod_sound.paused = value

        paused = property(get_paused, set_paused)

        def get_position(self):
            return self.fmod_sound.position

        def set_position(self, value):
            self.fmod_sound.position = value

        position = property(get_position, set_position)

        def get_isVirtual(self):
            return self.fmod_sound.isVirtual

        def set_isVirtual(self, value):
            self.fmod_sound.isVirtual = value

        isVirtual = property(get_isVirtual, set_isVirtual)

        def get_name(self):
            return self.fmod_sound.name

        name = property(get_name)

        def play(self):
            self.fmod_sound.play()
            if self.muted:
                self.fmod_sound.volume = 0

        def stop(self):
            self.fmod_sound.stop()
            if self in Sound.current_sounds:
                Sound.current_sounds.remove(self)

        def get_paused(self):
            return self.fmod_sound.paused

        def set_paused(self, paused):
            self.fmod_sound.paused = paused

        paused = property(get_paused, set_paused)

        def get_looped(self):
            return self.fmod_sound.duration < 0

        looped = property(get_looped)

        def onPlayBegin(self, fmod_snd):
            if self not in Sound.current_sounds:
                Sound.current_sounds.append(self)
                self.listeners.onPlayBegin()
                if callable(self.event_started_callback):
                    self.event_started_callback(self)

        def onPlayEnd(self, fmod_snd):
            if self in Sound.current_sounds:
                Sound.current_sounds.remove(self)
            self.listeners.onPlayEnd()
            if callable(self.sounddef_end_callback):
                self.sounddef_end_callback(self)

        current_sounds = []

        @staticmethod
        def playSound(sound = None, obj = None, volume = None, is_music = False):
            if not obj:
                obj = _FMOD
            if volume is None:
                volume = Settings.Settings().getMusicVolume() if is_music else Settings.Settings().getSfxVolume()
            try:
                fmod_sound = obj.playSound(sound)
            except ValueError:
                fmod_sound = None
            except StandardError:
                fmod_sound = None

            if fmod_sound:
                wrapped_sound = Sound(fmod_sound, is_music)
                wrapped_sound.volume = volume
                return wrapped_sound
            else:
                print 'playSound SOUND NOT FOUND:', [sound]
                traceback.print_stack()
                if obj:
                    for x in dir(obj):
                        if not x.startswith('_'):
                            print x, getattr(obj, x)

                print '_____'
                return

        @staticmethod
        def getSound(sound = None, volume = None, is_music = False):
            if volume is None:
                volume = Settings.Settings().getMusicVolume() if is_music else Settings.Settings().getSfxVolume()
            try:
                fmod_sound = _FMOD.getSound(sound)
            except ValueError:
                fmod_sound = None

            if fmod_sound:
                wrapped_sound = Sound(fmod_sound, is_music)
                wrapped_sound.volume = volume
                return wrapped_sound
            else:
                print 'getSound SOUND NOT FOUND:', [sound]
                traceback.print_stack()
                print '_____'
                return


    getSound = Sound.getSound
    playSound = Sound.playSound

    def getMusic(sound):
        return getSound(sound, volume=Settings.Settings().getMusicVolume(), is_music=True)


    getAmbientMusic = getSound

    def playMusic(sound, obj = None):
        return playSound(sound, obj, Settings.Settings().getMusicVolume(), True)


    playAmbientMusic = playSound