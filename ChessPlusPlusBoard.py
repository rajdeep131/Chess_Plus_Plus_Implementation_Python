from ChessPlusPlusPieces import King,Queen,Knight,Bishop,Rook,Catapult,Pawn,isInTheBoard
from Move import Move

class ChessPlusPlusBoard():
    def __init__(self): #initializing all the necessary variables
        self.board=[[0 for _ in range(8)] for _ in range(8)] #for standard chess pieces
        self.underBoard=[[0 for _ in range(8)] for _ in range(8)] #for catapults
        self.pieces={'Black':{},'White':{}} #dictionary for storing pieces for each color
        self.capturedWhitePieces=[]
        self.capturedBlackPieces=[]
        self.piecesCaptured=[]
        self.moveHistory=[]
        self.initializeBoard()
        #self.customBoard()


    def initializeBoard(self): #initializing chessplusplus starting board setup
        self.board[0][0]=Rook(color='Black',currentPos=(0,0),board=self)
        self.board[0][7]=Rook(color='Black',currentPos=(0,7),board=self)
        self.pieces['Black']['Rooks']=[self.board[0][0],self.board[0][7]]
        self.board[0][1]=Knight(color='Black',currentPos=(0,1),board=self)
        self.board[0][6]=Knight(color='Black',currentPos=(0,6),board=self)
        self.pieces['Black']['Knights']=[self.board[0][1],self.board[0][6]]
        self.board[0][2]=Bishop(color='Black',currentPos=(0,2),board=self)
        self.board[0][5]=Bishop(color='Black',currentPos=(0,5),board=self)
        self.pieces['Black']['Bishops']=[self.board[0][2],self.board[0][5]]
        self.board[0][3]=Queen(color='Black',currentPos=(0,3),board=self)
        self.pieces['Black']['Queen']= self.board[0][3]
        self.board[0][4]=King(color='Black',currentPos=(0,4),board=self)
        self.pieces['Black']['King']= self.board[0][4]
        self.underBoard[0][1]=Catapult(color='Black',currentPos=(0,1),board=self)
        self.underBoard[0][5]=Catapult(color='Black',currentPos=(0,5),board=self)
        self.pieces['Black']['Catapults']= [self.underBoard[0][1],self.underBoard[0][5]]
        self.pieces['Black']['Pawns']= [0 for _ in range(8)]
        for i in range(8):
            self.board[1][i]=Pawn(color='Black',currentPos=(1,i),board=self)
            self.pieces['Black']['Pawns'][i]=self.board[1][i]
        
        self.board[7][0]=Rook(color='White',currentPos=(7,0),board=self)
        self.board[7][7]=Rook(color='White',currentPos=(7,7),board=self)
        self.pieces['White']['Rooks']=[self.board[7][0],self.board[7][7]]
        self.board[7][1]=Knight(color='White',currentPos=(7,1),board=self)
        self.board[7][6]=Knight(color='White',currentPos=(7,6),board=self)
        self.pieces['White']['Knights']=[self.board[7][1],self.board[7][6]]
        self.board[7][2]=Bishop(color='White',currentPos=(7,2),board=self)
        self.board[7][5]=Bishop(color='White',currentPos=(7,5),board=self)
        self.pieces['White']['Bishops']=[self.board[7][2],self.board[7][5]]
        self.board[7][3]=Queen(color='White',currentPos=(7,3),board=self)
        self.pieces['White']['Queen']= self.board[7][3]
        self.board[7][4]=King(color='White',currentPos=(7,4),board=self)
        self.pieces['White']['King']= self.board[7][4]
        self.underBoard[7][1]=Catapult(color='White',currentPos=(7,1),board=self)
        self.underBoard[7][5]=Catapult(color='White',currentPos=(7,5),board=self)
        self.pieces['White']['Catapults']= [self.underBoard[7][1],self.underBoard[7][5]]
        self.pieces['White']['Pawns']= [0 for _ in range(8)]
        for i in range(8):
            self.board[6][i]=Pawn(color='White',currentPos=(6,i),board=self)
            self.pieces['White']['Pawns'][i]=self.board[6][i]
    
    def customBoard(self): # custom board for experimentation (may sometimes leads to bug)
        self.board[7][0]=Rook(color='White',currentPos=(7,0),board=self)
        self.board[7][7]=Rook(color='White',currentPos=(7,7),board=self)
        self.board[7][4]=King(color='White',currentPos=(7,4),board=self)

        self.board[0][0]=Rook(color='Black',currentPos=(0,0),board=self)
        self.board[0][7]=Rook(color='Black',currentPos=(0,7),board=self)
        self.board[0][4]=King(color='Black',currentPos=(0,4),board=self)
        self.board[3][3]=Queen(color='Black',currentPos=(3,3),board=self)

        #self.board[1][5]=Pawn(color='White',currentPos=(1,5),board=self)
        self.board[4][4]=Pawn(color='White',currentPos=(4,4),board=self)
        self.board[6][5]=Pawn(color='Black',currentPos=(6,5),board=self)
        self.board[5][6]=Pawn(color='Black',currentPos=(5,6),board=self)

        self.underBoard[3][3]=Catapult(color='Black',currentPos=(3,3),board=self)
        self.underBoard[7][5]=Catapult(color='Black',currentPos=(7,5),board=self)

        self.pieces['Black']['Catapults']= [self.underBoard[3][3],self.underBoard[7][5]]

        self.underBoard[3][2]=Catapult(color='White',currentPos=(3,2),board=self)
        self.underBoard[7][4]=Catapult(color='White',currentPos=(7,4),board=self)

        self.pieces['White']['Catapults']= [self.underBoard[3][2],self.underBoard[7][4]]
        self.pieces['White']['Pawns']=[]
        self.pieces['Black']['King']= self.board[0][4]
        self.pieces['White']['King']= self.board[7][4]
    
    def checkIfThreatenedSq(self,square,threatenedBy): #checking if any given square is threatened by the color given . This function is used to check for CHECK to King majorly , some other use are in castling posibility checking
        if threatenedBy=='White':
            for row in range(8):
                for col in range(8):
                    if self.board[row][col]!=0 and self.board[row][col].color=='White':
                        if self.board[row][col].name!='Pawn' :
                            endCoordinateList=[]
                            for el in self.board[row][col].returnValidMoves(checkRestricted=False): #Check Restricted =True will skip all the moves that leads to check to itself 
                                if el['endCoordinate']!=None :
                                    endCoordinateList.append(el['endCoordinate'])
                            if square in endCoordinateList:
                                return True
                        if self.board[row][col].name=='Pawn':
                            if square in [(self.board[row][col].currentPos[0]-1,self.board[row][col].currentPos[1]-1),(self.board[row][col].currentPos[0]-1,self.board[row][col].currentPos[1]+1)]:
                                return True
        
        if threatenedBy=='Black':
            for row in range(8):
                for col in range(8):
                    if self.board[row][col]!=0 and self.board[row][col].color=='Black': 
                        if self.board[row][col].name!='Pawn' :
                            endCoordinateList=[]
                            for el in self.board[row][col].returnValidMoves(checkRestricted=False):
                                if el['endCoordinate']!=None :
                                    endCoordinateList.append(el['endCoordinate'])
                            if square in endCoordinateList:
                                return True
                        if self.board[row][col].name=='Pawn':
                            if square in [(self.board[row][col].currentPos[0]+1,self.board[row][col].currentPos[1]-1),(self.board[row][col].currentPos[0]+1,self.board[row][col].currentPos[1]+1)]:
                                return True
        
        return False
    
    def checkIfOccupiedSq(self,square,occupiedBy,underBoradCheck=False): # this function is to check if some squre is occupied by some piece of given color
        if underBoradCheck:
            if self.underBoard[square[0]][square[1]]==0:
                return False
            elif self.underBoard[square[0]][square[1]].color==occupiedBy:
                return True
            else:
                return False
        else:
            if self.board[square[0]][square[1]]==0:
                return False
            elif self.board[square[0]][square[1]].color==occupiedBy:
                return True
            else:
                return False
        
    
    def isMoveLeadsToCheck(self,move,color): #checking if the move leads to CHECK to a given color king , it does so by creating a copy of main board and underboard and then play the move , then reassign the copied board to current board
        oldBorad=[[0 for _ in range(8)] for _ in range(8)]
        oldUnderBoard=[[0 for _ in range(8)] for _ in range(8)]
        for row in range(8):     
            for col in range(8):
                oldBorad[row][col]=self.board[row][col]  #copying the main board
        for row in range(8):
            for col in range(8):
                oldUnderBoard[row][col]=self.underBoard[row][col]  #copying the underboard
        self.playMove(move,updateValue=False,storeMove=False) #playing move without updating any value and storing any move
        kingPosition=None
        for row in range(8):
            for col in range(8):
                if self.board[row][col]==0:
                    continue
                if self.board[row][col].name=='King' and self.board[row][col].color==color:  #Finding king position
                    kingPosition=(row,col)
                    break
        if self.checkIfThreatenedSq(kingPosition,threatenedBy='White' if color=='Black' else 'Black'): #checking if its leading to CHECK
            for row in range(8): #reassign the copied board to current board
                for col in range(8):
                    self.board[row][col]=oldBorad[row][col]
            for row in range(8):
                for col in range(8):
                    self.underBoard[row][col]=oldUnderBoard[row][col]
            return True
        for row in range(8): #reassign the copied board to current board
            for col in range(8):
                self.board[row][col]=oldBorad[row][col]
        for row in range(8):
            for col in range(8):
                self.underBoard[row][col]=oldUnderBoard[row][col]
        return False

     
    def playMove(self,move,updateValue=True,storeMove=True): 
        if storeMove and updateValue:
            moveInClass=self.storeMoveInClass(move)
            self.moveHistory.append(moveInClass)
        self.piecesCaptured=[]
        if move['specialMove']=='W_Castling_KS': #Handling White castling King side
            self.board[7][6]=self.board[7][4]
            self.board[7][4]=0
            self.board[7][5]=self.board[7][7]
            self.board[7][7]=0
            if updateValue:
                self.board[7][6].updateCurrentPos((7,6))
                self.board[7][5].updateCurrentPos((7,5))
                self.board[7][6].castleRights['KS']=False
                self.board[7][6].castleRights['QS']=False
        if move['specialMove']=='W_Castling_QS': #Handling White castling Queen side
            self.board[7][2]=self.board[7][4]
            self.board[7][4]=0
            self.board[7][3]=self.board[7][0]
            self.board[7][0]=0
            if updateValue:
                self.board[7][2].updateCurrentPos((7,2))
                self.board[7][3].updateCurrentPos((7,3))
                self.board[7][2].castleRights['KS']=False
                self.board[7][2].castleRights['QS']=False
        if move['specialMove']=='B_Castling_KS': #Handling Black castling King side
            self.board[0][6]=self.board[0][4]
            self.board[0][4]=0
            self.board[0][5]=self.board[0][7]
            self.board[0][7]=0
            if updateValue:
                self.board[0][6].updateCurrentPos((0,6))
                self.board[0][5].updateCurrentPos((0,5))
                self.board[0][6].castleRights['KS']=False
                self.board[0][6].castleRights['QS']=False
        if move['specialMove']=='B_Castling_QS': #Handling Black castling Queen side
            self.board[0][2]=self.board[0][4]
            self.board[0][4]=0
            self.board[0][3]=self.board[0][0]
            self.board[0][0]=0
            if updateValue:
                self.board[0][2].updateCurrentPos((0,2))
                self.board[0][3].updateCurrentPos((0,3))
                self.board[0][2].castleRights['KS']=False
                self.board[0][2].castleRights['QS']=False
        
        if move['specialMove']!=None and 'En_Passant' in move['specialMove']: #Handling en Passant
            if move['movedBy']=='White':
                self.board[2][int(move['specialMove'][-1])]=self.board[3][int(move['specialMove'][-3])]
                self.board[3][int(move['specialMove'][-3])]=0
                pieceCaptured=self.board[3][int(move['specialMove'][-1])]
                self.board[3][int(move['specialMove'][-1])]=0
                if updateValue:
                    self.board[2][int(move['specialMove'][-1])].updateCurrentPos((2,int(move['specialMove'][-1])))
                    self.piecesCaptured.append(pieceCaptured)
            if move['movedBy']=='Black':
                self.board[5][int(move['specialMove'][-1])]=self.board[4][int(move['specialMove'][-3])]
                self.board[4][int(move['specialMove'][-3])]=0
                pieceCaptured=self.board[4][int(move['specialMove'][-1])]
                self.board[4][int(move['specialMove'][-1])]=0
                if updateValue:
                    self.board[5][int(move['specialMove'][-1])].updateCurrentPos((5,int(move['specialMove'][-1])))
                    self.piecesCaptured.append(pieceCaptured)
        
        if move['specialMove']!=None and 'Pawn_Promotion' in move['specialMove']: #Handling Pawn Promotion
            if move['movedBy']=='White':
                startCoordinate=(1,int(move['specialMove'][-3]))
                endCoordinate=(0,int(move['specialMove'][-1]))
                pieceCaptured=self.board[endCoordinate[0]][endCoordinate[1]]
                self.board[endCoordinate[0]][endCoordinate[1]]=self.board[startCoordinate[0]][startCoordinate[1]]
                self.board[startCoordinate[0]][startCoordinate[1]]=0

                if updateValue:
                    self.piecesCaptured.append(pieceCaptured)
                    self.piecesCaptured.append(self.board[endCoordinate[0]][endCoordinate[1]])

                if 'Queen' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Queen(color='White',currentPos=endCoordinate,board=self)
                if 'Knight' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Knight(color='White',currentPos=endCoordinate,board=self)
                if 'Bishop' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Bishop(color='White',currentPos=endCoordinate,board=self)
                if 'Rook' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Rook(color='White',currentPos=endCoordinate,board=self)
                
            
            if move['movedBy']=='Black':
                startCoordinate=(6,int(move['specialMove'][-3]))
                endCoordinate=(7,int(move['specialMove'][-1]))
                pieceCaptured=self.board[endCoordinate[0]][endCoordinate[1]]
                self.board[endCoordinate[0]][endCoordinate[1]]=self.board[startCoordinate[0]][startCoordinate[1]]
                self.board[startCoordinate[0]][startCoordinate[1]]=0

                if updateValue:
                    self.piecesCaptured.append(pieceCaptured)
                    self.piecesCaptured.append(self.board[endCoordinate[0]][endCoordinate[1]])

                if 'Queen' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Queen(color='Black',currentPos=endCoordinate,board=self)
                if 'Knight' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Knight(color='Black',currentPos=endCoordinate,board=self)
                if 'Bishop' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Bishop(color='Black',currentPos=endCoordinate,board=self)
                if 'Rook' in move['specialMove']:
                    self.board[endCoordinate[0]][endCoordinate[1]]=Rook(color='Black',currentPos=endCoordinate,board=self)
        
        if move['catapultMove']!= None: # Handle Catapult move (not to confuse with through catapult move)
            startCoordinate=move['catapultMove'][0]
            endCoordinate=move['catapultMove'][1]
            self.underBoard[endCoordinate[0]][endCoordinate[1]]=self.underBoard[startCoordinate[0]][startCoordinate[1]]
            self.underBoard[startCoordinate[0]][startCoordinate[1]]=0
            if updateValue:
                self.underBoard[endCoordinate[0]][endCoordinate[1]].updateCurrentPos(endCoordinate)
                self.underBoard[endCoordinate[0]][endCoordinate[1]].initialMobilityRights=False
        
        if move['startCoordinate']!=None: #Handling  non special moves (special moves are castling , en passant , pawn promotion , catapult moving)
            startCoordinate=move['startCoordinate']
            endCoordinate=move['endCoordinate']
            pieceCaptured=self.board[endCoordinate[0]][endCoordinate[1]]
            self.board[endCoordinate[0]][endCoordinate[1]]=self.board[startCoordinate[0]][startCoordinate[1]]
            self.board[startCoordinate[0]][startCoordinate[1]]=0
            if updateValue:
                if pieceCaptured!=0:
                    self.piecesCaptured.append(pieceCaptured)

                if self.board[endCoordinate[0]][endCoordinate[1]]!=0 and self.board[endCoordinate[0]][endCoordinate[1]].name=='Rook': #update castle rights if rook moved
                    if self.board[endCoordinate[0]][endCoordinate[1]].currentPos==(0,0):
                        self.pieces['Black']['King'].castleRights['QS']=False
                    if self.board[endCoordinate[0]][endCoordinate[1]].currentPos==(0,7):
                        self.pieces['Black']['King'].castleRights['KS']=False
                    if self.board[endCoordinate[0]][endCoordinate[1]].currentPos==(7,0):
                        self.pieces['White']['King'].castleRights['QS']=False
                    if self.board[endCoordinate[0]][endCoordinate[1]].currentPos==(7,7):
                        self.pieces['White']['King'].castleRights['KS']=False
                
                if self.board[endCoordinate[0]][endCoordinate[1]]!=0 and self.board[endCoordinate[0]][endCoordinate[1]].name=='King': #update castle rights if king moved
                    self.pieces[move['movedBy']]['King'].castleRights['QS']=False
                    self.pieces[move['movedBy']]['King'].castleRights['KS']=False

                if self.board[endCoordinate[0]][endCoordinate[1]]!=0 and self.board[endCoordinate[0]][endCoordinate[1]].name=='Pawn':
                    if self.board[endCoordinate[0]][endCoordinate[1]].color=='White': #giving en passsant rights
                        if startCoordinate[0]==6 and endCoordinate[0]==4:
                            if isInTheBoard((endCoordinate[0],endCoordinate[1]+1)) and self.board[endCoordinate[0]][endCoordinate[1]+1]!=0 and self.board[endCoordinate[0]][endCoordinate[1]+1].name=='Pawn' and self.board[endCoordinate[0]][endCoordinate[1]+1].color=='Black':
                                self.board[endCoordinate[0]][endCoordinate[1]+1].isZeroEnPassantPossible=True
                            if isInTheBoard((endCoordinate[0],endCoordinate[1]-1)) and self.board[endCoordinate[0]][endCoordinate[1]-1]!=0 and self.board[endCoordinate[0]][endCoordinate[1]-1].name=='Pawn' and self.board[endCoordinate[0]][endCoordinate[1]-1].color=='Black':
                                self.board[endCoordinate[0]][endCoordinate[1]-1].isSevenEnPassantPossible=True
                            
                    if self.board[endCoordinate[0]][endCoordinate[1]].color=='Black':
                        if startCoordinate[0]==1 and endCoordinate[0]==3:
                            if isInTheBoard((endCoordinate[0],endCoordinate[1]+1)) and self.board[endCoordinate[0]][endCoordinate[1]+1]!=0 and self.board[endCoordinate[0]][endCoordinate[1]+1].name=='Pawn' and self.board[endCoordinate[0]][endCoordinate[1]+1].color=='White':
                                self.board[endCoordinate[0]][endCoordinate[1]+1].isZeroEnPassantPossible=True
                            if isInTheBoard((endCoordinate[0],endCoordinate[1]-1)) and self.board[endCoordinate[0]][endCoordinate[1]-1]!=0 and self.board[endCoordinate[0]][endCoordinate[1]-1].name=='Pawn' and self.board[endCoordinate[0]][endCoordinate[1]-1].color=='White':
                                self.board[endCoordinate[0]][endCoordinate[1]-1].isSevenEnPassantPossible=True
                            
                if self.board[endCoordinate[0]][endCoordinate[1]]!=0:            
                    self.board[endCoordinate[0]][endCoordinate[1]].updateCurrentPos(endCoordinate)
        
        if updateValue:
            if self.pieces['White']['Catapults'][0].isOpponentOnMe() and self.pieces['White']['Catapults'][1].isOpponentOnMe(): # Checking if catapults are captured 
                catapult1Pos=self.pieces['White']['Catapults'][0].currentPos
                catapult2Pos=self.pieces['White']['Catapults'][1].currentPos
                self.underBoard[catapult1Pos[0]][catapult1Pos[1]]=0
                self.underBoard[catapult2Pos[0]][catapult2Pos[1]]=0
                if updateValue:
                    self.piecesCaptured.append(self.pieces['White']['Catapults'][0])
                    self.piecesCaptured.append(self.pieces['White']['Catapults'][1])
                    if storeMove:
                        self.moveHistory[-1].catapultCaptured=True
            
            if self.pieces['Black']['Catapults'][0].isOpponentOnMe() and self.pieces['Black']['Catapults'][1].isOpponentOnMe():
                catapult1Pos=self.pieces['Black']['Catapults'][0].currentPos
                catapult2Pos=self.pieces['Black']['Catapults'][1].currentPos
                self.underBoard[catapult1Pos[0]][catapult1Pos[1]]=0
                self.underBoard[catapult2Pos[0]][catapult2Pos[1]]=0
                if updateValue:
                    self.piecesCaptured.append(self.pieces['Black']['Catapults'][0])
                    self.piecesCaptured.append(self.pieces['Black']['Catapults'][1])
                    if storeMove:
                        self.moveHistory[-1].catapultCaptured=True
            
            for el in self.pieces[move['movedBy']]['Pawns']: #Updating En Passant rights as En passant is only possible in next move 
                el.initializeEnPassantRights()
        
    def storeMoveInClass(self,rawMove): # this is to store moves in a more structure way in Move class imported from Move.py.
        startCoordinate=rawMove['startCoordinate']
        endCoordinate=rawMove['endCoordinate']
        move=None
        if startCoordinate!=None and rawMove['specialMove']==None:
            pieceMovedName=self.board[startCoordinate[0]][startCoordinate[1]].name
            pieceCapturedName=self.board[endCoordinate[0]][endCoordinate[1]].name if self.board[endCoordinate[0]][endCoordinate[1]]!=0 else None
            move=Move(movedBy=rawMove['movedBy'],startCoordinate=startCoordinate,endCoordinate=endCoordinate,pieceMovedName=pieceMovedName,pieceCapturedName=pieceCapturedName)
        if rawMove['catapultMove']!=None:
            pieceMovedName='Catapult'
            move=Move(movedBy=rawMove['movedBy'],startCoordinate=rawMove['catapultMove'][0],endCoordinate=rawMove['catapultMove'][1],pieceMovedName=pieceMovedName)
        if rawMove['specialMove']!= None:
            startCoordinate=None
            endCoordinate=None
            if 'En_Passant' in rawMove['specialMove']:
                if rawMove['movedBy']=='White':
                    startCoordinate=(3,int(rawMove['specialMove'][-3]))
                    endCoordinate=(2,int(rawMove['specialMove'][-1]))
                if rawMove['movedBy']=='Black':
                    startCoordinate=(4,int(rawMove['specialMove'][-3]))
                    endCoordinate=(5,int(rawMove['specialMove'][-1]))
                move=Move(movedBy=rawMove['movedBy'],startCoordinate=startCoordinate,endCoordinate=endCoordinate,pieceMovedName='Pawn',pieceCapturedName='Pawn')
                move.specialMove=rawMove
            if 'Castling' in rawMove['specialMove']:
                move=Move(movedBy=rawMove['movedBy'])
                move.specialMove=rawMove
            if 'Pawn_Promotion' in rawMove['specialMove']:
                if rawMove['movedBy']=='White':
                    startCoordinate=(1,int(rawMove['specialMove'][-3]))
                    endCoordinate=(0,int(rawMove['specialMove'][-1]))
                if rawMove['movedBy']=='Black':
                    startCoordinate=(6,int(rawMove['specialMove'][-3]))
                    endCoordinate=(7,int(rawMove['specialMove'][-1]))
                pieceCapturedName=self.board[endCoordinate[0]][endCoordinate[1]].name if endCoordinate and self.board[endCoordinate[0]][endCoordinate[1]]!=0 else None
                move=Move(movedBy=rawMove['movedBy'],startCoordinate=startCoordinate,endCoordinate=endCoordinate,pieceMovedName='Pawn',pieceCapturedName=pieceCapturedName)
                move.specialMove=rawMove
            if rawMove['throughCatapultMove']:
                move.throughCatapultMove=True
        return move

        


                

    def showBoard(self): # Black catapult [], White Catapult () , for showing board
        print('-----------------------------------------')
        for row in range(8):
            print('',end="|")
            for col in range(8):
                piece=self.board[row][col]
                underPiece=self.underBoard[row][col]
                if piece==0 and underPiece==0:
                    print("    ",end="|")
                elif piece==0 and underPiece!=0:
                    if underPiece.color=='Black':
                        print("[  ]",end="|")
                    if underPiece.color=='White':
                        print("(  )",end="|")
                elif piece!=0 and underPiece==0:
                        if piece.name=='Knight':
                            print(" "+piece.color[0]+"N ",end="|")
                        else:
                            print(" "+piece.color[0]+piece.name[0]+" ",end="|")
                else:
                    if underPiece.color=='Black':
                        if piece.name=='Knight':
                            print("["+piece.color[0]+"N]",end="|")
                        else:
                            print("["+piece.color[0]+piece.name[0]+"]",end="|")
                    if underPiece.color=='White':
                        if piece.name=='Knight':
                            print("("+piece.color[0]+"N)",end="|")
                        else:
                            print("("+piece.color[0]+piece.name[0]+")",end="|")
                if col==7:
                    print('')
            print('-----------------------------------------')
    
    def showMoves(self,color): #show all possible moves
        for row in range(8):
            for col in range(8):
                piece=self.board[row][col]
                underPiece=self.underBoard[row][col]
                if piece!=0 and piece.color==color:
                    validMoves=piece.returnValidMoves()
                    print("-----------------------------")
                    print(piece.name)
                    for el in validMoves:
                        print(el)
                if underPiece!=0 and underPiece.color==color:
                    validMoves=underPiece.returnValidMoves()
                    print("-----------------------------")
                    print(underPiece.name)
                    for el in validMoves:
                        print(el)
                
        
    
