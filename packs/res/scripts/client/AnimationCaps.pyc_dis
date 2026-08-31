# Embedded file name: scripts/client/AnimationCaps.py
__author__ = 'muzhig'
__animation_caps__ = {}
import ResMgr

def loadAnimationCaps():
    if not __animation_caps__:
        for state in ResMgr.openSection('scripts/common/capabilities.xml').values():
            if state.name == 'state':
                __animation_caps__[state['name'].asString] = state.asInt


loadAnimationCaps()

def getCapByName(cap_name):
    return __animation_caps__.get(cap_name)


def setCap(model, cap_name, value = True):
    cap = getCapByName(cap_name)
    if cap is None:
        raise ValueError("Cap '%s' not exists!" % cap_name)
    matchCaps = model.motors[0].matchCaps
    if value == (cap in matchCaps):
        return
    else:
        if value:
            matchCaps.append(cap)
        else:
            matchCaps.remove(cap)
        model.motors[0].matchCaps = matchCaps
        return


def clearCaps(model):
    model.motors[0].matchCaps = []


def setCapsList(model, cap_names, value = True, exclusive = True):
    if exclusive:
        clearCaps(model)
    for cap_name in cap_names:
        setCap(model, cap_name, value)