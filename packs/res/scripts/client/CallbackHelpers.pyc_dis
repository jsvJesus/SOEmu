# Embedded file name: scripts/client/CallbackHelpers.py
"""This module contains a number of helper functions intended simplify
implementing callback functions in a safe way.
"""
import BigWorld
from collections import defaultdict
import time
import traceback

class callback(object):
    """Wrapper around BigWorld.callback()
    
    # regular callback
    callback(function, 1.5) # returns callback object
    
    # setup callback & cancel any previous callbacks with this function
    callback(function, 2.0, cancel_existing = True)
    
    # setup repeated callback
    c = callback(function, 2.0, interval = 2.0)
    
    # cancel callback - call `cancel` method on callback object,
    # or `callback.cancel` to cancel all callbacks by function
    c.cancel()
    callback.cancel(function)
    callback.cancel(id) # if id was specified when creating callback
    
    # keying: function is key by default, but you can specify id:
    callback(function1, 2.0, cancel_existing = True, id = 'my_special_callback')
    callback(function2, 2.0, cancel_existing = True, id = 'my_special_callback')
    
    # find callbacks: use id as a key, if it was specified, else use function
    callback.findAll('my_special_callback') # return all existing callbacks with this id
    a = callback.findFirst(function) # return all existing callbacks with this function
    a.cancel()
    """
    callbacks = defaultdict(list)

    @staticmethod
    def findAll(id_or_function):
        return list(callback.callbacks[id_or_function])

    @staticmethod
    def findFirst(id_or_function):
        r = callback.callbacks[id_or_function]
        if r:
            return r[0]
        else:
            return None

    @staticmethod
    def cancel(id_or_function):
        existing_callbacks = callback.findAll(id_or_function)
        for found in existing_callbacks[::-1]:
            found.cancel()

        return bool(existing_callbacks)

    def __init__(self, function, delay, interval = None, cancel_existing = False, id = None, error_ignore = False):
        self.id_or_function = id if id is not None else function
        self.cancel = self.__instance_cancel__
        if cancel_existing:
            callback.cancel(self.id_or_function)
        self.callbacks[self.id_or_function].append(self)
        self.interval = interval
        self.delay = delay
        self.error_ignore = error_ignore
        self.bwcallback = None
        self.function = function
        self.__start_bw_callback__()
        return

    def __start_bw_callback__(self, delay = None):
        if self.bwcallback is not None:
            return
        else:
            if delay is None:
                delay = self.delay
            self.expected_callback_time = time.time() + delay
            self.bwcallback = BigWorld.callback(delay, self.__on_bw_callback__)
            return

    def __cancel_bw_callback__(self):
        if self.bwcallback is not None:
            BigWorld.cancelCallback(self.bwcallback)
        self.bwcallback = None
        return

    def __on_bw_callback__(self):
        self.bwcallback = None
        timediff = self.expected_callback_time - time.time()
        if timediff > 0:
            self.__start_bw_callback__(timediff)
            return
        else:
            if self.interval is not None:
                self.__start_bw_callback__(self.interval)
            else:
                self.cancel()
            try:
                self.function()
            except:
                print ''
                traceback.print_exc()
                if self.error_ignore:
                    return
                self.interval = None
                self.cancel()
                self.__cancel_bw_callback__()

            return

    def __instance_cancel__(self):
        self.__cancel_bw_callback__()
        if self in self.callbacks[self.id_or_function]:
            self.callbacks[self.id_or_function].remove(self)


def IgnoreCallbackIfDestroyed(function):

    def checkIfDestroyed(self, *args, **kwargs):
        if not isinstance(self, BigWorld.Entity):
            raise AssertionError
            return self.isDestroyed or function(self, *args, **kwargs)

    return checkIfDestroyed