# Embedded file name: scripts/client/Bleeding.py
import SFXer
__author__ = 'muzhig'
import BigWorld
import Math
import particles
import BWPersonality

class Bleeding:
    blood_drop_particle = None
    isBleending = False
    bleed_callback_timer = None
    last_model = None

    def blood_rel_pos(self, body_zone):
        node = self.get_node_by_body_zone(body_zone)
        if node:
            return Math.Matrix(node).translation - self.position
        return (0, 1.3, 0)

    def blood_sfx_on_damage(self, damage_source, damagetaken_data):
        return 'sfx/Shoot/body_hit.xml'

    def bleed_on_damage(self, damage_source, damagetaken_data):
        damager = BigWorld.entity(damage_source['entity_id'], True)
        blood_rel_pos = self.blood_rel_pos(damagetaken_data['body_zone'])
        if damager:
            bloodvector = self.position - damager.position + blood_rel_pos - (0, 1, 0)
        else:
            bloodvector = (0, 1, 0)
        sfx_id = self.blood_sfx_on_damage(damage_source, damagetaken_data)
        self.bleed(blood_rel_pos, bloodvector, sfx_id)

    def pre_bleed(self, position, bodyZone):
        blood_sfx_id = self.blood_sfx_on_damage(None, {'body_zone': bodyZone})
        blood_orientation = position - BigWorld.camera().position - (0, 1, 0)
        SFXer.BodyHit(position, self, blood_orientation, -Math.Vector3(blood_orientation), blood_sfx_id)
        return

    def bleed(self, blood_rel_pos, blood_orientation, blood_sfx_id):
        SFXer.BodyHit(self.position + blood_rel_pos, self, blood_orientation, -Math.Vector3(blood_orientation), blood_sfx_id)

    def bleedglobal(self, blood_rel_pos, blood_orientation, blood_sfx_id):
        SFXer.BodyHit(blood_rel_pos, self, blood_orientation, -Math.Vector3(blood_orientation), blood_sfx_id)

    def bleedDropEff(self):
        self.isBleending = True
        BWPersonality.GUICore.bleedGUI.show()
        model = self.model
        if not self.blood_drop_particle:
            self.blood_drop_particle = particles.createBloodDroop()
        if not model:
            if not self.bleed_callback_timer:
                self.bleed_callback_timer = BigWorld.callback(5, self._checkIsLoadModel)
            return
        self.apllyBleedDrop()

    def _checkIsLoadModel(self):
        BigWorld.cancelCallback(self.bleed_callback_timer)
        self.bleed_callback_timer = None
        if not self.blood_drop_particle:
            return
        elif self.apllyBleedDrop():
            return
        else:
            self.bleed_callback_timer = BigWorld.callback(5, self._checkIsLoadModel)
            return

    def removeBleedDropEff(self):
        self.isBleending = False
        BWPersonality.GUICore.bleedGUI.hide()
        model = self.model
        if model:
            if self.blood_drop_particle:
                try:
                    model.root.detach(self.blood_drop_particle)
                except ValueError:
                    pass

            if self.last_model:
                try:
                    self.last_model.root.detach(self.blood_drop_particle)
                except ValueError:
                    pass

                self.last_model = None
        self.blood_drop_particle = None
        if self.bleed_callback_timer:
            BigWorld.cancelCallback(self.bleed_callback_timer)
            self.bleed_callback_timer = None
        return

    def apllyBleedDrop(self):
        if not self.isBleending:
            return False
        else:
            model = self.model
            if not model:
                return False
            if self.blood_drop_particle:
                if self.last_model:
                    try:
                        self.last_model.root.detach(self.blood_drop_particle)
                    except ValueError:
                        pass

                    self.last_model = None
                try:
                    model.root.attach(self.blood_drop_particle)
                    self.last_model = model
                    return True
                except Exception as e:
                    print 'apllyBleedDrop Error:', e

            return False