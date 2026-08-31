# Embedded file name: scripts/common/Chunks.py
import BigWorld
import ResMgr
from Math import Vector3
CHUNK_SIZE = 100

class ARRANGE:
    ABOVE, BELOW, INSIDE, SAME_LEVEL = xrange(4)


def _segments_intersect(a_min, a_max, b_min, b_max):
    return b_min < a_min < b_max or b_min < a_max < b_max or a_min < b_max < a_max


class AARect:
    """Axis-aligned rectangle"""

    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

    def intersect_rect(self, rect):
        return _segments_intersect(self.x_min, self.x_max, rect.x_min, rect.x_max) and _segments_intersect(self.z_min, self.z_max, rect.z_min, rect.z_max)


class BoundingBox:

    def __init__(self, min_point, max_point):
        self.min_point = Vector3(min_point)
        self.max_point = Vector3(max_point)


def get_segment(d):
    """Return borders of one of the chunk dimensions (x or z)"""
    n = d // CHUNK_SIZE * CHUNK_SIZE
    return (n, n + CHUNK_SIZE)


def get_chunk_data(space_name, position, _chunks_cache = {}):
    chunk_full_name = BigWorld.findChunkFromPoint(position, space_name)
    try:
        return _chunks_cache[chunk_full_name]
    except KeyError:
        chunk_name = chunk_full_name.split('@')[0]
        chunk_id, internal_chunk = chunk_name[:7], True if chunk_name[7] == 'i' else False
        if internal_chunk:
            chunk_bb = ResMgr.openSection('spaces/' + space_name + '/' + chunk_name + '.chunk/boundingBox')
            min_point, max_point = chunk_bb['min'].asVector3, chunk_bb['max'].asVector3
        else:
            x_min, x_max = get_segment(x)
            z_min, z_max = get_segment(z)
            min_point, max_point = Vector3(x_min, 0, z_min), Vector3(x_max, 0, z_max)
        data = _chunks_cache[chunk_full_name] = {'name': chunk_full_name,
         'internal': internal_chunk,
         'bb': BoundingBox(min_point, max_point),
         'rect': AARect(min_point.x, min_point.z, max_point.x, max_point.z)}
        return data


def get_chunks_arrangement(space_name, position1, position2):
    chunk1 = get_chunk_data(space_name, position1)
    chunk2 = get_chunk_data(space_name, position2)
    if chunk1['name'] == chunk2['name']:
        return ARRANGE.SAME_LEVEL
    bb1, bb2 = chunk1['bb'], chunk2['bb']
    if chunk1['internal'] and chunk2['internal']:
        if bb1.min_point.y >= bb2.max_point.y:
            return ARRANGE.ABOVE
        elif bb2.min_point.y >= bb1.max_point.y:
            return ARRANGE.BELOW
        else:
            return ARRANGE.SAME_LEVEL
    elif not chunk1['internal'] or not chunk2['internal']:
        if chunk1['rect'].intersect_rect(chunk2['rect']):
            return ARRANGE.INSIDE
        else:
            return ARRANGE.SAME_LEVEL