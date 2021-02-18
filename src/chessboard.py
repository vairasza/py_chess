import pygame
from typing import *
from src.meeple import *
from src.constants import *

class Chessboard:

    def __init__(self) -> None:
        #for easier access in meeple
        self.king_w: King = King(4,7, ASSET_W_K)
        self.king_b: King = King(4,0, ASSET_B_K, BLACK_PLAYER)
        self.rook_w_left: Rook = Rook(0,7, ASSET_W_R)
        self.rook_w_right: Rook = Rook(7,7, ASSET_W_R)
        self.rook_b_left: Rook = Rook(0, 0, ASSET_B_R, BLACK_PLAYER)
        self.rook_b_right: Rook = Rook(7, 0, ASSET_B_R, BLACK_PLAYER)

        self.array: List = [
            [self.rook_b_left,
            Knight(1,0, ASSET_B_N, BLACK_PLAYER),
            Bishop(2,0, ASSET_B_B, BLACK_PLAYER),
            Queen(3,0, ASSET_B_Q, BLACK_PLAYER),
            self.king_b,
            Bishop(5,0, ASSET_B_B, BLACK_PLAYER),
            Knight(6,0, ASSET_B_N, BLACK_PLAYER),
            self.rook_b_right],
            [Pawn(x,1, ASSET_B_P, BLACK_PLAYER) for x in range(ROWS)],
            [None for _ in range(ROWS)],
            [None for _ in range(ROWS)],
            [None for _ in range(ROWS)],
            [None for _ in range(ROWS)],
            [Pawn(x,6, ASSET_W_P) for x in range(ROWS)],
            [self.rook_w_left,
            Knight(1,7, ASSET_W_N),
            Bishop(2,7, ASSET_W_B),
            Queen(3,7, ASSET_W_Q),
            self.king_w,
            Bishop(5,7, ASSET_W_B),
            Knight(6,7, ASSET_W_N),
            self.rook_w_right]]
        
        self.highlightedMeeple: Union[Meeple, None] = None
        self.highlightedMoveTiles: List = []

    # returns all Meeple objects from self.array to draw them
    # pygame is expecting a list or tuple, when only one sprite is in a list, it outmerged 
    def loadSprites(self) -> Union[List, None]:
        array = []
        for sprites in self.array:
            for sprite in sprites:
                if sprite:
                    array.append(sprite)

        return array

    # generates tiles for the chessboard and returns them for event handling
    def loadTiles(self, background: pygame.Surface) -> List:
        chessboard_tiles = [] # drawn rectangles
        colour_flip = True #to alternate the first colour each row

        for col in range(0, WINDOW_SIZE_X, TILE_WIDTH):
            colour_flip = not colour_flip

            for row in range(0, WINDOW_SIZE_Y, TILE_HEIGHT):
                tile = pygame.Rect(col, row, TILE_HEIGHT, TILE_WIDTH)
                colour = COLOUR_BLACK if colour_flip else COLOUR_WHITE
                colour_flip = not colour_flip
                chessboard_tiles.append(tile)
                
                pygame.draw.rect(background, colour, tile)
        
        return chessboard_tiles
    
    #rework to class properties -> easier accessable
    def loadChessboardDescription(self, font: pygame.font) -> List:
        row_array = []
        for index, letter in enumerate(ROW_DESCRIPTION):
            row_array.append((font.render(letter, True, COLOUR_RED), ROW_DESCRIPTION_INDEX_X + index * TILE_WIDTH, ROW_DESCRIPTION_INDEX_Y))

        col_array = []
        for index, number in enumerate(COL_DESCRIPTION):
            col_array.append((font.render(number, True, COLOUR_RED), COL_DESCRIPTION_INDEX_X, COL_DESCRIPTION_INDEX_Y + index * TILE_HEIGHT))

        return [col_array, row_array]

    def getAllMoves(self, colour: str = "w") -> List:
        counter = 0

        for row in self.array:
            for col in row:
                if col != None and col.colour == colour:
                    counter += col.calcNewMoves(self)

        return counter
                

    #change input to set
    def highlightMeeple(self, row: int, col: int) -> Union[Meeple, None]:
        unhighlightAll(self)
        self.highlightedMeeple = None
        
        if self.array[col][row] == None:# or self.array[col][row].colour == BLACK_PLAYER:
            return None

        if not self.array[col][row].highlighted:
            self.array[col][row].highlighted = True
            self.highlightedMeeple = self.array[col][row]
            return self.highlightedMeeple

        else:
            self.array[col][row].highlighted = False
            self.highlightedMeeple = None
            return None
        
    def highlightMoves(self, moves: Set) -> None:
        self.highlightedMoveTiles = moves
    
    def moveMeeple(self, move: Set) -> List: #need start position and end position
        report = [] # contains information about this move relevant to terminal notation
        special = [] # contains special moves like castling and promotion

        start_x: int = self.highlightedMeeple.x
        start_y: int = self.highlightedMeeple.y
        end_x: int = move[0]
        end_y: int = move[1]

        report.append(self.array[start_y][start_x].symbol)
        report.append(start_x)
        report.append(start_y)
        report.append(end_x)
        report.append(end_y)

        killedMeeple: bool = self.array[end_y][end_x] == None
        report.append(killedMeeple)

        self.array[start_y][start_x] = None
        self.array[end_y][end_x] = self.highlightedMeeple
        self.array[end_y][end_x].x = end_x
        self.array[end_y][end_x].y = end_y
        self.array[end_y][end_x].rect.x = end_x * TILE_WIDTH
        self.array[end_y][end_x].rect.y = end_y * TILE_HEIGHT

        # pawn promotion
        if isinstance(self.array[end_y][end_x], Pawn) and self.array[end_y][end_x].colour == "w" and self.array[end_y][end_x].y == 0:
            self.array[end_y][end_x] = Queen(end_x,end_y, ASSET_W_Q)
            special.append("promotion")
        
        if isinstance(self.array[end_y][end_x], Pawn) and self.array[end_y][end_x].colour == "b" and self.array[end_y][end_x].y == 7:
            self.array[end_y][end_x] = Queen(end_x,end_y, ASSET_B_Q, "b")
            special.append("promotion")

        # castling white
        if (isinstance(self.array[end_y][end_x], King) and
            self.array[end_y][end_x].colour == "w" and
            self.array[end_y][end_x].x == 1 and
            self.array[end_y][end_x].castling == False and
            self.array[end_y][end_x].moved == False and 
            isinstance(self.array[7][0], Rook)):

            self.array[7][2] = self.array[7][0]
            self.array[7][7] = None
            self.array[7][2].x = 2
            self.array[7][2].y = 7
            self.array[7][2].rect.x = 2 * TILE_WIDTH
            self.array[7][2].rect.y = 7 * TILE_HEIGHT
            special.append("castling-long")
            self.array[end_y][end_x].castling = True
        
        if (isinstance(self.array[end_y][end_x], King) and
            self.array[end_y][end_x].colour == "w" and
            self.array[end_y][end_x].x == 6 and
            self.array[end_y][end_x].castling == False and
            self.array[end_y][end_x].moved == False and 
            isinstance(self.array[7][7], Rook)):

            self.array[7][5] = self.array[7][7]
            self.array[7][7] = None
            self.array[7][5].x = 5
            self.array[7][5].y = 7
            self.array[7][5].rect.x = 5 * TILE_WIDTH
            self.array[7][5].rect.y = 7 * TILE_HEIGHT
            special.append("castling")
            self.array[end_y][end_x].castling = True

        # castling black
        if (isinstance(self.array[end_y][end_x], King) and
            self.array[end_y][end_x].colour == "b" and
            self.array[end_y][end_x].x == 1 and
            self.array[end_y][end_x].castling == False and
            self.array[end_y][end_x].moved == False and 
            isinstance(self.array[0][0], Rook)):

            self.array[0][2] = self.array[0][0]
            self.array[0][7] = None
            self.array[0][2].x = 2
            self.array[0][2].y = 0
            self.array[0][2].rect.x = 2 * TILE_WIDTH
            self.array[0][2].rect.y = 0
            special.append("castling-long")
            self.array[end_y][end_x].castling = True
        
        if (isinstance(self.array[end_y][end_x], King) and
            self.array[end_y][end_x].colour == "b" and
            self.array[end_y][end_x].x == 6 and
            self.array[end_y][end_x].castling == False and
            self.array[end_y][end_x].moved == False and 
            isinstance(self.array[0][7], Rook)):

            self.array[0][5] = self.array[0][7]
            self.array[0][7] = None
            self.array[0][5].x = 5
            self.array[0][5].y = 0
            self.array[0][5].rect.x = 5 * TILE_WIDTH
            self.array[0][5].rect.y = 0
            special.append("castling")
            self.array[end_y][end_x].castling = True
            
        # double move and castling are only allowed on the first move
        if self.highlightedMeeple.symbol == "P" or self.highlightedMeeple.symbol == "K" or self.highlightedMeeple.symbol == "R":
            self.highlightedMeeple.moved = True
        
        self.highlightedMeeple = None

        report.append(special)

        return report

    def drawHighlightedMeeple(self) -> List[pygame.Surface]:
        highlighted_meeple = None

        if self.highlightedMeeple != None and self.highlightedMeeple.colour != BLACK_PLAYER:
            surface = pygame.Surface((TILE_HEIGHT, TILE_WIDTH))
            surface.set_alpha(COLOUR_ALPHA)
            surface.fill(COLOUR_GREEN)
            highlighted_meeple = (surface, self.highlightedMeeple.rect.x, self.highlightedMeeple.rect.y)

        return [highlighted_meeple]

    def drawHighlightedMoves(self) -> List[pygame.Surface]:
        surface_list = []

        for tile in self.highlightedMoveTiles:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(COLOUR_ALPHA)
            surface.fill(COLOUR_YELLOW)
            surface_list.append((surface, tile[0] * TILE_WIDTH, tile[1] * TILE_HEIGHT))

        return surface_list

    def promotePawn(self, position, colour = "w"): #TODO
        if colour == "w":
            self.array[position[1]][position[0]] = Queen(position[0], position[1], ASSET_W_Q)
        else:
            self.array[position[1]][position[0]] = Queen(position[0], position[1], ASSET_B_Q, BLACK_PLAYER)

#helper functions

def unhighlightAll(chessboard: Chessboard) -> None:
    for row in chessboard.array:
        for tile in row:
            if tile != None:
                tile.highlighted = False