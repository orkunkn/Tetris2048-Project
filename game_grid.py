import numpy as np  # fundamental Python module for scientific computing
import copy
import os
from picture import Picture  # used representing images to display
import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid


def draw_pause():  # draws the pause icon when paused
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/pause.png"
    # center coordinates to display the image
    img_center_x, img_center_y = 7.5, 10
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w, full_grid_h, full_grid_w):
        self.score = 0
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.full_grid_height = full_grid_h
        self.full_grid_width = full_grid_w
        # create the tile matrix to store the tiles placed on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # next tetromino
        self.next_tetromino = None
        # game_over flag shows whether the game is over/completed or not
        self.game_over = False
        # pause flag shows whether the game is paused or not
        self.pause = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(160, 160, 160)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(128, 128, 128)
        self.boundary_color = Color(128, 128, 128)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.0045
        self.box_thickness = self.line_thickness

    # Method used for displaying the game grid
    def display(self):
        # clear the background canvas to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current (active) tetromino
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # draw the second grid for showing score and next tetromino
        self.draw_information_grid()
        if self.pause:
            draw_pause()
        # show the resulting drawing with a pause duration = speed
        stddraw.show(self.speed)

    # method for clearing full lines
    def clearLines(self):
        col = len(self.tile_matrix[0])
        row = len(self.tile_matrix)
        score = 0
        for r in range(row):
            row_full = True
            for c in range(col):
                if self.tile_matrix[r][c] is None:  # break  at the sight of the first none on the row
                    row_full = False
                    break
            if row_full:  # if there is no None in that row
                for i in range(col):
                    self.tile_matrix[r][i].background_color = Color(0, 255, 0)
                    self.tile_matrix[r][i].foreground_color = Color(255, 255, 255)
                self.display()
                for c in range(col):
                    score += self.tile_matrix[r][c].number  # sum up values for the score
                    self.tile_matrix[r][c] = None  # remove those tiles
                    # drop the upper tiles
                    for i in range(r, row - 1):
                        if self.tile_matrix[i + 1][c] is not None:
                            self.tile_matrix[i + 1][c].move(0, -1)
                            self.tile_matrix[i][c] = self.tile_matrix[i + 1][c]
                            self.tile_matrix[i + 1][c] = None
        self.score += score  # update score

    # method for updating grid colors after each merge
    def updateGridColor(self):
        row = len(self.tile_matrix)
        col = len(self.tile_matrix[0])
        for r in range(row):
            for c in range(col):
                if self.tile_matrix[r][c] is not None:
                    self.tile_matrix[r][c].updateTileColor()

    # Method for merging the back to back tiles with same numbers
    def merge(self):
        # recursion check variable
        merged = False
        # determine the merge width border
        if self.current_tetromino.bottom_left_corner.x + self.current_tetromino.n > len(self.tile_matrix[0]):
            right_merge_border = len(self.tile_matrix[0])
        else:
            right_merge_border = self.current_tetromino.bottom_left_corner.x + self.current_tetromino.n
        # determine the merge height border
        if self.current_tetromino.bottom_left_corner.y + self.current_tetromino.n > len(self.tile_matrix):
            up_merge_border = len(self.tile_matrix)
        else:
            up_merge_border = self.current_tetromino.bottom_left_corner.y + self.current_tetromino.n
        # check in tetrominos height border
        for col in range(1, up_merge_border):
            # check in tetrominos width border
            for row in range(self.current_tetromino.bottom_left_corner.x, right_merge_border):
                # check if there are blocks on the controlled coordinates
                if self.tile_matrix[col][row] is not None and self.tile_matrix[col - 1][row] is not None:
                    # check if the tiles in same column have the same number
                    if self.tile_matrix[col - 1][row].number == self.tile_matrix[col][row].number:
                        # store the tiles initial color temporary
                        temp_color = self.tile_matrix[col][row].background_color
                        temp_number_color = self.tile_matrix[col][row].foreground_color
                        # change the merged tiles background colors to green, number colors to white
                        self.tile_matrix[col - 1][row].background_color = Color(0, 255, 0)
                        self.tile_matrix[col][row].background_color = Color(0, 255, 0)
                        self.tile_matrix[col - 1][row].foreground_color = Color(255, 255, 255)
                        self.tile_matrix[col][row].foreground_color = Color(255, 255, 255)
                        # display the green tiles
                        self.display()
                        # reverse the tile's color
                        self.tile_matrix[col - 1][row].foreground_color = temp_number_color
                        self.tile_matrix[col - 1][row].background_color = temp_color
                        # multiply the tile's number by 2
                        self.tile_matrix[col - 1][row].number *= 2
                        # add merged numbers to score
                        self.score += self.tile_matrix[col - 1][row].number
                        # delete top tile
                        self.tile_matrix[col][row] = None
                        # check for hanging tiles on the merge column
                        for i in range(col, up_merge_border):
                            # check if there is a tile with a space under it
                            if self.tile_matrix[i - 1][row] is None and self.tile_matrix[i][row] is not None:
                                # move the tile down
                                self.tile_matrix[i][row].move(0, -1)
                                # move the tile down in matrix
                                self.tile_matrix[i - 1][row] = self.tile_matrix[i][row]
                                # delete the top tile
                                self.tile_matrix[i][row] = None
                                self.display()
                        # change recursion variable to true
                        merged = True
                        self.updateGridColor()
                        # quit the loop
                        break
        # if a merge happened, call merge function again
        if merged:
            self.merge()

    # Method for moving isolated tiles down
    def remove_gaps(self):
        # recursive check variable
        removed = False
        # check every row except start and finish columns
        for i in reversed(range(1, len(self.tile_matrix) - 1)):
            # check every column
            for k in range(len(self.tile_matrix[0])):
                # check if controlled tile exist
                if self.tile_matrix[i][k] is not None:
                    # check if upper and bottom tiles do not exist
                    if self.tile_matrix[i - 1][k] is None and self.tile_matrix[i + 1][k] is None:
                        # if controlled column is final column, only control the left side
                        if k == (len(self.tile_matrix[0]) - 1):
                            if self.tile_matrix[i][k - 1] is None:
                                # drop the tile as long as it can
                                while self.tile_matrix[i - 1][k] is None:
                                    self.tile_matrix[i][k].move(0, -1)
                                    self.tile_matrix[i - 1][k] = self.tile_matrix[i][k]
                                    self.tile_matrix[i][k] = None
                                    self.display()
                                    removed = True
                        # if controlled column is starting column, only control the right side
                        elif k == 0:
                            if self.tile_matrix[i][k + 1] is None:
                                # drop the tile as long as it can
                                while self.tile_matrix[i - 1][k] is None:
                                    self.tile_matrix[i][k].move(0, -1)
                                    self.tile_matrix[i - 1][k] = self.tile_matrix[i][k]
                                    self.tile_matrix[i][k] = None
                                    self.display()
                                    removed = True

                        else:
                            if self.tile_matrix[i][k - 1] is None and self.tile_matrix[i][k + 1] is None:
                                # drop the tile as long as it can
                                while self.tile_matrix[i - 1][k] is None:
                                    self.tile_matrix[i][k].move(0, -1)
                                    self.tile_matrix[i - 1][k] = self.tile_matrix[i][k]
                                    self.tile_matrix[i][k] = None
                                    self.display()
                                    removed = True
        # if a remove happened, check for another removes
        if removed:
            self.remove_gaps()

    # Method for drawing the cells and the lines of the grid
    def draw_grid(self):
        # draw each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw()
                    # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # return False if the cell is out of the grid
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method for updating the game grid by placing the given tiles of a stopped
    # tetromino and checking if the game is over due to having tiles above the
    # topmost game grid row. The method returns True when the game is over and
    # False otherwise.
    def update_grid(self, tiles_to_place):
        # place all the tiles of the stopped tetromino onto the game grid
        n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each occupied tile onto the game grid
                if tiles_to_place[row][col] is not None:
                    pos = tiles_to_place[row][col].get_position()
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]
                    # the game is over if any placed tile is out of the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over

    # Method for drawing the information grid
    def draw_information_grid(self):
        # coordinates of left down corner of the grid
        pos_x, pos_y = -0.5, -0.5
        # set the color of information grid
        GRAY = Color(128, 128, 128)
        stddraw.setPenColor(GRAY)
        # draw the information grid
        stddraw.rectangle(pos_x + self.grid_width, pos_y, self.grid_width, self.grid_height)
        stddraw.filledRectangle(pos_x + self.grid_width, pos_y, self.grid_width, self.grid_height)
        # print the information titles (SCORE and NEXT)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setFontSize(self.grid_width * 2)
        stddraw.boldText((self.full_grid_width - self.grid_width) / 2.6 + self.grid_width, self.grid_height - 1,
                         "SCORE")
        stddraw.boldText((self.full_grid_width - self.grid_width) / 2.6 + self.grid_width, 5, "NEXT")
        # print the score
        stddraw.boldText((self.full_grid_width - self.grid_width) / 2.6 + self.grid_width, self.grid_height - 2,
                         str(self.score))
        # draw the next tetromino on information grid
        self.next_tetromino.draw()
