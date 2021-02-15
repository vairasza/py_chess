from typing import *
import pygame

class Meeple(pygame.sprite.Sprite):

    def __init__(self, row, col, image_path, colour = "w"):
        pygame.sprite.Sprite.__init__(self) #probably the super as super(self)

        self.x = row
        self.y = col

        self.alive = True
        self.colour = colour
        self.highlighted = False

        # allows for transparency
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        # position on screen surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = row * 80, col * 80

        # load the corresponding sprite image and draw on own surface.
        # similar process for the other pieces
        self.sprite = pygame.image.load(image_path)
        self.image.blit(self.sprite, (0, 0))

class King(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.moved = False
        self.symbol = "K"

class Queen(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "Q"

class Bishop(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "B"

class Knight(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "N"

class Rook(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.moved = False
        self.symbol = "R"

class Pawn(Meeple):

    def __init__(self, row, col, image_path, colour = "w"):
        Meeple.__init__(self, row, col, image_path, colour)
        self.moved = False
        self.symbol = "P"

    def canPawnPromotion(self, position_x, position_y):
        if self.white:
            #=> pawn must reach y = 0
            if position_y == 0:
                return True
        else:
            #=> pawn must reach y = 580(?)
            if position_y == 580: #constant
                return True
        #consider position
        return False

    #possible moves != valid moves => filter moves that are blocked by other meeple, boarder, check, etc
    def possibleMoves(self, chessboard):
        #append all moves as a set to this list and return to gameloop for highlighting
        moves = []
        singleMove = -1 if self.colour == "w" else 1
        doubleMove = -2 if self.colour == "w" else  2
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

def compromiseKing():
    return 1

#check if move is within boarders, field is free or of other colour
def checkMove():
    return 1

#check if a enemies meeple can be killed
def canCapture():
    return 1

def getLineMoves(chessboard):
    return 1

# return [(x,y), ...] or None
def getDiagonalMoves(chessboard):
    return 1

def withinBorders(meeple, move: Set) -> bool:
    if meeple.x + move[0] >= 0 and meeple.y + move[1] >= 0 and meeple.x + move[0] < 8 and meeple.y + move[1] < 8:
        return True

    return False

#return true if new game situation does not set your king into check
def evalCheck(meeple, new_position):
    return True