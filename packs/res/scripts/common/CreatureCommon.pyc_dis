# Embedded file name: scripts/common/CreatureCommon.py
import BigWorld
import bwdecorators
from utils import hierarchy_get
from Config import Creatures as Cfg

class CreatureCommon:
    """Creature methods which are the same on cell and client."""

    @bwdecorators.callableOnGhost
    def get_config(self, param = None):
        if param is None:
            return Cfg.get_config(self.creatureType, self.level)
        else:
            return Cfg.get_config(self.creatureType, self.level)[param]
            return

    @bwdecorators.callableOnGhost
    def get_state_config(self, state = None):
        if state is None:
            return self.get_config(Cfg.STATES)[self.state]
        else:
            return self.get_config(Cfg.STATES)[state]
            return

    @bwdecorators.callableOnGhost
    def get_skill_config(self, skill_id):
        return self.get_config(Cfg.SKILLS)[skill_id]

    @bwdecorators.callableOnGhost
    def get_skills_number(self):
        return len(self.get_config(Cfg.SKILLS))

    @bwdecorators.callableOnGhost
    def get_name(self):
        uniq_name = Cfg.get_uniq_mob_name(self.uniq_id)
        if uniq_name is not None:
            return uniq_name
        else:
            return self.get_config(Cfg.NAME)

    @bwdecorators.callableOnGhost
    def get_height(self):
        return self.get_config(Cfg.HEIGHT)

    @bwdecorators.callableOnGhost
    def get_width(self):
        return self.get_config(Cfg.WIDTH)