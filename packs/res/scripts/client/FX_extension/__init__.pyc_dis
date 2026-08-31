# Embedded file name: scripts/client/FX_extension/__init__.py
from functools import partial
import BigWorld
from Math import Vector3, MatrixProduct, Matrix
import FX
import client_utils
from math_bw import VECTOR3_ZERO, VECTOR3_UP
from matrix_providers import ScaleProvider

def get_sfx_model(entity):
    """ Is used to create/retrieve special model to attach sfxes to it.
        It's needed, because entities sometimes change their main models
        (e.g. avatar equips armor) - and particles are destroyed.
    
        LARGE_INVISIBLE_BOX model is used to allow particles to be visible
        even if main model is not - e.g. behind fence
    
        TODO: allow box size customization on the basis of entity
    """
    if not hasattr(entity, '__sfx_model__'):
        model = BigWorld.Model(client_utils.LARGE_INVISIBLE_BOX)
        d = 3
        model.addMotor(BigWorld.Servo(ScaleProvider(entity.matrix, (d, d, d))))
        entity.addModel(model)
        entity.__sfx_model__ = model
    return entity.__sfx_model__


class SFXEffect:

    def playOnce(self, target_nodes = None):
        pass

    def play(self, target_nodes = None):
        pass

    def stop(self):
        pass

    def destroy(self, hard_destroy = False):
        pass


class iSFXDisposer:

    def __init__(self, sfx, owner_entity, position = VECTOR3_ZERO, direction = VECTOR3_UP):
        self.disposed_model = BigWorld.Model(client_utils.PARTICLES_HELPER_MODEL)
        sfx.set_node_name('Scene Root')
        try:
            sfx.attach(self.disposed_model)
        except AttributeError:
            pass

        self.owner_entity = owner_entity
        self.owner_entity.addModel(self.disposed_model)
        self.set_position(position)
        self.set_direction(direction)

    def set_position(self, position):
        """Place sfx to defined position."""
        self.disposed_model.position = position

    def set_direction(self, direction):
        """Direct sfx to defined direction."""
        client_utils.direct_model(self.disposed_model, direction)

    def set_direction_to(self, object_to):
        """Direct sfx to position defined by Vector3/Matrix/MatrixProvider."""
        client_utils.direct_model_to(self.disposed_model, object_to)

    def __del__(self):
        try:
            self.owner_entity.delModel(self.disposed_model)
        except ValueError:
            pass


class PersistentSFXBase(SFXEffect):

    def __init__(self, sfx_path):
        self.destroyed = False
        self.path = sfx_path
        self.sfx = FX.PersistentExt(self.path)

    def playOnce(self, TargetNodes = None):
        self.sfx.stop()
        self.sfx.go(TargetNodes=TargetNodes or [], callbackFn=self.stop)

    def play(self, TargetNodes = None):
        self.sfx.stop()
        self.sfx.go(TargetNodes=TargetNodes or [])

    def stop(self):
        self.sfx.stop()

    def destroy(self, hard_destroy = False):
        if self.destroyed:
            return
        self.stop()
        if hard_destroy:
            self.sfx.detach()
        else:
            self.sfx.event_no_particles(self.sfx.detach)
        self.destroyed = True

    def __del__(self):
        self.destroy()


class PersistentSFX(PersistentSFXBase):

    def __init__(self, sfx_path, source, source_node_name = None):
        PersistentSFXBase.__init__(self, sfx_path)
        if isinstance(source, BigWorld.Entity) and source_node_name is None:
            self.source = get_sfx_model(source)
        else:
            self.source = source
        if source_node_name is not None:
            self.sfx.set_node_name(source_node_name)
        self.sfx.attach(self.source)
        return


class DisposedPersistentSFX(PersistentSFXBase, iSFXDisposer):

    def __init__(self, sfx_path, owner_entity, position = VECTOR3_ZERO, direction = VECTOR3_UP):
        PersistentSFXBase.__init__(self, sfx_path)
        iSFXDisposer.__init__(self, self.sfx, owner_entity, position, direction)

    def __del__(self):
        PersistentSFXBase.__del__(self)
        iSFXDisposer.__del__(self)


class DisposedOneShotSFX:

    def __init__(self, sfx_path, owner_entity = None):
        self.path = sfx_path
        self.sfx = FX.OneShotExt(self.path)
        self.sfx.set_node_name('Scene Root')
        self.owner_entity = owner_entity or BigWorld.player()

    def play(self, position = VECTOR3_ZERO, direction = VECTOR3_UP, direct_to = None, TargetNodes = None):
        disposed_model = BigWorld.Model(client_utils.PARTICLES_HELPER_MODEL)
        self.owner_entity.addModel(disposed_model)
        disposed_model.position = position
        if direct_to:
            client_utils.direct_model_to(disposed_model, direct_to)
        else:
            client_utils.direct_model(disposed_model, direction)
        self.sfx.go(disposed_model, TargetNodes=TargetNodes or [], callbackFn=partial(self.owner_entity.delModel, disposed_model))


class SFXGroup:

    def __init__(self):
        self.sfxes = set()

    def addSFX(self, sfx):
        self.sfxes.add(sfx)

    def play(self):
        for sfx in self.sfxes:
            sfx.play()

    def playOnce(self):
        for sfx in self.sfxes:
            sfx.playOnce()

    def stop(self):
        for sfx in self.sfxes:
            sfx.stop()


def preload_buffered_oneshot_sfx(sfx_path):
    if not sfx_path:
        return
    prereqs = FX.prerequisites(sfx_path)
    BigWorld.loadResourceListBG(prereqs, partial(FX.getBufferedOneShotEffect, sfx_path))