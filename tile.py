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
    boundary_thickness = 0.003
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # Constructor that creates a tile at a given position with 2 as its number
    def __init__(self, position=Point(0, 0)):  # (0, 0) is the default position
        # assign the number on the tile
        temp = random.randint(0, 1)
        if temp == 0:
            self.number = 2
        else:
            self.number = 4
        # set the colors of the tile
        if self.number == 2:
            self.background_color = Color(238, 228, 218)
        else:
            self.background_color = Color(236, 223, 190)

        self.foreground_color = Color(64, 64, 64)  # foreground (number) color
        self.boundary_color = Color(128, 128, 128)  # boundary (box) color
        # set the position of the tile as the given position
        self.position = Point(position.x, position.y)

    # method for updating tile colors after each merge
    def updateTileColor(self):
        # check for numbers color
        if self.number >= 8:
            self.foreground_color = Color(255, 255, 255)
        else:
            self.foreground_color = Color(64, 64, 64)
        # check for tile background colors
        if self.number == 2:
            self.background_color = Color(238, 228, 218)
        elif self.number == 4:
            self.background_color = Color(236, 223, 190)
        elif self.number == 8:
            self.background_color = Color(242, 177, 121)
        elif self.number == 16:
            self.background_color = Color(246, 149, 98)
        elif self.number == 32:
            self.background_color = Color(246, 124, 94)
        elif self.number == 64:
            self.background_color = Color(255, 88, 68)
        elif self.number == 128:
            self.background_color = Color(243, 209, 89)
        elif self.number == 256:
            self.background_color = Color(236, 203, 106)
        elif self.number == 512:
            self.background_color = Color(238, 200, 82)
        elif self.number == 1024:
            self.background_color = Color(233, 200, 60)
        elif self.number == 2048:
            self.background_color = Color(240, 196, 36)
        else:
            self.background_color = Color(62, 57, 51)

    # Setter method for the position of the tile
    def set_position(self, position):
        # set the position of the tile as the given position
        self.position = cp.copy(position)

    # Getter method for the position of the tile
    def get_position(self):
        # return the position of the tile
        return cp.copy(self.position)

    # Rotate method for tiles
    def rotateTile(self, centerCoord, rotDir):  # 1 for right -1 for left
        relativeCoord = []
        # rotation arrays
        clockwiseArr = np.array([[0, 1], [-1, 0]])
        counterClockwiseArrr = np.array([[0, -1], [1, 0]])
        relativeCoord.append(self.position.x - centerCoord.x)
        relativeCoord.append(self.position.y - centerCoord.y)
        if rotDir == 1:
            # dot product is the new relative coordinates array
            newCoord = np.dot(clockwiseArr, relativeCoord)
            # to get from relative coordinates to new coordinates, coordinates of the axis are added
            self.position.x = newCoord[0] + centerCoord.x
            self.position.y = newCoord[1] + centerCoord.y
        else:
            newCoord = np.dot(counterClockwiseArrr, relativeCoord)
            self.position.x = newCoord[0] + centerCoord.x
            self.position.y = newCoord[1] + centerCoord.y

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
