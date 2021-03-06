from typing import *
import pygame


# Colours that are used for chessboard tiles and highlights
COLOUR_BLACK: Final[pygame.Color] = pygame.Color(0, 0, 0)
COLOUR_WHITE: Final[pygame.Color] = pygame.Color(255, 255, 255)
COLOUR_RED: Final[pygame.Color] = pygame.Color(255, 0, 0)
COLOUR_YELLOW: Final[pygame.Color] = pygame.Color(255, 255, 0)
COLOUR_GREEN: Final[pygame.Color] = pygame.Color(0, 255, 0)
COLOUR_ALPHA: Final[int] = 120
COLOUR_GAME_OVER_ALPHA: Final[int] = 220


# font that is used in for col/row display and text terminal
FONT_TYPE: Final[str] = "assets/Roboto-Light.ttf"
TERMINAL_FONT_SIZE: Final[int] = 20
DESCRIPTION_FONT_SIZE: Final[int] = 25
GAME_OVER_FONT_SIZE: Final[int] = 80


# configuration
ROWS: Final[int] = 8
COLS: Final[int] = ROWS
TILE_WIDTH: Final[int] = 80
TILE_HEIGHT: Final[int] = TILE_WIDTH
WINDOW_SIZE_X: Final[int] = TILE_WIDTH * COLS
WINDOW_SIZE_Y: Final[int] = TILE_HEIGHT * ROWS
GAME_NAME: Final[str] = "Chess"
WHITE_PLAYER: Final[str] = "w"
BLACK_PLAYER: Final[str] = "b"
ROW_DESCRIPTION: Final[List[str]] = ["a", "b", "c", "d", "e", "f", "g", "h"]
COL_DESCRIPTION: Final[List[str]] = ["1", "2", "3", "4", "5", "6", "7", "8"]
ROW_DESCRIPTION_INDEX_X: Final[int] = 68
ROW_DESCRIPTION_INDEX_Y: Final[int] = 622
COL_DESCRIPTION_INDEX_X: Final[int] = 2
COL_DESCRIPTION_INDEX_Y: Final[int] = 2


# game over screen
GAME_OVER_TEXT_WIN: Final[str] = "{} player wins!"
GAME_OVER_TEXT_DRAW: Final[str] = "Draw!"
GAME_OVER_TEXT_X: Final[int] = 70
GAME_OVER_TEXT_Y: Final[int] = 290
GAME_OVER_DRAW_OFFSET: Final[int] = 170


# terminal configuration
TERMINAL_WIDTH: Final[int] = 220

BUTTON_WIDTH: Final[int] = 150
BUTTON_HEIGHT: Final[int] = 30
BUTTON_X: Final[int] = WINDOW_SIZE_X + 25
BUTTON_Y: Final[int] = 20
BUTTON_TEXT_X: Final[int] = WINDOW_SIZE_X + 65
BUTTON_TEXT_Y: Final[int] = 27
BUTTON_TEXT: Final[str] = "NEW GAME"

TERMINAL_RECT_WIDTH: Final[int] = 200
TERMINAL_RECT_HEIGHT: Final[int] = 565
TERMINAL_RECT_X: Final[int] = WINDOW_SIZE_X + 10
TERMINAL_RECT_Y: Final[int] = 70
TERMINAL_TEXT_X_WHITE: Final[int] = WINDOW_SIZE_X + 15
TERMINAL_TEXT_X_BLACK: Final[int] = WINDOW_SIZE_X + 120
TERMINAL_TEXT_Y: Final[int] = 75
TERMINAL_TEXT_Y_OFFSET: Final[int] = 20
TERMINAL_MAX_LINES: Final[int] = 28


# meeple image paths
ASSET_W_K: Final[str] = "assets/w_k.png"
ASSET_W_R: Final[str] = "assets/w_r.png"
ASSET_W_N: Final[str] = "assets/w_n.png"
ASSET_W_B: Final[str] = "assets/w_b.png"
ASSET_W_Q: Final[str] = "assets/w_q.png"
ASSET_W_P: Final[str] = "assets/w_p.png"
ASSET_B_K: Final[str] = "assets/b_k.png"
ASSET_B_R: Final[str] = "assets/b_r.png"
ASSET_B_N: Final[str] = "assets/b_n.png"
ASSET_B_B: Final[str] = "assets/b_b.png"
ASSET_B_Q: Final[str] = "assets/b_q.png"
ASSET_B_P: Final[str] = "assets/b_p.png"


# calculation
MAX_ITERATIONS: Final[int] = 9
