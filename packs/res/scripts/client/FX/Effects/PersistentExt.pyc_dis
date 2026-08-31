# Embedded file name: scripts/client/FX/Effects/PersistentExt.py
__author__ = 'monitorius'
from functools import partial
import BigWorld
import Pixie
from Persistent import Persistent
from FX.Effects.DynamicNodes import iDynamicNodes

class PersistentExt(Persistent, iDynamicNodes):

    def __init__(self, fileName = None, prereqs = None):
        Persistent.__init__(self, fileName, prereqs)
        iDynamicNodes.__init__(self)
        self.spawn_rates = {}
        self.spawn_stopped = False

    def __str__(self):
        return 'PersistentExt {0}'.format(self.fileName)

    def attach(self, source):
        """ Some particles (like MatrixSwarm) start playing immediately after attach,
            without go() calling. So we need stop() effect right after attaching.
        """
        self.stop()
        Persistent.attach(self, source)

    def go_delayed(self, source = None, target = None, callbackFn = None, delay = 0, **kargs):
        """Run sfx after delay time."""
        if delay:
            BigWorld.callback(delay, partial(self.go, target, callbackFn, **kargs))
        else:
            self.go(target, callbackFn, **kargs)

    def go(self, target = None, callbackFn = None, **kargs):
        self.resume_particles_spawn()
        Persistent.go(self, target, callbackFn, **kargs)

    def stop(self):
        self.stop_particles_spawn()
        Persistent.stop(self)

    def iterate_particle_systems(self):
        """Iterator through all PyParticleSystems of actor."""
        for actor_name, actor in self.actors.items():
            if isinstance(actor, Pixie.MetaParticleSystem):
                for system_ind, system in enumerate([ actor.system(i) for i in range(actor.nSystems()) ]):
                    key = (actor_name, system_ind)
                    yield (key, system)

    def iterate_particle_sources(self):
        """Iterator through all SourcePSA in all particle systems of actor."""
        for (actor_name, system_ind), system in self.iterate_particle_systems():
            for action_ind, action in enumerate(system.actions):
                if isinstance(action, Pixie.SourcePSA):
                    key = (actor_name, system_ind, action_ind)
                    yield (key, action)

    def stop_particles_spawn(self):
        if not self.spawn_stopped:
            for action_key, action in self.iterate_particle_sources():
                self.spawn_rates[action_key] = action.rate
                action.rate = 0

            self.spawn_stopped = True

    def resume_particles_spawn(self):
        if self.spawn_stopped:
            for action_key, action in self.iterate_particle_sources():
                try:
                    action.rate = self.spawn_rates[action_key]
                except KeyError:
                    pass

            self.spawn_stopped = False

    def get_particles_number(self):
        return sum((system.size() for key, system in self.iterate_particle_systems()))

    def event_no_particles(self, callback):

        def check_particles():
            if self.get_particles_number() > 0:
                BigWorld.callback(1, check_particles)
            else:
                callback()

        check_particles()