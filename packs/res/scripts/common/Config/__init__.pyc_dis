# Embedded file name: scripts/common/Config/__init__.py
import json
from utils import hierarchial_update
import ResMgr
AVATAR_AOI_RANGE = 150
COMMON_PATH = 'scripts/common/'
DATA_PATH = COMMON_PATH + 'data/'

def remove_json_comments(json_string):
    return '\n'.join((s for s in json_string.split('\n') if not s.lstrip().startswith('#')))


def load_json(path):
    ResMgr.purge(path)
    data_section = ResMgr.openSection(path)
    if data_section is None:
        return
    else:
        return json.loads(data_section.asBinary)
        return