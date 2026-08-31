# Embedded file name: scripts/client/FX/Effects/OneShotExt.py
__author__ = 'monitorius'
from functools import partial
import BigWorld
from OneShot import OneShot
from FX.Effects.DynamicNodes import iDynamicNodes

class OneShotExt(OneShot, iDynamicNodes):

    def go_delayed(self, source, target = None, callbackFn = None, delay = 0, **kargs):
        if delay:
            BigWorld.callback(delay, partial(self.go, source, target, callbackFn, **kargs))
        else:
            self.go(source, target, callbackFn, **kargs)