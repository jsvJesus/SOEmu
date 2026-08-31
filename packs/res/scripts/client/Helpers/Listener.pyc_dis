# Embedded file name: scripts/client/Helpers/Listener.py
import copy

class Listenable:
    """
            An interface that specifies an object may be listened to. Derive from
            this class, then call self.listeners.eventeventName when an event occurs. It
            will go through the list of listeners and call the specified method
            name on the listener object, if it exists.
    """

    def __init__(self):
        self.listeners = _Listeners()

    def addListener(self, eventName, fn):
        self.listeners.addListener(eventName, fn)

    def removeListener(self, eventName, fn):
        self.listeners.removeListener(eventName, fn)


class _Listeners(object):

    def __init__(self):
        self.listeners = {}

    def addListener(self, eventName, fn):
        if eventName not in self.listeners:
            self.listeners[eventName] = list()
        self.listeners[eventName].append(fn)

    def removeListener(self, eventName, fn):
        if eventName in self.listeners:
            if fn in self.listeners[eventName]:
                self.listeners[eventName].remove(fn)
            if not len(self.listeners[eventName]):
                del self.listeners[eventName]

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return _ListenerDispatch(self, name)


class _ListenerDispatch:

    def __init__(self, dispatcher, eventName):
        self.dispatcher = dispatcher
        self.eventName = eventName

    def __call__(self, *args, **kargs):
        if self.eventName not in self.dispatcher.listeners:
            return
        functions = self.dispatcher.listeners[self.eventName]
        for fn in copy.copy(functions):
            fn(*args, **kargs)