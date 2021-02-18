# ============================================================================ #
# Abgabe Projektarbeit Einführung ins Programmieren mit Python
# Namen
#     Michael Bierschneider, Mat.Nr. 1652774
#     - benötige Note für dieses Projekt

import sys
import pygame
import random
from typing import *
from src.chessboard import Chessboard
from src.bot import Bot
from src.constants import *
from src.terminal import Terminal

class Game:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(GAME_NAME)

        self.window = pygame.display.set_mode((WINDOW_SIZE_X + TERMINAL_WIDTH, WINDOW_SIZE_Y))  
        self.background = pygame.Surface((TILE_HEIGHT * ROWS, TILE_WIDTH * COLS))
        self.clock = pygame.time.Clock()
        self.terminal_font = pygame.font.SysFont(FONT_TYPE, TERMINAL_FONT_SIZE)
        self.description_font = pygame.font.SysFont(FONT_TYPE, DESCRIPTION_FONT_SIZE)
        self.game_over_font = pygame.font.SysFont(FONT_TYPE, GAME_OVER_FONT_SIZE)

        # init chessboard: load sprites from board list, add it to sprite group which easier draws them 
        self.board = Chessboard()
        self.sprites = self.board.loadSprites()

        self.chess_sprite_list = pygame.sprite.Group()
        self.chess_sprite_list.add(self.sprites)

        # rectangle for chessboard; returns rectangles to interact on click events
        self.chessboard_tiles = self.board.loadTiles(self.background)

        # init terminal
        self.terminal = Terminal(self.terminal_font)
        
        pygame.draw.rect(self.window, COLOUR_WHITE, self.terminal.button)
        pygame.draw.rect(self.window, COLOUR_WHITE, self.terminal.terminal_background)
        self.window.blit(self.terminal.button_text, (BUTTON_TEXT_X, BUTTON_TEXT_Y))
                    
        # conditions for the game loop
        self.gameRunning = True         # condition for gameloop
        self.playerTurn = True          # white starts playing
        self.selectedField = False      # player has selected a field

        # init computer player | black side
        self.bot = Bot()

    def run(self):
        number_of_moves = self.board.getAllMoves()

        while self.gameRunning:

            if pygame.event.get(pygame.QUIT):
                sys.exit()

            # only white players
            if self.playerTurn:

                if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # reset the game when clicking on the "new game" button by calling __init__ from Game
                    if self.terminal.button.collidepoint((mouse_x, mouse_y)):
                        self.__init__()
                        self.board.getAllMoves()

                    # finds selected tiles on the chessboard
                    selected_tile = [tile for tile in self.chessboard_tiles if tile.collidepoint((mouse_x, mouse_y))]

                    # if a position outside the chessboard was selected, jump to the next iteration of the game loop
                    # prevents out of bound exception
                    if len(selected_tile) != 1:
                        continue

                    tile_x, tile_y = convert(selected_tile[0].x, selected_tile[0].y)
                    self.board.king_w.check = False

                    if not self.selectedField:
                        meeple = self.board.highlightMeeple(tile_x, tile_y) ##choose from available moves

                        if meeple != None:
                            moves = meeple.possible_moves
                            self.board.highlightMoves(moves)
                            self.selectedField = True
                    else:
                        #display moves & wait for player reaction
                        #checkpromotion of
                        if not (tile_x, tile_y) in self.board.highlightedMoveTiles:
                            self.board.highlightMoves([])
                            self.board.highlightedMeeple = None
                            self.selectedField = False

                        else:
                            self.board.highlightMoves([])
                            result = self.board.moveMeeple((tile_x, tile_y))

                            self.chess_sprite_list.empty()
                            meeple_sprites = self.board.loadSprites()
                            self.chess_sprite_list.add(meeple_sprites)
                            
                            number_of_moves = self.board.getAllMoves("b")
                            black_king_check = self.board.king_b.isCheck(self.board)

                            if number_of_moves > 0 and black_king_check:
                                result[6].append("check")
                                self.board.king_b.check = True

                            if number_of_moves < 1 and black_king_check:
                                result[6].append("check_mate")
                                self.board.king_b.check_mate = True
                                
                            if number_of_moves < 1 and not black_king_check:
                                result[6].append("draw")
                                self.board.king_b.draw = True

                            self.terminal.addNotation(result, "w")
                            self.playerTurn = False

            #this is black player
            else:
                if self.board.king_w.check:
                    print("check: move away!")

                self.playerTurn = True
                self.selectedField = False
                self.board.king_b.check = False

                number_of_moves = self.board.getAllMoves()
                meeples = [meeple for row in self.board.array for meeple in row if meeple != None and meeple.colour == "b"]

                meeple = None
                while True:
                    meeple = random.choice(meeples)
                    if len(meeple.possible_moves) > 0:
                        break

                meeple = self.board.highlightMeeple(meeple.x, meeple.y)

                result = self.board.moveMeeple(random.choice(meeple.possible_moves))

                self.chess_sprite_list.empty()
                meeple_sprites = self.board.loadSprites()
                self.chess_sprite_list.add(meeple_sprites)

                number_of_moves = self.board.getAllMoves()
                white_king_check = self.board.king_w.isCheck(self.board)

                if number_of_moves > 0 and white_king_check:
                    result[6].append("check")
                    self.board.king_w.check = True

                if number_of_moves < 1 and white_king_check:
                    result[6].append("check_mate")
                    self.board.king_w.check_mate = True

                if number_of_moves < 1 and not white_king_check:
                    result[6].append("draw")
                    self.board.king_w.draw = True

                self.terminal.addNotation(result, "b")
            
            #draw GUI - end of loop
            self.drawChessboard()

            if self.board.king_b.draw or self.board.king_w.draw or self.board.king_b.check_mate or self.board.king_w.check_mate:
                showGameOver(self)

            pygame.display.flip()
            self.clock.tick(30)
        
    def drawChessboard(self):
        self.window.blit(self.background, (0, 0))
        pygame.draw.rect(self.window, COLOUR_WHITE, self.terminal.button)
        pygame.draw.rect(self.window, COLOUR_WHITE, self.terminal.terminal_background)
        self.window.blit(self.terminal.button_text, (BUTTON_TEXT_X, BUTTON_TEXT_Y))

        highlights = self.board.drawHighlightedMeeple() + self.board.drawHighlightedMoves()
        board_description = self.board.loadChessboardDescription(self.description_font)

        for highlight_info in highlights:
            if highlight_info != None:
                self.window.blit(highlight_info[0], (highlight_info[1], highlight_info[2]))

        for letter_info in board_description[0]:
            if letter_info != None:
                self.window.blit(letter_info[0], (letter_info[1], letter_info[2]))
        
        for number_info in board_description[1]:
            if number_info != None:
                self.window.blit(number_info[0], (number_info[1], number_info[2]))        
        
        for index, text in enumerate(self.terminal.terminal_white_notation):
            self.window.blit(text, (TERMINAL_TEXT_X_WHITE, TERMINAL_TEXT_Y + index * TERMINAL_TEXT_Y_OFFSET))

        for index, text in enumerate(self.terminal.terminal_black_notation):
            self.window.blit(text, (TERMINAL_TEXT_X_BLACK, TERMINAL_TEXT_Y + index * TERMINAL_TEXT_Y_OFFSET))

        if self.board.king_b.check:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(120)
            surface.fill(COLOUR_RED)
            game.window.blit(surface, (self.board.king_b.x * TILE_HEIGHT, self.board.king_b.y * TILE_WIDTH))
        
        if self.board.king_w.check:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(120)
            surface.fill(COLOUR_RED)
            game.window.blit(surface, (self.board.king_w.x * TILE_HEIGHT, self.board.king_w.y * TILE_WIDTH))

        #draw sprites at last so they are on top of everything
        self.chess_sprite_list.draw(self.window)

def convert(coordinate_x: int, coordinate_y: int) -> Set:
    return (coordinate_x // TILE_WIDTH, coordinate_y // TILE_HEIGHT)

def showGameOver(game):
    surface = pygame.Surface((TILE_WIDTH * COLS, TILE_HEIGHT * ROWS))
    surface.set_alpha(220)
    surface.fill(COLOUR_WHITE)
    game.window.blit(surface, (0, 0))

    if game.board.king_b.draw or game.board.king_w.draw:
        button_text = game.game_over_font.render(GAME_OVER_TEXT_DRAW, True, COLOUR_BLACK)
    else:
        winning_player = "White" if game.board.king_b.check_mate else "Black"
        button_text = game.game_over_font.render(GAME_OVER_TEXT_WIN.format(winning_player), True, COLOUR_BLACK)

    game.window.blit(button_text, (GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y))

if __name__ == "__main__":
    game = Game()
    game.run()
