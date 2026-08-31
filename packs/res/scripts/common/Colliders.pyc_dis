# Embedded file name: scripts/common/Colliders.py
import ResMgr
from Config.Damage import get_body_zone
COLLIDER_NODE_NAME = 'nodeName'
COLLIDER_BOX_NAME = 'boxName'
COLLIDER_BODY_ZONE = 'bodyZone'
COLLIDER_MIN_BOUNDS = 'minBounds'
COLLIDER_MAX_BOUNDS = 'maxBounds'

def get_colliders_cfg(file_path, reload = False):
    """ Load colliders configuration from xml as exported from 3DMax.
    
            Example:
            <Worm.xml>
              <SkeletonCollider>
                <BoxAttachment>
                  <nodeName>Bone01</nodeName>
                  <boxName>head_Bone01_bwhitbox</boxName>
                  <bodyZone>HEAD</bodyZone>
                  <minBounds>-0.827802 -0.044755 -0.040000</minBounds>
                  <maxBounds>0.962385 0.044755 0.040000</maxBounds>
                </BoxAttachment>
                <BoxAttachment>
                    ...
                </BoxAttachment>
                ...
              </SkeletonCollider>
            </Worm.xml>
    """
    if reload:
        ResMgr.purge(file_path)
    cfg = []
    for entry in ResMgr.openSection(file_path + '/SkeletonCollider').values():
        if entry.name == 'BoxAttachment':
            cfg.append({COLLIDER_NODE_NAME: entry[COLLIDER_NODE_NAME].asString,
             COLLIDER_BOX_NAME: entry[COLLIDER_BOX_NAME].asString,
             COLLIDER_BODY_ZONE: get_body_zone(entry[COLLIDER_BODY_ZONE].asString),
             COLLIDER_MIN_BOUNDS: entry[COLLIDER_MIN_BOUNDS].asVector3,
             COLLIDER_MAX_BOUNDS: entry[COLLIDER_MAX_BOUNDS].asVector3})

    return cfg