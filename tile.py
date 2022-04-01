import copy as cp  # the copy module is used for copying tile positions
import random

import numpy as np

import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the tile and the number on it
from point import Point  # used for representing the position of the tile


# Class used for representing numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # value used for the thickness of the boxes (boundaries) around the tiles
    boundary_thickness = 0.004
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # Constructor that creates a tile at a given position with 2 as its number
    def __init__(self, position=Point(0, 0)):  # (0, 0) is the default position
        # assign the number on the tile
        temp = random.randint(0, 1)
        if (temp == 0):
            self.number = 2
        else:
            self.number = 4
        # set the colors of the tile
        self.background_color = Color(151, 178, 199)  # background (tile) color
        self.foreground_color = Color(0, 100, 200)  # foreground (number) color
        self.boundary_color = Color(0, 100, 200)  # boundary (box) color
        # set the position of the tile as the given position
        self.position = Point(position.x, position.y)

    # Setter method for the position of the tile
    def set_position(self, position):
        # set the position of the tile as the given position
        self.position = cp.copy(position)

        # Getter method for the position of the tile
    #r
    def rotateTile(self, centerCoord, rotDir): # 1 for right -1 for left
        relativeCoord = []
        clockwiseArr=np.array([[0,1],[-1,0]])
        counterClockwiseArrr=np.array([[0,-1],[1,0]])
        relativeCoord.append(self.position.x-centerCoord.x)
        relativeCoord.append(self.position.y - centerCoord.y)
        if (rotDir == 1):
            newCoord = np.dot(clockwiseArr,relativeCoord)
            self.position.x=newCoord[0]+centerCoord.x
            self.position.y=newCoord[1]+centerCoord.y
        else:
            newCoord = np.dot(counterClockwiseArrr,relativeCoord)
            self.position.x=newCoord[0]+centerCoord.x
            self.position.y=newCoord[1]+centerCoord.y


    def get_position(self):
        # return the position of the tile
        return cp.copy(self.position)

        # Method for moving the tile by dx along the x-axis and by dy along the y-axis

    def move(self, dx, dy):
        self.position.translate(dx, dy)

    # Method for drawing the tile
    def draw(self):
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(self.position.x, self.position.y, 0.5)
        # draw the bounding box of the tile as a square
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(self.position.x, self.position.y, 0.5)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.boldText(self.position.x, self.position.y, str(self.number))
