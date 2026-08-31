# Embedded file name: scripts/common/Fractions.py
from Localization import lc
ALL_FRACTIONS = AVATAR_STALKER, AVATAR_INDIGENOUS, AVATAR_MILITARY, AVATAR_LONERS, BIG_TRADERS, BIG_BARTERS, BIG_BANDITS, BIG_MILITARYS, BIG_MERCENARYS, BIG_CLANS, BIG_HUNTERS, BIG_SCIENTISTS, BIG_OLD_STALKERS, BIG_MUTANTS = xrange(1, 15)
FractionNames = {AVATAR_STALKER: lc('Fractions.common.FRACTION1'),
 AVATAR_INDIGENOUS: lc('Fractions.common.FRACTION2'),
 AVATAR_MILITARY: lc('Fractions.common.FRACTION3'),
 AVATAR_LONERS: lc('Fractions.common.FRACTION4'),
 BIG_TRADERS: lc('Fractions.common.FRACTION5'),
 BIG_BARTERS: lc('Fractions.common.FRACTION6'),
 BIG_BANDITS: lc('Fractions.common.FRACTION7'),
 BIG_MILITARYS: lc('Fractions.common.FRACTION8'),
 BIG_MERCENARYS: lc('Fractions.common.FRACTION9'),
 BIG_CLANS: lc('Fractions.common.FRACTION10'),
 BIG_HUNTERS: lc('Fractions.common.FRACTION11'),
 BIG_SCIENTISTS: lc('Fractions.common.FRACTION12'),
 BIG_OLD_STALKERS: lc('Fractions.common.FRACTION13'),
 BIG_MUTANTS: lc('Fractions.common.FRACTION14')}
FractionFriends = {AVATAR_STALKER: [],
 AVATAR_INDIGENOUS: [],
 AVATAR_MILITARY: [],
 AVATAR_LONERS: [],
 BIG_TRADERS: [],
 BIG_BARTERS: [],
 BIG_BANDITS: [],
 BIG_MILITARYS: [],
 BIG_MERCENARYS: [],
 BIG_CLANS: [],
 BIG_HUNTERS: [],
 BIG_SCIENTISTS: [],
 BIG_OLD_STALKERS: [],
 BIG_MUTANTS: []}
FractionEnemies = {AVATAR_STALKER: [],
 AVATAR_INDIGENOUS: [],
 AVATAR_MILITARY: [],
 AVATAR_LONERS: [],
 BIG_TRADERS: [],
 BIG_BARTERS: [],
 BIG_BANDITS: [],
 BIG_MILITARYS: [],
 BIG_MERCENARYS: [],
 BIG_CLANS: [],
 BIG_HUNTERS: [],
 BIG_SCIENTISTS: [],
 BIG_OLD_STALKERS: [],
 BIG_MUTANTS: []}
PlayerStatusDefault = {AVATAR_STALKER: 0,
 AVATAR_INDIGENOUS: 0,
 AVATAR_MILITARY: 0,
 AVATAR_LONERS: 0,
 BIG_TRADERS: 0,
 BIG_BARTERS: 0,
 BIG_BANDITS: 0,
 BIG_MILITARYS: 0,
 BIG_MERCENARYS: 0,
 BIG_CLANS: 0,
 BIG_HUNTERS: 0,
 BIG_SCIENTISTS: 0,
 BIG_OLD_STALKERS: 0,
 BIG_MUTANTS: 0}
AvatarFractions = []
STATUS_MINIMUM = -100000
STATUS_MAXIMUM = 100000
STATUS_KILL = -1001

class Fraction(object):

    def __init__(self, name):
        object.__init__(self)
        self.name = name
        self.fractionTypeAvatar = False
        self.defaultFractionRelation = 0
        self.friends = []
        self.enemies = []

    def __str__(self):
        return self.name


class FractiondictBuilder:

    @staticmethod
    def build():
        fractions = {}
        for fractionID in ALL_FRACTIONS:
            name = FractionNames.get(fractionID, u'')
            fraction = Fraction(name)
            fraction.fractionTypeAvatar = fractionID in AvatarFractions
            fraction.defaultFractionRelation = PlayerStatusDefault.get(fractionID, 0)
            fractions[fractionID] = fraction

        for fractionID in ALL_FRACTIONS:
            fraction = fractions[fractionID]
            for friendID in FractionFriends.get(fractionID, []):
                friend = fractions[friendID]
                fraction.friends.append(friend)

            for enemyID in FractionEnemies.get(fractionID, []):
                enemy = fractions[enemyID]
                fraction.enemies.append(enemy)

        return fractions


fractions = FractiondictBuilder.build()