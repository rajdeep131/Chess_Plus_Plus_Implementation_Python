from abc import abstractmethod

def isInTheBoard(coordinate):
    if coordinate[0]>7 or coordinate[0]<0 or coordinate[1]>7 or coordinate[1]<0 :
        return False
    return True

def createMoveDictionary():
    moveDict={
        'movedBy':None,
        'startCoordinate':None,
        'endCoordinate': None,
        'specialMove':None,
        'catapultMove':None,
        'throughCatapultMove':False
    }
    return moveDict


class Piece:
    def __init__(self,color,currentPos,name,boardObject):
        self.color=color
        self.currentPos=currentPos
        self.name=name
        self.boardObject=boardObject
    
    def updateCurrentPos(self,pos):
        self.currentPos=pos
    
    @abstractmethod
    def returnValidMoves(self):
        pass

    def isOnCatapult(self,catapultColor):
        if self.boardObject.underBoard[self.currentPos[0]][self.currentPos[1]]!=0:
            if self.boardObject.underBoard[self.currentPos[0]][self.currentPos[1]].color==catapultColor:
                return True
        return False

    def throughCatapultMove(self):
        move=createMoveDictionary()
        if self.isOnCatapult(catapultColor=self.color):
            catapultCoordinate1=self.boardObject.pieces[self.color]['Catapults'][0].currentPos
            catapultCoordinate2=self.boardObject.pieces[self.color]['Catapults'][1].currentPos
            if not self.boardObject.checkIfOccupiedSq(catapultCoordinate1,occupiedBy=self.color):
                move['movedBy']=self.color
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=catapultCoordinate1
                move['throughCatapultMove']=True
                return [move]
            if not self.boardObject.checkIfOccupiedSq(catapultCoordinate2,occupiedBy=self.color):
                move['movedBy']=self.color
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=catapultCoordinate2
                move['throughCatapultMove']=True
                return [move]
        return []
        

class Knight(Piece):
    def __init__(self, color, currentPos, board, name='Knight'):
        super().__init__(color, currentPos, name, board)

    def returnValidMoves(self,checkRestricted=True):
        validMoveList=[]
        tempList=[(self.currentPos[0]+2,self.currentPos[1]+1),(self.currentPos[0]+2,self.currentPos[1]-1),
                  (self.currentPos[0]-2,self.currentPos[1]+1),(self.currentPos[0]-2,self.currentPos[1]-1),
                  (self.currentPos[0]+1,self.currentPos[1]+2),(self.currentPos[0]-1,self.currentPos[1]+2),
                  (self.currentPos[0]+1,self.currentPos[1]-2),(self.currentPos[0]-1,self.currentPos[1]-2)]
        
        
        for el in tempList:
            if (not isInTheBoard(el)) or self.boardObject.checkIfOccupiedSq(el,occupiedBy=self.color):
                continue
            move=createMoveDictionary()
            move['movedBy']=self.color
            move['startCoordinate']=self.currentPos
            move['endCoordinate']=el
            validMoveList.append(move)
        
        validMoveList+=self.throughCatapultMove()

        
        checkRestrictedValidMoveList=[]
        if checkRestricted:
            for el in validMoveList:
                if not self.boardObject.isMoveLeadsToCheck(el,self.color):
                    checkRestrictedValidMoveList.append(el)
            return checkRestrictedValidMoveList

        
        return validMoveList
    
class Bishop(Piece):
    def __init__(self, color, currentPos, board, name='Bishop'):
        super().__init__(color, currentPos, name, board)

    def returnValidMoves(self,checkRestricted=True):
        validMoveList=[]      
        for el in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            posX=self.currentPos[0]
            posY=self.currentPos[1]
            while True:
                posX+=el[0]
                posY+=el[1]
                if not isInTheBoard((posX,posY)):
                    break
                if self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color==self.color:
                    break
                if  self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color!=self.color:
                    move=createMoveDictionary()
                    move['movedBy']=self.color
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(posX,posY)
                    validMoveList.append(move)
                    break
                move=createMoveDictionary()
                move['movedBy']=self.color
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=(posX,posY)
                validMoveList.append(move)
            
        validMoveList+=self.throughCatapultMove()

        checkRestrictedValidMoveList=[]
        if checkRestricted:
            for el in validMoveList:
                if not self.boardObject.isMoveLeadsToCheck(el,self.color):
                    checkRestrictedValidMoveList.append(el)
            return checkRestrictedValidMoveList
       
        
        return validMoveList

class Rook(Piece):
    def __init__(self, color, currentPos, board, name='Rook'):
        super().__init__(color, currentPos, name, board)
    
    def returnValidMoves(self,checkRestricted=True):
        validMoveList=[]      
        for el in [(0,1),(0,-1),(-1,0),(1,0)]:
            posX=self.currentPos[0]
            posY=self.currentPos[1]
            while True:
                posX+=el[0]
                posY+=el[1]
                if not isInTheBoard((posX,posY)):
                    break
                if self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color==self.color:
                    break
                if  self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color!=self.color:
                    move=createMoveDictionary()
                    move['movedBy']=self.color
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(posX,posY)
                    validMoveList.append(move)
                    break
                move=createMoveDictionary()
                move['movedBy']=self.color
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=(posX,posY)
                validMoveList.append(move)
            
        validMoveList+=self.throughCatapultMove()

        checkRestrictedValidMoveList=[]
        if checkRestricted:
            for el in validMoveList:
                if not self.boardObject.isMoveLeadsToCheck(el,self.color):
                    checkRestrictedValidMoveList.append(el)
            return checkRestrictedValidMoveList

             
        return validMoveList
    
class Queen(Piece):
    def __init__(self, color, currentPos, board, name='Queen'):
        super().__init__(color, currentPos, name, board)

    def returnValidMoves(self,checkRestricted=True):
        validMoveList=[]      
        for el in [(0,1),(0,-1),(-1,0),(1,0)]:
            posX=self.currentPos[0]
            posY=self.currentPos[1]
            while True:
                posX+=el[0]
                posY+=el[1]
                if not isInTheBoard((posX,posY)):
                    break
                if  self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color==self.color:
                    break
                if  self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color!=self.color:
                    move=createMoveDictionary()
                    move['movedBy']=self.color
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(posX,posY)
                    validMoveList.append(move)
                    break
                move=createMoveDictionary()
                move['movedBy']=self.color
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=(posX,posY)
                validMoveList.append(move)
        
        for el in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            posX=self.currentPos[0]
            posY=self.currentPos[1]
            while True:
                posX+=el[0]
                posY+=el[1]
                if not isInTheBoard((posX,posY)):
                    break
                if self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color==self.color:
                    break
                if  self.boardObject.board[posX][posY]!=0 and self.boardObject.board[posX][posY].color!=self.color:
                    move=createMoveDictionary()
                    move['movedBy']=self.color
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(posX,posY)
                    validMoveList.append(move)
                    break
                move=createMoveDictionary()
                move['movedBy']=self.color
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=(posX,posY)
                validMoveList.append(move)
    
        validMoveList+=self.throughCatapultMove()

        checkRestrictedValidMoveList=[]
        if checkRestricted:
            for el in validMoveList:
                if not self.boardObject.isMoveLeadsToCheck(el,self.color):
                    checkRestrictedValidMoveList.append(el)
            return checkRestrictedValidMoveList
        
        return validMoveList
            
class King(Piece):
    def __init__(self, color, currentPos, board, name='King'):
        self.castleRights={'QS':True,'KS':True}
        super().__init__(color, currentPos, name, board)
    
    def returnValidMoves(self,checkRestricted=True):
        validMoveList=[]
        for el in [(1,1),(1,0),(0,1),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1)]:
            posX=self.currentPos[0]+el[0]
            posY=self.currentPos[1]+el[1]
            if not isInTheBoard((posX,posY)):
                continue
            if  self.boardObject.checkIfOccupiedSq((posX,posY),occupiedBy=self.color):
                continue
            move=createMoveDictionary()
            move['movedBy']=self.color
            move['startCoordinate']=self.currentPos
            move['endCoordinate']=(posX,posY)
            validMoveList.append(move)
        
        validMoveList+=self.throughCatapultMove()
        
        if checkRestricted:       
            if self.color=='White' and (not self.boardObject.checkIfThreatenedSq((7,4),threatenedBy='Black')):
                if self.castleRights['KS'] :
                    if self.boardObject.board[7][5]==0 and self.boardObject.board[7][6]==0 and \
                    (not self.boardObject.checkIfThreatenedSq((7,5),threatenedBy='Black')) and (not self.boardObject.checkIfThreatenedSq((7,6),threatenedBy='Black')):
                        move=createMoveDictionary()
                        move['movedBy']=self.color
                        move['specialMove']='W_Castling_KS'
                        validMoveList.append(move)                   
                
                if self.castleRights['QS'] :
                    if self.boardObject.board[7][3]==0 and self.boardObject.board[7][2]==0 and self.boardObject.board[7][1]==0 and \
                    (not self.boardObject.checkIfThreatenedSq((7,3),threatenedBy='Black')) and (not self.boardObject.checkIfThreatenedSq((7,2),threatenedBy='Black')) :
                        move=createMoveDictionary()
                        move['movedBy']=self.color
                        move['specialMove']='W_Castling_QS'
                        validMoveList.append(move)
            
            if self.color=='Black' and (not self.boardObject.checkIfThreatenedSq((0,4),threatenedBy='White')):
                if self.castleRights['KS'] :
                    if self.boardObject.board[0][5]==0 and self.boardObject.board[0][6]==0 and \
                        (not self.boardObject.checkIfThreatenedSq((0,5),threatenedBy='White')) and (not self.boardObject.checkIfThreatenedSq((0,6),threatenedBy='White')):
                        move=createMoveDictionary()
                        move['movedBy']=self.color
                        move['specialMove']='B_Castling_KS'
                        validMoveList.append(move)
                
                if self.castleRights['QS'] :
                    if self.boardObject.board[0][3]==0 and self.boardObject.board[0][2]==0 and self.boardObject.board[0][1]==0 and \
                    (not self.boardObject.checkIfThreatenedSq((0,3),threatenedBy='White')) and (not self.boardObject.checkIfThreatenedSq((0,2),threatenedBy='White')) :
                        move=createMoveDictionary()
                        move['movedBy']=self.color
                        move['specialMove']='B_Castling_QS'
                        validMoveList.append(move)
        
            checkRestrictedValidMoveList=[]
            if checkRestricted:
                for el in validMoveList:
                    if not self.boardObject.isMoveLeadsToCheck(el,self.color):
                        checkRestrictedValidMoveList.append(el)
                return checkRestrictedValidMoveList
      
        
        return validMoveList
    
    def isKingInCheck(self):
        return self.boardObject.checkIfThreatenedSq(self.currentPos,threatenedBy='White' if self.color=='Black' else 'Black')

class Catapult(Piece):
    def __init__(self, color, currentPos, board, name='Catapult'):
        self.initialMobilityRights=True
        super().__init__(color, currentPos, name, board)
    
    def isOpponentOnMe(self):
        if self.boardObject.board[self.currentPos[0]][self.currentPos[1]]==0:
            return False
        return self.boardObject.board[self.currentPos[0]][self.currentPos[1]].color != self.color 
    
    def returnValidMoves(self):
        validMoveList=[]
        if self.boardObject.checkIfThreatenedSq(self.boardObject.pieces[self.color]['King'].currentPos,threatenedBy='White' if self.color=='Black' else 'Black'):
            return validMoveList
        if self.boardObject.board[self.currentPos[0]][self.currentPos[1]]!=0:
            return validMoveList
        else:
            for el in [(1,1),(1,0),(0,1),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1)]:
                posX=self.currentPos[0]
                posY=self.currentPos[1]
                posX+=el[0]
                posY+=el[1]
                if (not isInTheBoard((posX,posY))) or self.boardObject.board[posX][posY]!=0 or self.boardObject.underBoard[posX][posY]!=0:
                    continue
                move=createMoveDictionary()
                move['movedBy']=self.color
                move['catapultMove']=(self.currentPos,(posX,posY))
                validMoveList.append(move)

            if self.initialMobilityRights:
                validMoveList=[]
                for el in [(1,1),(1,0),(0,1),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1),(-2, -2), (-2, -1), (-2,  0), (-2,  1), (-2,  2),(-1, -2),(-1,  2),( 0, -2),( 0,  2),( 1, -2),( 1,  2),( 2, -2), ( 2, -1), ( 2,  0), ( 2,  1), ( 2,  2)]:
                    posX=self.currentPos[0]
                    posY=self.currentPos[1]
                    posX+=el[0]
                    posY+=el[1]
                    if (not isInTheBoard((posX,posY))) or self.boardObject.board[posX][posY]!=0 or self.boardObject.underBoard[posX][posY]!=0:
                        continue
                    move=createMoveDictionary()
                    move['movedBy']=self.color
                    move['catapultMove']=(self.currentPos,(posX,posY))
                    validMoveList.append(move)
        

        return validMoveList
    
class Pawn(Piece):
    def __init__(self, color, currentPos, board, name='Pawn'):
        self.isZeroEnPassantPossible=False
        self.isSevenEnPassantPossible=False
        super().__init__(color, currentPos, name, board)
    
    def initializeEnPassantRights(self):
        self.isZeroEnPassantPossible=False
        self.isSevenEnPassantPossible=False
    
    def returnValidMoves(self,checkRestricted=True):
        validMoveList=[]
        if self.color=='White':
            if self.boardObject.board[self.currentPos[0]-1][self.currentPos[1]] == 0:
                if self.currentPos[0]==1: #Pawn Promotion
                    for pieceName in ['Queen','Rook','Bishop','Knight']:
                        move=createMoveDictionary()
                        move['movedBy']='White'
                        move['specialMove']=f'Pawn_Promotion_W_{pieceName}_{self.currentPos[1]}_{self.currentPos[1]}'
                        validMoveList.append(move)
                else:
                    move=createMoveDictionary()
                    move['movedBy']='White'
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(self.currentPos[0]-1,self.currentPos[1])
                    validMoveList.append(move)
                    
            if self.currentPos[0]==6 and self.boardObject.board[self.currentPos[0]-2][self.currentPos[1]] == 0 and self.boardObject.board[self.currentPos[0]-1][self.currentPos[1]] == 0:
                move=createMoveDictionary()
                move['movedBy']='White'
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=(self.currentPos[0]-2,self.currentPos[1])
                validMoveList.append(move)
            
            if isInTheBoard((self.currentPos[0]-1,self.currentPos[1]+1)) and self.boardObject.checkIfOccupiedSq((self.currentPos[0]-1,self.currentPos[1]+1),'Black'):
                if self.currentPos[0]==1:
                    for pieceName in ['Queen','Rook','Bishop','Knight']:
                        move=createMoveDictionary()
                        move['movedBy']='White'
                        move['specialMove']=f'Pawn_Promotion_W_{pieceName}_{self.currentPos[1]}_{self.currentPos[1]+1}'
                        validMoveList.append(move)
                else:
                    move=createMoveDictionary()
                    move['movedBy']='White'
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(self.currentPos[0]-1,self.currentPos[1]+1)
                    validMoveList.append(move)
            if isInTheBoard((self.currentPos[0]-1,self.currentPos[1]-1)) and self.boardObject.checkIfOccupiedSq((self.currentPos[0]-1,self.currentPos[1]-1),'Black'):
                if self.currentPos[0]==1:
                    for pieceName in ['Queen','Rook','Bishop','Knight']:
                        move=createMoveDictionary()
                        move['movedBy']='White'
                        move['specialMove']=f'Pawn_Promotion_W_{pieceName}_{self.currentPos[1]}_{self.currentPos[1]-1}'
                        validMoveList.append(move)
                else:
                    move=createMoveDictionary()
                    move['movedBy']='White'
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(self.currentPos[0]-1,self.currentPos[1]-1)
                    validMoveList.append(move)
            
            if self.isZeroEnPassantPossible:
                move=createMoveDictionary()
                move['movedBy']='White'
                move['specialMove']=f'En_Passant_{self.currentPos[1]}_{self.currentPos[1]-1}'
                validMoveList.append(move)
            if self.isSevenEnPassantPossible:
                move=createMoveDictionary()
                move['movedBy']='White'
                move['specialMove']=f'En_Passant_{self.currentPos[1]}_{self.currentPos[1]+1}'
                validMoveList.append(move)

        
        if self.color=='Black':
            if self.boardObject.board[self.currentPos[0]+1][self.currentPos[1]] == 0:
                if self.currentPos[0]==6: #Pawn Promotion
                    for pieceName in ['Queen','Rook','Bishop','Knight']:
                        move=createMoveDictionary()
                        move['movedBy']='Black'
                        move['specialMove']=f'Pawn_Promotion_B_{pieceName}_{self.currentPos[1]}_{self.currentPos[1]}'
                        validMoveList.append(move)
                else:
                    move=createMoveDictionary()
                    move['movedBy']='Black'
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(self.currentPos[0]+1,self.currentPos[1])
                    validMoveList.append(move)
                    
            if self.currentPos[0]==1 and self.boardObject.board[self.currentPos[0]+2][self.currentPos[1]] == 0 and self.boardObject.board[self.currentPos[0]+1][self.currentPos[1]] == 0:
                move=createMoveDictionary()
                move['movedBy']='Black'
                move['startCoordinate']=self.currentPos
                move['endCoordinate']=(self.currentPos[0]+2,self.currentPos[1])
                validMoveList.append(move)
            
            if isInTheBoard((self.currentPos[0]+1,self.currentPos[1]-1)) and self.boardObject.checkIfOccupiedSq((self.currentPos[0]+1,self.currentPos[1]-1),'White'):
                if self.currentPos[0]==6:
                    for pieceName in ['Queen','Rook','Bishop','Knight']:
                        move=createMoveDictionary()
                        move['movedBy']='Black'
                        move['specialMove']=f'Pawn_Promotion_B_{pieceName}_{self.currentPos[1]}_{self.currentPos[1]-1}'
                        validMoveList.append(move)
                else:
                    move=createMoveDictionary()
                    move['movedBy']='Black'
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(self.currentPos[0]+1,self.currentPos[1]-1)
                    validMoveList.append(move)
            if isInTheBoard((self.currentPos[0]+1,self.currentPos[1]+1)) and self.boardObject.checkIfOccupiedSq((self.currentPos[0]+1,self.currentPos[1]+1),'White'):
                if self.currentPos[0]==6:
                    for pieceName in ['Queen','Rook','Bishop','Knight']:
                        move=createMoveDictionary()
                        move['movedBy']='Black'
                        move['specialMove']=f'Pawn_Promotion_B_{pieceName}_{self.currentPos[1]}_{self.currentPos[1]+1}'
                        validMoveList.append(move)
                else:
                    move=createMoveDictionary()
                    move['movedBy']='Black'
                    move['startCoordinate']=self.currentPos
                    move['endCoordinate']=(self.currentPos[0]+1,self.currentPos[1]+1)
                    validMoveList.append(move)
            
            if self.isZeroEnPassantPossible:
                move=createMoveDictionary()
                move['movedBy']='Black'
                move['specialMove']=f'En_Passant_{self.currentPos[1]}_{self.currentPos[1]-1}'
                validMoveList.append(move)
            if self.isSevenEnPassantPossible:
                move=createMoveDictionary()
                move['movedBy']='Black'
                move['specialMove']=f'En_Passant_{self.currentPos[1]}_{self.currentPos[1]+1}'
                validMoveList.append(move)
        
        checkRestrictedValidMoveList=[]
        if checkRestricted:
            for el in validMoveList:
                if not self.boardObject.isMoveLeadsToCheck(el,self.color):
                    checkRestrictedValidMoveList.append(el)
            return checkRestrictedValidMoveList
        
        
        return validMoveList



        
        

            
            

        

        
