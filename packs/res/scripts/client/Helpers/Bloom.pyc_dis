# Embedded file name: scripts/client/Helpers/Bloom.py
import GUI
import BigWorld
import ResMgr
import Math
bloomDebug = None
bloomController = Math.Vector4Morph()
bloomColourAttenuation = Math.Vector4Morph()
preloadedXML = ResMgr.openSection('scripts/data/bloom.xml', True)

def toggleDebugGUI():
    """This function turns on and off a bloom debug GUI, which displays
    the various intermediate render targets used by blooming.
    """
    global bloomDebug
    if not bloomDebug:
        w = GUI.Window('')
        w.position = (0, -0.75, 1)
        w.s1 = GUI.Simple('')
        w.s2 = GUI.Simple('')
        w.s3 = GUI.Simple('')
        GUI.addRoot(w)
        bloomDebug = w
        w.visible = False
    w = bloomDebug
    w.visible = not w.visible
    w.size = (1.5, 0.5)
    w.s1.size = (0.5, 0.5)
    w.s1.position = (-0.5, 0, 1)
    w.s1.materialFX = 'SOLID'
    w.s2.size = (0.5, 0.5)
    w.s2.position = (-0.0, 0, 1)
    w.s2.mapping = ((0, 1),
     (0, 0),
     (1, 0),
     (1, 1))
    w.s2.materialFX = 'SOLID'
    w.s3.size = (0.5, 0.5)
    w.s3.position = (0.5, 0, 1)
    w.s3.materialFX = 'SOLID'
    w.s1.texture = BigWorld.getTextureFeed('wasteOfMemory')
    w.s2.texture = BigWorld.getTextureFeed('bloom')
    w.s3.texture = BigWorld.getTextureFeed('bloom2')


def getCurrentBloomControllerSettings():
    base = 'Client Settings/fx/Bloom/'
    nPasses = int(BigWorld.getWatcher(base + 'num passes'))
    power = float(BigWorld.getWatcher(base + 'scale power'))
    width = float(BigWorld.getWatcher(base + 'width'))
    cutoff = float(BigWorld.getWatcher(base + 'hi-pass cutoff'))
    return (nPasses,
     power,
     width,
     cutoff)


def getCurrentBloomAttenuationSettings():
    base = 'Client Settings/fx/Bloom/'
    s = BigWorld.getWatcher(base + 'colour attenuation')
    att = Math.Vector4([ float(i) for i in s.strip('(,)').split(',') ])
    return att


def savePreset(name):
    """This function saves the current bloom settings to bloom.xml data section
    that is referenced at the top of this file.  It saves it to the specified
    name and can be loaded at a later time using selectBloomPreset.
    """
    preset = preloadedXML[name]
    if not preset:
        preset = preloadedXML.createSection(name)
    base = 'Client Settings/fx/Bloom/'
    preset.writeBool('enable', bool(BigWorld.getWatcher(base + 'enable')))
    preset.writeInt('filterMode', int(BigWorld.getWatcher(base + 'filter mode')))
    att = getBloomAttenuationSettings()
    preset.writeVector4('attenuation', att)
    nPasses, power, width, cutoff = getCurrentBloomControllerSettings()
    preset.writeInt(nPasses)
    preset.writeFloat(power)
    preset.writeFloat(width)
    preset.writeBool('bloomAndBlur', bool(BigWorld.getWatcher(base + 'bloom and blur')))
    preloadedXML.save()


def loadStyle(ds, fadeSpeed = 1.0):
    """Load a bloom style from any data section"""
    base = 'Client Settings/fx/Bloom/'
    if ds != None:
        BigWorld.setWatcher(base + 'enable', ds.readBool('enable', True))
        BigWorld.setWatcher(base + 'filter mode', ds.readInt('filterMode', 1))
        BigWorld.setWatcher(base + 'bloom and blur', ds.readBool('bloomAndBlur', True))
        BigWorld.bloomController(bloomController)
        BigWorld.bloomColourAttenuation(bloomColourAttenuation)
        bloomColourAttenuation.duration = fadeSpeed
        bloomController.duration = fadeSpeed
        bloomController.target = getCurrentBloomControllerSettings()
        bloomController.time = bloomController.duration
        bloomColourAttenuation.target = getCurrentBloomAttenuationSettings()
        bloomColourAttenuation.time = bloomColourAttenuation.duration
        bloomColourAttenuation.target = ds.readVector4('attenuation', (1, 1, 1, 1))
        np = ds.readInt('numPasses', 2)
        pw = ds.readFloat('power', 8)
        wd = ds.readFloat('width', 1.0)
        bloomController.target = (np,
         pw,
         wd,
         1)
    return


def selectPreset(name, fadeSpeed = 1.0):
    """This function loads the named bloom settings from the bloom.xml
    data section that is referenced at the top of this file.  It loads settings
    formerly saved via the saveBloomPreset command.
    """
    ds = preloadedXML[name]
    loadStyle(ds, fadeSpeed)