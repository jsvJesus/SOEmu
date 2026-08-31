# Embedded file name: scripts/client/Effects.py
import BigWorld
import BWPersonality
from utils import hierarchy_get
from EffectUtils import getEffect
from FX_extension import SFXGroup, PersistentSFX

class Effects:

    def __init__(self):
        self.initEffects()
        self.current_effects = set()
        self.effects_sfxes = {}
        self.effects_posteffects = {}
        self.addEffectsSFXes(self.effectsVisibleForAll)

    def initEffects(self):
        pass

    def addPosteffects(self, effectId):
        posteffects = getEffect(effectId)['posteffects']
        for postEf in posteffects:
            postEfNum = self.effects_posteffects.get(postEf, 0)
            if postEfNum == 0:
                BWPersonality.GUICore.addPPEffect(postEf)
            self.effects_posteffects[postEf] = postEfNum + 1

    def removePosteffects(self, effectId):
        posteffects = getEffect(effectId)['posteffects']
        for postEf in posteffects:
            postEfNum = self.effects_posteffects.get(postEf, 0)
            if postEfNum == 1:
                BWPersonality.GUICore.delPPEffect(postEf)
            if postEfNum > 0:
                self.effects_posteffects[postEf] = postEfNum - 1

    def addEffectSFX(self, effectId):
        if effectId in self.effects_sfxes:
            return
        sfxes = hierarchy_get(getEffect(effectId), ['sfxes', 'persistent'])
        if sfxes and len(sfxes) > 0:
            sfxGroup = self.effects_sfxes[effectId] = SFXGroup()
            for sfxData in sfxes:
                on_other_clients = sfxData.get('other_clients', True)
                if on_other_clients or self is BigWorld.player():
                    sfxGroup.addSFX(PersistentSFX(sfxData['path'], self))

            sfxGroup.play()
        if effectId == 402:
            self.bleedDropEff()

    def addEffectsSFXes(self, effectIdList):
        for effId in effectIdList:
            self.addEffectSFX(effId)

    def removeEffectSFX(self, effectId):
        sfxGroup = self.effects_sfxes.get(effectId)
        if sfxGroup:
            sfxGroup.stop()
            del self.effects_sfxes[effectId]
        for sfxData in hierarchy_get(getEffect(effectId), ['sfxes', 'onRemove'], []):
            PersistentSFX(sfxData['path'], self).playOnce()

        if effectId == 402:
            self.removeBleedDropEff()

    def removeEffectsSFXes(self, effectIdList):
        for effId in effectIdList:
            self.removeEffectSFX(effId)

    def set_effectsVisibleForAll(self, oldValues):
        self.removeEffectsSFXes(oldValues)
        self.addEffectsSFXes(self.effectsVisibleForAll)

    def setSlice_effectsVisibleForAll(self, path, oldValues):
        newValues = self.effectsVisibleForAll[path[-1][0]:path[-1][1]]
        self.removeEffectsSFXes(oldValues)
        self.addEffectsSFXes(newValues)

    def changeVisibleEffect(self, effect):
        """ Return True if new effect was added, return False if effect is already present """
        effectID = effect['id']
        if 806 == effectID:
            self.startSpiderHallucianations()
        if effectID in self.current_effects:
            return False
        else:
            self.current_effects.add(effectID)
            return True

    def removeVisibleEffect(self, effectID):
        """ Return True if successfully removed effect, otherwise return False """
        if 806 == effectID:
            self.stopSpiderHallucianations()
        if effectID in self.current_effects:
            self.current_effects.remove(effectID)
            return True
        else:
            return False