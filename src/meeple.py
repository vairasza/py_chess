from typing import *
import pygame
from src.constants import *

# argument chessboard has no type annotation because you cant circular import a class

# base class for alle meeples
class Meeple(pygame.sprite.Sprite):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        pygame.sprite.Sprite.__init__(self) # probably the same as super(self)

        # position in chessboard array
        self.x: int = row
        self.y: int = col

        self.colour: pygame.Color = colour
        self.highlighted: bool = False
        self.moved: bool = False
        self.possible_moves: List = []

        # allows for transparency
        self.image: pygame.Surface = pygame.Surface((TILE_HEIGHT, TILE_WIDTH), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        # position on screen surface
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = row * TILE_WIDTH, col * TILE_HEIGHT

        # load the corresponding sprite image and c on own surface.
        # similar process for the other pieces
        self.sprite = pygame.image.load(image_path)
        self.image.blit(self.sprite, (0, 0))

        # move patterns
        self.line_patterns = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.diag_patterns = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        self.pawn_offset_pattern = [(-1, -1), (1, -1)] if self.colour == "w" else [(-1, 1), (1, 1)]
        self.pawn_singleMove = -1 if self.colour == "w" else 1
        self.pawn_doubleMove = -2 if self.colour == "w" else 2
        self.king_move_patterns = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        self.knight_move_pattern = [(1, -2), (-1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]

    # calculates moves for rook and queen - moves in vertical and horizontal direction that have no limit to one step
    def lineMoves(self, chessboard) -> List[Set]:
        # append all moves as a set to this list and return to gameloop for highlighting
        moves = []

        for pattern in self.line_patterns:
            for i in range(1, 9):
                if not withinBorders((self.x + pattern[0] * i, self.y + pattern[1] * i)):
                    break
                if willCheckKing(chessboard, self, (self.x + pattern[0], self.y + pattern[1])):
                    break
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i] != None:
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour == self.colour:
                        break
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour != self.colour:
                        moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))
                        break
                if willCheckKing(chessboard, self, (self.x + pattern[0], self.y + pattern[1])):
                    continue
                moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))

        return moves
    
    # calculates moves for bishop and queen - moves in diagonal directions that have no limit to one step
    def diagonalMoves(self, chessboard) -> List[Set]:
        # append all moves as a set to this list and return to gameloop for highlighting
        moves = [] 

        for pattern in self.diag_patterns:
            for i in range(1, 9):
                if not withinBorders((self.x + pattern[0] * i, self.y + pattern[1] * i)):
                    break
                if willCheckKing(chessboard, self, (self.x + pattern[0], self.y + pattern[1])):
                    break
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i] != None:
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour == self.colour:
                        break
                    if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour != self.colour:
                        moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))
                        break
                if willCheckKing(chessboard, self, (self.x + pattern[0], self.y + pattern[1])):
                    continue
                moves.append((self.x + pattern[0] * i, self.y + pattern[1] * i))

        return moves

class King(Meeple):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "K"
        self.castling = False
    
    # when castling, king initiates it => move rook too
    # if castling possbile, somehow tell the corresponding rook that he also has to move
    #   reflected in chessboard.move
    def calcNewMoves(self, chessboard) -> int:
        moves = []

        for pattern in self.king_move_patterns:
            if not withinBorders((self.x + pattern[0], self.y + pattern[1])):
                continue
            if willCheckKing(chessboard, self, (self.x + pattern[0], self.y + pattern[1])):
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] != None:
                if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                    continue
            moves.append((self.x + pattern[0], self.y + pattern[1]))

        # castling
        if not self.isCheck(chessboard):
            if self.moved == False:
                if self.colour == "w":
                    if (isinstance(chessboard.array[7][0], Rook) and
                        chessboard.array[7][0].colour == self.colour and
                        chessboard.rook_w_left.moved == False and 
                        chessboard.array[7][1] == None and
                        chessboard.array[7][2] == None and
                        chessboard.array[7][3] == None and
                        not willCheckKing(chessboard, self, (1, 7))):
                        moves.append((1, 7))
                    if (isinstance(chessboard.array[7][7], Rook) and
                        chessboard.array[7][7].colour == self.colour and
                        chessboard.rook_w_right.moved == False and 
                        chessboard.array[7][5] == None and
                        chessboard.array[7][6] == None and
                        not willCheckKing(chessboard, self, (6, 7))):
                        moves.append((6, 7))
                else:
                    if (isinstance(chessboard.array[0][0], Rook) and
                        chessboard.array[0][0].colour == self.colour and
                        chessboard.rook_b_left.moved == False and 
                        chessboard.array[0][1] == None and
                        chessboard.array[0][2] == None and
                        chessboard.array[0][3] == None and
                        not willCheckKing(chessboard, self, (1, 0))):
                        moves.append((1, 0))
                    if (isinstance(chessboard.array[0][7], Rook) and
                        chessboard.array[0][7].colour == self.colour and
                        chessboard.rook_b_right.moved == False and 
                        chessboard.array[0][5] == None and
                        chessboard.array[0][6] == None and
                        not willCheckKing(chessboard, self, (6, 0))):
                        moves.append((6, 0))

        self.possible_moves = moves
        return len(self.possible_moves)

    # returns true if king is in check
    def isCheck(self, chessboard) -> bool:
        # consider all position from where the king can be checked  

        # diagonal patterns - queen and bishop
        for pattern in self.diag_patterns:
            for i in range(1, 9):
                if not withinBorders((self.x + pattern[0] * i, self.y + pattern[1] * i)):
                    break
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i] == None:
                    continue
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour == self.colour:
                    break
                if (not (isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Queen) or
                    isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Bishop)) and 
                    chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour != self.colour):
                    break
                if (isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Queen) or
                    isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Bishop)):
                    return True
    
        # line patterns - queen and rook
        for pattern in self.line_patterns:
            for i in range(1, 9):
                if not withinBorders((self.x + pattern[0] * i, self.y + pattern[1] * i)):
                    break
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i] == None:
                    continue
                if chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour == self.colour:
                    break
                if (not (isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Queen) or
                    isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Rook)) and 
                    chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i].colour != self.colour):
                    break
                if (isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Queen) or
                    isinstance(chessboard.array[self.y + pattern[1] * i][self.x + pattern[0] * i], Rook)):
                    return True

        # knight pattern
        for pattern in self.knight_move_pattern:
            if not withinBorders((self.x + pattern[0], self.y + pattern[1])):
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] == None:
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                continue
            if isinstance(chessboard.array[self.y + pattern[1]][self.x + pattern[0]], Knight):
                return True
        
        # pawn patterns
        for pattern in self.pawn_offset_pattern:
            if not withinBorders((self.x + pattern[0], self.y + pattern[1])):
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] == None:
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                continue
            if isinstance(chessboard.array[self.y + pattern[1]][self.x + pattern[0]], Pawn):
                return True

        # king patterns
        for pattern in self.king_move_patterns:
            if not withinBorders((self.x + pattern[0], self.y + pattern[1])):
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] == None:
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                continue
            if isinstance(chessboard.array[self.y + pattern[1]][self.x + pattern[0]], King):
                return True

        return False

class Queen(Meeple):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "Q"

    def calcNewMoves(self, chessboard) -> int:
        self.possible_moves = self.diagonalMoves(chessboard) + self.lineMoves(chessboard)
        return len(self.possible_moves)

class Bishop(Meeple):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "B"
    
    def calcNewMoves(self, chessboard) -> int:
        self.possible_moves = self.diagonalMoves(chessboard)
        return len(self.possible_moves)

class Knight(Meeple):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "N"

    def calcNewMoves(self, chessboard,) -> int:
        moves = []

        for pattern in self.knight_move_pattern:
            if not withinBorders((self.x + pattern[0], self.y + pattern[1])):
                continue
            if willCheckKing(chessboard, self, (self.x + pattern[0], self.y + pattern[1])):
                continue
            if chessboard.array[self.y + pattern[1]][self.x + pattern[0]] != None:
                if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour == self.colour:
                    continue
                if chessboard.array[self.y + pattern[1]][self.x + pattern[0]].colour != self.colour:
                    moves.append((self.x + pattern[0], self.y + pattern[1]))
                    continue
            moves.append((self.x + pattern[0], self.y + pattern[1]))

        self.possible_moves = moves
        return len(self.possible_moves)

class Rook(Meeple):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "R"
    
    def calcNewMoves(self, chessboard) -> int:
        self.possible_moves = self.lineMoves(chessboard)
        return len(self.possible_moves)

class Pawn(Meeple):

    def __init__(self, row: int, col: int, image_path: str, colour: pygame.Color = "w") -> None:
        Meeple.__init__(self, row, col, image_path, colour)
        self.symbol = "P"

    # possible moves != valid moves => filter moves that are blocked by other meeple, boarder, check, etc
    def calcNewMoves(self, chessboard) -> int:
        # append all moves as a set to this list and return to gameloop for highlighting
        moves = []
        
        # one step forward
        # white pawns are moving up => y -= 1 because point of origin is
        # check if tile ahead is free of meeples and your move does not set your king into check
        # we dont have to check if move is within border cause pawn will promote to e.g. queen on last row
        if chessboard.array[self.y + self.pawn_singleMove][self.x] == None and not willCheckKing(chessboard, self, (self.x, self.y + self.pawn_singleMove)):
            moves.append((self.x, self.y + self.pawn_singleMove))

        # two steps forward
        # this move is only allowed once per meeple; set self.moved to True meeple has actually moved, not in the possibleMoves function
        # we dont have to check if move is within border cause this move is only allowed once
        # check both fields
        if (not self.moved and
            chessboard.array[self.y + self.pawn_singleMove][self.x] == None and
            chessboard.array[self.y + self.pawn_doubleMove][self.x] == None and
            not willCheckKing(chessboard, self, (self.x, self.y + self.pawn_doubleMove))):

            moves.append((self.x, self.y + self.pawn_doubleMove))

        # this move can only be performed when a meeple of the opposing side is diagonal to this meeple
        # can promote: handler later!
        for move in self.pawn_offset_pattern:
            if (withinBorders((self.x + move[0], self.y + move[1])) and 
                chessboard.array[self.y + move[1]][self.x + move[0]] != None and 
                chessboard.array[self.y + move[1]][self.x + move[0]].colour != self.colour and 
                not willCheckKing(chessboard, self, (self.x + move[0], self.y + move[1]))):

                moves.append((self.x + move[0], self.y + move[1]))

        self.possible_moves = moves
        return len(self.possible_moves)

# helper functions

def withinBorders(meeple_pos: Set) -> bool:
    if meeple_pos[0] >= 0 and meeple_pos[1] >= 0 and meeple_pos[0] < 8 and meeple_pos[1] < 8:
        return True

    return False

# return true if new game situation sets your king into check
def willCheckKing(chessboard, meeple: Meeple, new_position: Set) -> bool:
    king = chessboard.king_w if meeple.colour == "w" else chessboard.king_b

    start_x, start_y = meeple.x, meeple.y
    end_x, end_y = new_position[0], new_position[1]

    # move the meeple to possible new position
    save_killed_meeple = chessboard.array[end_y][end_x]
    chessboard.array[start_y][start_x] = None
    chessboard.array[end_y][end_x] = meeple
    chessboard.array[end_y][end_x].x = end_x
    chessboard.array[end_y][end_x].y = end_y

    result = king.isCheck(chessboard)

    #return meeple to its previous location
    chessboard.array[start_y][start_x] = meeple
    chessboard.array[end_y][end_x].x = start_x
    chessboard.array[end_y][end_x].y = start_y
    chessboard.array[end_y][end_x] = save_killed_meeple

    return result