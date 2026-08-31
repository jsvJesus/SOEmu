# Embedded file name: scripts/client/sfx/__init__.py
import BigWorld
import ResMgr
from bwdebug import *
from Queue import Queue
import Math
from functools import partial
import traceback
s_sectionProcessors = {}

def typeCheck(self, listOrType):
    return 1


def prerequisites(filename):
    if filename == '':
        return ()
    fx = SFX(filename)
    fx.prerequisites()
    return tuple(fx.prereqs)


debugTimings = 0

class EventTimer:

    def __init__(self):
        self.semaphore = 0
        self.callbackFn = None
        return

    def going(self):
        return self.semaphore != 0

    def reserve(self):
        self.semaphore += 1

    def release(self):
        self.semaphore -= 1

    def begin(self, duration, callbackFn):
        self.callbackFn = callbackFn
        self.semaphore += 1
        BigWorld.callback(duration, self.end)

    def extend(self, duration):
        self.semaphore += 1
        BigWorld.callback(duration, self.end)

    def end(self):
        self.semaphore -= 1
        if self.semaphore == 0:
            if self.callbackFn:
                self.callbackFn()
                self.callbackFn = None
        return


class SFX:

    def __init__(self, fileName):
        self.actors = {}
        self.joints = {}
        self.events = []
        self.fileName = fileName

    def prerequisites(self):
        self.prereqs = set()
        pSection = ResMgr.openSection(self.fileName)
        if not pSection:
            ERROR_MSG('Could not open file', self.fileName)
            return None
        else:
            self.prerequisitesFromSection(pSection)
            self.prereqs.add(self.fileName)
            return None

    def create(self, prereqs = None):
        global debugTimings
        try:
            pSection = prereqs[self.fileName]
        except KeyError:
            pSection = ResMgr.openSection(self.fileName)
        except TypeError:
            pSection = ResMgr.openSection(self.fileName)

        if pSection != None:
            self.createFromSection(pSection, prereqs)
        else:
            ERROR_MSG('Could not open file', self.fileName)
            return
        if debugTimings == 1:
            self.events.append(('', timedEvents.DebugEventTiming()))
        return

    def parse(self, tag, store, pSection, prereqs = None, gatherPrerequisites = False):
        for sname, ds in pSection.items():
            if sname == tag:
                section = ds.items()[0][1]
                if s_sectionProcessors.has_key(section.name):
                    instance = s_sectionProcessors[section.name]()
                    if not gatherPrerequisites:
                        result = instance.load(section, prereqs)
                        if result != None:
                            try:
                                store[ds.asString] = result
                            except:
                                store.append((ds.asString, result))

                        else:
                            ERROR_MSG('None was returned.  Not adding to this effect : ', section.name, ds.asString)
                    else:
                        self.prereqs.add(section.asString)
                        if hasattr(instance, 'prerequisites'):
                            self.prereqs.update(instance.prerequisites(section))
                else:
                    ERROR_MSG('No section processor matches the tag ', section.name, ds.asString)
                    result = None

        return

    def modelName(self, visualName):
        if len(visualName) > 7:
            if visualName[-7:] == '.visual':
                return visualName[:-7] + '.model'
        return visualName

    def prerequisitesFromSection(self, pSection):
        self.parse('Actor', self.actors, pSection, gatherPrerequisites=True)
        self.parse('Event', self.events, pSection, gatherPrerequisites=True)

    def createFromSection(self, pSection, prereqs = None):
        self.parse('Actor', self.actors, pSection, prereqs)
        self.parse('Joint', self.joints, pSection, prereqs)
        self.parse('Event', self.events, pSection, prereqs)
        for actor in self.joints.keys():
            if not self.actors.has_key(actor):
                ERROR_MSG('Actor not found', actor)
                del self.joints[actor]

        for actor in self.actors.keys():
            if not self.joints.has_key(actor):
                WARNING_MSG('Actor exists, but is not attached anywhere', actor)

    def extendTime(self, event, duration):
        pass


class OneShotSFX(SFX):

    def __init__(self, fileName = None, maxDuration = 10.0, prereqs = None):
        SFX.__init__(self, fileName)
        SFX.create(self, prereqs)
        self.timer = EventTimer()
        self.timers = {}
        for actorName in self.actors.keys():
            self.timers[actorName] = EventTimer()

        self.maxDuration = maxDuration
        if self.maxDuration < 0.0:
            WARNING_MSG('maxDuration was negative!  setting to 10', self.maxDuration)
            self.maxDuration = 10.0

    def playEvents(self, eventTiming, source, target = None, callbackFn = None, **kargs):
        for actorName, event in self.events:
            if event.eventTiming() == eventTiming:
                try:
                    actor = self.actors[actorName]
                except:
                    actor = None

                duration = min(event.go(self, actor, source, target, **kargs), self.maxDuration)
                if actorName != '':
                    if not self.lengths.has_key(actorName):
                        self.lengths[actorName] = duration
                    else:
                        self.lengths[actorName] = max(self.lengths[actorName], duration)
                self.totalDuration = max(duration, self.totalDuration)

        return self.totalDuration

    def go(self, source, target = None, callbackFn = None, **kargs):
        if self.timer.going():
            return
        self.timer.reserve()
        self.lengths = {}
        self.totalDuration = 0.0
        for actorName, attacher in self.joints.items():
            attacher.attach(self.actors[actorName], source, target)

        self.playEvents(IMMEDIATE_EVENT, source, target, callbackFn, **kargs)
        BigWorld.callback(0.001, lambda : self.go2(source, target, callbackFn, **kargs))

    def go2(self, source, target, callbackFn, **kargs):
        self.playEvents(TRANSFORM_DEPENDENT_EVENT, source, target, callbackFn, **kargs)
        for actorName, duration in self.lengths.items():
            if duration <= 0.0:
                duration = self.maxDuration
                self.totalDuration = self.maxDuration
            self.timers[actorName].begin(duration, partial(self.detach, actorName, source, target))

        if self.totalDuration > self.maxDuration or self.totalDuration <= 0.0:
            WARNING_MSG('using maxDuration for this effect. perhaps this was unexpected?', self.fileName, self, source, target)
            self.totalDuration = self.maxDuration
        kargs['totalDuration'] = self.totalDuration
        kargs['actorDurations'] = self.lengths
        self.playEvents(DURATION_DEPENDENT_EVENT, source, target, callbackFn, **kargs)
        self.timer.begin(self.totalDuration, lambda : self.stop(source, target, callbackFn))
        self.timer.release()

    def detach(self, actorName, source, target):
        self.joints[actorName].detach(self.actors[actorName], source, target)

    def stop(self, source, target, callbackFn):
        if callbackFn:
            callbackFn()

    def extendTime(self, event, duration):
        for actorName, ev in self.events:
            if event == ev:
                self.timers[actorName].extend(duration)

        self.timer.extend(duration)


overruns = {}
sfxBuffer = {}

def outputOverruns():
    global overruns
    if len(overruns.keys()) == 0:
        return
    DEBUG_MSG('---------------SFX Buffer Overruns------------------')
    DEBUG_MSG('Warning - during that run, some buffered sfx ran out')
    DEBUG_MSG('')
    for fileName, (discard, largest) in overruns.items():
        DEBUG_MSG(fileName, largest)

    overruns = {}
    DEBUG_MSG('----------------------------------------------------')


def cleanupBufferedEffects():
    global sfxBuffer
    sfxBuffer = {}


class BufferedOneShotSFX(OneShotSFX):

    def __init__(self, fileName, maxDuration, queue, prereqs = None):
        OneShotSFX.__init__(self, fileName, maxDuration, prereqs)
        self.queue = queue

    def stop(self, source, target, callbackFn):
        OneShotSFX.stop(self, source, target, callbackFn)
        self.queue.put(self)


def onAsyncLoadBufferedSFX(fileName, maxDuration, resourceRefs):
    queue = sfxBuffer[fileName]
    queue.put(BufferedOneShotSFX(fileName, maxDuration, queue, resourceRefs))


def preloadBufferedOneShotSFX(fileName, maxDuration = 10.0, prereqs = None):
    pSection = None
    if prereqs != None:
        pSection = prereqs[fileName]
    else:
        pSection = ResMgr.openSection(fileName)
    if not pSection:
        ERROR_MSG('Could not open file', fileName)
        return False
    else:
        sfxBuffer[fileName] = Queue()
        queue = sfxBuffer[fileName]
        bufferSize = pSection.readInt('bufferSize', 10)
        if prereqs != None:
            resourceIDs = tuple(prereqs.keys())
            queue.put(BufferedOneShotSFX(fileName, maxDuration, queue, prereqs))
            for i in xrange(0, bufferSize - 1):
                BigWorld.loadResourceListBG(resourceIDs, partial(onAsyncLoadBufferedSFX, fileName, maxDuration))

        else:
            for i in xrange(0, bufferSize):
                queue.put(BufferedOneShotSFX(fileName, maxDuration, queue))

        return True


def getBufferedOneShotSFX(fileName, maxDuration = 10.0, prereqs = None):
    if not sfxBuffer.has_key(fileName):
        if preloadBufferedOneShotSFX(fileName, maxDuration, prereqs) == False:
            return None
    queue = sfxBuffer[fileName]
    if not queue.empty():
        if overruns.has_key(fileName):
            current, largest = overruns[fileName]
            overruns[fileName] = (0, largest)
        return queue.get()
    else:
        if not overruns.has_key(fileName):
            overruns[fileName] = (1, 1)
        else:
            current, largest = overruns[fileName]
            overruns[fileName] = (current + 1, max(largest, current + 1))
        return None
        return None


def bufferedOneShotSFX(fileName, source, target = None, callbackFn = None, maxDuration = 10.0, prereqs = None, **kargs):
    s = getBufferedOneShotSFX(fileName, maxDuration, prereqs)
    if s:
        s.maxDuration = maxDuration
        s.go(source, target, callbackFn, **kargs)


class PersistentSFX(SFX):

    def __init__(self, fileName = None, prereqs = None):
        SFX.__init__(self, fileName)
        SFX.create(self, prereqs)
        self.timer = EventTimer()
        self.source = None
        self.target = None
        return

    def attach(self, source):
        self.source = source
        for actor, attacher in self.joints.items():
            attacher.attach(self.actors[actor], source)

    def go(self, target = None, callbackFn = None, **kargs):
        self.totalDuration = 0.0
        self.target = target
        for actorName, event in self.events:
            if event.eventTiming() == 0:
                try:
                    actor = self.actors[actorName]
                except:
                    actor = None

                self.totalDuration = max(self.totalDuration, event.go(self, actor, self.source, target, **kargs))

        BigWorld.callback(0.001, lambda : self.go2(target, callbackFn, **kargs))
        return

    def go2(self, target = None, callbackFn = None, **kargs):
        for actorName, event in self.events:
            if event.eventTiming() > 0:
                try:
                    actor = self.actors[actorName]
                except:
                    actor = None

                self.totalDuration = max(self.totalDuration, event.go(self, actor, self.source, target, **kargs))

        if callbackFn:
            self.timer.begin(self.totalDuration + 0.001, callbackFn)
        return

    def stop(self):
        stopTime = 0.0
        for actorName, event in self.events:
            actor = self.actors[actorName]
            stopTime = max(stopTime, event.stop(actor, self.source, self.target))

        return stopTime

    def goNextFrame(self, target = None, callbackFn = None, **kargs):
        self.go(target, callbackFn, **kargs)

    def detach(self):
        for actor, attacher in self.joints.items():
            attacher.detach(self.actors[actor], self.source)

        self.source = None
        self.target = None
        return


import Pixie
queue = Queue()
import actors
import events
import moreEvents
import timedEvents
import joints
import shockwave
from events import IMMEDIATE_EVENT
from events import TRANSFORM_DEPENDENT_EVENT
from events import DURATION_DEPENDENT_EVENT