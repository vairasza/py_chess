import pygame
from typing import *
from src.meeple import *
from src.constants import *

class Chessboard:

    def __init__(self):
        #replace filepaths
        self.array = [
            [Rook(0, 0, "assets/b_r.png", BLACK_PLAYER), Knight(1,0, "assets/b_n.png", BLACK_PLAYER),
            Bishop(2,0, "assets/b_b.png", BLACK_PLAYER), Queen(3,0, "assets/b_q.png", BLACK_PLAYER),
            King(4,0, "assets/b_k.png", BLACK_PLAYER), Bishop(5,0, "assets/b_b.png", BLACK_PLAYER),
            Knight(6,0, "assets/b_n.png", BLACK_PLAYER), Rook(7,0, "assets/b_r.png", BLACK_PLAYER)],
            [Pawn(x,1, "assets/b_p.png", BLACK_PLAYER) for x in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn(x,6, "assets/w_p.png") for x in range(8)],
            [Rook(0, 7, "assets/w_r.png"), Knight(1,7, "assets/w_n.png"), Bishop(2,7, "assets/w_b.png"), Queen(3,7, "assets/w_q.png"),
            King(4,7, "assets/w_k.png"), Bishop(5,7, "assets/w_b.png"), Knight(6,7, "assets/w_n.png"), Rook(7,7, "assets/w_r.png")]]
        
        self.highlightedMeeple: Meeple or None = None
        self.highlightedMoveTiles: List = []

    # returns all Meeple objects from self.array to draw them
    # pygame is expecting a list or tuple, when only one sprite is in a list, it outmerged 
    def loadSprites(self) -> List or None:
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
    def loadChessboardDescription(self, font) -> List:
        row_array = []
        for index, letter in enumerate(ROW_DESCRIPTION):
            row_array.append((font.render(letter, True, COLOUR_RED), ROW_DESCRIPTION_INDEX_X + index * TILE_WIDTH, ROW_DESCRIPTION_INDEX_Y))

        col_array = []
        for index, number in enumerate(COL_DESCRIPTION):
            col_array.append((font.render(number, True, COLOUR_RED), COL_DESCRIPTION_INDEX_X, COL_DESCRIPTION_INDEX_Y + index * TILE_HEIGHT))

        return [col_array, row_array]

    #change input to set
    def highlightMeeple(self, row: int, col: int) -> None or Meeple:
        unhighlightAll(self)
        self.highlightedMeeple = None
        
        if self.array[col][row] == None or self.array[col][row].colour == BLACK_PLAYER:
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
    
    def moveMeeple(self, move: Set) -> None or Meeple: #need start position and end position
        start_x = self.highlightedMeeple.x
        start_y = self.highlightedMeeple.y
        end_x = move[0]
        end_y = move[1]

        killedMeeple = None if self.array[end_y][end_x] == None else self.array[end_y][end_x]

        if self.highlightedMeeple.symbol == "P" or self.highlightedMeeple.symbol == "K" or self.highlightedMeeple.symbol == "R":
            self.highlightedMeeple.moved = True

        self.array[start_y][start_x] = None
        self.array[end_y][end_x] = self.highlightedMeeple
        self.array[end_y][end_x].x = end_x
        self.array[end_y][end_x].y = end_y
        self.array[end_y][end_x].rect.x = end_x * 80
        self.array[end_y][end_x].rect.y = end_y * 80

        self.highlightedMeeple = None

        #check moved property!!!
        #check if player can be killed
        #(self.array[end_y][end_x].symbol, start_x, start_y, end_x, end_y, True, ["check", "check_mate", "promotion", "castling", "remis"])
        return (self.array[end_y][end_x].symbol, start_x, start_y, end_x, end_y, True, ["check", "", "promotion", "", ""])

    def drawHighlightedMeeple(self) -> List[pygame.Surface]:
        highlighted_meeple = None

        if self.highlightedMeeple != None and self.highlightedMeeple.colour != BLACK_PLAYER:
            surface = pygame.Surface((80, 80))
            surface.set_alpha(120)
            surface.fill(COLOUR_YELLOW)
            highlighted_meeple = (surface, self.highlightedMeeple.rect.x, self.highlightedMeeple.rect.y)

        return [highlighted_meeple]

    def drawHighlightedMoves(self):
        surface_list = []

        for tile in self.highlightedMoveTiles:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(COLOUR_ALPHA)
            surface.fill(COLOUR_RED)
            surface_list.append((surface, tile[0] * TILE_WIDTH, tile[1] * TILE_HEIGHT))

        return surface_list

    def promotePawn(self, position, colour = "w"):
        if colour == "w":
            self.array[position[1]][position[0]] = Queen(position[0], position[1], "assets/w_q.png")
        else:
            self.array[position[1]][position[0]] = Queen(position[0], position[1], "assets/b_q.png", BLACK_PLAYER)

#helper functions

def unhighlightAll(chessboard: Chessboard) -> None:
    for row in chessboard.array:
        for tile in row:
            if tile != None:
                tile.highlighted = False