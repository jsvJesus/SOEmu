# Embedded file name: scripts/client/FMOD.py
try:
    from _FMOD import *
except ImportError:
    print 'WARNING: FMOD support is not enabled.'
    from _FMODStubs import *

from sounds import playSound as my_playSound, getSound as my_getSound
import BigWorld
BigWorld.getSound = my_getSound
BigWorld.getSoundBanks = getSoundBanks
BigWorld.playSound = my_playSound
BigWorld.setDefaultSoundProject = setDefaultSoundProject
BigWorld.loadSoundBankIntoMemory = loadSoundBankIntoMemory
BigWorld.loadSoundBank = loadEventProject
BigWorld.loadSoundGroup = loadSoundGroup
BigWorld.reloadSoundBank = reloadEventProject
BigWorld.unloadSoundBankFromMemory = unloadSoundBankFromMemory
BigWorld.unloadSoundBank = unloadEventProject
BigWorld.unloadSoundGroup = unloadSoundGroup
BigWorld.setMasterVolume = setMasterVolume
del BigWorld