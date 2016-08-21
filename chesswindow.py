import xbmc, xbmcgui, sunfish, thread, xbmcaddon, os, json, lib

#Consts

ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_LEFT   = 1
ACTION_RIGHT  = 2
ACTION_UP     = 3
ACTION_DOWN   = 4
ACTION_ENTER  = 7
ACTION_BSPACE = 92
ACTION_SPACE  = 12

WHITE = 0
BLACK = 1

MATE_VALUE = 30000

FILES = 'abcdefgh'
SEARCHDEPTH = [5000, 10000, 20000, 50000, 100000]

_ = lib._

#TODO: Add info panel
#TODO: Add Last Computer Move indicator

class ChessWindow(xbmcgui.Window):
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_BSPACE:
            self.close()

        if action == ACTION_LEFT:
            self.cursorX = (self.cursorX-1) % 8

        if action == ACTION_RIGHT:
            self.cursorX = (self.cursorX+1) % 8

        if action == ACTION_UP:
            self.cursorY = (self.cursorY-1) % 8

        if action == ACTION_DOWN:
            self.cursorY = (self.cursorY+1) % 8

        if action == ACTION_ENTER:
            if self.selectedX==self.cursorX and self.selectedY==self.cursorY:
                self.selectedX=-100
            elif self.selectedX<0:
                self.selectedX = self.cursorX
                self.selectedY = self.cursorY
            elif self.isPlayersTurn():
                moveFrom = FILES[ self.selectedX] + str( 8-self.selectedY)
                moveTo   = FILES[ self.cursorX]   + str( 8-self.cursorY)
                
                move = ( sunfish.parse( moveFrom), sunfish.parse( moveTo))

                if move not in self.pos.gen_moves():
                    self.feedback( "Invalid move!")
                    return

                self.selectedX = -100

                self.makeMove( move)
                self.displayPieces()

                thread.start_new_thread( self.computerMove, ())
            else:
                self.feedback( "Not your turn yet!")

            self.images['selected'].setPosition( 100 + self.selectedX*110,
                                                 100 + self.selectedY*110)

        self.images['cursor'].setPosition( 97 + self.cursorX*110,
                                           97 + self.cursorY*110)

        print( action.getId())
    
    def reverseCase(self, s):
        return ''.join([x.lower() if x.isupper() else x.upper() for x in s])
    
    def setPlayerSide(self, side):
        self.playerSide = side
        
    def saveGame(self):
        self.gameData['board']      = self.pos.board
        self.gameData['score']      = self.pos.score
        self.gameData['wc']         = self.pos.wc
        self.gameData['bc']         = self.pos.bc 
        self.gameData['ep']         = self.pos.ep 
        self.gameData['kp']         = self.pos.kp
        self.gameData['movecount']  = self.moveCount
        self.gameData['difficulty'] = self.difficulty
        self.gameData['playerside'] = self.playerSide
        
        f = open( lib.savefile, "w")
        f.write( json.dumps( self.gameData))
        f.close()
        
    def loadGame( self):
        
        if not os.path.isfile( lib.savefile):
            return
        
        f = open( lib.savefile, "r")
        data = json.loads( f.read())
        f.close()
        
        self.pos = sunfish.Position( data['board'],
                                     data['score'],
                                     tuple( data['wc']),
                                     tuple( data['bc']),
                                     data['ep'],
                                     data['kp'])
        self.moveCount = data['movecount']
        self.setDifficulty( data['difficulty'])
        self.setPlayerSide( data['playerside'])
        
        self.displayPieces()
        
    def setDifficulty( self, dif):
        self.difficulty = dif

    def __init__( self, side=WHITE, difficulty=1, loadGame=False):
        self.moveCount    = 0
        self.setPlayerSide( side)
        self.setDifficulty( difficulty)
        self.gameData = {}

        self.setCoordinateResolution( 0)
        lib.imgpath = 'special://home/addons/script.chess/resources/media/'
        self.images = {}
        self.images['background'] = xbmcgui.ControlImage(
                        x=0,
                        y=0,
                        width    = 1920,
                        height   = 1080,
                        filename = lib.imgpath + 'ingamebg.jpg')
        self.addControl( self.images['background'])

        self.cursorX = 4 # starts at 0, so 4 is column E
        self.cursorY = 6

        self.images['cursor'] = xbmcgui.ControlImage(
                        x = 97 + self.cursorX*110,
                        y = 97 + self.cursorY*110,
                        width  = 116,
                        height = 116,
                        filename = lib.imgpath + 'cursor.png')
        self.addControl( self.images['cursor'])

        self.selectedX = -100
        self.selectedY = -100

        self.images['selected'] = xbmcgui.ControlImage(
                        x = 100 + self.selectedX*110,
                        y = 100 + self.selectedY*110,
                        width  = 110,
                        height = 110,
                        filename = lib.imgpath + 'selected.png')
        self.addControl( self.images['selected'])

        self.txtHelp = xbmcgui.ControlTextBox(
                            x = 1130,
                            y = 330,
                            width  = 690,
                            height = 650,
                            font   = 'font14')
        self.addControl( self.txtHelp)
        self.txtHelp.setText( _('help_text'))
        
        print("d")

        tilelist = [] # adding the controls one by one is really slow, so
                      # I'm using a tilelist to add the 64 images in one go
                      # with addControls instead of addControl
        for row in range( 1, 9):
            for col in range( 1, 9):
                self.images['{0}x{1}'.format( col, row)] = xbmcgui.ControlImage(
                    x = col * 110,
                    y = row * 110,
                    width    = 90,
                    height   = 90,
                    filename = lib.imgpath + 't.png')
                tilelist.append( self.images['{0}x{1}'.format( col, row)])
        self.addControls( tilelist)

        self.lblFeedback = xbmcgui.ControlLabel( x      = 1170,
                                                 y      = 100,
                                                 width  = 750,
                                                 height = 160,
                                                 label     = 'Status',
                                                 font      = 'font35_title',
                                                 textColor = '0xFFFFFFFF')
        self.addControl( self.lblFeedback)

        initialPosition = sunfish.initial
        
        if loadGame:
            self.loadGame()
        else:
            self.pos = sunfish.Position( initialPosition, 0,
                                         (True, True),
                                         (True, True), 0, 0)

        if side==BLACK:
            thread.start_new_thread( self.computerMove, ())
            
        self.displayPieces()
      

    def isPlayersTurn( self):
        return self.playerSide==(self.moveCount%2)

    def feedback( self, s):
        self.lblFeedback.setLabel( s)

    def clearSaveGame( self):
        if os.path.isfile( lib.savefile):
            os.unlink( lib.savefile)

    def computerMove( self):
        
        self.feedback( "Thinking...")

        move, score     = sunfish.search( self.pos, SEARCHDEPTH[ self.difficulty])

        if score <= -MATE_VALUE:
            self.feedback("Checkmate! You won!")
            self.clearSaveGame();
            return
        if score >= MATE_VALUE:
            self.feedback("Checkmate! You lost!")
            self.clearSaveGame()
            return

        self.makeMove( move)

        self.displayPieces()
        self.feedback( "Your move!")

    def makeMove( self, move):
        self.pos = self.pos.move( move)
        self.moveCount += 1
        self.saveGame()

    def displayPieces( self):
        p = self.pos if self.isPlayersTurn() else self.pos.rotate()
        for row in range( 1, 9):
            for col in range( 1, 9):
                piece = p.board[ col + row*10 + 10]
                if piece == '.':
                    piece = 't'
                elif self.playerSide == BLACK:
                    piece = self.reverseCase( piece)
                
                piece = piece + '.png'
                self.images['{0}x{1}'.format( col, row)].setImage( lib.imgpath + piece)
