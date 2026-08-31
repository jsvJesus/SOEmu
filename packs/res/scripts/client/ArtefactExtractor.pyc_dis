# Embedded file name: scripts/client/ArtefactExtractor.py
import BigWorld
import Keys
import Math
from copy import copy
import Helpers.Caps
import math
import BWPersonality
import soGUI
import random
import ItemsUtils

class PressGame:
    ALL_KEYS = [Keys.KEY_UPARROW,
     Keys.KEY_DOWNARROW,
     Keys.KEY_LEFTARROW,
     Keys.KEY_RIGHTARROW,
     Keys.KEY_1,
     Keys.KEY_2,
     Keys.KEY_3,
     Keys.KEY_4,
     Keys.KEY_5,
     Keys.KEY_6,
     Keys.KEY_7,
     Keys.KEY_8,
     Keys.KEY_9]

    def onDeath(self):
        BWPersonality.GUICore.removeListener('artifactQTEEvent', self.artifactQTEEvent)

    def __init__(self, extractor_params, item):
        self.fGameStarted = False
        self.InitGame()
        self.extractor_params = extractor_params
        self.item_dict = item
        BWPersonality.GUICore.addListener('artifactQTEEvent', self.artifactQTEEvent)
        BWPersonality.GUICore.showArtifactQTE()
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)

    def InitGame(self):
        self.game_timer = None
        self.TIME_DISCRETE = 0.05
        self.flow_time = 0
        self.game_stage = 0
        self.TIME_GATES = [1.0,
         2.0,
         3.0,
         4.0,
         5.0]
        self.NEEDED_KEYS = []
        for index in xrange(len(self.TIME_GATES)):
            self.NEEDED_KEYS.append(self.ALL_KEYS[random.randint(0, len(self.ALL_KEYS) - 1)])

        self.current_needed_key = None
        self.fStagePassed = False
        self.fGameWin = True
        self.retried_artifact = 0
        self.detector_visual_data = {'slider': 0.0,
         'QTEdata': {},
         'keyData': [],
         'selector': 0,
         'QTEStatus': soGUI.soArtifactQTE.STATUS_IDLE}
        return

    def OnGameEnded(self):
        BigWorld.cancelCallback(self.game_timer)
        self.fGameStarted = False
        self.DefaultScaner()
        if self.fGameWin:
            BigWorld.player().cell.PickUpItem(self.retried_artifact, ItemsUtils.PICK_UP_SOURCE_EXTRACTOR)
        else:
            self.SetQTEStatus(soGUI.soArtifactQTE.STATUS_FAIL)

    def ChangeGameStage(self):
        self.current_needed_key = self.NEEDED_KEYS[self.game_stage]
        if self.current_needed_key:
            print 'Input Symbol', BigWorld.keyToString(self.current_needed_key)

    def onStageChange(self, oldStage, newStage):
        if self.fStagePassed:
            self.fStagePassed = False
            self.UpdateKeys()
        else:
            self.fGameWin = False
            self.OnGameEnded()

    def handle_key(self, key):
        if key == Keys.KEY_NUMPAD1:
            key = Keys.KEY_1
        elif key == Keys.KEY_NUMPAD2:
            key = Keys.KEY_2
        elif key == Keys.KEY_NUMPAD3:
            key = Keys.KEY_3
        elif key == Keys.KEY_NUMPAD4:
            key = Keys.KEY_4
        elif key == Keys.KEY_NUMPAD5:
            key = Keys.KEY_5
        elif key == Keys.KEY_NUMPAD6:
            key = Keys.KEY_6
        elif key == Keys.KEY_NUMPAD7:
            key = Keys.KEY_7
        elif key == Keys.KEY_NUMPAD8:
            key = Keys.KEY_8
        elif key == Keys.KEY_NUMPAD9:
            key = Keys.KEY_9
        elif key == Keys.KEY_NUMPAD0:
            key = Keys.KEY_0
        if self.game_stage < len(self.TIME_GATES):
            if key in self.ALL_KEYS:
                if key == self.current_needed_key:
                    self.fStagePassed = True
                else:
                    self.fGameWin = False
                    self.OnGameEnded()
                return True
        return False

    def GetGameStage(self):
        stage_count = 0
        for gate in self.TIME_GATES:
            if gate < self.flow_time:
                stage_count += 1
            else:
                return stage_count

        return len(self.TIME_GATES)

    def onFlowChanged(self):
        self.UpdateSlider()

    def CheckGameState(self):
        self.flow_time += self.TIME_DISCRETE
        self.onFlowChanged()
        new_stage = self.GetGameStage()
        if new_stage != self.game_stage:
            self.game_stage = new_stage
            self.onStageChange(self.game_stage, new_stage)
            if not self.fGameStarted:
                return
            if self.game_stage >= len(self.TIME_GATES):
                self.OnGameEnded()
                return
            self.ChangeGameStage()
        self.game_timer = BigWorld.callback(self.TIME_DISCRETE, self.CheckGameState)

    def StartGame(self, art_id):
        if self.fGameStarted:
            return
        if not BigWorld.player().CanStartArtefactExtraction(self.extractor_params, self.item_dict):
            return
        self.fGameStarted = True
        self.InitGame()
        self.UpdateDotSelection(art_id)
        self.UpdateKeys()
        self.ChangeGameStage()
        self.game_timer = BigWorld.callback(self.TIME_DISCRETE, self.CheckGameState)

    def GetCoordDict(self):
        player_look = copy(BigWorld.camera().direction)
        player_right_hand = Math.Vector3(0, 1, 0) * player_look
        player_look = Math.Vector2(player_look[0], player_look[2])
        player_right_hand = Math.Vector2(player_right_hand[0], player_right_hand[2])
        player_look.normalise()
        player_right_hand.normalise()
        QTECodes = {}
        show_range = ItemsUtils.DETECTOR_RANGE
        for entity in BigWorld.entities.values():
            if Helpers.Caps.CAP_CAN_PICKUP in entity.targetCaps:
                player_position = BigWorld.player().position
                if entity.position.distTo(player_position) < show_range:
                    entity_vector = entity.position - player_position
                    entity_vector = Math.Vector2(entity_vector[0], entity_vector[2])
                    x_coord = entity_vector.dot(player_right_hand)
                    y_coord = entity_vector.dot(player_look)
                    QTECodes[entity.id] = (x_coord / show_range, y_coord / show_range)

        return QTECodes

    def UpdateQTDots(self):
        if not BigWorld.player().CanStartArtefactScan(self.extractor_params, self.item_dict):
            return
        self.detector_visual_data['QTEdata'] = self.GetCoordDict()
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)

    def UpdateSlider(self):
        self.detector_visual_data['slider'] = self.flow_time / self.TIME_GATES[-1]
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)

    def SetQTEStatus(self, status):
        self.detector_visual_data['QTEStatus'] = status
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)

    def UpdateDotSelection(self, id):
        self.retried_artifact = id
        self.detector_visual_data['selector'] = self.retried_artifact
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)

    def UpdateKeys(self):
        key_data = []
        for index, key in enumerate(self.NEEDED_KEYS):
            if index <= self.game_stage:
                key_data.append((key, True))
            else:
                key_data.append((key, False))

        print 'UpdateKeys', key_data
        self.detector_visual_data['keyData'] = key_data
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)

    def StartArtExtraction(self, id):
        if self.fGameStarted:
            return
        art = BigWorld.entities[id]
        if art.position.distTo(BigWorld.player().position) < ItemsUtils.EXTRACTION_RANGE:
            self.SetQTEStatus(soGUI.soArtifactQTE.STATUS_PLAY)
            self.StartGame(id)

    def artifactQTEEvent(self, event, data):
        if event == soGUI.soArtifactQTE.EVENT_SCANNED:
            self.UpdateQTDots()
        elif event == soGUI.soArtifactQTE.EVENT_SELECT:
            self.StartArtExtraction(data)
        elif event == soGUI.soArtifactQTE.EVENT_CLOSED:
            self.onDeath()
            BigWorld.player().artefactExtractor = None
        return

    def DestroyExtractor(self):
        self.onDeath()
        BigWorld.player().artefactExtractor = None
        BWPersonality.GUICore.showArtifactQTE(False)
        return

    def DefaultScaner(self):
        self.detector_visual_data = {'slider': 0.0,
         'QTEdata': {},
         'keyData': [],
         'selector': 0,
         'QTEStatus': soGUI.soArtifactQTE.STATUS_IDLE}
        BWPersonality.GUICore.setArtifactQTEData(self.detector_visual_data)