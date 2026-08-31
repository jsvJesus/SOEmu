# Embedded file name: scripts/client/Anomaly.py
import random
from functools import partial
import BigWorld
import FX
from FX_extension import PersistentSFX
from AnomalyCommon import AnomalyCommon
from Damager import Damager

class Anomaly(BigWorld.Entity, AnomalyCommon, Damager):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.loaded_resources = None
        return

    def required_resources(self):
        self.state = self.get_config('default_state')
        resources = ['models/misc/particles/helper_attach.model']
        state_config = self.get_state_config()
        if state_config['particles']:
            resources.append(state_config['particles'])
        if state_config['particlesOut']:
            resources.append(state_config['particlesOut'])
        if state_config['sfx_self']:
            resources.extend(FX.prerequisites(state_config['sfx_self']))
        if state_config['sfx_target']:
            resources.extend(FX.prerequisites(state_config['sfx_target']))
        return resources

    def prerequisites(self):
        return self.required_resources()

    def Update(self):
        if BigWorld.camera().position.distTo(self.position) <= 30.0:
            self.attachParticles('in')
            self.sound.play()
        else:
            self.attachParticles('out')
            self.sound.stop()
        BigWorld.callback(1, self.Update)

    def onEnterWorld(self, prereqs):
        self.filter = BigWorld.AvatarDropFilter()
        self.loaded_resources = prereqs
        if 'models/misc/particles/helper_attach.model' not in self.loaded_resources.failedIDs:
            self.model = self.loaded_resources['models/misc/particles/helper_attach.model']
        self.initialize()
        self.Update()

    def onLeaveWorld(self):
        self.finalize()

    def reset_params(self, anomalyType, state):
        """ Works like anomaly was recreated. """
        self.finalize()
        self.anomalyType = anomalyType
        self.state = state
        BigWorld.loadResourceListBG(self.required_resources(), partial(self.on_resources_loaded, self.initialize))

    def change_state(self, state):
        """Direct state change. Don't use set_state callback to react on state change."""
        self.finalize_state()
        self.state = state
        BigWorld.loadResourceListBG(self.required_resources(), partial(self.on_resources_loaded, self.initialize_state))

    def on_resources_loaded(self, callback, resources):
        if self.inWorld:
            self.loaded_resources = resources
            callback()

    def initialize(self):
        self.initialize_state()

    def initialize_state(self):
        res = self.loaded_resources
        state_config = self.get_state_config()
        if state_config['particlesOut'] and state_config['particlesOut'] not in res.failedIDs:
            self.particles = res[state_config['particlesOut']]
            self.model.root.attach(self.particles)
        else:
            self.particles = None
        if state_config['sfx_self']:
            self.sfx_self = PersistentSFX(state_config['sfx_self'], self, 'Scene Root')
            self.sfx_self_callback = BigWorld.callback(self.get_sfx_delay(), self.repeatSfx)
        else:
            self.sfx_self = None
            self.sfx_self_callback = None
        if state_config['sfx_target']:
            self.sfx_target = FX.OneShot(state_config['sfx_target'])
        else:
            self.sfx_target = None
        if state_config['sound']:
            self.sound = BigWorld.playSound(state_config['sound'], self.model)
        else:
            self.sound = None
        return

    def attachParticles(self, type):
        try:
            res = self.loaded_resources
            state_config = self.get_state_config()
            inParticle = res[state_config['particles']]
            OutParticle = res[state_config['particlesOut']]
            if inParticle is None and not OutParticle:
                inParticle = OutParticle
            if OutParticle is None and not inParticle:
                OutParticle = inParticle
        except:
            print 'problem in anomaly!!!!!!!!!!, view file scripts\\common\\data\\Anomalies\\_config_.json, anomaly type ', self.anomalyType

        if self.particles:
            self.model.root.detach(self.particles)
            self.particles = None
        if type == 'in':
            self.particles = inParticle
            self.model.root.attach(self.particles)
        else:
            self.particles = OutParticle
            self.model.root.attach(self.particles)
        return

    def finalize(self):
        self.finalize_state()
        self.loaded_resources = None
        return

    def finalize_state(self):
        if self.particles:
            self.model.root.detach(self.particles)
            self.particles = None
        if self.sfx_self_callback is not None:
            BigWorld.cancelCallback(self.sfx_self_callback)
            self.sfx_self_callback = None
        if self.sfx_self:
            self.sfx_self.stop()
            self.sfx_self = None
        if self.sfx_target:
            self.sfx_target = None
        if self.sound:
            self.sound.stop()
            self.sound = None
        return

    def get_sfx_delay(self):
        interval = self.get_state_config()['sfx_self_interval']
        return interval['min'] + random.random() * (interval['max'] - interval['min'])

    def repeatSfx(self):
        if self.sfx_self:
            self.sfx_self.play()
        self.sfx_self_callback = BigWorld.callback(self.get_sfx_delay(), self.repeatSfx)

    def onShot(self, target_id):
        if self.sfx_target:
            entity = BigWorld.entities.get(target_id)
            if entity:
                self.sfx_target.go(self, entity)