# Embedded file name: scripts/client/FootPrinter.py
import BigWorld
import time
from Notices import Notices
import SFXer
import Math
import Settings
import sfx
import traceback

class FootPrinter(object):
    DEBUG_PRINT = False
    LEFT_FOOT_NODE = 'leftsole'
    RIGHT_FOOT_NODE = 'rightsole'
    WATER_NODE_HIPS_STAY = 'rightleg'
    WATER_NODE_HIPS_CROUCH = 'spine'
    WATER_NODE_HEAD = 'HP_spine1'
    FOOTSOUNDPATH = 'players/footsteps'
    underWaterLevel1 = 0
    underWaterLevel2 = 0
    underWaterLevel3 = 0
    underWaterPathLevel1 = ''
    underWaterPathLevel2 = ''
    underWaterPathLevel3 = ''
    avatarInWaterLevel = 0
    timeEnterWater1 = 0
    timeWaterExplosionDelta = 0.2

    def createFootTriger(self):
        self.deleteFootTriger()
        self.waterListenerHead = BigWorld.addWaterVolumeListener(self.model.node(self.WATER_NODE_HEAD), self.waterCross3)
        hips = self.WATER_NODE_HIPS_CROUCH if self.crouching else self.WATER_NODE_HIPS_STAY
        self.waterListenerHips = BigWorld.addWaterVolumeListener(self.model.node(hips), self.waterCross2)
        self.waterListener = BigWorld.addWaterVolumeListener(self.matrix, self.waterCross1)
        lfoot = self.model.node(self.LEFT_FOOT_NODE)
        rfoot = self.model.node(self.RIGHT_FOOT_NODE)
        self.footTriggers = [BigWorld.FootTrigger(0, self.FOOTSOUNDPATH), BigWorld.FootTrigger(1, self.FOOTSOUNDPATH)]
        lfoot.attach(self.footTriggers[0])
        rfoot.attach(self.footTriggers[1])
        for triger in self.footTriggers:
            if hasattr(triger, 'underWaterPathLevel1'):
                triger.underWaterPathLevel1 = self.underWaterPathLevel1
            if hasattr(triger, 'underWaterPathLevel2'):
                triger.underWaterPathLevel2 = self.underWaterPathLevel2
            if hasattr(triger, 'underWaterPathLevel3'):
                triger.underWaterPathLevel3 = self.underWaterPathLevel3
            if hasattr(triger, 'underWater'):
                triger.underWater = self.avatarInWaterLevel
            if hasattr(triger, 'footstepWaterCallback'):
                triger.footstepWaterCallback = self.footstepWaterCallback
            if hasattr(triger, 'soundEnable'):
                triger.soundEnable = 0

    def deleteFootTriger(self):
        if getattr(self, 'waterListener', False):
            BigWorld.delWaterVolumeListener(self.waterListener)
            self.waterListener = None
        if getattr(self, 'waterListenerHips', False):
            BigWorld.delWaterVolumeListener(self.waterListenerHips)
            self.waterListenerHips = None
        if getattr(self, 'waterListenerHead', False):
            BigWorld.delWaterVolumeListener(self.waterListenerHead)
            self.waterListenerHead = None
        try:
            self.model.node(self.LEFT_FOOT_NODE).attachments = []
        except:
            pass

        try:
            self.model.node(self.LEFT_FOOT_NODE).attachments = []
        except:
            pass

        self.footTriggers = []
        return

    def waterCross1(self, enterWater, volume):
        self.underWaterLevel1 = int(enterWater)
        self.applyWaterLevel()
        if enterWater:
            self.timeEnterWater1 = time.time()
        self.changeWater([Notices.LEAVE_WATER, Notices.ENTER_WATER], enterWater, volume)

    def waterCross2(self, enterWater, volume):
        self.underWaterLevel2 = int(enterWater)
        self.applyWaterLevel()
        if enterWater:
            self.checkSplashingWater()
        self.changeWater([Notices.LEAVE_WATER_HIPS, Notices.ENTER_WATER_HIPS], enterWater, volume)

    def waterCross3(self, enterWater, volume):
        self.underWaterLevel3 = int(enterWater)
        self.applyWaterLevel()
        self.changeWater([Notices.LEAVE_WATER_HEAD, Notices.ENTER_WATER_HEAD], enterWater, volume)

    def applyWaterLevel(self):
        self.avatarInWaterLevel = max([self.underWaterLevel1, self.underWaterLevel2 * 2, self.underWaterLevel3 * 3])

    def checkSplashingWater(self):
        difTime = time.time() - self.timeEnterWater1
        if self.DEBUG_PRINT:
            print 'difTime', difTime
        if difTime < self.timeWaterExplosionDelta:
            print 'SplashingWater'
            sfx.bufferedOneShotSFX('sfx/waterFoot/splashingWater.xml', self.model)

    def changeWater(self, levels, enterWater, volume):
        if self.DEBUG_PRINT:
            print 'changeWater', self.avatarInWaterLevel
        for triger in self.footTriggers:
            triger.underWater = self.avatarInWaterLevel

        if self != BigWorld.player():
            return
        if enterWater:
            ht = str(volume.surfaceHeight)
            self.cell.notify(levels[int(enterWater)], [ht])
        else:
            self.cell.notify(levels[int(enterWater)], [])

    def footstepWaterCallback(self, vel, odd, underwater, strmsound):
        sound = None
        if underwater:
            if underwater == 1:
                sfxpath = 'sfx/waterFoot/water_foot.xml'
                sfx.bufferedOneShotSFX(sfxpath, self.model)
                node = self.LEFT_FOOT_NODE if odd else self.RIGHT_FOOT_NODE
                toPos = Math.Matrix(self.model.node(node)).translation
                fromPos = toPos + (0, 10, 0)
                waterpos = BigWorld.waterCollide(0, fromPos, toPos)
                if waterpos:
                    waterpos = waterpos[0]
                    SFXer.footWaterStep(self, waterpos, sfxpath, alignToVector=None, lifeTime=3.3)
                    if self.DEBUG_PRINT:
                        print waterpos, sfxpath
            else:
                if underwater == 2:
                    sfxpath = 'sfx/waterFoot/water_hips_'
                if underwater == 3:
                    sfxpath = 'sfx/waterFoot/water_head_'
                if odd:
                    sfxpath += 'left.xml'
                else:
                    sfxpath += 'right.xml'
                if self.DEBUG_PRINT:
                    print sfxpath
                sfx.bufferedOneShotSFX(sfxpath, self.model, maxDuration=4.0)
            path = ['',
             self.underWaterPathLevel1,
             self.underWaterPathLevel2,
             self.underWaterPathLevel3][underwater]
            if path:
                sound = self.model.getSound(path)
        else:
            if 'INVALID_MATERIAL_KIND' in strmsound:
                if self.DEBUG_PRINT:
                    print 'footTrigger INVALID_MATERIAL_KIND'
                return
            sound = self.model.getSound(self.FOOTSOUNDPATH + '/' + strmsound)
        if sound:
            try:
                if vel < 4:
                    speed = 1.0
                elif vel < 8:
                    speed = 2.0
                else:
                    speed = 3.0
                sound.volume = Settings.Settings().getSfxVolume()
                sound.param('Speed').value = speed
                sound.param('LeftRight').value = 0.0 if odd else 1.0
            except:
                pass

            sound.play()
        return

    def drawWaterFire(self, scr, hitPoint):
        if not scr:
            return False
        elif not hitPoint:
            return False
        waterpos = None
        if hasattr(BigWorld, 'waterCollide'):
            waterpos = BigWorld.waterCollide(0, scr, hitPoint)
        self.lastwaterposscr = (scr, hitPoint)
        if waterpos is not None:
            waterpos = waterpos[0]
            waterpos = waterpos + (0, -0.1, 0)
            sfxpath = 'sfx/Shoot/water_hit.xml'
            self.lastwaterpos = waterpos
            SFXer.waterHit(self, waterpos, sfxpath, alignToVector=None, lifeTime=3.3)
            return True
        else:
            return False

    def tooFootUpdateCrouch(self):
        hips = self.WATER_NODE_HIPS_CROUCH if self.crouching else self.WATER_NODE_HIPS_STAY
        try:
            BigWorld.delWaterVolumeListener(self.waterListenerHips)
        except:
            traceback.print_exc()

        self.waterListenerHips = BigWorld.addWaterVolumeListener(self.model.node(hips), self.waterCross2)