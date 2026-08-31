# Embedded file name: scripts/client/AnomalyField.py
from functools import partial
from random import uniform
import BigWorld
from Math import Vector3
from utils import hierarchy_get
from AnomalyFieldCommon import AnomalyFieldCommon
from Config import AnomalyFields as Cfg
import SpatialFieldUtils
from FX_extension import SFXGroup, DisposedPersistentSFX

class AnomalyField(BigWorld.Entity, AnomalyFieldCommon):
    GROUND_SEARCH_VECTOR = Vector3(0.0, 1000.0, 0.0)

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.hasEnteredWorld = False
        self.chunkX, self.chunkZ = SpatialFieldUtils.getChunk(self.position)
        self.cellsSFXes = dict()
        self.cellsPositions = []
        self.revealedCells = set()

    def calculateCellPos(self, cellX, cellZ):
        pos = SpatialFieldUtils.getCellPosition(self.chunkX, self.chunkZ, cellX, cellZ)
        collision = BigWorld.collide(self.spaceID, pos - self.GROUND_SEARCH_VECTOR, pos + self.GROUND_SEARCH_VECTOR)
        if collision:
            return collision[0]
        else:
            return None

    def initCellsPositions(self):
        self.cellsPositions = []
        for x in xrange(Cfg.getCellsXNum(self.pattern_id)):
            self.cellsPositions.append([ self.calculateCellPos(x, z) for z in xrange(Cfg.getCellsZNum(self.pattern_id)) ])

    def getCellPos(self, cellX, cellZ):
        return self.cellsPositions[cellX][cellZ]

    def getCellSFXData(self, cellX, cellZ, sfxType):
        return self.get_anomaly_config(cellX, cellZ, Cfg.ANOM_SFXES)[sfxType]

    def createSFXGroup(self, cellX, cellZ, groupName):
        if (cellX, cellZ) not in self.cellsSFXes:
            groups = self.cellsSFXes[cellX, cellZ] = dict()
        else:
            groups = self.cellsSFXes[cellX, cellZ]
        if groupName in groups:
            groups[groupName].destroy()
        groups[groupName] = SFXGroup()
        return groups[groupName]

    def initSFXGroup(self, cellX, cellZ, sfxType):
        sfxesData = self.get_anomaly_config(cellX, cellZ, Cfg.ANOM_SFXES)[sfxType]
        if not sfxesData:
            return None
        else:
            group = self.createSFXGroup(cellX, cellZ, sfxType)
            for sfx_path in sfxesData:
                pos = self.getCellPos(cellX, cellZ)
                if pos:
                    align_x_axis_to = Vector3(1, 0, 0)
                    group.addSFX(DisposedPersistentSFX(sfx_path, self, pos, align_x_axis_to))

            return group

    def getSFXGroup(self, cellX, cellZ, groupName):
        group = hierarchy_get(self.cellsSFXes, [(cellX, cellZ), groupName])
        if not group:
            group = self.initSFXGroup(cellX, cellZ, groupName)
        return group

    def playSFX(self, cellX, cellZ, groupName):
        group = self.getSFXGroup(cellX, cellZ, groupName)
        if group:
            group.play()

    def playOnceSFX(self, cellX, cellZ, groupName):
        group = self.getSFXGroup(cellX, cellZ, groupName)
        if group:
            group.playOnce()

    def stopSFX(self, cellX, cellZ, groupName):
        group = self.getSFXGroup(cellX, cellZ, groupName)
        if group:
            group.stop()

    def onEnterWorld(self, prereqs):
        if self.hasEnteredWorld:
            print '\tAnomalyField.onEnterWorld: has already entered world'
        if self.pattern_id == '':
            self.pattern_id = 'mushroom1'
        if self.group_id == '':
            self.group_id = 'group1'
        self.initCellsPositions()
        self.set_configuration(self.pattern_id, self.group_id)
        self.hasEnteredWorld = True

    def set_configuration(self, pattern_id, group_id):
        self.stop_all_sfxes()
        self.cellsSFXes = dict()
        self.pattern_id = pattern_id
        self.group_id = group_id
        self.start_all_sfxes()

    def start_all_sfxes(self):
        for x, z in self.each_cell():
            self.playSFX(x, z, 'persistent')
            if (x, z) in self.revealedCells:
                self.playSFX(x, z, 'revealed')

    def stop_all_sfxes(self):
        for x, z in self.each_cell():
            self.stopSFX(x, z, 'persistent')
            self.stopSFX(x, z, 'warning')
            if (x, z) in self.revealedCells:
                self.stopSFX(x, z, 'revealed')

    def revealCell(self, cellX, cellZ):
        self.playSFX(cellX, cellZ, 'revealed')
        self.revealedCells.add((cellX, cellZ))

    def hideCell(self, cellX, cellZ):
        self.stopSFX(cellX, cellZ, 'revealed')
        self.playOnceSFX(cellX, cellZ, 'hide')
        cell = (cellX, cellZ)
        if cell in self.revealedCells:
            self.revealedCells.remove(cell)

    def start_warning(self):
        for x, z in self.each_cell():
            self.playSFX(x, z, 'warning')
            self.stopSFX(x, z, 'persistent')