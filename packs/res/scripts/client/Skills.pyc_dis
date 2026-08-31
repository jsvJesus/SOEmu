# Embedded file name: scripts/client/Skills.py
from functools import partial
import copy
import BigWorld
from Math import Matrix
import FX
import client_utils
import FX_extension
from Thrower import Thrower

def run_sfx_timed(sfx, target_node, play_time, delay):
    if play_time == -1:
        BigWorld.callback(delay, partial(sfx.playOnce, TargetNodes=[target_node]))
    else:
        BigWorld.callback(delay, partial(sfx.play, TargetNodes=[target_node]))
        BigWorld.callback(delay + play_time, sfx.stop)


class Skill:

    def __init__(self, entity):
        self.entity = entity
        self.actions = []
        self.sfxes_on_self = []
        self.sfxes_on_target = []

    def add_action(self, action_name):
        self.actions.append(action_name)

    def create_sfx_data(self, sfx_path, source_node_name, target_node_name, direct_to_target, delay, play_time):
        if direct_to_target:
            sfx = FX_extension.DisposedPersistentSFX(sfx_path, self.entity)
        else:
            sfx = FX_extension.PersistentSFX(sfx_path, self.entity.model, source_node_name)
        return dict(sfx=sfx, sfx_path=sfx_path, source_node_name=source_node_name, target_node_name=target_node_name, direct_to_target=direct_to_target, delay=delay, play_time=play_time)

    def add_sfx_on_self(self, sfx_path, source_node_name, target_node_name = None, direct_to_target = False, delay = 0, play_time = None):
        sfx_data = self.create_sfx_data(sfx_path, source_node_name, target_node_name, direct_to_target, delay, play_time)
        self.sfxes_on_self.append(sfx_data)

    def add_sfx_on_target(self, sfx_path, source_node_name, target_node_name = None, direct_to_target = False, delay = 0, play_time = None):
        sfx_data = self.create_sfx_data(sfx_path, source_node_name, target_node_name, direct_to_target, delay, play_time)
        self.sfxes_on_target.append(sfx_data)

    def run_sfx(self, sfx_data, source, target):
        sfx = sfx_data['sfx']
        target_node = target.model.node(sfx_data['target_node_name']) if target else None
        if sfx_data['direct_to_target'] and target:

            def wait_for_node_init(node):
                sfx.set_position(Matrix(node).translation)
                sfx.set_direction_to(target_node)
                run_sfx_timed(sfx, target_node, sfx_data['play_time'], sfx_data['delay'])

            source_node = source.model.node(sfx_data['source_node_name'])
            BigWorld.callback(0.0001, partial(wait_for_node_init, source_node))
        else:
            run_sfx_timed(sfx, target_node, sfx_data['play_time'], sfx_data['delay'])
        return

    def use(self, target):
        for action_name in self.actions:
            self.entity.do_named_action(action_name)

        for sfx_data in self.sfxes_on_self:
            self.run_sfx(sfx_data, self.entity, target)

        for sfx_data in self.sfxes_on_target:
            self.run_sfx(sfx_data, target, self.entity)


class Skills(Thrower):
    """ Bot interface. Implements skills using """

    def __init__(self):
        self.__wait_for_throwed = {}
        self.__throwed_entities = {}
        self.__sfxes = {}

    def create_skill(self, skill_id):
        raise NotImplementedError('Skills.create_skill for {0} {1} is not implemented.'.format(self, self.id))

    def get_skill(self, skill_id):
        if not hasattr(self, '_Skills__skills_cache'):
            self.__skills_cache = {}
        try:
            return self.__skills_cache[skill_id]
        except KeyError:
            skill = self.__skills_cache[skill_id] = self.create_skill(skill_id)
            return skill

    def use_skill(self, skill_id, target_id):
        skill = self.get_skill(skill_id)
        target = BigWorld.entities.get(target_id)
        skill.use(target)

    def skill_throwGrenade(self, skill_id, throwed_id):
        if throwed_id in self.__throwed_entities.keys():
            self.onThrowingEntityAppears(BigWorld.entities[throwed_id])
        else:
            self.__wait_for_throwed[throwed_id] = skill_id

    def onThrowingEntityAppears(self, throwed_entity):
        if throwed_entity.id in self.__wait_for_throwed:
            Thrower.onThrowingEntityAppears(self, throwed_entity)
            self.use_skill(self.__wait_for_throwed[throwed_entity.id], 0)
            del self.__wait_for_throwed[throwed_entity.id]
        else:
            self.__throwed_entities[throwed_entity.id] = throwed_entity