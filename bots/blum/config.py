MANUAL_USERNAME = False
GAME_TOGGLE_ON = True # По умолчанию играть в мини-игру звездочки - True, пропускать - False

try:
    from bots.blum.config_local import *
except ImportError:
    pass