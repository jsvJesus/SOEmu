# Embedded file name: scripts/client/sfx/actors.py
from sfx import s_sectionProcessors
import Pixie
import BigWorld
import ResMgr
from bwdebug import *

class ParticleSystem:

    def __call__(self):
        return self

    def load(self, pSection, prereqs = None):
        try:
            actor = prereqs.pop(pSection.asString)
        except:
            try:
                actor = Pixie.create(pSection.asString)
            except:
                ERROR_MSG('Could not create particle system', pSection.asString)
                actor = None

        return actor

    def prerequisites(self, pSection):
        return [pSection.asString]


s_particleSystem = ParticleSystem()
s_sectionProcessors['ParticleSystem'] = s_particleSystem

class Model:

    def __call__(self):
        return self

    def load(self, pSection, prereqs = None):
        try:
            actor = prereqs.pop(pSection.asString)
        except:
            try:
                actor = BigWorld.Model(pSection.asString)
            except:
                ERROR_MSG('Could not create Model', pSection.asString)
                actor = None

        return actor

    def prerequisites(self, pSection):
        return [pSection.asString]


s_model = Model()
s_sectionProcessors['Model'] = s_model

class Light:

    def __call__(self):
        return self

    def load(self, pSection, prereqs = None):
        try:
            actor = BigWorld.PyChunkLight()
            actor.innerRadius = pSection.readFloat('innerRadius', 0)
            actor.outerRadius = pSection.readFloat('outerRadius', 10)
            actor.colour = pSection.readVector4('colour', (255, 255, 255, 255))
        except:
            ERROR_MSG('Could not create Light', pSection.asString)
            actor = None

        return actor


s_light = Light()
s_sectionProcessors['Light'] = s_light