# Embedded file name: scripts/client/client_utils.py
__author__ = 'mon'
import BigWorld
from Math import Vector3, Matrix
MatrixProvider = Matrix.__bases__[0]
from utils_bw import isinstance_ext
PARTICLES_HELPER_MODEL = 'models/misc/particles/helper_attach.model'
TEST_BALL_MODEL = 'helpers/models/unit_sphere.model'
TEST_BALL_MODEL_2 = 'models/bolvan/sfera.model'
BLYAK_MODEL = 'characters/creatures/blyak/blyak_lod1.model'
EMPTY_MODEL = 'models/misc/particles/helper_attach.model'
LARGE_INVISIBLE_BOX = 'models/bolvan/box_micro.model'

def direct_model(model, direction):
    """Direct model x-axis to defined direction."""
    direction = Vector3(direction)
    direction.normalise()
    model.alignToVector(direction, model.position, False)


def direct_model_to(model, object_to):
    """Direct model x-axis to position defined by Vector3/Matrix/MatrixProvider."""
    if isinstance(object_to, MatrixProvider):
        object_pos = Matrix(object_to).translation
    elif isinstance(object_to, Matrix):
        object_pos = object_to.translation
    else:
        object_pos = object_to
    direct_model(model, object_pos - model.position)


def entitiesOfClass(className):
    return [ e for e in BigWorld.entities.values() if isinstance_ext(e, className) ]


ents = entitiesOfClass

def get_action_frame_rate(action, duration):
    return action.frameRate * action.duration / duration


def execute_model_action(action, duration = None, callback = None):
    callback_delay = 0
    if action:
        if duration is None:
            duration = action.duration
        if duration == 0:
            action()
        elif duration > 0:
            framerate = get_action_frame_rate(action, duration)
            action(0, None, 0, -1, -1, framerate)
            callback_delay = duration - 3 / framerate
    if callback:
        if callback_delay > 0:
            return BigWorld.callback(callback_delay, callback)
        callback()
    return


def get_entity_name(entity, utf8 = False):
    if hasattr(entity, 'name'):
        name = entity.name
    elif isinstance_ext(entity, 'Creature'):
        name = entity.get_name()
    else:
        name = ''
    if utf8:
        if isinstance(name, unicode):
            return name
        return name.decode('utf-8')
    elif isinstance(name, str):
        return name
    else:
        return name.encode('utf-8')