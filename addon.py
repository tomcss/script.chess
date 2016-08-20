import xbmcaddon
import xbmcgui
import xbmc
import random
import sunfish
import chesswindow
import menuwindow
import time
import os
import lib

if not os.path.exists( lib.profile):
    os.mkdir( lib.profile)

print('ji')
print( xbmcaddon.Addon().getLocalizedString(32001))
menuWindow = menuwindow.MenuWindow()
menuWindow.show()
menuWindow.doModal()

