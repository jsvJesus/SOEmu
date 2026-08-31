# Embedded file name: scripts/common/Localization.py
import ResMgr
__author__ = 'Leviathan'
import os
import traceback
import json
language = 'russian'
try:
    settings_filepath = 'settings.json'
    if os.path.isfile(settings_filepath):
        json_data = open(settings_filepath)
        data = json.load(json_data)
        language = data.get('language')
        if language is None:
            language = 'russian'
    else:
        language = 'russian'
except:
    traceback.print_exc()
    language = 'russian'

class Localization:
    globalLanguage = language
    print 'globalLanguage ', globalLanguage
    loaded_loc_files = {}
    loaded_loc_files_english = {}

    def __init__(self, file_names = None):
        if file_names is None:
            self.loaded_loc_files = dict(((filename[:-4], section) for filename, section in ResMgr.openSection('local')['Russian'].items() if filename.endswith('.xml')))
            self.loaded_loc_files_english = dict(((filename[:-4], section) for filename, section in ResMgr.openSection('local')['English'].items() if filename.endswith('.xml')))
        else:
            for file_name in file_names:
                try:
                    core_name = file_name[file_name.rindex('/') + 1:file_name.rindex('.')]
                except ValueError:
                    print 'Error loading localization file'
                    continue

                self.loaded_loc_files[core_name] = ResMgr.openSection(file_name)
                print 'Loaded localization:', file_name

        return

    def getXMLData(self, filename, language = None):
        if not language:
            language = self.globalLanguage
        if language == 'russian':
            return self.loaded_loc_files[filename]
        else:
            return self.loaded_loc_files_english[filename]

    def GetLocalizationString(self, string, utf8, DEFAULT_STRING = None, language = None):
        if DEFAULT_STRING == None:
            if utf8:
                DEFAULT_STRING = string
            else:
                DEFAULT_STRING = unicode(string)
        strings_list = string.split('.')
        localization_file_name = strings_list.pop(0)
        if language != None:
            lang = language
        else:
            lang = self.globalLanguage
        try:
            if lang == 'russian':
                new_section = self.loaded_loc_files[localization_file_name]
            else:
                new_section = self.loaded_loc_files_english[localization_file_name]
        except KeyError:
            return DEFAULT_STRING

        for obj_name in strings_list:
            if new_section == None:
                return DEFAULT_STRING
            try:
                new_section = new_section[obj_name]
            except KeyError:
                return DEFAULT_STRING

        if new_section == None:
            return DEFAULT_STRING
        else:
            return_string = new_section.asString
            if utf8:
                return return_string
            return return_string.decode('utf-8')
            return


print 'Start loading localization'
localization_object = Localization()

def lc(string, utf8 = False, default = None):
    global localization_object
    return localization_object.GetLocalizationString(string, utf8, default)


def openLocalizeSection(filename, language = None):
    return localization_object.getXMLData(filename, language)