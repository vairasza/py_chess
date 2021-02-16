from typing import *
import pygame
from src.constants import *

class Meeple(pygame.sprite.Sprite):

    def __init__(self, row, col, image_path, colour = "w"):
        pygame.sprite.Sprite.__init__(self) #probably the super as super(self)

        self.x: int = row
        self.y: int = col

        self.alive: bool = True
        self.colour: pygame.Color = colour
        self.highlighted: bool = False
        self.moved: bool = False

        # allows for transparency
        self.image: pygame.Surface = pygame.Surface((TILE_HEIGHT, TILE_WIDTH), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        # position on screen surface
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = row * TILE_WIDTH, col * TILE_HEIGHT

        # load the corresponding sprite image and draw on own surface.
        # similar process for the other pieces
        self.sprite = pygame.image.load(image_path)
        self.image.blit(self.sprite, (0, 0))

    def lineMoves(self, chessboard) -> List[Set]:
        #append all moves as a set to this list and return to gameloop for highlighting
        moves = []
        movePattern = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for pattern in movePattern:
            for i in range(1, 9):
                if not withinBorders(self, (pattern[0] * i, pattern[1] * i)):
                    break
                if not evalCheck(self, (self.x + pattern[0], self.y + pattern[1])):
                    break
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i] != None:
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour == self.colour:
                        break
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour != self.colour:
                        moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))
                        break
                moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))

        return moves
    
    def diagonalMoves(self, chessboard) -> List[Set]:
        #append all moves as a set to this list and return to gameloop for highlighting
        moves = []
        movePattern = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

        for pattern in movePattern:
            for i in range(1, 9):
                if not withinBorders(self, (pattern[0] * i, pattern[1] * i)):
                    break
                if not evalCheck(self, (self.x + pattern[0], self.y + pattern[1])):
                    break
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i] != None:
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour == self.colour:
                        break
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour != self.colour:
                        moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))
                        break
                moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))

        return moves

class King(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "K"
    
    #when castling, king initiates it => move rook too
    #if castling possbile, somehow tell the corresponding rook that he also has to move
    def possibleMoves(self, chessboard) -> List[Set]:
        moves = []
        movePattern = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for pattern in movePattern:
                if not withinBorders(self, (pattern[0], pattern[1])):
                    break
                if not evalCheck(self, (self.x + pattern[0], self.y + pattern[1])):
                    break
                if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] != None:
                    if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                        break
                    if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour != self.colour:
                        moves.append((self.x + pattern[0], self.y + pattern[1]))
                        break
                moves.append((self.x + pattern[0], self.y + pattern[1]))

        # + castling if possible:

        return moves

class Queen(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "Q"

    def possibleMoves(self, chessboard) -> List[Set]:
        return self.diagonalMoves(chessboard) + self.lineMoves(chessboard)

class Bishop(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "B"
    
    def possibleMoves(self, chessboard) -> List[Set]:
        return self.diagonalMoves(chessboard)

class Knight(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "N"

    def possibleMoves(self, chessboard) -> List[Set]:
        moves = []
        movePattern = [(1, -2), (-1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]

        for pattern in movePattern:
            if not withinBorders(self, (pattern[0], pattern[1])):
                continue
            if not evalCheck(self, (self.x + pattern[0], self.y + pattern[1])):
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] != None:
                if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                    continue
                if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour != self.colour:
                    moves.append((self.x + pattern[0], self.y + pattern[1]))
                    continue
            moves.append((self.x + pattern[0], self.y + pattern[1]))

        return moves

class Rook(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "R"
    
    def possibleMoves(self, chessboard) -> List[Set]:
        return self.lineMoves(chessboard)

class Pawn(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "P"

    #possible moves != valid moves => filter moves that are blocked by other meeple, boarder, check, etc
    def possibleMoves(self, chessboard):
        #append all moves as a set to this list and return to gameloop for highlighting
        moves = []
        singleMove = -1 if self.colour == "w" else 1
        doubleMove = -2 if self.colour == "w" else 2
        offsetMove = [(-1, -1), (1, -1)] if self.colour == "w" else [(-1, 1), (1, 1)]

        #one step forward
        #white pawns are moving up => y -= 1 because point of origin is
        #check if tile ahead is free of meeples and your move does not set your king into check
        #we dont have to check if move is within border cause pawn will promote to e.g. queen on last row
        if chessboard.array[self.y + singleMove][self.x] == None and evalCheck(self, (self.x, self.y + singleMove)):
            moves.append((self.x, self.y + singleMove))

        #two steps forward
        #this move is only allowed once per meeple; set self.moved to True meeple has actually moved, not in the possibleMoves function
        #we dont have to check if move is within border cause this move is only allowed once
        #check both fields
        if (not self.moved and
            chessboard.array[self.y + singleMove][self.x] == None and
            chessboard.array[self.y + doubleMove][self.x] == None and
            evalCheck(self, (self.x, self.y + doubleMove))):
            moves.append((self.x, self.y + doubleMove))

        #this move can only be performed when a meeple of the opposing side is diagonal to this meeple
        #can promote: handler later!
        for move in offsetMove:
            if (withinBorders(self, move) and 
                chessboard.array[self.y + move[1]][self.x + move[0]] != None and 
                chessboard.array[self.y + move[1]][self.x + move[0]].colour != self.colour and 
                evalCheck(self, (self.x + move[0], self.y + move[1]))):
                moves.append((self.x + move[0], self.y + move[1]))

        return moves

#helper functions

def withinBorders(meeple: Meeple, move: Set) -> bool:
    if meeple.x + move[0] >= 0 and meeple.y + move[1] >= 0 and meeple.x + move[0] < 8 and meeple.y + move[1] < 8:
        return True

    return False

#return true if new game situation does not set your king into check
def evalCheck(meeple, new_position):
    return True