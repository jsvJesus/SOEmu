# Embedded file name: scripts/client/QuestObject.py
__author__ = 'Madcat'
import BigWorld
from ModelSelector import ModelSelector
import Quest

class QuestObject(BigWorld.Entity, ModelSelector):
    NO_QUEST, HAS_QUEST, OPENED, CLOSED, FAILED, ON_TEST = range(0, 6)

    def __init__(self):
        BigWorld.Entity.__init__(self)

    def onEnterWorld(self, prereqs):
        ModelSelector.onEnterWorld(self, prereqs)
        if self.show_if != self.NO_QUEST:
            self.hideModel()
        from PlayerAvatar import PlayerAvatar
        for e in BigWorld.entities.values():
            if isinstance(e, PlayerAvatar):
                for quest in e.QuestObjInfo:
                    if quest['id'] == self.questID:
                        self.onChangeQuest(quest['state'])
                        return

    def showModel(self):
        if self.model:
            self.model.visible = True

    def hideModel(self):
        if self.model:
            self.model.visible = False

    def onChangeQuest(self, state):
        if self.show_if == self.NO_QUEST:
            self.hideModel()
        elif self.show_if == self.HAS_QUEST:
            self.showModel()
        elif self.show_if == self.OPENED:
            if state == Quest.STATE_OPENED:
                self.showModel()
            else:
                self.hideModel()
        elif self.show_if == self.CLOSED:
            if state == Quest.STATE_CLOSED:
                self.showModel()
            else:
                self.hideModel()
        elif self.show_if == self.FAILED:
            if state == Quest.STATE_FAILED:
                self.showModel()
            else:
                self.hideModel()
        elif self.show_if == self.ON_TEST:
            if state == Quest.STATE_ONTEST:
                self.showModel()
            else:
                self.hideModel()

    def onRemoveQuest(self):
        if self.show_if == self.NO_QUEST:
            self.showModel()
        else:
            self.hideModel()