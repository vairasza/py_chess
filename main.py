# ============================================================================ #
# Abgabe Projektarbeit Einführung ins Programmieren mit Python
# Namen
#     Michael Bierschneider, Mat.Nr. 1652774
#     - benötige Note für dieses Projekt

from typing import *
import sys
import pygame
import random
from src.bot import Bot
from src.chessboard import Chessboard
from src.constants import *
from src.terminal import Terminal

class Game:

    def __init__(self) -> None:
        # basic init for pygame: window/screen, blackground, clock and fonts
        # fonts need to be initialized extra
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(GAME_NAME)

        self.window = pygame.display.set_mode((WINDOW_SIZE_X + TERMINAL_WIDTH, WINDOW_SIZE_Y))  
        self.background = pygame.Surface((TILE_HEIGHT * ROWS, TILE_WIDTH * COLS))
        self.clock = pygame.time.Clock()
        self.terminal_font = pygame.font.SysFont(FONT_TYPE, TERMINAL_FONT_SIZE)
        self.description_font = pygame.font.SysFont(FONT_TYPE, DESCRIPTION_FONT_SIZE)
        self.game_over_font = pygame.font.SysFont(FONT_TYPE, GAME_OVER_FONT_SIZE)

        # init chessboard
        #   an array of meeples is created that reflects the default setup
        #   sprites are loaded from board list which are then added to the sprite group, because it is easier to draw them
        self.board = Chessboard()
        self.sprites = self.board.loadSprites()
        self.chess_sprite_list = pygame.sprite.Group()
        self.chess_sprite_list.add(self.sprites)

        # tile representation of the chessboard
        # used to determine tile/meeple on click events
        self.chessboard_tiles = self.board.loadTiles(self.background)

        # init terminal
        #   clickable button without UX -> no highlighting are click reaction
        #   terminal window that logs the moves performed by the players
        #   notations for each player are saved to different arrays; if notations exceed 28 lines -> list.pop is used / no scrolling possible
        #   instance variables for a white meeple that a player has selected and the possbile moves for the according meeple
        self.terminal = Terminal(self.terminal_font)

        # init black player
        self.bot = Bot()
        
        # draw terminal on the right side of the game window including a "new game" button
        drawTerminal(self)
                    
        # conditions for the game loop
        self.gameRunning = True         # condition for gameloop
        self.playerTurn = True          # white starts playing
        self.selectedField = False      # player has selected a field
        self.check_white = False
        self.check_black = False
        self.draw = False
        self.check_mate_white = False
        self.check_mate_black = False
        
        # init first possible moves for white player
        # saves the next possibles for each side
        self.number_of_moves = self.board.getAllMoves("w")

    def run(self):
        while self.gameRunning:
            if pygame.event.get(pygame.QUIT):
                sys.exit()

            # white player's turn
            if self.playerTurn:

                if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # reset the game when clicking on the "new game" button by calling __init__ from Game
                    if self.terminal.button.collidepoint((mouse_x, mouse_y)):
                        self.__init__()
                        self.board.getAllMoves("w")
                    
                    if self.number_of_moves > 0:
                        self.check_white = False
                        # finds selected tiles on the chessboard
                        selected_tile = [tile for tile in self.chessboard_tiles if tile.collidepoint((mouse_x, mouse_y))]

                        # if a position outside the chessboard was selected, jump to the next iteration of the game loop
                        # prevents out of bound exception
                        if len(selected_tile) != 1:
                            continue

                        tile_x, tile_y = convert(selected_tile[0].x, selected_tile[0].y)

                        # in this game status the white player has to select a meeple to see possible moves
                        # a move can only be performed when a highlighted possible move is clicked
                        if not self.selectedField:
                            meeple = self.board.highlightMeeple(tile_x, tile_y) # choose from available moves

                            # if the clicked meeple is a white meeple -> the according tiles are highlighted
                            if meeple != None and meeple.colour == "w":
                                moves = meeple.possible_moves
                                self.board.highlightMoves(moves)
                                self.selectedField = True
                        else:
                            # while possible moves (yellow tiles) are displayed, clicking on the highlighted meeple (green) or on any
                            # other tile on the chessboard, desselects the possible moves and the highlighted meeple and returns to previous
                            # if statement where the player has to select a meeple
                            if not (tile_x, tile_y) in self.board.highlightedMoveTiles:
                                self.board.highlightMoves([])
                                self.board.highlightedMeeple = None
                                self.selectedField = False

                            else:
                                # if a hightlighted possible move is clicked (yellow tiles), the move to this tile is performed
                                # sprites group is updated, check status calculated and move rendered on terminal
                                self.board.highlightMoves([])
                                result = self.board.moveMeeple((tile_x, tile_y))

                                self.updateSprites()
                                self.check_black = self.board.king_b.isCheck(self.board)
                                self.number_of_moves = self.board.getAllMoves("b")
                                self.displayNotation(result)
                                self.playerTurn = False

            # black player's turn represented by a stupid computer player
            else:
                self.playerTurn = True
                self.selectedField = False

                # directly skip to end game screen when black is check mate; if possibles moves is > 0 check can be dissolved because
                # there are only moves calculated that "free" the king of check
                if self.number_of_moves > 0:
                    # delay black side move a little bit to see that the black king was checked
                    pygame.time.delay(400)
                    self.check_black = False

                    meeple = self.bot.run(self.board)

                    meeple = self.board.highlightMeeple(meeple.x, meeple.y)
                    result = self.board.moveMeeple(random.choice(meeple.possible_moves))

                    self.updateSprites()
                    self.check_white = self.board.king_w.isCheck(self.board)
                    self.number_of_moves = self.board.getAllMoves("w")
                    self.displayNotation(result, "b")
            
            #draw GUI - end of loop
            self.drawChessboard()

            if self.draw or self.check_mate_black or self.check_mate_white:
                showGameOver(self)

            pygame.display.flip()
            self.clock.tick(30)
    
    # when a meeple is moved, the function is used to update the sprites group which is rendered thereafter
    def updateSprites(self):
        self.chess_sprite_list.empty()
        meeple_sprites = self.board.loadSprites()
        self.chess_sprite_list.add(meeple_sprites)
    
    def displayNotation(self, result: List, side: str = "w") -> None:
        if side == "w":
            if self.number_of_moves > 0 and self.check_black:
                result[6].append("check")
                self.check_black = True

            if self.number_of_moves < 1 and self.check_black:
                result[6].append("check_mate")
                self.check_mate_black = True                

            if self.number_of_moves < 1 and not self.check_black:
                result[6].append("draw")
                self.draw = True
        else:
            if self.number_of_moves > 0 and self.check_white:
                result[6].append("check")
                self.check_white = True

            if self.number_of_moves < 1 and self.check_white:
                result[6].append("check_mate")
                self.check_mate_white = True

            if self.number_of_moves < 1 and not self.check_white:
                result[6].append("draw")
                self.draw = True

        self.terminal.addNotation(result, side)

    # important that all drawings on the chessboard are in one function so the layering can be controlled
    def drawChessboard(self) -> None:
        self.window.blit(self.background, (0, 0))
        pygame.draw.rect(self.window, COLOUR_WHITE, self.terminal.button)
        pygame.draw.rect(self.window, COLOUR_WHITE, self.terminal.terminal_background)
        self.window.blit(self.terminal.button_text, (BUTTON_TEXT_X, BUTTON_TEXT_Y))

        # indicator for the selected meeple and the resulting possible moves
        # selected player meeple is highlighted with a green rec while possible moves are indicated with yellow recs
        highlights = self.board.drawHighlightedMeeple() + self.board.drawHighlightedMoves()
        board_description = self.board.loadChessboardDescription(self.description_font)

        for highlight_info in highlights:
            if highlight_info != None:
                self.window.blit(highlight_info[0], (highlight_info[1], highlight_info[2]))

        # board descrption in red color that indicate the row and col
        for letter_info in board_description[0]:
            if letter_info != None:
                self.window.blit(letter_info[0], (letter_info[1], letter_info[2]))
        
        for number_info in board_description[1]:
            if number_info != None:
                self.window.blit(number_info[0], (number_info[1], number_info[2]))        
        
        # draws text from terminal arrays to terminal box with a column for white (left side) including the numbered round and black (right side)
        for index, text in enumerate(self.terminal.terminal_white_notation):
            self.window.blit(text, (TERMINAL_TEXT_X_WHITE, TERMINAL_TEXT_Y + index * TERMINAL_TEXT_Y_OFFSET))

        for index, text in enumerate(self.terminal.terminal_black_notation):
            self.window.blit(text, (TERMINAL_TEXT_X_BLACK, TERMINAL_TEXT_Y + index * TERMINAL_TEXT_Y_OFFSET))

        # draws a red rectangle under the kings if they are check
        if self.check_black:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(COLOUR_ALPHA)
            surface.fill(COLOUR_RED)
            self.window.blit(surface, (self.board.king_b.x * TILE_HEIGHT, self.board.king_b.y * TILE_WIDTH))
        
        if self.check_white:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(COLOUR_ALPHA)
            surface.fill(COLOUR_RED)
            self.window.blit(surface, (self.board.king_w.x * TILE_HEIGHT, self.board.king_w.y * TILE_WIDTH))

        #draw sprites at last so they are on top of everything
        self.chess_sprite_list.draw(self.window)

# converts the coordinates (e.g. 160, 160) on the screen to indexes (e.g. 2, 2)
def convert(coordinate_x: int, coordinate_y: int) -> Set:
    return (coordinate_x // TILE_WIDTH, coordinate_y // TILE_HEIGHT)

# game over screen that covers the chess tiles with a message for the player indicationg win/lose/draw
def showGameOver(self) -> None:
    surface = pygame.Surface((TILE_WIDTH * COLS, TILE_HEIGHT * ROWS))
    surface.set_alpha(COLOUR_GAME_OVER_ALPHA)
    surface.fill(COLOUR_WHITE)
    self.window.blit(surface, (0, 0))

    if self.draw:
        button_text = self.game_over_font.render(GAME_OVER_TEXT_DRAW, True, COLOUR_BLACK)
        self.window.blit(button_text, (GAME_OVER_TEXT_X + GAME_OVER_DRAW_OFFSET, GAME_OVER_TEXT_Y))
    else:
        winning_player = "White" if self.check_mate_black else "Black"
        button_text = self.game_over_font.render(GAME_OVER_TEXT_WIN.format(winning_player), True, COLOUR_BLACK)
        self.window.blit(button_text, (GAME_OVER_TEXT_X, GAME_OVER_TEXT_Y))

def drawTerminal(game: Game) -> None:
    pygame.draw.rect(game.window, COLOUR_WHITE, game.terminal.button)
    pygame.draw.rect(game.window, COLOUR_WHITE, game.terminal.terminal_background)
    game.window.blit(game.terminal.button_text, (BUTTON_TEXT_X, BUTTON_TEXT_Y))

if __name__ == "__main__":
    game = Game()
    game.run()
