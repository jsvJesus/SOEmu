# Embedded file name: scripts/common/DataManagerConst.py
OK = 0
CHEATER = 1
EMPTY_ID = 2
ID_BANNED = 3
VALIDATE_TYPE_OK = 0
VALIDATE_TYPE_NEED_CODE_EMAIL = 1
VALIDATE_TYPE_NEED_CODE_SMS = 2
VALIDATE_TYPE_WAIT_ID = 33

def NeedValidate(func):

    def ff(*args):
        if args[0].needConfirmIDUser == VALIDATE_TYPE_OK:
            return func(*args)
        else:
            acc = args[0]
            print 'Account foo NeedValidate! Break.', acc, acc.id, [acc.accountName], acc.needConfirmIDUser
            return args[0].reSendValidateWindow()

    return ff