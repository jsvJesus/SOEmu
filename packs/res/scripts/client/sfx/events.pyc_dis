# Embedded file name: scripts/client/sfx/events.py
import BigWorld
import math
from sfx import s_sectionProcessors
from sfx import typeCheck
from Pixie import MetaParticleSystem
from bwdebug import *
import random
import traceback
from functools import partial
from Math import Vector3
from Math import Vector4LFO
from Math import Vector4Shader
from Math import Vector4
from Math import Vector4Animation
from Helpers.V4ShaderConsts import _mul
from Helpers.V4ShaderConsts import _add
from Helpers.V4ShaderConsts import _r0
from Helpers.V4ShaderConsts import _r1
from sounds import playSound
IMMEDIATE_EVENT = 0
TRANSFORM_DEPENDENT_EVENT = 1
DURATION_DEPENDENT_EVENT = 2
SOURCE_PSA = 1
SINK_PSA = 2
BARRIER_PSA = 3
FORCE_PSA = 4
STREAM_PSA = 5
JITTER_PSA = 6
SCALER_PSA = 7
TINT_SHADER_PSA = 8
NODE_CLAMP_PSA = 9
ORBITOR_PSA = 10
FLARE_PSA = 11
COLLIDE_PSA = 12
MATRIX_SWARM_PSA = 13
MAGNET_PSA = 14
SPLAT_PSA = 15

class Event:

    def __init__(self):
        pass

    def load(self, pSection, prereqs = None):
        return self

    def go(self, sfx, actor, source, target, **kargs):
        return 0.0

    def stop(self, actor, source, target):
        return 0.0

    def duration(self, actor, source, target):
        return 0.0

    def eventTiming(self):
        return IMMEDIATE_EVENT


class RandomDelayEvent(Event):

    def __init__(self):
        Event.__init__(self)
        self.events = []
        self.minDelay = 0.0
        self.maxDelay = 1.0
        self.nextDelay = 1.0

    def load(self, pSection, prereqs = None):
        for name, section in pSection.items():
            eventSection = pSection.items()[0][1]
            result = None
            if name not in ('MinDelay', 'MaxDelay'):
                if s_sectionProcessors.has_key(name):
                    result = s_sectionProcessors[name]().load(section)
                else:
                    ERROR_MSG('No section processor matches the tag ', name, section.asString)
                if result:
                    self.events.append(result)

        self.minDelay = pSection.readFloat('MinDelay', self.minDelay)
        self.maxDelay = pSection.readFloat('MaxDelay', self.maxDelay)
        if self.minDelay > self.maxDelay:
            ERROR_MSG('Min Delay was greater than Max Delay', self, pSection.asString)
            self.minDelay = 0.0
        self.nextDelay = self.getNextDelay()
        return self

    def getNextDelay(self):
        return random.random() * (self.maxDelay - self.minDelay) + self.minDelay

    def go(self, sfx, actor, source, target, **kargs):
        duration = 0.0
        if len(self.events) > 0:
            BigWorld.callback(self.nextDelay, lambda : self.spawnEvents(sfx, actor, source, target))
            return self.duration(actor, source, target)
        return self.nextDelay

    def spawnEvents(self, sfx, actor, source, target):
        for i in self.events:
            i.go(sfx, actor, source, target)

        self.nextDelay = self.getNextDelay()

    def duration(self, actor, source, target):
        total = self.nextDelay
        for i in self.events:
            eventDuration = i.duration(actor, source, target)
            if eventDuration >= 0.0:
                total += eventDuration

        return total


s_sectionProcessors['RandomDelayEvent'] = RandomDelayEvent

class PlaySound(Event):

    def __init__(self):
        Event.__init__(self)
        self.tag = None
        self.attachToActor = False
        return

    def load(self, pSection, prereqs = None):
        self.tag = pSection.asString
        if self.tag == '':
            WARNING_MSG('PlaySound had no associated tag')
        self.attachToActor = pSection.has_key('attachToActor')
        return self

    def go(self, sfx, actor, source, target, **kargs):
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
                    traceback.print_stack()

            else:
                try:
                    sound = playSound(tag, source.model)
                except:
                    try:
                        sound = playSound(tag, source)
                    except:
                        ERROR_MSG('error playing sound', self, actor, source, tag)
                        traceback.print_exc()
                        traceback.print_stack()

        if sound:
            return sound.duration
        else:
            return 0.0

    def eventTiming(self):
        return TRANSFORM_DEPENDENT_EVENT


s_sectionProcessors['PlaySound'] = PlaySound

class ForceParticle(Event):

    def __call__(self):
        return self

    def go(self, sfx, actor, source, target, **kargs):
        try:
            amount = kargs['NumberToForce']
        except:
            amount = 1

        try:
            actor.force(amount)
            return actor.duration() + 0.001
        except:
            ERROR_MSG('actor is not a particle system!', actor)
            return 0.0

    def duration(self, actor, source, target):
        try:
            return actor.duration() + 0.001
        except:
            return 0.0

    def eventTiming(self):
        return TRANSFORM_DEPENDENT_EVENT


s_forceParticle = ForceParticle()
s_sectionProcessors['ForceParticle'] = s_forceParticle
s_sectionProcessors['Force'] = s_forceParticle

class ParticleSubSystemEvent(Event):

    def __init__(self):
        Event.__init__(self)
        self.subSystems = []

    def load(self, pSection, prereqs = None):
        self.subSystems = pSection.readStrings('systemName')
        return self

    def duration(self, actor, source, target):
        return 0.0

    def isInteresting(self, subSystem):
        return 1

    def populateSubSystemList(self, actor):
        if type(actor) == MetaParticleSystem:
            if len(self.subSystems) == 0:
                self.subSystems = []
                for i in xrange(0, actor.nSystems()):
                    sys = actor.system(i)
                    if self.isInteresting(sys):
                        self.subSystems.append(i)

    def subSystemIterate(self, actor, source, target, callbackFn):
        if type(actor) == MetaParticleSystem:
            if len(self.subSystems) == 0:
                self.populateSubSystemList(actor)
            for i in self.subSystems:
                sys = actor.system(i)
                callbackFn(actor, source, target, sys)

        else:
            try:
                callbackFn(actor, source, target, actor)
            except:
                ERROR_MSG('actor is not a particle system!', actor)


class SwarmTargets(ParticleSubSystemEvent):

    def __init__(self):
        Event.__init__(self)
        self.nodeList = []

    def load(self, pSection, prereqs = None):
        self.nodeList = pSection.readStrings('Node')
        return ParticleSubSystemEvent.load(self, pSection)

    def isInteresting(self, subSystem):
        act = None
        try:
            act = subSystem.action(MATRIX_SWARM_PSA)
            return True
        except ValueError:
            act = None

        return act != None

    def setTargets(self, actor, source, target, subSystem):
        act = subSystem.action(MATRIX_SWARM_PSA)
        act.targets = self.targetNodes

    def go(self, sfx, actor, source, target, **kargs):
        nodes = []
        for i in self.nodeList:
            try:
                try:
                    nodes.append(target.model.node(i))
                except AttributeError:
                    nodes.append(target.node(i))

            except ValueError:
                pass
            except TypeError:
                nodes.append(target.root)

        if kargs.has_key('TargetNodes'):
            nodes += kargs['TargetNodes']
        self.targetNodes = nodes
        self.subSystemIterate(actor, source, target, self.setTargets)
        self.targetNodes = None
        return 0

    def duration(self, actor, source, target):
        return 0.0


s_sectionProcessors['SwarmTargets'] = SwarmTargets

class CorrectMotionTriggeredParticle(ParticleSubSystemEvent):

    def resetMotionTriggerFlag(self, actions):
        for i in actions:
            i.motionTriggered = 1

    def isInteresting(self, subSystem):
        act = subSystem.action(SOURCE_PSA)
        return act and act.motionTriggered

    def buildActionList(self, actor, source, target, subSystem):
        act = subSystem.action(SOURCE_PSA)
        if act:
            self.actions.append(act)

    def go(self, sfx, actor, source, target, **kargs):
        self.actions = []
        self.subSystemIterate(actor, source, target, self.buildActionList)
        self.resetMotionTriggerFlag(self.actions)
        BigWorld.callback(0.001, lambda : self.resetMotionTriggerFlag(self.actions))
        return 0.0


s_sectionProcessors['CorrectMotionTriggeredParticle'] = CorrectMotionTriggeredParticle

class ResetTimeTriggeredParticles(ParticleSubSystemEvent):

    def isInteresting(self, subSystem):
        act = subSystem.action(SOURCE_PSA)
        return act and act.timeTriggered

    def resetTimeTrigger(self, actor, source, target, subSystem):
        subSystem.clear()
        act = subSystem.action(SOURCE_PSA)
        act.timeTriggered = 0
        act.timeTriggered = 1

    def go(self, sfx, actor, source, target, **kargs):
        self.subSystemIterate(actor, source, target, self.resetTimeTrigger)
        return 0.0


s_sectionProcessors['ResetTimeTriggeredParticles'] = ResetTimeTriggeredParticles

class RampTimeTriggeredParticles:

    def load(self, pSection, prereqs = None):
        self.duration = pSection.readFloat('Duration', 0.0)
        self.fadeTime = pSection.readFloat('FadeTime', 2.0)
        if self.duration > 0.0 and self.fadeTime > self.duration:
            self.fadeTime = self.duration / 2.0
        return self

    def saveTimes(self, actor):
        self.timeTriggeredSources = []
        for i in xrange(0, actor.nSystems()):
            try:
                source = actor.system(i).action(1)
                if source.timeTriggered:
                    self.timeTriggeredSources.append((source, source.rate))
            except:
                pass

    def restoreTimes(self, actor):
        for source, rate in self.timeTriggeredSources:
            source.rate = rate

    def setAll(self, actor, rate):
        for source, ignore in self.timeTriggeredSources:
            source.rate = rate

    def go(self, sfx, actor, source, target, **kargs):
        if not hasattr(self, 'timeTriggeredSources'):
            self.saveTimes(actor)
        actor.clear()
        self.setAll(actor, 0.0)
        BigWorld.callback(0.0, partial(self.restoreTimes, actor))
        if self.duration > 0.0:
            BigWorld.callback(self.duration - self.fadeTime, partial(self.stop, actor, source, target))
        return self.duration

    def stop(self, actor, source, target):
        self.setAll(actor, 0.0)
        return self.fadeTime

    def duration(self):
        return self.duration

    def eventTiming(self):
        return IMMEDIATE_EVENT


s_sectionProcessors['RampTimeTriggeredParticles'] = RampTimeTriggeredParticles

class SetOrbitorPoint(ParticleSubSystemEvent):

    def isInteresting(self, subSystem):
        act = subSystem.action(ORBITOR_PSA)
        return act != None

    def setOrbitorPoint(self, actor, source, target, subSystem):
        try:
            act = subSystem.action(ORBITOR_PSA)
            act.point = source.position
        except:
            ERROR_MSG('setOrbitorPoint has a problem with finding the position of the source object', source)

    def go(self, sfx, actor, source, target, **kargs):
        self.subSystemIterate(actor, source, target, self.setOrbitorPoint)
        return 0.0


s_sectionProcessors['SetOrbitorPoint'] = SetOrbitorPoint

class SetColour(ParticleSubSystemEvent):

    def isInteresting(self, subSystem):
        act = subSystem.action(TINT_SHADER_PSA)
        return act != None

    def setModulator(self, actor, source, target, subSystem):
        act = subSystem.action(TINT_SHADER_PSA)
        act.modulator = self.colour

    def go(self, sfx, actor, source, target, **kargs):
        try:
            self.colour = kargs['SetColour']
            self.subSystemIterate(actor, source, target, self.setModulator)
        except:
            WARNING_MSG('No colour was passed into the argument list', self, actor, source, target, kargs)

        return 0.0


s_sectionProcessors['SetColour'] = SetColour

class SetBasis(ParticleSubSystemEvent):

    def setBasis(self, actor, source, target, subSystem):
        subSystem.explicitPosition = self.worldPos
        subSystem.explicitDirection = self.worldDir

    def go(self, sfx, actor, source, target, **kargs):
        try:
            self.worldDir, self.worldPos = kargs['Basis']
            self.subSystemIterate(actor, source, target, self.setBasis)
            del self.worldDir
            del self.worldPos
        except:
            WARNING_MSG('No basis was passed into the argument list', self, actor, source, target, kargs)

        return 0.0


s_sectionProcessors['SetBasis'] = SetBasis

class AlignModel(ParticleSubSystemEvent):

    def go(self, sfx, actor, source, target, **kargs):
        try:
            if kargs.has_key('ModelAlignment'):
                dir, pos = kargs['ModelAlignment']
            elif kargs.has_key('Basis'):
                dir, pos = kargs['Basis']
            actor.position = pos
            actor.yaw = math.atan2(dir.x, dir.z)
        except:
            WARNING_MSG('No basis was passed into the argument list', self, actor, source, target, kargs)

        return 0.0


s_sectionProcessors['AlignModel'] = AlignModel

class ClearParticles(ParticleSubSystemEvent):

    def clearSubSystem(self, actor, source, target, subSystem):
        subSystem.clear()

    def go(self, sfx, actor, source, target, **kargs):
        self.subSystemIterate(actor, source, target, self.clearSubSystem)
        return 0.0


s_sectionProcessors['ClearParticles'] = ClearParticles

class PlayAction:

    def __init__(self):
        self.actions = []

    def load(self, pSection, prereqs = None):
        self.actions = pSection.readStrings('Action')
        return self

    def go(self, sfx, actor, source, target, **kargs):
        dur = 0.0
        curr = actor
        for i in self.actions:
            try:
                curr = getattr(curr, i)()
                dur += curr.duration
            except EnvironmentError:
                DEBUG_MSG('ActionQueuer op() cannot queue actions when our Model is not in the world', i, actor, source, target)

        return dur

    def duration(self, actor, source, target):
        dur = 0.0
        try:
            for i in self.actions:
                try:
                    dur += actor.action(i).duration
                except:
                    pass

            return dur
        except:
            return 0.0

    def eventTiming(self):
        return TRANSFORM_DEPENDENT_EVENT


s_sectionProcessors['PlayAction'] = PlayAction
s_sectionProcessors['PlayActions'] = PlayAction

class AddDecal(Event):

    def __init__(self):
        Event.__init__(self)
        self.decalIndex = -1
        self.decalSize = 0.0
        self.decalExtent = (0, 0, 0)

    def load(self, pSection, prereqs = None):
        try:
            self.decalIndex = BigWorld.decalTextureIndex(pSection.asString)
        except:
            return

        if self.decalIndex != -1:
            self.decalSize = pSection.readFloat('size', 1)
            self.decalExtent = pSection.readVector3('extent', (0, -1, 0))
        else:
            WARNING_MSG('AddDecal had no associated tag')
        return self

    def go(self, sfx, actor, source, target, **kargs):
        if self.decalIndex == -1:
            return
        try:
            start = kargs['DecalInfo'][0]
            end = kargs['DecalInfo'][1]
        except KeyError:
            start = Vector3(source.position)
            for i in xrange(0, 3):
                start[i] -= self.decalExtent[i] * 0.5

            end = start + self.decalExtent

        try:
            BigWorld.addDecal(start, end, self.decalSize, self.decalIndex)
        except:
            ERROR_MSG('Could not add decal')

        return 0.0

    def eventTiming(self):
        return TRANSFORM_DEPENDENT_EVENT


s_sectionProcessors['AddDecal'] = AddDecal

class Flicker:

    def __init__(self):
        self.colour = None
        self.lightFlicker = None
        self.amplitude = 1.0
        self.speed = 1.0
        return

    def load(self, pSection, prereqs = None):
        self.amplitude = pSection.readFloat('amplitude', self.amplitude)
        self.speed = pSection.readFloat('speed', self.speed)
        return self

    def go(self, sfx, actor, source, target, **kargs):
        self.colour = actor.colour
        lfo1 = Vector4LFO()
        lfo1.period = 0.4 / self.speed
        lfo1.amplitude = self.amplitude
        lfo2 = Vector4LFO()
        lfo2.period = 0.149 / self.speed
        scalarOffset = 1.0 - self.amplitude
        offset = Vector4(scalarOffset, scalarOffset, scalarOffset, scalarOffset)
        self.lightFlicker = Vector4Shader()
        self.lightFlicker.addOp(_mul, _r1, lfo1, lfo2)
        self.lightFlicker.addOp(_add, _r1, _r1, offset)
        self.lightFlicker.addOp(_mul, _r0, self.colour, _r1)
        actor.shader = self.lightFlicker
        return 0.0

    def stop(self, actor, source, target):
        actor.colour = self.colour
        actor.shader = None
        self.lightFlicker = None
        return 0.0

    def duration(self, actor, source, target):
        return 0.0

    def eventTiming(self):
        return IMMEDIATE_EVENT


s_sectionProcessors['Flicker'] = Flicker

class Fade:

    def __init__(self):
        self.colour = None
        self.time = 1.0
        return

    def load(self, pSection, prereqs = None):
        self.time = pSection.readFloat('time', self.time)
        return self

    def go(self, sfx, actor, source, target, **kargs):
        if not self.colour:
            self.colour = actor.colour
        self.lightFader = Vector4Animation()
        self.lightFader.duration = 100000.0
        self.lightFader.keyframes = [(0.0 * self.time, self.colour), (1.0 * self.time, (0, 0, 0, 0))]
        actor.shader = self.lightFader
        return self.time

    def stop(self, actor, source, target):
        actor.shader = None
        actor.colour = self.colour
        self.lightFader = None
        return 0.0

    def duration(self, actor, source, target):
        return self.time

    def eventTiming(self):
        return IMMEDIATE_EVENT


s_sectionProcessors['Fade'] = Fade