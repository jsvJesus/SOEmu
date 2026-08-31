# Embedded file name: scripts/common/Waypoint.py
import BigWorld

class Waypoint:
    EMPTY_POS = (0.0, 0.0, 0.0)
    EMPTY_ID = 0
    EMPTY_RADIUS = 0.0

    def __init__(self, **properties):
        self.position = properties.get('position', Waypoint.EMPTY_POS)
        self.id = properties.get('id', Waypoint.EMPTY_ID)
        self.radius = properties.get('radius', Waypoint.EMPTY_RADIUS)

    def set_id(self, id):
        self.id = id

    @staticmethod
    def fromUDO(udo, id = 0):
        if udo and udo.__class__.__name__ == 'WaypointUDO':
            try:
                pos = udo.position
                rad = udo.radius
                return Waypoint(id=id, position=pos, radius=rad)
            except BigWorld.UnresolvedUDORefException:
                pass


class WaypointConverter:

    def getDictFromObj(self, obj):
        return dict(id=obj.id, position=obj.position, radius=obj.radius)

    def createObjFromDict(self, dic):
        return Waypoint(**dic)

    def isSameType(self, obj):
        return isinstance(obj, Waypoint)


converter = WaypointConverter()