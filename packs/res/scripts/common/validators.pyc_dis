# Embedded file name: scripts/common/validators.py
import re
from Localization import lc

class AvatarName:
    MAX_LEN = 32
    MIN_LEN = 3
    MAX_GROUNDS = 1
    ERR__NOT_ALLOWED_SYMBOLS = 1
    ERR__TOO_SHORT = 2
    ERR__TOO_LONG = 3
    ERR__BEGIN_WITH_GROUND = 4
    ERR__END_WITH_GROUND = 5
    ERR__TOO_MANY_GROUNDS = 6
    REGEX = re.compile(lc('Account.base.REGEX1'))
    errmsg = {ERR__NOT_ALLOWED_SYMBOLS: lc('Codes.common.FORBIDDEN_CHARS'),
     ERR__TOO_SHORT: lc('Codes.common.SHORT_NAME'),
     ERR__TOO_LONG: lc('Codes.common.LONG_NAME'),
     ERR__BEGIN_WITH_GROUND: lc('Codes.common.STARTS_WITH_UNDERSCORE'),
     ERR__END_WITH_GROUND: lc('Codes.common.ENDS_WITH_UNDERSCORE'),
     ERR__TOO_MANY_GROUNDS: lc('Codes.common.MANY_UNDERSCORES')}

    @staticmethod
    def validate(name):
        name = name.strip()
        if len(name) < AvatarName.MIN_LEN:
            error = AvatarName.ERR__TOO_SHORT
        elif len(name) > AvatarName.MAX_LEN:
            error = AvatarName.ERR__TOO_LONG
        else:
            uid = name.lower()
            if AvatarName.REGEX.match(uid):
                if uid.count(u'_') > AvatarName.MAX_GROUNDS:
                    error = AvatarName.ERR__TOO_MANY_GROUNDS
                elif uid[0] == u'_':
                    error = AvatarName.ERR__BEGIN_WITH_GROUND
                elif uid[-1] == u'_':
                    error = AvatarName.ERR__END_WITH_GROUND
                else:
                    return {'valid': True,
                     'uid': name}
            else:
                error = AvatarName.ERR__NOT_ALLOWED_SYMBOLS
        return {'valid': False,
         'error': (error, AvatarName.errmsg[error])}