# ============================================================================ #
# Abgabe Projektarbeit Einführung ins Programmieren mit Python
# Namen
#     Michael Bierschneider, Mat.Nr. 1652774

import pygame
from src.meeple import Meeple
from src.chessboard import Chessboard
from src.constants import config

pygame.init()

colour_white = pygame.Color(255, 255, 255)
colour_black = pygame.Color(0, 0, 0)
colour_red = pygame.Color(255, 0, 0)
colour_yellow = pygame.Color(255, 255, 0)
colour_flip = True

window = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")

width, height = 8 * config["CELL_WIDTH"], 8 * config["CELL_HEIGHT"]
background = pygame.Surface((width, height))

rects = []

for x in range(0, width, config["CELL_WIDTH"]):
    colour_flip = not colour_flip
    for y in range(0, height, config["CELL_HEIGHT"]):
        rectangle = pygame.Rect(x, y, config["CELL_WIDTH"], config["CELL_HEIGHT"])
        colour = colour_black if colour_flip else colour_white
        colour_flip = not colour_flip
        rects.append(rectangle)
        pygame.draw.rect(background, colour, rectangle)

gameRunning = True
playerTurn = True # white starts playing
selectedField = False

#first draw highlight
#then draw meeple
board = Chessboard()
i = pygame.sprite.Group()
sprites = [sprites for sprites in board.array for sprite in sprites if sprite]
i.add(sprites)

while gameRunning:
    if playerTurn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for j in rects:
                    if j.collidepoint((mouse_x, mouse_y)):
                        if not selectedField:
                            meeple = board.highlightMeeple(j.x, j.y)
                            if meeple != None:
                                moves = meeple.possibleMoves(board)
                                board.highlightMoves(moves)
                                #wait for movefieldclick
                                selectedField = True
                        else:
                            #display moves & wait for player reaction
                            #checkpromotion of 
                            if (j.x // 80, j.y // 80) == (board.hightlightedMeepleTile.x, board.hightlightedMeepleTile.y):
                                board.highlightMoves([])
                                board.hightlightedMeepleTile = None
                                selectedField = False
                            elif ((j.x // 80, j.y // 80) in board.hightlightedMoveFields):
                                board.highlightMoves([])
                                result = board.moveMeeple((j.x, j.y))

                                i.empty()
                                #sprites = [sprites for sprites in board.array for sprite in sprites if sprite]
                                for sprites in board.array:
                                    array = []
                                    for sprite in sprites:
                                        if sprite:
                                            array.append(sprite)
                                    i.add(array) #pygame is expecting a list or tuple, when only one sprite is in a list, it outmerged 
                                    #to object and cant be iterated anymore


                                #i.add(sprites)

                                playerTurn = False

                            #if click on hightlight => selectedField false
    else:
        playerTurn = True
        selectedField = False


    window.blit(background, (0, 0))

    #for its in board.hightlights:
    piece = board.hightlightedMeepleTile
    if piece != None and piece.colour != "b":
        test = pygame.Surface((80, 80))
        test.set_alpha(120)
        test.fill((255,255,0))
        window.blit(test, (piece.rect.x, piece.rect.y))

    for tile in board.hightlightedMoveFields:
        test1 = pygame.Surface((80, 80))
        test1.set_alpha(120)
        test1.fill((255,0,0))
        window.blit(test1, (tile[0] * 80, tile[1] * 80))

    #for row in sprites:
    #     for sprite in row:
    #       sprite.draw(window)
    i.draw(window)

    pygame.display.flip()
    clock.tick(30)
