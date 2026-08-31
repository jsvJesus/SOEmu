# Embedded file name: scripts/client/Creature.py
"""
Created on 18.08.2010

@author: muzhig
"""
from functools import partial
import BigWorld
from Math import Vector3
import particles
from utils import hierarchy_get, multi_get
from client_utils import execute_model_action
from Victim import Victim
from Damager import Damager
from sounds import playSound
from Effects import Effects
from Teleportable import Teleportable
from CreatureCommon import CreatureCommon
from Skills import Skills, Skill
from Config import Creatures as Cfg
from Config.Creatures import get_state_name, BrainStates
from Bleeding import Bleeding
from Colliders import COLLIDER_NODE_NAME, COLLIDER_BOX_NAME, COLLIDER_BODY_ZONE, COLLIDER_MIN_BOUNDS, COLLIDER_MAX_BOUNDS
dictNames = {'Spider': 0,
 'Bear': 1,
 'Dog': 2,
 'Boar': 3,
 'Rat': 4,
 'Verlioka': 5,
 'Blyak': 6,
 'Bes': 7,
 'Brutor': 8,
 'Outcast': 9,
 'Vedun': 10,
 'Silvan': 11,
 'Jelly': 12,
 'Noob_dog': 13,
 'Worm_hulud': 14,
 'Impenetrable': 15}
creatureNames = dict()
for entry in dictNames:
    creatureNames[dictNames[entry]] = entry

sfx_Impenetrable = {-1: 'sfx/Shoot/heavy_metall_hit.xml',
 0: 'sfx/Shoot/body_hit_d_red_max.xml'}
{-1: 'sfx/Shoot/body_hit_d_red_max.xml'}
sfx_def = {-1: 'sfx/Shoot/body_hit.xml'}
bleed_sfx = {'Impenetrable': sfx_Impenetrable,
 'Bes': {-1: 'sfx/Shoot/body_hit_d_red_max.xml'},
 'Spider': {-1: 'sfx/Shoot/body_hit_green_max.xml'},
 'Verlioka': {-1: 'sfx/Shoot/body_hit_green_max.xml'},
 'Worm_hulud': {-1: 'sfx/Shoot/plastic_hit.xml'}}
_bleed_sfx = dict(((dictNames[name], path) for name, path in bleed_sfx.items()))
from soGUI.soInworldMarkers import soInworldMarker
brainStateToIcon = {BrainStates.ATTACK_NO_TARGET: None,
 BrainStates.ATTACK_COOLDOWN: soInworldMarker.MARKER_USE,
 BrainStates.ATTACK_SUCCESS: soInworldMarker.MARKER_USE,
 BrainStates.ATTACK_TOO_FAR: None,
 BrainStates.GO_PROMENADE: soInworldMarker.MARKER_TRADE,
 BrainStates.GO_NEXT_WAYPOINT: soInworldMarker.MARKER_PLAYER,
 BrainStates.FOLLOW_TARGET: soInworldMarker.MARKER_PICKUP,
 BrainStates.DEAD: soInworldMarker.MARKER_PK}

class EntityFXAction:

    def __init__(self, entity, actions = None, sounds = None, sfxes = None):
        self.entity = entity
        self.actions = actions if actions is not None else []
        self.sounds = sounds if sounds is not None else []
        self.sfxes = sfxes if sfxes is not None else []
        self.active_callbacks = {}
        return

    def run(self, duration = None, callback = None, restart = False):

        def model_action_callback(index, name):
            del self.active_callbacks[index]
            if not self.active_callbacks and callback:
                callback()

        if not self.active_callbacks or restart:
            self.active_callbacks = {}
            for index, act_name in enumerate(self.actions):
                self.active_callbacks[index] = None
                handle = self.run_model_action(act_name, duration, partial(model_action_callback, index, act_name))
                if handle:
                    self.active_callbacks[index] = handle

            for sound_path in self.sounds:
                self.run_sound(sound_path)

            for sfx_path in self.sfxes:
                self.run_sfx(sfx_path)

        return

    def cancel_callbacks(self):
        for callback_handle in self.active_callbacks.values():
            if callback_handle:
                BigWorld.cancelCallback(callback_handle)

        self.active_callbacks = {}

    def stop(self):
        self.cancel_callbacks()
        for action_name in self.actions:
            self.stop_model_action(action_name)

        for sound_path in self.sounds:
            pass

        for sfx_path in self.sfxes:
            pass

    def run_model_action(self, action_name, duration, callback):
        pass

    def run_sound(self, sound_path):
        pass

    def run_sfx(self, sfx_path):
        pass

    def stop_model_action(self, action_name):
        pass


class CompositeFXAction:

    def __init__(self, mob):
        self.mob = mob
        self.actions = []
        self.current_action = None
        self.run_callback = None
        return

    def add_action(self, action_name):
        self.actions.append(CreatureFXAction(self.mob, action_name))

    def run(self, duration = None, callback = None, restart = False):
        if not self.actions:
            return
        else:
            if self.current_action is None or restart:
                self.current_action = -1

                def run_next_action():
                    self.current_action += 1
                    if self.current_action < len(self.actions):
                        self.actions[self.current_action].run(duration, run_next_action, restart)
                    else:
                        self.current_action = None
                        callback()
                    return

                run_next_action()
            return

    def stop(self):
        if self.current_action is not None:
            self.actions[self.current_action].stop()
            self.current_action = None
        return


class CreatureFXAction(EntityFXAction):

    def __init__(self, entity, action_name):
        self.action_name = action_name
        try:
            config = entity.get_config(Cfg.ACTIONS)[self.action_name]
        except KeyError:
            print 'DESIGNER_ERROR: CreatureFXAction: creature({0} {1}) has no action {2}'.format(entity.creatureType, Cfg.get_subtype_name(entity.creatureType, entity.level), action_name)

        actions, sounds, sfxes = multi_get(config, Cfg.ACT_MODEL_ACTIONS, Cfg.ACT_SOUNDS, Cfg.ACT_SFXES)
        EntityFXAction.__init__(self, entity, actions, sounds, sfxes)

    def run_model_action(self, action_name, duration, callback):
        try:
            action = self.entity.model.action(action_name)
        except ValueError:
            print 'DESIGNER_WARNING: creature {0} level {1} has no action {2}'.format(self.entity.creatureType, self.entity.level, action_name)
            return

        return execute_model_action(action, duration, callback)

    def run_sound(self, sound_path):
        self.entity.playSoundM(sound_path, self.entity.model)

    def stop_model_action(self, action_name):
        self.entity.model.action(action_name).stop()


class Creature(BigWorld.Entity, CreatureCommon, Victim, Damager, Skills, Effects, Teleportable, Bleeding):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        Skills.__init__(self)
        self.filter = BigWorld.AvatarDropFilter()
        self.model = None
        self.soundsList = []
        self.state_transition_callback = None
        self.actions = {}
        return

    def onEnterWorld(self, prereqs):
        if self.get_model_path() not in prereqs.failedIDs:
            self.model = prereqs[self.get_model_path()]
        action_matcher = self.model.motors[0]
        action_matcher.entityCollision = 0
        action_matcher.collisionRooted = 0
        action_matcher.collisionHeight = self.get_height()
        action_matcher.collisionRadius = self.get_width() * 0.5
        action_matcher.collisionMoveSpeed = 2.0
        action_matcher.turnModelToEntity = True
        scale = self.get_config(Cfg.MODEL_SCALE)
        self.model.scale = Vector3(scale, scale, scale)
        tints_cfg = self.get_config(Cfg.TINTS)
        for tint_name, tint_value in tints_cfg[self.tint_id].items():
            try:
                self.model.__setattr__(tint_name, tint_value)
            except Exception as e:
                print 'Creature.onEnterWorld: wrong tint ({0} = {1}) for self {2}, lv {3}'.format(tint_name, tint_value, self.creatureType, self.level)
                raise

        self.add_collider()
        foot_nodes = self.get_config(Cfg.FOOT_NODES)
        if foot_nodes:
            self.addFootTrigers(foot_nodes[0], foot_nodes[1])
        self.checkDecomposed()
        self._set_current_state(self.state)

    def get_model_path(self):
        return Cfg.MODELS_ROOT + self.get_config(Cfg.MODEL)

    def _set_current_state(self, new_state):
        """Direct state change."""
        new_state_config = self.get_config(Cfg.STATES)[new_state]
        self.model.motors[0].matchCaps = list(new_state_config['caps'])
        for action in new_state_config.get('persistent_actions', []):
            self.do_named_action(action)

        self.current_state = new_state

    def change_state(self, prev_state, new_state):
        """Start state transition."""
        if self.state_transition_callback is not None:
            BigWorld.cancelCallback(self.state_transition_callback)
            self.state_transition_callback = None
        curr_state_config = self.get_state_config(self.current_state)
        new_state_config = self.get_state_config(new_state)
        self.current_state = new_state
        entering_data = curr_state_config.get('entering_actions', {})
        for action in entering_data.get('actions', []):
            self.get_action(action).cancel_callbacks()

        for action in curr_state_config.get('persistent_actions', []):
            self.stop_named_action(action)

        self.model.motors[0].matchCaps = list(new_state_config['caps'])
        trans_data = hierarchy_get(curr_state_config, ['transitions', new_state])
        if trans_data and trans_data['time'] > 0:
            for action in trans_data['actions']:
                self.do_named_action(action, duration=trans_data['time'])

            self.state_transition_callback = BigWorld.callback(trans_data['time'], partial(self._init_new_state, new_state))
        else:
            self._init_new_state(new_state)
        return

    def _init_new_state(self, new_state):
        new_state_config = self.get_state_config(new_state)
        entering_data = new_state_config['entering_actions']
        if entering_data and entering_data['time'] > 0:
            callbacks_needed = len(entering_data['actions'])

            def action_ended():
                action_ended.callbacks_received += 1
                if action_ended.callbacks_received == callbacks_needed:
                    self._set_current_state(new_state)

            action_ended.callbacks_received = 0
            for action in entering_data['actions']:
                self.do_named_action(action, duration=entering_data['time'], callback=action_ended)

        else:
            self._set_current_state(new_state)

    def get_action(self, action_name):
        try:
            return self.actions[action_name]
        except KeyError:
            self.actions[action_name] = CreatureFXAction(self, action_name)
            return self.actions[action_name]

    def do_named_action(self, action_name, duration = None, callback = None):
        self.get_action(action_name).run(duration, callback)

    def stop_named_action(self, action_name):
        self.get_action(action_name).stop()

    def event_fired(self, event_name):
        for action_name in self.get_config(Cfg.EVENTS).get(event_name, []):
            self.do_named_action(action_name)

    def create_skill(self, skill_id):
        skill_cfg = self.get_skill_config(skill_id)
        skill = Skill(self)
        for action_name in skill_cfg['actions']:
            skill.add_action(action_name)

        def add_sfxes(cfg_key, method):
            for sfx_cfg in skill_cfg.get(cfg_key, {}):
                play_time = sfx_cfg['play_time']
                method(sfx_path=sfx_cfg['path'], source_node_name=sfx_cfg['source_node'], target_node_name=sfx_cfg.get('target_node'), direct_to_target=bool(sfx_cfg['direct_to_target']), delay=sfx_cfg['delay'], play_time=play_time if play_time > 0 else None)

            return

        add_sfxes(Cfg.SKILL_SELF_SFXES, skill.add_sfx_on_self)
        add_sfxes(Cfg.SKILL_TARGET_SFXES, skill.add_sfx_on_target)
        return skill

    def prerequisites(self):
        list = [self.get_model_path()]
        return list

    def add_collider(self):
        Victim.add_collider(self)
        for box_cfg in self.get_config(Cfg.COLLIDERS):
            self.attach_collider_box(box_cfg[COLLIDER_BOX_NAME], box_cfg[COLLIDER_NODE_NAME], box_cfg[COLLIDER_BODY_ZONE], box_cfg[COLLIDER_MIN_BOUNDS], box_cfg[COLLIDER_MAX_BOUNDS])

    def addFootTrigers(self, lFootNodeName, rFootNodeName):
        lfoot = self.model.node(lFootNodeName)
        rfoot = self.model.node(rFootNodeName)
        footSoundPath = self.get_config(Cfg.FOOTSTEPS_SOUND)
        if footSoundPath == '':
            print 'Creature::addFootTrigers: No sound specified for ', self.creatureType
            return
        self.footTriggers = [BigWorld.FootTrigger(0, footSoundPath), BigWorld.FootTrigger(1, footSoundPath)]
        lfoot.attach(self.footTriggers[0])
        rfoot.attach(self.footTriggers[1])
        for footTrigger in self.footTriggers:
            footTrigger.maxLod = 25

        self.dustSource = particles.attachDustSource(self.model)

    def checkDecomposed(self):
        if self.isDecomposed:
            BigWorld.delShadowEntity(self)
            self.model.visible = False
        else:
            self.model.visible = True
            BigWorld.addShadowEntity(self)

    def onLeaveWorld(self):
        self.stopSounds()

    def set_isDecomposed(self, b):
        self.checkDecomposed()

    def on_death(self, source_data, noSound = False):
        Victim.on_death(self, source_data)
        self.stopSounds()

    def on_damaged(self, source_data, damagetaken_data):
        Victim.on_damaged(self, source_data, damagetaken_data)
        self.bleed_on_damage(source_data, damagetaken_data)
        if not self.is_dead():
            self.event_fired(Cfg.EV_ON_TAKE_DAMAGE)

    def blood_sfx_on_damage(self, damage_source, damagetaken_data):
        body_zone = damagetaken_data['body_zone']
        sfx_byzone = _bleed_sfx.get(self.creatureType, sfx_def)
        eff = sfx_byzone.get(body_zone, sfx_byzone[-1])
        return eff

    def bleed_on_damage(self, damage_source, damagetaken_data):
        if damage_source['entity_id'] == BigWorld.player().id:
            return
        damager = BigWorld.entity(damage_source['entity_id'], True)
        blood_rel_pos = self.blood_rel_pos(damagetaken_data['body_zone']) + self.position
        if damager:
            bloodvector = self.position - damager.position + blood_rel_pos - (0, 1, 0)
            damager_pos = damager.position + (0, 1, 0)
            damager_dir = blood_rel_pos - damager_pos
            doCollide = self.skeletonCollider.doCollide(damager_pos, damager_dir)
            if doCollide:
                blood_rel_pos = self.skeletonCollider.impactPoint
        else:
            bloodvector = (0, 1, 0)
        sfx_id = self.blood_sfx_on_damage(damage_source, damagetaken_data)
        self.bleedglobal(blood_rel_pos, bloodvector, sfx_id)

    def playSoundM(self, soundPath, model):
        if not soundPath:
            return
        else:
            sound = playSound(soundPath, model)
            if sound is None:
                return
            if sound.duration < 0:
                self.soundsList.append(sound)
            return sound

    def stopSounds(self):
        for s in xrange(len(self.soundsList)):
            sound = self.soundsList[s]
            if sound is not None:
                sound.stop()

        self.soundsList = []
        return

    def beginAnimation(self, animationID, duration):
        pass

    def endAnimation(self, animationID):
        pass

    def onTeleportCalled(self, teleport_type, expected_position):
        self.filter = BigWorld.DumbFilter()

    def onTeleportEnded(self, wasSuccessful):
        self.filter = BigWorld.AvatarDropFilter()