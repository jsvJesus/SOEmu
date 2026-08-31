# Embedded file name: scripts/client/sfx/joints.py
from sfx import s_sectionProcessors
from sfx import typeCheck
from bwdebug import *
import BigWorld
import traceback

class Joint:

    def __init__(self):
        pass

    def load(self, pSection, prereqs = None):
        return self

    def attach(self, actor, source, target = None):
        pass

    def detach(self, actor, source, target = None):
        pass


class SingletonJoint(Joint):

    def __init__(self):
        Joint.__init__(self)

    def __call__(self):
        return self


class Entity(SingletonJoint):

    def attach(self, actor, source, target = None):
        typeCheck(actor, [BigWorld.Entity])
        if actor.attached:
            ERROR_MSG('actor is already attached!', self, actor, source)
            return 0
        try:
            source.addModel(actor)
        except:
            ERROR_MSG('error in addModel to entity', self, actor, source)

        moved = 0
        try:
            actor.addMotor(BigWorld.Servo(actor.matrix))
            moved = 1
        except AttributeError:
            try:
                actor.explicitPosition = source.position
                moved = 1
            except AttributeError:
                try:
                    for i in xrange(0, actor.nSystems()):
                        actor.system(i).explicitPosition = source.position

                    moved = 1
                except:
                    traceback.print_exc()
                    traceback.print_stack()

        if not moved:
            ERROR_MSG('Unknown error trying to move actor to the correct location', actor, source)

    def detach(self, actor, source, target = None):
        if not actor.attached:
            ERROR_MSG('actor is not attached!', self, actor, source)
            return 0
        try:
            source.delModel(actor)
        except:
            ERROR_MSG('error in delModel from entity', self, actor, source)


s_entity = Entity()
s_sectionProcessors['Entity'] = s_entity

class ModelRoot(SingletonJoint):

    def attach(self, actor, source, target = None):
        if actor.attached:
            ERROR_MSG('actor is already attached!', self, actor, source)
            return 0
        try:
            source.root.attach(actor)
        except:
            try:
                source.model.root.attach(actor)
            except:
                ERROR_MSG('error in addModel to modelRoot', self, actor, source)

    def detach(self, actor, source, target = None):
        if not actor.attached:
            return 0
        try:
            source.root.detach(actor)
        except Exception as ex1:
            try:
                if hasattr(source, 'isDestroyed'):
                    if source.isDestroyed:
                        return
                source.model.root.detach(actor)
            except Exception as ex:
                ERROR_MSG('error in detach from modelRoot', self, actor, source, ex)


s_modelRoot = ModelRoot()
s_sectionProcessors['ModelRoot'] = s_modelRoot

class Node(Joint):

    def load(self, pSection, prereqs = None):
        self.nodeName = pSection.asString
        return self

    def attach(self, actor, source, target = None):
        if actor.attached:
            ERROR_MSG('actor is already attached!', actor, self.nodeName)
            return 0
        try:
            source.model.node(self.nodeName).attach(actor)
        except AttributeError:
            try:
                source.node(self.nodeName).attach(actor)
            except ValueError:
                ERROR_MSG('No such node', self.nodeName)

        except ValueError:
            ERROR_MSG('No such node', self.nodeName)

    def detach(self, actor, source, target = None):
        if not actor.attached:
            ERROR_MSG('actor is not attached!', actor, self.nodeName)
            return 0
        try:
            source.model.node(self.nodeName).detach(actor)
        except AttributeError:
            try:
                source.node(self.nodeName).detach(actor)
            except ValueError:
                ERROR_MSG('No such node', self.nodeName)

        except ValueError:
            ERROR_MSG('No such node', self.nodeName)


s_sectionProcessors['Node'] = Node

class HardPoint(Joint):

    def load(self, pSection, prereqs = None):
        self.hpName = pSection.asString
        return self

    def attach(self, actor, source, target = None):
        if actor.attached:
            ERROR_MSG('actor is already attached!', actor, self.hpName)
            return 0
        try:
            setattr(source.model, self.hpName, actor)
        except AttributeError:
            try:
                setattr(source, self.hpName, actor)
            except AttributeError:
                ERROR_MSG('Missing hardpoint', source, 'HP_' + self.hpName)

        except:
            try:
                setattr(source, self.hpName, actor)
            except:
                ERROR_MSG('Unknown error', source, self.hpName)

    def detach(self, actor, source, target = None):
        if not actor.attached:
            ERROR_MSG('Actor is not attached', actor, self.hpName)
            return 0
        try:
            source.model.node('HP_' + self.hpName).detach(actor)
        except AttributeError:
            try:
                source.node('HP_' + self.hpName).detach(actor)
            except:
                ERROR_MSG('Unknown error', source, self.hpName)


s_sectionProcessors['HardPoint'] = HardPoint
s_sectionProcessors['Hardpoint'] = HardPoint

class LightSource(Joint):

    def load(self, pSection, prereqs = None):
        self.nodeName = pSection.asString
        return self

    def attach(self, actor, source, target = None):
        node = None
        if self.nodeName != '':
            try:
                node = source.node(self.nodeName)
            except TypeError:
                pass
            except ValueError:
                ERROR_MSG('No such node', self.nodeName)

        try:
            if node != None:
                actor.source = node
            else:
                actor.source = source.root
            actor.visible = True
        except:
            ERROR_MSG('error in set light source', self, actor, source)

        return

    def detach(self, actor, source, target = None):
        actor.visible = False
        actor.source = None
        return


s_sectionProcessors['LightSource'] = LightSource

class DummyModel(SingletonJoint):

    def __init__(self):
        SingletonJoint.__init__(self)
        self.dummy = None
        return

    def attach(self, actor, source, target = None):
        if actor.attached:
            ERROR_MSG('actor is already attached!', self, actor, source)
            return 0
        player = BigWorld.player()
        if not player:
            ERROR_MSG('Cannot add effect to dummy model if there is no player.', self, actor, source)
            return 0
        self._ensureDummyExists()
        try:
            self.dummy.root.attach(actor)
        except:
            ERROR_MSG('error in addModel to dummy', self, actor, source)

    def detach(self, actor, source, target = None):
        if not actor.attached:
            ERROR_MSG('actor is not attached!', self, actor, source)
            return 0
        else:
            player = BigWorld.player()
            if player != None:
                self.dummy.root.detach(actor)
            return

    def _ensureDummyExists(self):
        if None is self.dummy:
            self.dummy = BigWorld.Model('')
            self.dummy.visibleAttachments = True
            BigWorld.player().addModel(self.dummy)
            servo = BigWorld.Servo(BigWorld.player().matrix)
            self.dummy.motors = (servo,)
        return


s_dummyModel = DummyModel()
s_sectionProcessors['DummyModel'] = s_dummyModel