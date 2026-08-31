# Embedded file name: scripts/client/Damager.py
from generic.victimdamager import GenericDamager
import BigWorld

class Damager(GenericDamager):

    def on_victim_damaged(self, victim_id, damagetaken_data):
        return BigWorld.entity(victim_id, True)

    def on_victim_death(self, victim_id):
        return BigWorld.entity(victim_id, True)