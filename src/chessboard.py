from src.meeple import King, Meeple, Queen, Bishop, Knight, Rook, Pawn
import pygame

def unhighlightAll(chessboard):
    for row in chessboard.array:
        for tile in row:
            if tile != None:
                tile.highlighted = False


class Chessboard:

    def __init__(self):
        self.dimension_x = 8
        self.dimension_y = 8
        self.tile_size = 80
        self.array = [
            [Rook(0, 0, "assets/b_r.png", "b"), Knight(1,0, "assets/b_n.png", "b"), Bishop(2,0, "assets/b_b.png", "b"), Queen(3,0, "assets/b_q.png", "b"),
            King(4,0, "assets/b_k.png", "b"), Bishop(5,0, "assets/b_b.png", "b"), Knight(6,0, "assets/b_n.png", "b"), Rook(7,0, "assets/b_r.png", "b")],
            [Pawn(x,1, "assets/b_p.png", "b") for x in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn(x,6, "assets/w_p.png") for x in range(8)],
            [Rook(0, 7, "assets/w_r.png"), Knight(1,7, "assets/w_n.png"), Bishop(2,7, "assets/w_b.png"), Queen(3,7, "assets/w_q.png"),
            King(4,7, "assets/w_k.png"), Bishop(5,7, "assets/w_b.png"), Knight(6,7, "assets/w_n.png"), Rook(7,7, "assets/w_r.png")]]
        
        self.hightlightedMeepleTile = None
        self.hightlightedMoveFields = []

    def boardDimensions(self):
        return self.dimension_x

    def highlightMeeple(self, row, col):
        #convert somewhere else
        row = row // 80
        col = col // 80

        unhighlightAll(self)
        self.hightlightedMeepleTile = None
        
        if self.array[col][row] == None:
            return None

        if not self.array[col][row].highlighted:
            self.array[col][row].highlighted = True
            self.hightlightedMeepleTile = self.array[col][row]
            return self.hightlightedMeepleTile

        else:
            self.array[col][row].highlighted = False
            self.hightlightedMeepleTile = None
            return None
        
    def highlightMoves(self, moves):
        self.hightlightedMoveFields = moves
    
    def moveMeeple(self, move): #need start position and end position
        start_x = self.hightlightedMeepleTile.x
        start_y = self.hightlightedMeepleTile.y
        end_x = move[0] // 80
        end_y = move[1] // 80

        if self.array[end_y][end_x] == None:
            self.array[start_y][start_x] = None
            self.array[end_y][end_x] = self.hightlightedMeepleTile
            self.array[end_y][end_x].x = end_x
            self.array[end_y][end_x].y = end_y
            self.array[end_y][end_x].rect.x = end_x * 80
            self.array[end_y][end_x].rect.y = end_y * 80

            self.hightlightedMeepleTile = None
            #check moved property!!!
        #check if player can be killed

    def performMove(self, meeple, endposition):
        return 1