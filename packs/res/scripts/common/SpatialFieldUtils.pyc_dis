# Embedded file name: scripts/common/SpatialFieldUtils.py
from Math import Vector3
from Chunks import CHUNK_SIZE
HALF_CHUNK_SIZE = CHUNK_SIZE / 2
CELL_SIZE = 5.0
CELL_CENTER = CELL_SIZE * 0.5

def getChunk(position):
    """ returns chunk number for both axes """
    chunkX = position.x // CHUNK_SIZE
    chunkZ = position.z // CHUNK_SIZE
    return (int(chunkX), int(chunkZ))


def toChunkCoord(value):
    """ maps value to [0; CHUNK_SIZE) interval """
    if value < 0:
        return -(value // CHUNK_SIZE) * CHUNK_SIZE + value
    else:
        return value % CHUNK_SIZE


def getChunkCenter(chunkX, chunkZ):
    return Vector3(chunkX * CHUNK_SIZE + HALF_CHUNK_SIZE, 0, chunkZ * CHUNK_SIZE + HALF_CHUNK_SIZE)


def getCell(position):
    """ returns cell number, no matter what chunk """
    cellX = int(toChunkCoord(position.x) // CELL_SIZE)
    cellZ = int(toChunkCoord(position.z) // CELL_SIZE)
    return (cellX, cellZ)


def getCellPosition(chunkX, chunkZ, cellX, cellZ):
    """ converts chunk and cell coords to world coords"""
    return Vector3(chunkX * CHUNK_SIZE + cellX * CELL_SIZE + CELL_CENTER, 0, chunkZ * CHUNK_SIZE + cellZ * CELL_SIZE + CELL_CENTER)