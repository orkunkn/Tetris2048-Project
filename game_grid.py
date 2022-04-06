import numpy as np  # fundamental Python module for scientific computing

import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w, full_grid_h, full_grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.full_grid_height = full_grid_h
        self.full_grid_width = full_grid_w
        self.score = 0

        # create the tile matrix to store the tiles placed on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # next tetromino
        self.next_tetromino = None
        # game_over flag shows whether the game is over/completed or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(42, 69, 99)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 2 * self.line_thickness

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
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(250)

    # method checks whether the rows are filled or empty.
    # all rows and columns are checked
    # deleted rows are filled
    # adding the numbers there and adding them to the score.
    def clearLines(self):
        # variables where controls should be started and the limits set.
        col = len(self.tile_matrix[0])
        row = len(self.tile_matrix)
        score = 0

        # start from the bottom row
        for r in range(row):
            row_full = True
            for c in range(col):
                if self.tile_matrix[r][c] == None:
                    row_full = False
                    break
            if row_full:
                # addition of numbers
                # delete a full line
                for c in range(col):
                    score += self.tile_matrix[r][c].number
                    self.tile_matrix[r][c] = None

                    # loops created to drop lines

                    # if self.tile_matrix[r-1][c] is not None:
                    #     self.tile_matrix[r-1][c].move(0, -1)
                    # self.tile_matrix[r][c] = copy.deepcopy(self.tile_matrix[r-1][c])
                    # self.tile_matrix[r-1][c] = None
                # for NewR in range(r, 0, -1):  # start from the bottom row
                #     print('a')
                #     for NewC in range(col):
                #         self.tile_matrix[NewR][NewC] = self.tile_matrix[NewR - 1][NewC]
                #         if self.tile_matrix[NewR][NewC] is not None:
                #             print('ran')
                #             self.tile_matrix[NewR][NewC].move(0, -1)
        # upgrade the score
        self.score += score

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
        stddraw.boldText((self.full_grid_width - self.grid_width)/2.6 + self.grid_width, self.grid_height - 1, "SCORE")
        stddraw.boldText((self.full_grid_width - self.grid_width)/2.6 + self.grid_width, 5, "NEXT")
        # print the score
        stddraw.boldText((self.full_grid_width - self.grid_width)/2.6 + self.grid_width, self.grid_height - 2, str(self.score))
        # draw the next tetromino on information grid
        self.next_tetromino.draw()
