# Embedded file name: scripts/client/Music.py
import sounds
import BigWorld
import random
from Settings import Settings

class Music:

    def __init__(self):
        self.currentTrack = None
        self.menuTrack = None
        self.tracks = None
        self.musicEnabled = True
        self.lastSpaceSound = None
        self.lastSpaceSoundName = ''
        return

    def onInit(self):
        BigWorld.setMasterVolume(1.0)
        self.initMusicTracks()
        self.startMenuTrack()

    def updateVolume(self):
        s = Settings()
        v = s.getMusicVolume()
        if self.tracks:
            for track in self.tracks:
                if not track.isVirtual:
                    track.volume = v

        v = s.getSfxVolume()
        if self.lastSpaceSound and not self.lastSpaceSound.isVirtual:
            self.lastSpaceSound.volume = v

    def initMusicTracks(self):
        self.menuTrack = sounds.getMusic('music/story_bullet')
        self.musicEnabled = True
        if self.menuTrack is None:
            print "Error loading 'music/story_bullet': music disabled"
            self.musicEnabled = False
            return
        else:
            self.randomTrackCallback = None
            self.tracks = [sounds.getMusic('music/menu_theme'),
             sounds.getMusic('music/story_bullet'),
             sounds.getMusic('music/ambient_autumn-empty'),
             sounds.getMusic('music/ambient_cold-clean'),
             sounds.getMusic('music/ambient_deep-forest'),
             sounds.getMusic('music/ambient_perfect'),
             sounds.getMusic('music/ambient_silent-suicide'),
             sounds.getMusic('music/ambient_Pain-of-Angels-v.2'),
             sounds.getMusic('music/ambient_Place-The-Shadows'),
             sounds.getMusic('music/ambient_Theme-of-burial'),
             sounds.getMusic('music/ambient_Theme-of-Heathland')]
            self.menuTrack = self.tracks[0]
            self.trackPlaylist = []
            for x in self.tracks:
                x.setCallback('EVENTSTARTED', self.onGenericMusicStarted)
                x.setCallback('SOUNDDEF_END', self.onGenericMusicFinished)

            self.updateVolume()
            return

    def setMusicState(self, state):
        self.musicEnabled = state
        print 'Music %s' % ('ON' if self.musicEnabled else 'OFF')
        for mus in self.tracks:
            mus.muted = not self.musicEnabled

        if not self.musicEnabled:
            self.stopAllMusic()
        else:
            self.startRandomTrack()

    def toggleMusic(self):
        self.musicEnabled = not self.musicEnabled
        self.setMusicState(self.musicEnabled)

    def stopAllMusic(self):
        if hasattr(self, 'randomTrackCallback'):
            if self.randomTrackCallback is not None:
                BigWorld.cancelCallback(self.randomTrackCallback)
                self.randomTrackCallback = None
        if self.tracks is None:
            return
        else:
            for x in self.tracks:
                x.setCallback('EVENTSTARTED', None)
                x.setCallback('SOUNDDEF_END', None)
                x.stop()
                x.setCallback('EVENTSTARTED', self.onGenericMusicStarted)
                x.setCallback('SOUNDDEF_END', self.onGenericMusicFinished)

            return

    def startMenuTrack(self):
        self.stopAllMusic()
        if self.musicEnabled:
            self.tracks[0].play()

    def startRandomTrack(self):
        if not self.musicEnabled:
            return
        if len(self.trackPlaylist) <= 0:
            for x in self.tracks[2:]:
                self.trackPlaylist.append(x)

            random.shuffle(self.trackPlaylist)
            while self.currentTrack == self.trackPlaylist[0]:
                random.shuffle(self.trackPlaylist)

        self.currentTrack = self.trackPlaylist.pop()
        self.currentTrack.play()
        print 'MUSIC: startRandomTrack: ', self.currentTrack.name, 'volume = ', self.currentTrack.volume

    def onGenericMusicStarted(self, snd):
        print 'onGenericMusicStarted:', '::', snd.name, '::', snd.duration, '::', BigWorld.time(), '::', snd.volume

    def onGenericMusicFinished(self, snd):
        print 'onGenericMusicFinished', '::', snd.name, '::', snd.duration, '::', BigWorld.time(), '::', snd.volume
        self.randomTrackCallback = BigWorld.callback(60.0, self.startRandomTrack)

    def playSpaceSound(self, spacename):
        soundName = 'ambient/' + spacename
        print 'Play music (space ambient):', soundName
        if self.lastSpaceSound is not None and self.lastSpaceSoundName != soundName:
            self.lastSpaceSound.stop()
        if self.lastSpaceSoundName != soundName:
            self.lastSpaceSoundName = soundName
            self.lastSpaceSound = sounds.playAmbientMusic(soundName, None, None, True)
        elif self.lastSpaceSound:
            self.lastSpaceSound.play()
        return

    def stopSpaceSound(self):
        if self.lastSpaceSound:
            self.lastSpaceSound.stop()
        self.lastSpaceSound = None
        self.lastSpaceSoundName = ''
        return