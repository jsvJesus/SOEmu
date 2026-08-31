# Embedded file name: scripts/client/particles.py
"""This module provides utility functions for particle systems."""
import BigWorld
import random
import Pixie

def createBloodDroop():
    return Pixie.create('particles/blood_drops.xml')


def createGlow():
    return Pixie.create('particles/glow.xml')


def createRipperDust():
    return Pixie.create('particles/ripper_dust.xml')


def createJetStream():
    return None


def createRipperBreath():
    breath = Pixie.create('particles/ripper_breath.xml')
    breath.system(0).action(1).sleepPeriod = random.randint(40, 80) / 10.0
    return breath


def createDustSource():
    return Pixie.create('particles/dust_source.xml')


def createFragGrenadeExplosion():
    return Pixie.create('particles/fx_frag_grenade_explosion_outside.xml')


def createGroundMist():
    return None


def createEnergySphere(position):
    energySphere = Pixie.create('particles/energy_sphere.xml')
    x, y, z = position
    orbitor = energySphere.system(0).action(10)
    source = energySphere.system(0).action(1)
    sourceRadius = source.getPositionSourceMaxRadius()
    orbitor.point = (x, y + sourceRadius, z)
    return energySphere


def createChimneySmoke():
    return Pixie.create('particles/chimney_smoke.xml')


def createBonfire():
    return Pixie.create('particles/bonfire.xml')


def createBonfireTwo():
    return None


def createRisingSteam():
    return Pixie.create('particles/rising_steam.xml')


def createDustStorm():
    return None


def createDustStormChunks():
    return None


def createSparkExplosion():
    return None


def createPchangSparks():
    return None


def createSmokeTrail():
    return Pixie.create('particles/smoke_trail.xml')


def createFlareTrace():
    return None


def createRespawnMist():
    return Pixie.create('particles/respawn_mist.xml')


def createBloodSpray():
    return None


def createSparks():
    return None


def createDirectedSparks():
    return Pixie.create('particles/directed_sparks.xml')


def createDirectedChunks():
    return None


def attachRipperDust(model):
    trails = createRipperDust()
    if trails != None:
        model.root.attach(trails)
    return trails


def attachRipperBreath(model):
    breath = createRipperBreath()
    if breath != None:
        model.root.attach(breath)
    return breath


def attachDustSource(model):
    ps = createDustSource()
    if ps != None:
        model.root.attach(ps)
    return ps


def attachBoosted(model):
    boosted = createBoosted()
    if boosted != None:
        model.root.attach(boosted)
    return boosted


def attachGroundMist(model):
    mist = createGroundMist()
    if mist != None:
        model.root.attach(mist)
    return mist


def attachEnergySphere(model, position):
    sphere = createEnergySphere(position)
    if sphere != None:
        model.root.attach(sphere)
    return sphere


def attachJetStream(model):
    js = createJetStream()
    if js != None:
        model.root.attach(js)
    return js


def attachChimneySmoke(model):
    cs = createChimneySmoke()
    if cs != None:
        model.root.attach(cs)
    return cs


def attachBonfire(model, animated = True):
    fire = 0
    if animated:
        fire = createBonfire()
    else:
        fire = createBonfireTwo()
    if fire != None:
        model.root.attach(fire)
    return fire


def attachRisingSteam(model):
    steam = createRisingSteam()
    if steam != None:
        model.root.attach(steam)
    return steam


def attachBloodDrop(model):
    blood = createBloodDroop()
    if blood != None:
        model.root.attach(blood)
    return blood


def flickeringLight():
    import Math
    flame_r = 250
    flame_g = 250
    flame_b = 250
    timescale = 0.5
    pulseShader = Math.Vector4Animation()
    pulseShader.duration = 6.6 * timescale
    pulseShader.keyframes = [(0.0 * timescale, (0.35 * flame_r,
       0.35 * flame_g,
       0.35 * flame_b,
       0)),
     (0.6 * timescale, (0.65 * flame_r,
       0.65 * flame_g,
       0.65 * flame_b,
       0)),
     (0.7 * timescale, (0.33 * flame_r,
       0.33 * flame_g,
       0.33 * flame_b,
       0)),
     (0.9 * timescale, (0.65 * flame_r,
       0.65 * flame_g,
       0.65 * flame_b,
       0)),
     (1.2 * timescale, (0.41 * flame_r,
       0.41 * flame_g,
       0.41 * flame_b,
       0)),
     (1.5 * timescale, (0.65 * flame_r,
       0.65 * flame_g,
       0.65 * flame_b,
       0)),
     (1.7 * timescale, (0.41 * flame_r,
       0.41 * flame_g,
       0.41 * flame_b,
       0)),
     (1.9 * timescale, (0.8 * flame_r,
       0.8 * flame_g,
       0.8 * flame_b,
       0)),
     (2.1 * timescale, (0.2 * flame_r,
       0.2 * flame_g,
       0.2 * flame_b,
       0)),
     (2.4 * timescale, (0.92 * flame_r,
       0.92 * flame_g,
       0.92 * flame_b,
       0)),
     (2.7 * timescale, (0.44 * flame_r,
       0.44 * flame_g,
       0.44 * flame_b,
       0)),
     (3.2 * timescale, (0.72 * flame_r,
       0.72 * flame_g,
       0.72 * flame_b,
       0)),
     (3.7 * timescale, (0.32 * flame_r,
       0.32 * flame_g,
       0.32 * flame_b,
       0)),
     (3.9 * timescale, (0.78 * flame_r,
       0.78 * flame_g,
       0.78 * flame_b,
       0)),
     (4.2 * timescale, (0.18 * flame_r,
       0.18 * flame_g,
       0.18 * flame_b,
       0)),
     (4.4 * timescale, (0.86 * flame_r,
       0.86 * flame_g,
       0.86 * flame_b,
       0)),
     (4.8 * timescale, (0.46 * flame_r,
       0.46 * flame_g,
       0.46 * flame_b,
       0)),
     (5.5 * timescale, (0.76 * flame_r,
       0.76 * flame_g,
       0.76 * flame_b,
       0)),
     (5.8 * timescale, (0.22 * flame_r,
       0.22 * flame_g,
       0.22 * flame_b,
       0)),
     (6.3 * timescale, (0.8 * flame_r,
       0.8 * flame_g,
       0.8 * flame_b,
       0)),
     (6.5 * timescale, (0.36 * flame_r,
       0.36 * flame_g,
       0.36 * flame_b,
       0)),
     (6.5 * timescale, (0.54 * flame_r,
       0.54 * flame_g,
       0.54 * flame_b,
       0))]
    pulse = BigWorld.PyChunkLight()
    pulse.innerRadius = 1
    pulse.outerRadius = 10
    pulse.position = (0, 0, 0)
    pulse.shader = pulseShader
    pulse.specular = 1
    pulse.diffuse = 1
    pulse.visible = True
    return pulse