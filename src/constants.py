from typing import *
import pygame


# Colours that are used for chessboard tiles and highlights
COLOUR_BLACK: Final[Set] = pygame.Color(0, 0, 0)
COLOUR_WHITE: Final[Set] = pygame.Color(255, 255, 255)
COLOUR_RED: Final[Set] = pygame.Color(255, 0, 0)
COLOUR_YELLOW: Final[Set] = pygame.Color(255, 255, 0)
COLOUR_GREEN: Final[Set] = pygame.Color(0, 255, 0)
COLOUR_ALPHA: Final[int] = 120


# font that is used in for col/row display and text terminal
FONT_TYPE: Final[str] = "assets/Roboto-Light.ttf"
TERMINAL_FONT_SIZE: Final[int] = 18
DESCRIPTION_FONT_SIZE: Final[int] = 25


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
TERMINAL_TEXT_X_BLACK: Final[int] = WINDOW_SIZE_X + 130
TERMINAL_TEXT_Y: Final[int] = 75
TERMINAL_TEXT_Y_OFFSET: Final[int] = 20