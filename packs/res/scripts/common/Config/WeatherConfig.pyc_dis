# Embedded file name: scripts/common/Config/WeatherConfig.py
import json
import Config
from time import gmtime
from random import choice
WEATHER_PATH = Config.DATA_PATH + 'Weather.json'
DEFAULT_WEATHER = 'Clear'
try:
    import ResMgr
    dataSection = ResMgr.openSection(WEATHER_PATH)
    data = json.loads(dataSection.asBinary)
except ImportError:
    configPath = Config.__file__
    parts = configPath.split('\\')
    efConfigPath = '\\'.join(parts[:-2]) + '\\data\\Weather.json'
    s = open(efConfigPath, 'r').read()
    data = json.loads(s)

weather = data.get('Weather', {})
zone_weather = data.get('ZoneWeather', {})
DEFAULT_WEATHER = weather.get('default', DEFAULT_WEATHER)

def getPeriodsOnSpaceName(space_name):
    return weather.get(space_name, {})


def getDefaultWeather(space_name):
    periods = getPeriodsOnSpaceName(space_name)
    default_weather = periods.get('default', DEFAULT_WEATHER)
    if type(default_weather) == list:
        default_weather = choice(default_weather)
    return str(default_weather)


def getPeriodsOnZoneWeatherName(zone_name):
    return zone_weather.get(zone_name, {})


def getDefaultZoneWeather(zone_name):
    periods = getPeriodsOnZoneWeatherName(zone_name)
    return str(periods.get('default', DEFAULT_WEATHER))