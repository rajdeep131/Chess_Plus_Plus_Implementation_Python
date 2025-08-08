
class Move:
    def __init__(self,movedBy,startCoordinate=None,endCoordinate=None,pieceMovedName=None,pieceCapturedName=None):
        self.startCoordinate=startCoordinate
        self.endCoordinate=endCoordinate
        self.pieceMovedName=pieceMovedName
        self.pieceCapturedName=pieceCapturedName
        self.movedBy=movedBy
        self.specialMove=None
        self.catapultCaptured=False
        self.throughCatapultMove=False
        self.moveTiming=None
        
    def generateMoveDetails(self):
        pass 

        
        


            
        
        
    
    
    
    