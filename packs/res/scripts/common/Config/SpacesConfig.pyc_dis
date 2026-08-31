# Embedded file name: scripts/common/Config/SpacesConfig.py
import json
import Config
from time import gmtime
SPACES_PATH = Config.DATA_PATH + 'Spaces.json'
DEFAULT_START_GLOBAL_TIME = '00:00'
DEFAULT_START_LOCAL_TIME = '00:00'
DEFAULT_PERIOD_DURATION = 24
SECONDS_IN_DAY = 86400
DEFAULT_PERIOD_NAME = 'default'
try:
    import ResMgr
    dataSection = ResMgr.openSection(SPACES_PATH)
    data = json.loads(dataSection.asBinary)
except ImportError:
    configPath = Config.__file__
    parts = configPath.split('\\')
    efConfigPath = '\\'.join(parts[:-2]) + '\\data\\Spaces.json'
    s = open(efConfigPath, 'r').read()
    data = json.loads(s)

spaces = data.get('Spaces', {})
defaults = spaces.get('defaults', {})
if defaults:
    DEFAULT_PERIOD_DURATION = defaults.get('period_duration', DEFAULT_PERIOD_DURATION)
    DEFAULT_START_GLOBAL_TIME = defaults.get('start_global_time', DEFAULT_START_GLOBAL_TIME)
    DEFAULT_START_LOCAL_TIME = defaults.get('start_local_time', DEFAULT_START_LOCAL_TIME)

def getInitialSpaceTime(space_name):

    def calcParam(start_time, period_duration, start_local_time):
        sec_in_sec = SECONDS_IN_DAY / period_duration
        dict_time = gmtime()
        now_passed = dict_time.tm_hour * 3600 + dict_time.tm_min * 60
        game_current_seconds = start_time - now_passed
        passed_real_seconds_from_last_start = SECONDS_IN_DAY - game_current_seconds
        passed_game_time_from_last_start = passed_real_seconds_from_last_start * sec_in_sec
        passed_seconds = passed_game_time_from_last_start + start_local_time
        passed_seconds = passed_seconds % SECONDS_IN_DAY
        return (passed_seconds, sec_in_sec)

    space = spaces.get(space_name, dict())
    if not space:
        print "SpaceConfig::getInitialSpaceTime Can't find config for space {0}. Using default value.".format(space_name)
    start_time = space.get('start_global_time', DEFAULT_START_GLOBAL_TIME)
    start_h, start_m = start_time.split(':')
    start_time = int(start_h) * 3600 + int(start_m) * 60
    period_duration = space.get('period_duration', DEFAULT_PERIOD_DURATION)
    period_duration *= 3600
    start_local_time = space.get('start_local_time', DEFAULT_START_LOCAL_TIME)
    start_local_h, start_local_m = start_local_time.split(':')
    start_local_time = int(start_local_h) * 3600 + int(start_local_m) * 60
    return calcParam(start_time, period_duration, start_local_time)


def getPeriodNameOnID(space_name, id):
    periods_info = defaults.get('periods', dict())
    space = spaces.get(space_name)
    if space:
        periods_info.update(space.get('periods', dict()))
    for period_name in periods_info.keys():
        if hash(period_name) & 4294967295L == id:
            return str(period_name)

    return ''


def getIDOnPeriodName(period_name):
    return hash(period_name) & 4294967295L


def getPeriodsOnSpaceName(space_name):
    periods_info = defaults.get('periods', dict())
    space = spaces.get(space_name)
    if space:
        periods_info.update(space.get('periods', dict()))
    return periods_info


def getDefaultPeriodName(space_name):
    return str(DEFAULT_PERIOD_NAME)