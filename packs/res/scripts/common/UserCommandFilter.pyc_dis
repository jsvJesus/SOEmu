# Embedded file name: scripts/common/UserCommandFilter.py
import time

class UserCommandFilter:
    USER_COMMAND_PAUSE = 0.5
    time_func = time.time

    def __init__(self):
        self.userCommandLastUse = self.time_func() - self.USER_COMMAND_PAUSE

    def PlayerToFastError(self):
        print 'Player is too fast'

    def CheckTime(self):
        current_time = self.time_func()
        if current_time - self.userCommandLastUse > self.USER_COMMAND_PAUSE:
            self.userCommandLastUse = current_time
            return True
        return False


def UserCommand(func):

    def FunctionSelect(*args):
        if args[0].CheckTime():
            return func(*args)
        else:
            return args[0].PlayerToFastError()

    return FunctionSelect