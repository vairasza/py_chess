import pygame
from src.constants import *

class Terminal:

    def __init__(self, terminal_font: pygame.font) -> None:
        self.button = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.terminal_font = terminal_font
        self.button_text = self.terminal_font.render(BUTTON_TEXT, True, COLOUR_BLACK)
        self.terminal_background = pygame.Rect(TERMINAL_RECT_X, TERMINAL_RECT_Y, TERMINAL_RECT_WIDTH, TERMINAL_RECT_HEIGHT)

        self.terminal_white_notation = []
        self.terminal_black_notation = []
        self.index = 0

    #(self.array[end_y][end_x].symbol, start_x, start_y, end_x, end_y, True, ["check", "check_mate", "promotion", "castling", "draw"])
    def addNotation(self, result: List, colour: str = "w") -> None:
        #translate rows => lookup in consts
        text = str(result[0]) + str(ROW_DESCRIPTION[result[1]]) + str(result[2] + 1)
        text += "-" if result[5] else "x" 
        text += str(ROW_DESCRIPTION[result[3]]) + str(result[4] + 1)

        if "promotion" in result[6]:
            text += "Q"
        if "castling" in result[6]:
            text = "o-o"
        if "castling-long" in result[6]:
            text = "o-o-o"
        if "check" in result[6]:
            text += "+"
        elif "check_mate" in result[6]:
            text += "#"
        elif "draw" in result[6]:
            text = "= ="

        if colour == "w":
            # to have a leading number that indicates the round
            self.index += 1
            text = str(self.index) + "  " + text
            self.terminal_white_notation.append(self.terminal_font.render(text, True, COLOUR_BLACK))
        else:
            self.terminal_black_notation.append(self.terminal_font.render(text, True, COLOUR_BLACK))

        #remove overflowing round notations    
        if len(self.terminal_white_notation) > TERMINAL_MAX_LINES:
            self.terminal_white_notation.pop(0)
            self.terminal_black_notation.pop(0)
