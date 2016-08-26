import xbmc, xbmcgui, sunfish, thread, chesswindow, thread, xbmcaddon, os
import random, lib

#TODO: Feedback

_ = lib._

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_BSPACE = 92
ACTION_LEFT   = 1
ACTION_RIGHT  = 2
ACTION_UP     = 3
ACTION_DOWN   = 4
ACTION_ENTER  = 7

WHITE = 0
BLACK = 1

DIFFICULTIES = [ _('level_1'),
                 _('level_2'),
                 _('level_3'),
                 _('level_4'),
                 _('level_5')]
SIDES = [ _('white'),
          _('black'),
          _('random')]
FILES = 'abcdefgh'

class MenuWindow(xbmcgui.Window):
    def onAction( self, action):
        if action == ACTION_PREVIOUS_MENU or \
           action == ACTION_BSPACE:
            self.close()

    def onControl( self, control):
        cid = control.getId()

        if cid == self.btnDifficulty.getId():
            self.setDifficulty( (self.difficulty+1)%len(DIFFICULTIES))
            
        if cid == self.btnSide.getId():
            self.setSide( (self.playerSide+1)%len(SIDES))

        if cid == self.btnNewGame.getId():
            if self.playerSide == 2:
                self.setSide( random.randint(0,1))
            
            chessWindow = chesswindow.ChessWindow(
                side=self.playerSide,
                difficulty=self.difficulty)
            chessWindow.show()
            chessWindow.clearSaveGame()
            chessWindow.doModal()

        if cid == self.btnContinue.getId():
            chessWindow = chesswindow.ChessWindow()
            chessWindow.setDifficulty( self.difficulty)
            chessWindow.show()
            chessWindow.loadGame()
            chessWindow.doModal()

        if cid == self.btnQuit.getId():
            self.close()
            
    def setSide(self, side):
        self.playerSide = side
        self.btnSide.setLabel( SIDES[ self.playerSide])
        
    def setDifficulty( self, dif):
        self.difficulty = dif
        self.btnDifficulty.setLabel( "{}: {}".format(_('level'), DIFFICULTIES[self.difficulty]))

    def setTabOrder( self, controls):
        for index, control in enumerate( controls):
            control.controlUp(   controls[index-1])
            control.controlDown( controls[(index+1)%len(controls)])

    def __init__( self):
        self.setCoordinateResolution( 0)

        self.imgBackground = xbmcgui.ControlImage(
            x = 0,
            y = 0,
            width    = 1920,
            height   = 1080,
            filename = lib.imgpath+'menubg.jpg')
        self.addControl( self.imgBackground)

        self.btnContinue = xbmcgui.ControlButton(
            x = 760,
            y = 200,
            width  = 400,
            height = 60,
            label  = xbmcaddon.Addon().getLocalizedString(32001),
            font   = 'font14',
            alignment      = 2,
            noFocusTexture = lib.imgpath+'buttonbg.png')
        self.addControl( self.btnContinue)

        self.btnNewGame = xbmcgui.ControlButton(
            x = 760,
            y = 300,
            width  = 400,
            height = 60,
            label  = _('new_game'),
            font   = 'font14',
            alignment      = 2,
            noFocusTexture = lib.imgpath+'buttonbg.png')
        self.addControl( self.btnNewGame)

        self.btnDifficulty = xbmcgui.ControlButton(
            x = 760,
            y = 500,
            width  = 400,
            height = 60,
            alignment      = 2,
            label          = '',
            font           = 'font14',
            noFocusTexture = lib.imgpath+'buttonbg.png')
        self.addControl( self.btnDifficulty)
        self.setDifficulty( 1)
        

        self.btnSide = xbmcgui.ControlButton(
            x = 760,
            y = 400,
            width  = 400,
            height = 60,
            alignment = 2,
            label     = '',
            font      = 'font14',
            noFocusTexture = lib.imgpath+'buttonbg.png')
        self.addControl( self.btnSide)
        self.setSide( 0)
        
        self.btnQuit = xbmcgui.ControlButton(
            x = 760,
            y = 700,
            width  = 400,
            height = 60,
            alignment    = 2,
            label        = _('quit'),
            font         = 'font14',
            noFocusTexture = lib.imgpath+'buttonbg.png')
        self.addControl( self.btnQuit)
        
        self.setTabOrder( [self.btnContinue,
                           self.btnNewGame,
                           self.btnSide,
                           self.btnDifficulty,
                           self.btnQuit])

        self.setFocus( self.btnNewGame)
