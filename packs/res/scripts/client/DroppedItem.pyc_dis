# Embedded file name: scripts/client/DroppedItem.py
from Localization import lc
import BigWorld
from ItemHolder import ItemHolder
from Items import ItemsCatalog
import ItemsUtils
import GUI
import Pixie
from Helpers.Caps import CAP_CAN_PICKUP

class DroppedItem(BigWorld.Entity, ItemHolder):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.targetCaps = [CAP_CAN_PICKUP]
        self._messageTimerHandle = None
        self._messageAttachment = None
        self.name = lc('DroppedItem.client.VOID_ITEM')
        return

    def drawItem(self):
        item_type = self.pItemTypeModel
        item_params = ItemsCatalog.GetItemParam(item_type)
        if item_params.has_key('OnFlorModel'):
            item_model = BigWorld.Model(item_params['OnFlorModel'])
            if item_params.has_key('OnFlorTint'):
                item_model.tints = item_params['OnFlorTint']
        else:
            item_model = self.getModelByNamesDict(item_params['ModelNames'].values())
        self.model = item_model
        particle_name = self.getParticleName()
        if particle_name:
            ps = Pixie.createBG(particle_name, self.onLoadPS)

    def onLoadPS(self, ps):
        self.model.root.attach(ps)
        ps.force()

    def getModelName(self):
        tints = {}
        item_type = self.pItemTypeModel
        item_params = ItemsCatalog.GetItemParam(item_type)
        if item_params.has_key('OnFlorModel'):
            item_model = item_params['OnFlorModel']
            if item_params.has_key('OnFlorTint'):
                tints = item_params['OnFlorTint']
        else:
            item_model = self.getModelNameByNamesDict(item_params['ModelNames'].values())
            if item_params.has_key('Tint'):
                tints = item_params['Tint']
        return (item_model, tints)

    def getParticleName(self):
        item_type = self.pItemTypeModel
        item_params = ItemsCatalog.GetItemParam(item_type)
        if item_params.has_key('ParticleName'):
            ps = item_params['ParticleName']
        else:
            ps = 'particles/item_light.xml'
        return ps

    def prerequisites(self):
        pre = []
        md, tints = self.getModelName()
        if md.__class__.__name__ == 'list':
            for e in md:
                pre.append(e)

        else:
            pre.append(md)
        particle_name = self.getParticleName()
        if particle_name:
            pre.append(self.getParticleName())
        return pre

    def onEnterWorld(self, prereqs):
        md, tints = self.getModelName()
        self.name = ItemsUtils.GetItemName(self.pItemTypeModel)
        if md.__class__.__name__ == 'list':
            self.model = BigWorld.Model(*md)
        elif md not in prereqs.failedIDs:
            self.model = prereqs[md]
        for tint in tints:
            setattr(self.model, tint, tints[tint])

        if self.getParticleName() not in prereqs.failedIDs:
            try:
                ps = prereqs[self.getParticleName()]
                self.model.root.attach(ps)
                ps.force()
            except KeyError:
                print 'Error init dropped item, item type:', self.pItemTypeModel, 'particle name:', self.getParticleName()

        else:
            print self.getParticleName(), 'failed to load'
        if self.model is None:
            print self.getModelName()[0], 'failed to load'
        else:
            try:
                self.model.idle()
            except:
                pass

        return

    def hitPot(self, enteredTrap, handle):
        if enteredTrap:
            self.model.visible = True
        else:
            self.model.visible = False

    def _displayMessage(self, msg):
        self._clearMessage()
        text = GUI.Text(msg)
        text.explicitSize = True
        text.size = (0, 0.3)
        text.colour = (255, 205, 149, 245)
        text.filterType = 'LINEAR'
        text.verticalAnchor = 'BOTTOM'
        text.position = (0, 1, 0)
        atch = GUI.Attachment()
        atch.component = text
        atch.faceCamera = True
        self.model.root.attach(atch)
        self._messageAttachment = atch
        self._setMessageHideTimer()

    def _clearMessage(self):
        self._cancelMessageTimer()
        if self._messageAttachment is not None:
            self.model.root.detach(self._messageAttachment)
            self._messageAttachment = None
        return

    def _setMessageHideTimer(self, timeout = 5.0):
        self._cancelMessageTimer()
        self._messageTimerHandle = BigWorld.callback(timeout, self._handleMessageHideTimer)

    def _cancelMessageTimer(self):
        if self._messageTimerHandle is not None:
            BigWorld.cancelCallback(self._messageTimerHandle)
            self._messageTimerHandle = None
        return

    def _handleMessageHideTimer(self):
        self._messageTimerHandle = None
        self._clearMessage()
        return

    def onLeaveWorld(self):
        self._cancelMessageTimer()
        del self._messageTimerHandle
        del self._messageAttachment