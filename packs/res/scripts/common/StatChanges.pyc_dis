# Embedded file name: scripts/common/StatChanges.py
CHANGE_NONE, ADD_BEFORE_MULT, MULT, ADD_AFTER_MULT, PERCENTS, SPECIFIED = xrange(6)

class StatChanges:

    def __init__(self, changeID = None, value = None):
        self.before, self.mult, self.after, self.percents = (0, 1, 0, 0)
        self.specified = None
        if changeID is not None and value is not None:
            self.addChangeValue(changeID, value)
        return

    def getChangedValue(self, baseValue = 0.0):
        return (baseValue + self.before) * self.mult * (1 + self.percents / 100.0) + self.after

    def __str__(self):
        return 'before: ' + str(self.before) + ', mult:' + str(self.mult) + ', percents: ' + str(self.percents) + ', after: ' + str(self.after)

    def addChangeValue(self, changeID, value):
        if changeID == ADD_BEFORE_MULT:
            self.before += value
        elif changeID == MULT:
            self.mult *= value
        elif changeID == ADD_AFTER_MULT:
            self.after += value
        elif changeID == PERCENTS:
            self.percents += value
        elif changeID == SPECIFIED:
            self.specified = value

    def addBeforeValue(self, value):
        self.before += value

    def addMultValue(self, value):
        self.mult *= value

    def addPercentsValue(self, value):
        self.percents += value

    def addAfterValue(self, value):
        self.after += value

    def add(self, appendChanges):
        if isinstance(appendChanges, StatChanges):
            self.before += appendChanges.before
            self.mult *= appendChanges.mult
            self.after += appendChanges.after
            self.percents += appendChanges.percents
        return self

    def __add__(self, other):
        return self.add(other)