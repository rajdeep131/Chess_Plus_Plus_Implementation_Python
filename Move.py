
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
        """
        Generate a detailed string representation of the move.
        Returns a formatted string describing the move in chess notation.
        """
        if self.specialMove:
            return self._generateSpecialMoveDetails()
        elif self.throughCatapultMove:
            return self._generateTeleportationMoveDetails()
        else:
            return self._generateRegularMoveDetails()
    
    def _generateRegularMoveDetails(self):
        """Generate details for regular moves"""
        details = f"{self.movedBy} {self.pieceMovedName}"
        
        if self.startCoordinate and self.endCoordinate:
            start_square = self._coordinateToSquare(self.startCoordinate)
            end_square = self._coordinateToSquare(self.endCoordinate)
            details += f" {start_square}-{end_square}"
        
        if self.pieceCapturedName:
            details += f" (captures {self.pieceCapturedName})"
        
        if self.catapultCaptured:
            details += " (catapult captured)"
        
        return details
    
    def _generateSpecialMoveDetails(self):
        """Generate details for special moves (castling, en passant, pawn promotion)"""
        if 'Castling' in self.specialMove:
            return self._generateCastlingDetails()
        elif 'En_Passant' in self.specialMove:
            return self._generateEnPassantDetails()
        elif 'Pawn_Promotion' in self.specialMove:
            return self._generatePawnPromotionDetails()
        else:
            return f"{self.movedBy} Special Move: {self.specialMove}"
    
    def _generateCastlingDetails(self):
        """Generate details for castling moves"""
        if 'W_Castling_KS' in self.specialMove:
            return "White Kingside Castling (O-O)"
        elif 'W_Castling_QS' in self.specialMove:
            return "White Queenside Castling (O-O-O)"
        elif 'B_Castling_KS' in self.specialMove:
            return "Black Kingside Castling (O-O)"
        elif 'B_Castling_QS' in self.specialMove:
            return "Black Queenside Castling (O-O-O)"
        else:
            return f"{self.movedBy} Castling: {self.specialMove}"
    
    def _generateEnPassantDetails(self):
        """Generate details for en passant moves"""
        if self.startCoordinate and self.endCoordinate:
            start_square = self._coordinateToSquare(self.startCoordinate)
            end_square = self._coordinateToSquare(self.endCoordinate)
            return f"{self.movedBy} Pawn En Passant {start_square}-{end_square}"
        else:
            return f"{self.movedBy} Pawn En Passant"
    
    def _generatePawnPromotionDetails(self):
        """Generate details for pawn promotion moves"""
        if self.startCoordinate and self.endCoordinate:
            start_square = self._coordinateToSquare(self.startCoordinate)
            end_square = self._coordinateToSquare(self.endCoordinate)
            
            # Extract promotion piece from special move string
            if 'Queen' in self.specialMove:
                promoted_piece = "Queen"
            elif 'Rook' in self.specialMove:
                promoted_piece = "Rook"
            elif 'Bishop' in self.specialMove:
                promoted_piece = "Bishop"
            elif 'Knight' in self.specialMove:
                promoted_piece = "Knight"
            else:
                promoted_piece = "Unknown"
            
            capture_info = ""
            if self.pieceCapturedName:
                capture_info = f" (captures {self.pieceCapturedName})"
            
            return f"{self.movedBy} Pawn Promotion {start_square}-{end_square}={promoted_piece}{capture_info}"
        else:
            return f"{self.movedBy} Pawn Promotion"
    
    def _generateTeleportationMoveDetails(self):
        """Generate details for teleportation moves through catapults"""
        if self.startCoordinate and self.endCoordinate:
            start_square = self._coordinateToSquare(self.startCoordinate)
            end_square = self._coordinateToSquare(self.endCoordinate)
            return f"{self.movedBy} {self.pieceMovedName} Teleportation {start_square}-{end_square}"
        else:
            return f"{self.movedBy} {self.pieceMovedName} Teleportation"
    
    def _coordinateToSquare(self, coordinate):
        """Convert board coordinates to chess square notation (e.g., (7,4) -> 'e1')"""
        if not coordinate:
            return "??"
        
        row, col = coordinate
        file_letter = chr(ord('a') + col)  # a-h for columns
        rank_number = 8 - row  # 1-8 for rows (1 is bottom, 8 is top)
        return f"{file_letter}{rank_number}"
    
    def __str__(self):
        """String representation of the move"""
        return self.generateMoveDetails()
    
    def __repr__(self):
        """Detailed representation for debugging"""
        return f"Move({self.generateMoveDetails()})" 

        
        


            
        
        
    
    
    
    