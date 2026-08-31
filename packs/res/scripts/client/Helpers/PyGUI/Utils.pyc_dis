# Embedded file name: scripts/client/Helpers/PyGUI/Utils.py
import BigWorld, GUI, Math

def applyMapping(component, mappingType, mapping):
    if mappingType == 'PIXEL':
        texture = component.texture
        if texture:
            clipMapping = [None,
             None,
             None,
             None]
            width = component.texture.width
            height = component.texture.height
            clipMapping[0] = (float(mapping[0][0]) / width, float(mapping[0][1]) / height)
            clipMapping[1] = (float(mapping[1][0]) / width, float(mapping[1][1]) / height)
            clipMapping[2] = (float(mapping[2][0]) / width, float(mapping[2][1]) / height)
            clipMapping[3] = (float(mapping[3][0]) / width, float(mapping[3][1]) / height)
            component.mapping = tuple(clipMapping)
        else:
            component.mapping = mapping
    else:
        component.mapping = mapping
    return


def mouseScreenPosition():
    clipPos = GUI.mcursor().position
    res = GUI.screenResolution()
    return ((clipPos[0] + 1.0) / 2.0 * res[0], (-clipPos[1] + 1.0) / 2.0 * res[1])


def moveBy(component, (x, y, z)):
    component.position = (component.position[0] + x, component.position[1] + y, component.position[2] + z)
    for child in component.children:
        moveBy(child[1], (x, y, z))


def moveTo(c, (x, y, z)):
    ox, oy, oz = x - c.position[0], y - c.position[1], z - c.position[2]
    moveBy(c, (ox, oy, oz))


def recurseSetColour(colour, c):
    c.colour = colour
    for name, i in c.children:
        recurseSetColour(colour, i)


def nearestRelativeParent(component, depth = 0):
    if depth > 0 and hasattr(component, 'maxScroll'):
        return component
    elif component.parent is None:
        return
    else:
        return nearestRelativeParent(component.parent, depth + 1)
        return


def clipSize(component):
    horzMode = component.widthMode
    vertMode = component.heightMode
    component.widthMode = 'CLIP'
    component.heightMode = 'CLIP'
    width = component.width
    height = component.height
    component.widthMode = horzMode
    component.heightMode = vertMode
    return (width, height)


def legacyPosition(component):
    p = Math.Vector3()
    horzMode = component.horizontalPositionMode
    vertMode = component.verticalPositionMode
    component.horizontalPositionMode = 'LEGACY'
    component.verticalPositionMode = 'LEGACY'
    p = Math.Vector3(component.position)
    component.horizontalPositionMode = horzMode
    component.verticalPositionMode = vertMode
    return p


def clipPosition(component):
    p = Math.Vector3()
    horzMode = component.horizontalPositionMode
    vertMode = component.verticalPositionMode
    component.horizontalPositionMode = 'CLIP'
    component.verticalPositionMode = 'CLIP'
    p = Math.Vector3(component.position)
    component.horizontalPositionMode = horzMode
    component.verticalPositionMode = vertMode
    return p


def absoluteClipPosition(component):
    pos = legacyPosition(component)
    nrp = nearestRelativeParent(component)
    while nrp is not None:
        nrpPos = legacyPosition(nrp)
        pos.x += nrpPos.x
        pos.y += nrpPos.y
        nrp = nearestRelativeParent(nrp)

    return pos


class Budget:

    def __init__(self, creationFn, deletionFn):
        self.creator = creationFn
        self.reaper = deletionFn
        self.items = []

    def balance(self, num):
        newItems = []
        have = len(self.items)
        want = num
        budget = have - want
        while budget < 0:
            g = self.creator()
            newItems.append(g)
            self.items.append(g)
            budget = budget + 1

        while budget > 0:
            self.reaper(self.items.pop())
            budget = budget - 1

        return newItems


class GridLayoutManager:

    def __init__(self, horiziontalFirst = 1):
        self.horiziontalFirst = horiziontalFirst
        self.windowlessChildren = 0
        self.margin = 0.0
        self.stride = 0
        self.numRows = 0
        self.numItems = 0

    def doLayout(self, parent):
        if self.horiziontalFirst:
            self.doHorizontalLayout(parent)
        else:
            self.doVerticalLayout(parent)

    def doHorizontalLayout(self, parent):
        x = parent.position[0] - parent.width / 2 + self.margin / 2
        y = parent.position[1] + parent.height / 2 - self.margin / 2
        r = parent.width + x
        self.stride = 0
        self.numRows = 0
        self.numItems = len(parent.children)
        for discard, i in parent.children:
            w = i.width
            h = i.height
            i.position = (x + w / 2, y - h / 2, i.position[2])
            if self.windowlessChildren:
                for discard, j in i.children:
                    j.position = i.position

            x = x + w + self.margin
            if self.numRows == 0:
                self.stride = self.stride + 1
            if x > r - w:
                x = parent.position[0] - parent.width / 2 + self.margin / 2
                y = y - h - self.margin
                self.numRows = self.numRows + 1

        if x > -parent.width / 2:
            self.numRows = self.numRows + 1

    def doVerticalLayout(self, parent):
        x = parent.position[0] - parent.width / 2 + self.margin / 2
        y = parent.position[1] + parent.height / 2 - self.margin / 2
        b = y - parent.height
        self.stride = 0
        self.numRows = 0
        for discard, i in parent.children:
            w = i.width
            h = i.height
            i.position = (x + w / 2, y - h / 2, i.position[2])
            if self.windowlessChildren:
                for discard, j in i.children:
                    j.position = i.position

            y = y - h - self.margin
            if self.stride == 0:
                self.numRows = self.numRows + 1
            if y < b + h:
                x = x + w + self.margin
                y = parent.position[1] + parent.height / 2 - self.margin / 2
                self.stride = self.stride + 1

        if y < parent.height / 2:
            self.stride = self.stride + 1