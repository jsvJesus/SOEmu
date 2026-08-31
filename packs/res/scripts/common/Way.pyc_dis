# Embedded file name: scripts/common/Way.py
from Waypoint import Waypoint
import BigWorld
from random import choice

class Way:
    RANDOM, CYCLED_FIRST_AFTER_LAST, CYCLED_PREV_AFTER_LAST, GO_ONCE, EMPTY = xrange(5)
    FORWARD, BACKWARD = xrange(2)
    DIRECTION_INVERSE = {FORWARD: BACKWARD,
     BACKWARD: FORWARD}
    DIRECTION_SHIFT = {FORWARD: 1,
     BACKWARD: -1}

    def __init__(self, **properties):
        self.waypoints = properties.get('waypoints', [])
        self.name = properties.get('name', '')
        self.wayType = properties.get('wayType', Way.EMPTY)
        self.wayDirection = properties.get('wayDirection', Way.FORWARD)

    def getNextWaypoint(self, waypoint_id):

        def searchWP(waypoint_id):
            for i, wp in enumerate(self.waypoints):
                if wp.id == waypoint_id:
                    return i

            return None

        if not self.waypoints:
            return
        elif self.wayType == Way.RANDOM:
            return choice(self.waypoints)
        else:
            if self.wayType == Way.GO_ONCE:
                found = searchWP(waypoint_id)
                if found is None:
                    return self.waypoints[0]
                elif found == len(self.waypoints) - 1:
                    return
                else:
                    return self.waypoints[found + 1]
            else:
                found = searchWP(waypoint_id)
                if found is None:
                    return self.waypoints[0]
                if self.wayType == Way.CYCLED_FIRST_AFTER_LAST:
                    next = self.waypoints[(found + Way.DIRECTION_SHIFT[self.wayDirection]) % len(self.waypoints)]
                    return next
                if self.wayType == Way.CYCLED_PREV_AFTER_LAST:
                    if found in [0, len(self.waypoints) - 1]:
                        self.wayDirection = Way.DIRECTION_INVERSE[self.wayDirection]
                    return self.waypoints[(found + Way.DIRECTION_SHIFT[self.wayDirection]) % len(self.waypoints)]
                return
            return

    @staticmethod
    def fromUDO(udo, failIfHasNotReadyWaypoints = True):
        if udo and udo.__class__.__name__ == 'WayUDO':
            try:
                wayType = udo.wayType
                name = udo.name
                waypoints = []
                index = 0
                for waypointUDO in udo.waypoints:
                    index += 1
                    if waypointUDO:
                        if waypointUDO.__class__.__name__ == 'WaypointUDO':
                            try:
                                wp = Waypoint.fromUDO(waypointUDO, id=index)
                                if wp is not None:
                                    waypoints.append(wp)
                                    continue
                            except BigWorld.UnresolvedUDORefException:
                                pass

                        elif waypointUDO.__class__.__name__ != 'UserDataObjectRef':
                            print 'Way (GUID ' + udo.guid + ') has wrong WaypointUDO: ', waypointUDO.__class__.__name__
                            try:
                                print 'WRONG Waypoint.GUID:', waypointUDO.guid
                            except:
                                pass

                    if failIfHasNotReadyWaypoints:
                        return False

                if not waypoints:
                    print 'Way (GUID ' + udo.guid + ') has no connected WaypointUDOs'
                return Way(name=name, wayType=wayType, waypoints=waypoints)
            except BigWorld.UnresolvedUDORefException:
                pass

        return


class Converter:

    @staticmethod
    def getDictFromObj(obj):
        return dict(name=obj.name, wayType=obj.wayType, wayDirection=obj.wayDirection, waypoints=obj.waypoints)

    @staticmethod
    def createObjFromDict(dic):
        return Way(**dic)

    @staticmethod
    def isSameType(obj):
        return isinstance(obj, Way)