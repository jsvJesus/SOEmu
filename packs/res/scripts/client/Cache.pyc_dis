# Embedded file name: scripts/client/Cache.py
__author__ = 'Madcat'
import os
import ResMgr
from xml.dom.minidom import *
QUESTS_VERSION = 1

class Cache:
    DIALOG_CACHE_FILE_NAME = 'cache//dialogs.xml'
    DIALOG_CACHE_FILE_NAME_RES = '../game/cache/dialogs.xml'
    dialog_cache_file = None
    dialogs = {}
    dialogs_changed = False
    quests_version = 0
    dialogs_version = 0

    def __init__(self):
        if not os.path.exists('cache'):
            os.mkdir('cache')
        self.parseDialog()
        self.parseQuest()
        self.checkVersion()

    def parseDialog(self):
        if not os.path.exists(self.DIALOG_CACHE_FILE_NAME):
            new_xml = file(self.DIALOG_CACHE_FILE_NAME, 'wt')
            new_xml.write('<root></root>')
            file.close(new_xml)
        ResMgr.purge(self.DIALOG_CACHE_FILE_NAME_RES, True)
        self.dialog_cache_file = ResMgr.openSection(self.DIALOG_CACHE_FILE_NAME_RES)
        if self.dialog_cache_file:
            for npc in self.dialog_cache_file.values():
                name = npc['name'].asString
                for dialog in npc['dialogs'].values():
                    if not self.dialogs.has_key(npc['name'].asString):
                        self.dialogs[npc['name'].asString] = dict()
                    self.dialogs[npc['name'].asString][dialog['id'].asInt] = dict(text=dialog['text'].asWideString, title=dialog['title'].asWideString, ver=dialog['ver'].asInt)

    def getCacheDialog(self, name, id):
        dialog = None
        npc = self.dialogs.get(name, None)
        if npc:
            dialog = npc.get(id, None)
        return dialog

    def setCacheDialog(self, name, id, title, text, version):
        if not self.dialogs.has_key(name):
            self.dialogs[name] = dict()
        if not self.dialogs[name].has_key(id) or self.dialogs[name][id]['ver'] != version:
            self.dialogs[name][id] = dict(id=id, title=title, text=text, ver=version)
            self.dialogs_changed = True

    def getDialogIDs(self, name):
        version = []
        npc = self.dialogs.get(name, None)
        if npc:
            for id in npc.keys():
                version.append(npc[id]['ver'])

            return (npc.keys(), version)
        else:
            return ([], [])

    def saveCacheDialog(self):
        if self.dialogs_changed:
            file = open(self.DIALOG_CACHE_FILE_NAME, 'w')
            doc = Document()
            root = doc.createElement('root')
            for npc in self.dialogs:
                npc_section = doc.createElement('npc')
                npc_name_section = doc.createElement('name')
                npc_name = doc.createTextNode(npc)
                npc_name_section.appendChild(npc_name)
                npc_section.appendChild(npc_name_section)
                dialogs_section = doc.createElement('dialogs')
                npc_section.appendChild(dialogs_section)
                for id in self.dialogs[npc]:
                    info = self.dialogs[npc][id]
                    dialog_section = doc.createElement('dialog')
                    id_section = doc.createElement('id')
                    id = doc.createTextNode(str(id))
                    id_section.appendChild(id)
                    title_section = doc.createElement('title')
                    title = doc.createTextNode(info['title'])
                    title_section.appendChild(title)
                    text_section = doc.createElement('text')
                    text = doc.createTextNode(info['text'])
                    text_section.appendChild(text)
                    version_section = doc.createElement('ver')
                    ver = doc.createTextNode(str(info['ver']))
                    version_section.appendChild(ver)
                    dialog_section.appendChild(id_section)
                    dialog_section.appendChild(title_section)
                    dialog_section.appendChild(text_section)
                    dialog_section.appendChild(version_section)
                    dialogs_section.appendChild(dialog_section)

                root.appendChild(npc_section)

            doc.appendChild(root)
            file.write(doc.toprettyxml(indent='', encoding='utf-8'))
            file.close()
            self.dialogs_changed = False

    QUEST_CACHE_FILE_NAME = 'cache//quests.xml'
    QUEST_CACHE_FILE_NAME_RES = '../game/cache/quests.xml'
    quest_cache_file = None
    quests = {}
    quests_changed = False

    def parseQuest(self):
        if not os.path.exists(self.QUEST_CACHE_FILE_NAME):
            new_xml = file(self.QUEST_CACHE_FILE_NAME, 'wt')
            new_xml.write('<root></root>')
            file.close(new_xml)
        ResMgr.purge(self.QUEST_CACHE_FILE_NAME_RES, True)
        self.quest_cache_file = ResMgr.openSection(self.QUEST_CACHE_FILE_NAME_RES)
        if self.quest_cache_file:
            for npc in self.quest_cache_file.values():
                name = npc['name'].asString
                if name == 'version':
                    version = npc['value'].asInt
                    self.quests_version = version
                else:
                    for quest in npc['quests'].values():
                        if not self.quests.has_key(name):
                            self.quests[name] = dict()
                        self.quests[name][quest['id'].asInt] = dict(title=quest['title'].asWideString, description=quest['description'].asWideString, ver=quest['ver'].asInt)

    def getCacheQuestIDs(self, name):
        cachedIDs = []
        cachedVersions = []
        if self.quests.has_key(name):
            for questID in self.quests[name]:
                cachedIDs.append(questID)
                cachedVersions.append(self.quests[name][questID]['ver'])

        return (cachedIDs, cachedVersions)

    def getAllCachedQuestIDs(self):
        IDs = []
        versionIDs = []
        for npc in self.quests:
            for qID in self.quests[npc]:
                ver = self.quests[npc][qID]['ver']
                if qID not in IDs:
                    IDs.append(qID)
                    versionIDs.append(ver)

        return (IDs, versionIDs)

    def getCacheQuest(self, name, id):
        quest = None
        npc = self.quests.get(name, None)
        if npc:
            quest = npc.get(id, None)
        return quest

    def getCacheQuestOnID(self, id):
        for npc_name in self.quests.keys():
            npc = self.quests[npc_name]
            quest = npc.get(id, None)
            if quest:
                return quest

        return

    def setCacheQuest(self, name, id, title, description, version):
        if not self.quests.has_key(name):
            self.quests[name] = dict()
        if not self.quests[name].has_key(id) or self.quests[name][id]['ver'] != version:
            self.quests[name][id] = dict()
            self.quests[name][id] = dict(title=title, description=description, ver=version)
            self.quests_changed = True

    def saveCacheQuest(self):
        if self.quests_changed:
            file = open(self.QUEST_CACHE_FILE_NAME, 'w')
            doc = Document()
            root = doc.createElement('root')
            for object in self.quests:
                object_section = doc.createElement('object')
                object_name_section = doc.createElement('name')
                object_name = doc.createTextNode(object)
                object_name_section.appendChild(object_name)
                object_section.appendChild(object_name_section)
                quests_section = doc.createElement('quests')
                object_section.appendChild(quests_section)
                for id in self.quests[object]:
                    info = self.quests[object][id]
                    quest_section = doc.createElement('quest')
                    id_section = doc.createElement('id')
                    id = doc.createTextNode(str(id))
                    id_section.appendChild(id)
                    title_section = doc.createElement('title')
                    title = doc.createTextNode(info['title'])
                    title_section.appendChild(title)
                    text_section = doc.createElement('description')
                    text = doc.createTextNode(info['description'])
                    text_section.appendChild(text)
                    version_section = doc.createElement('ver')
                    ver = doc.createTextNode(str(info['ver']))
                    version_section.appendChild(ver)
                    quest_section.appendChild(id_section)
                    quest_section.appendChild(title_section)
                    quest_section.appendChild(text_section)
                    quest_section.appendChild(version_section)
                    quests_section.appendChild(quest_section)

                root.appendChild(object_section)

            object_section = doc.createElement('object')
            object_name_section = doc.createElement('name')
            object_name = doc.createTextNode('version')
            object_name_section.appendChild(object_name)
            object_section.appendChild(object_name_section)
            object_name_section = doc.createElement('value')
            object_name = doc.createTextNode(str(self.quests_version))
            object_name_section.appendChild(object_name)
            object_section.appendChild(object_name_section)
            root.appendChild(object_section)
            doc.appendChild(root)
            file.write(doc.toprettyxml(indent='', encoding='utf-8'))
            file.close()
            self.quests_changed = False

    def clearCacheQuest(self):
        self.quests = {}
        self.saveCacheQuest()

    def checkVersion(self):
        if self.quests_version < QUESTS_VERSION:
            self.clearCacheQuest()
            self.quests_version = QUESTS_VERSION
            self.quests_changed = True
            self.saveCacheQuest()