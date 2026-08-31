# Embedded file name: scripts/client/SoundNode.py
import BigWorld
from random import choice
import BWPersonality
from sounds import playSound, playMusic

class SoundNode(BigWorld.Entity):
    MODEL = 'models/misc/particles/helper_attach.model'

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.hasPlayer = False
        self.lastSound = None
        self.lastSoundName = ''
        self.wasPlayed = False
        if self.radius > 0:
            BigWorld.addPot(self.matrix, self.radius, self.hitPot)
        return

    def hitPot(self, enteredTrap, handle):
        if self.isDestroyed:
            BigWorld.delPot(handle)
            return
        if enteredTrap:
            self.hasPlayer = True
            self.playRandom()
        else:
            self.hasPlayer = False
            self.stopSound()

    def prerequisites(self):
        return [self.MODEL]

    def startSound(self):
        print 'SoundNode: startSound()'

    def stopSound(self):
        if self.lastSound:
            if self.muteOnLeave or self.lastSound.looped:
                self.lastSound.muted = True
            else:
                self.lastSound.stop()
        self.lastSoundName = ''

    def onEnterWorld(self, prereq):
        if self.MODEL not in prereq.failedIDs:
            self.model = prereq[self.MODEL]
        self.snd = []
        self.soundCallback = None
        self.playRandom()
        return

    def onLeaveWorld(self):
        if self.soundCallback is not None:
            BigWorld.cancelCallback(self.soundCallback)
        if self.lastSound != None:
            self.lastSound.stop()
        return

    def playNodeSound(self):
        pass

    def playRandom(self):
        if len(self.sounds) == 0:
            print 'No sounds to play for SoundNode at', self.position
            return
        else:
            randomSnd = choice(self.sounds)
            if self.playOnce and self.wasPlayed:
                return
            if self.hasPlayer or self.radius == 0:
                self.wasPlayed = True
                if self.lastSound:
                    if (self.muteOnLeave or self.lastSound.looped) and self.lastSound.muted:
                        self.lastSound.muted = False
                        return
                    if self.lastSoundName != randomSnd:
                        self.lastSound.stop()
                if self.lastSoundName != randomSnd:
                    self.lastSound = (playMusic if self.musicNode else playSound)(randomSnd, self.model)
                    self.lastSoundName = randomSnd
                else:
                    self.lastSound.play()
            if self.soundCallback is not None:
                BigWorld.cancelCallback(self.soundCallback)
            if self.playFrequency > 0.0:
                self.soundCallback = BigWorld.callback(self.playFrequency, self.playRandom)
            return

    def play(self, index):
        print 'SoundNode:play()'

    def stop(self):
        pass