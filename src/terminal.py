import pygame
from src.constants import *

class Terminal:

    def __init__(self, description_font, terminal_font) -> None:
        self.button = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.description_font = description_font
        self.terminal_font = terminal_font
        self.button_text = self.description_font.render(BUTTON_TEXT, True, COLOUR_BLACK)
        self.terminal_background = pygame.Rect(TERMINAL_RECT_X, TERMINAL_RECT_Y, TERMINAL_RECT_WIDTH, TERMINAL_RECT_HEIGHT)

        self.terminal_white_notation = []
        self.terminal_black_notation = []

    #(self.array[end_y][end_x].symbol, start_x, start_y, end_x, end_y, True, ["check", "check_mate", "promotion", "castling", "remis"])
    def addNotation(self, result, colour = "w") -> None:
        #translate rows => lookup in consts
        text = str(result[0]) + str(ROW_DESCRIPTION[result[1]]) + str(result[2] + 1) + "-" if result[5] else "x" 
        text += str(ROW_DESCRIPTION[result[3]]) + str(result[4] + 1)

        if result[6][2] == "promotion":
            text += "Q"
        if result[6][3] == "castling":
            text = "o-o"
        if result[6][0] == "check":
            text += "+"
        elif result[6][1] == "check_mate":
            text += "#"
        else:
            text += ""
        if result[6][4] == "remis":
            text = "= ="

        if colour == "w":
            self.terminal_white_notation.append(self.terminal_font.render(str(len(self.terminal_white_notation) + 1) + "  " + text, True, COLOUR_BLACK))
        else:
            self.terminal_black_notation.append(self.terminal_font.render(text, True, COLOUR_BLACK))