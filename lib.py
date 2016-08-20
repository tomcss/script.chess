import xbmcaddon
import xbmc

addon    = xbmcaddon.Addon()
profile  = xbmc.translatePath( addon.getAddonInfo('profile') ).decode("utf-8")
imgpath  = "special://home/addons/script.chess/resources/media/"
savefile = profile + "savegame.json"

STRINGS = {
        "continue"  :32001,
        "new_game"  :32002,
        "play_as"   :32003,
        "white"     :32004,
        "black"     :32005,
        "random"    :32006,
        "level"     :32007,
        "level_1"   :32008,
        "level_2"   :32009,
        "level_3"   :32010,
        "level_4"   :32011,
        "level_5"   :32012,
        "quit"      :32013
        }

def _(string_id):
    if string_id in STRINGS:
        #print(string_id)
        print( "--{0}--".format(addon.getLocalizedString(32003)))
        return addon.getLocalizedString(STRINGS[string_id])
    else:
        print("Fuck me!")
        xbmc.log('String is missing: %s' % string_id, level=xbmc.LOGDEBUG)
        return string_id