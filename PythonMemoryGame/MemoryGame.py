#Author: Trent Krogman
#Project: Advanced Technologies Presentation 1
#Date: 09/03/20

import pygame
import time
import random
import sys
from pygame.locals import *

#Constants
FPS = 30
REVEALSPEED = 8
WINDOWWIDTH = 500
WINDOWHEIGHT = 500

BOXSIZE = 100
GAPSIZE = 20
COLS = 4
ROWS = 4

BGCOLOR = (0, 0, 128)
BOXCOLOR = (255, 255, 255)

def main():
    global CLOCK, SCREEN

    pygame.init()
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption("Memory Game")
    icon = pygame.image.load("shapes/starLogo.png")
    pygame.display.set_icon(icon)

    mouseX = 0
    mouseY = 0

    #Create the board
    mainBoard = randomizeBoard()
    firstStep = True
    firstSelection = True

    #Game loop
    running = True
    while running:
        #Use Clicked boolean to ensure only one click action per loop
        clicked = False

        #Update Screen
        SCREEN.fill(BGCOLOR)
        drawBoard(mainBoard)

        #Event Handlers
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                clicked = True

            #Get mouse location
            tileX, tileY = isInsideBox(mouseX, mouseY)

            #If mouse is in a tile
            if tileX != None and tileY != None:
                currSelection = getTile(mainBoard, tileX, tileY)
                
                #If clicked tile isn't revealed 
                if clicked and currSelection.revealed == False:
                    currSelection.revealed = True
                    
                    #First step
                    if firstStep == True:
                        firstSelection = currSelection
                        firstStep = False
                    #Second step
                    else:
                        #Show second selection
                        drawBoard(mainBoard)
                        pygame.display.update()
                        #Check for match
                        if currSelection.key != firstSelection.key:                            
                            time.sleep(1)
                            firstSelection.revealed = False
                            currSelection.revealed = False
                        #Check for win
                        elif hasWon(mainBoard):                       
                            winScreen()
                            for tile in mainBoard:
                                tile.revealed = False
                            mainBoard = randomizeBoard()
                        firstStep = True

        #Update display
        pygame.display.update()
        CLOCK.tick(FPS)

#Determines whether to draw the front or back of tile based on the tiles revealed status
def drawBoard(board):
    for tile in board:
        left, top = leftTopOfBox(tile.tileX, tile.tileY)
        if tile.revealed == True:
            SCREEN.blit(tile.image, (left, top))
        else:
            pygame.draw.rect(SCREEN, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

#Creates and returns a newly randomized board
def randomizeBoard():
    #Uses two lists, one as a source and one to build on
    icons = [arrow1, arrow2, circle1, circle2, diamond1, diamond2, hexagon1,
            hexagon2, pentagon1, pentagon2, square1, square2, star1, star2, triangle1, triangle2]
    board = []
    #Shuffle source list
    random.shuffle(icons)
    i = 0
    for x in range(COLS):
        for y in range(ROWS):           
            board.append(icons[0])
            #Write coordinates tile was placed at
            board[i].tileX = x
            board[i].tileY = y
            #Delete from source list to ensure no duplicates
            del icons[0]
            i=i+1
    return board

#Finds the top left pixel of a tile
def leftTopOfBox(tileX, tileY):
    xMargin = int((WINDOWWIDTH - (COLS * (BOXSIZE + GAPSIZE) - GAPSIZE)) / 2)
    yMargin = int((WINDOWWIDTH - (COLS * (BOXSIZE + GAPSIZE) - GAPSIZE)) / 2)

    left = tileX * (BOXSIZE + GAPSIZE) + xMargin
    top = tileY * (BOXSIZE + GAPSIZE) + yMargin

    return (left, top)

def isInsideBox(x, y):
    #Source: Found in "Making games with Python and Pygame" by Al Sweigart
    #Draw rectangles with collision over location of tiles
    for boxX in range(COLS):
        for boxY in range(ROWS):
            left, top = leftTopOfBox(boxX, boxY)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxX, boxY)
    return(None, None)

#Returns the tile located at the passed coordinates      
def getTile(board, tileX, tileY):
    i = 0
    for x in range(COLS):
        for y in range(ROWS):
            if (board[i].tileX == tileX and board[i].tileY == tileY):
                return board[i]
            i = i + 1

#Checks if every tile has been revealed
def hasWon(board):
    i = 0
    for x in range(COLS):
        for y in range(ROWS):
            if board[i].revealed == False:
                return False
            i = i + 1
    return True

#Briefly displays win screen
def winScreen():
    time.sleep(0.75)
    SCREEN.fill(BGCOLOR)
    SCREEN.blit(pygame.image.load("shapes/win.png"), (0, 0))
    pygame.display.update()
    time.sleep(2)

#Tile class
class Tile:
    def __init__(self, image, key):
        self.image = pygame.image.load(image)
        self.tileX = 0
        self.tileY = 0
        self.revealed = False
        self.key = key

arrow1 = Tile("shapes/arrow.png", 1)
arrow2 = Tile("shapes/arrow.png", 1)
circle1 = Tile("shapes/circle.png", 2)
circle2 = Tile("shapes/circle.png", 2)
diamond1 = Tile("shapes/diamond.png", 3)
diamond2 = Tile("shapes/diamond.png", 3)
hexagon1 = Tile("shapes/hexagon.png", 4)
hexagon2 = Tile("shapes/hexagon.png", 4)
pentagon1 = Tile("shapes/pentagon.png", 5)
pentagon2 = Tile("shapes/pentagon.png", 5)
square1 = Tile("shapes/square.png", 6)
square2 = Tile("shapes/square.png", 6)
star1 = Tile("shapes/star.png", 7)
star2 = Tile("shapes/star.png", 7)
triangle1 = Tile("shapes/triangle.png", 8)
triangle2 = Tile("shapes/triangle.png", 8)

main()
