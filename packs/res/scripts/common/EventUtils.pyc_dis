# Embedded file name: scripts/common/EventUtils.py
"""
Created on 23.06.2010

@author: muzhig
"""
import Math

class Context:
    All, Client, Cell, Base, Clients = xrange(0, 5)


typeconsts = {int: 0,
 float: 1,
 list: 2,
 tuple: 2,
 Math.Vector3: 2,
 dict: 3}

def pack(val, floats = None, ints = None):
    if floats is None:
        floats = []
    if ints is None:
        ints = []
    if type(val) == int:
        ints.append(val)
    elif type(val) == float:
        floats.append(val)
    elif type(val) in [list, Math.Vector3, tuple]:
        ints.append(len(val))
        if len(val) > 0:
            ints.append(typeconsts[type(val[0])])
        for element in val:
            pack(element, floats, ints)

    elif type(val) == dict:
        pack(val.keys(), floats, ints)
        pack(val.values(), floats, ints)
    return (floats, ints)


def unpack(datatype, floats, ints, fshift = 0, ishift = 0):
    if datatype == 0:
        return (ints[ishift], 0, 1)
    if datatype == 1:
        return (floats[fshift], 1, 0)
    if datatype == 2:
        val = []
        ishift_temp = ishift
        fshift_temp = fshift
        lenval = ints[ishift]
        ishift += 1
        if lenval > 0:
            valtype = ints[ishift]
            ishift += 1
        for x in xrange(lenval):
            element, fsh, ish = unpack(valtype, floats, ints, fshift, ishift)
            val.append(element)
            ishift += ish
            fshift += fsh

        return (val, fshift - fshift_temp, ishift - ishift_temp)
    if datatype == 3:
        ishift_temp = ishift
        fshift_temp = fshift
        val = {}
        keys, fsh, ish = unpack(2, floats, ints, fshift, ishift)
        ishift += ish
        fshift += fsh
        vals, fsh, ish = unpack(2, floats, ints, fshift, ishift)
        ishift += ish
        fshift += fsh
        for i in xrange(min([len(keys), len(vals)])):
            val[keys[i]] = vals[i]

        return (val, fshift - fshift_temp, ishift - ishift_temp)
        floats, ints = pack([[10, 6],
         (1.6, 1.6, 1.6),
         (1.7, 1.7, 1.7),
         [(1.5, 1.5, 1.5)],
         [],
         [((0, 0.2, 0), (0, 0.2, 0), [10, 0])]])
        print unpack(2, floats, ints)