import numpy as np  # fundamental Python module for scientific computing
import copy
import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game grid


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w, full_grid_h, full_grid_w):
        self.score = 0
        # set the dimensions of the game grid as the given arguments
        self.speed = 250
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
                for c in range(col):
                    score += self.tile_matrix[r][c].number  # sum up values for the score
                    self.tile_matrix[r][c] = None  # remove those tiles
                    for i in range(r, row-1):
                        if self.tile_matrix[i+1][c] is not None:
                            self.tile_matrix[i + 1][c].move(0, -1)
                            self.tile_matrix[i][c] = self.tile_matrix[i+1][c]
                            self.tile_matrix[i + 1][c] = None

        self.score += score  # update score

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

    # Method for merging the back to back tiles with same numbers
    def merge(self, tetromino):
        # recursion check variable
        merged = False
        # determine the merge width border
        if tetromino.bottom_left_corner.x + tetromino.n > self.grid_width:
            right_merge_border = self.grid_width
        else:
            right_merge_border = tetromino.bottom_left_corner.x + tetromino.n
        # determine the merge height border
        if tetromino.bottom_left_corner.y + tetromino.n > self.grid_height:
            up_merge_border = self.grid_height
        else:
            up_merge_border = tetromino.bottom_left_corner.y + tetromino.n
        # check in tetrominos height border
        for col in range(tetromino.bottom_left_corner.y, up_merge_border):
            # check in tetrominos width border
            for row in range(tetromino.bottom_left_corner.x, right_merge_border):
                # check if there are blocks on the controlled coordinates
                if self.tile_matrix[col][row] is not None and self.tile_matrix[col - 1][row] is not None:
                    # check if the tiles in same column have the same number
                    if self.tile_matrix[col - 1][row].number == self.tile_matrix[col][row].number:
                        # store the tiles initial color temporary
                        temp_color = self.tile_matrix[col][row].background_color
                        # change the merged tiles color to green
                        self.tile_matrix[col - 1][row].background_color = Color(0, 255, 0)
                        self.tile_matrix[col][row].background_color = Color(0, 255, 0)
                        # display the green tiles
                        self.display()
                        # reverse the tile's color
                        self.tile_matrix[col - 1][row].background_color = temp_color
                        # multiply the tile's number by 2
                        self.tile_matrix[col - 1][row].number *= 2
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
                        # change recursion variable to true
                        merged = True
                        # quit the loop
                        break
        # if a merge happened, call merge function again
        if merged:
            self.merge(tetromino)
