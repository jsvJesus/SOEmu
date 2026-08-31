# Embedded file name: scripts/client/__debug/fastlogin.py
import BWPersonality as so

def fast_login():
    username = so.settings.getSetting('username')
    password = so.settings.getSetting('password')
    character = so.settings.getSetting('character')
    so.game.loginEventListener(so.soGUI.soLoginScreen.EVENT_LOGIN, [username, password, False], fast_login_character=character)