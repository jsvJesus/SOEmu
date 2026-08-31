# Embedded file name: scripts/common/RestrictionsUtils.py
__author__ = 'leviathan'
CHANNEL_ITEMS = 0
import BigWorld
import time

class RestrictionCommon:
    MAX_NUM_CHANNELS = 3

    def InitRestrictionArray(self):
        self.restrictions = []
        for channel in xrange(self.MAX_NUM_CHANNELS):
            self.restrictions.append(0.0)

    def CheckRestriction(self, channel):
        if not self.CheckChannel(channel):
            return False
        else:
            curr_time = time.time()
            if curr_time >= self.restrictions[channel]:
                return True
            return False

    def CheckChannel(self, channel):
        if channel >= len(self.restrictions):
            print 'Unknown restriction channel', channel
            return False
        return True

    def DoAction(self, channel, action_duration):
        if not self.CheckChannel(channel):
            return
        else:
            if action_duration != None or action_duration > 0.0:
                curr_time = time.time()
                if curr_time >= self.restrictions[channel]:
                    self.restrictions[channel] = curr_time + action_duration
                    return True
                else:
                    return False
            return

    def ReleaseRestriction(self, channel):
        curr_time = time.time()
        self.restrictions[channel] = curr_time

    def canShoot(self):
        return not self.sprinting and not self.binoculing and self.CheckRestriction(CHANNEL_ITEMS)

    def canSprint(self):
        return not self.crouching and self.CheckRestriction(CHANNEL_ITEMS)

    def canCrouch(self):
        return not self.sprinting

    def canJump(self):
        return not self.crouching and self.CheckRestriction(CHANNEL_ITEMS)

    def canPickUp(self):
        return not self.sprinting and not self.dead

    def canUse(self):
        return not self.sprinting and not self.dead

    def canReload(self):
        return not self.sprinting and not self.dead

    def canLoadAmmo(self, id):
        return not self.sprinting and not self.dead

    def canEquip(self):
        return not self.dead

    def canDrop(self):
        return not self.sprinting and not self.dead

    def canUnjam(self):
        return not self.sprinting and not self.dead

    def canInformJamm(self):
        return not self.sprinting and not self.dead

    def canThrowGrenade(self):
        if not self.canShoot() or not self.canDamage:
            return False
        return self.GetGrenadeThrowPossibility()

    def canThrowStone(self):
        if not self.canShoot() or not self.canDamage:
            return False
        return True

    def canBinoculing(self):
        return not self.sniping and not self.dead and not self.sprinting and not self.dead