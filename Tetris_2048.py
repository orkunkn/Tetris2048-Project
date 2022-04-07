import os  # used for file and directory operations
import random  # used for creating tetrominoes with random types/shapes

import stddraw  # the stddraw module is used as a basic graphics library
from color import Color  # used for coloring the game menu
from game_grid import GameGrid  # class for modeling the game grid
from picture import Picture  # used representing images to display
from tetromino import Tetromino  # class for modeling the tetrominoes


# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # right information grid
    information_grid_h, information_grid_w = grid_h, grid_w / 3
    # sum of game and information grid
    full_grid_h, full_grid_w = grid_h, grid_w + information_grid_w
    # set the size of the drawing canvas
    canvas_h, canvas_w = 40 * full_grid_h, 40 * full_grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, full_grid_w - 0.5)
    stddraw.setYscale(-0.5, full_grid_h - 0.5)

    # create the game grid
    grid = GameGrid(grid_h, grid_w, full_grid_h, full_grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w)
    # set the position of current tetromino
    current_tetromino.position()
    grid.current_tetromino = current_tetromino
    # create the next tetromino to show
    next_tetromino = create_tetromino(grid_h, grid_w)
    grid.next_tetromino = next_tetromino

    # display a simple menu before opening the game
    display_game_menu(full_grid_h, full_grid_w)
    restart=False
    pause = False
    # main game loop (keyboard interaction for moving the tetromino)
    while True :
        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the tetromino left by one
                current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the tetromino down by one
                # (causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid)
            elif (key_typed == "a"):
                current_tetromino.rotateTetromino(-1,grid)
            elif (key_typed == "d"):
                current_tetromino.rotateTetromino(1,grid)
            # clear the queue that stores all the keys pressed/typed
            elif (key_typed == "escape"): # pressing escape pauses the game
                pause = not pause
            stddraw.clearKeysTyped()

        # do if the game is not paused
        if not pause:
            # move (drop) the tetromino down by 1 at each iteration
            success = current_tetromino.move("down", grid)

            # place the tetromino on the game grid when it cannot go down anymore
            if not success:
                # get the tile matrix of the tetromino
                tiles_to_place = current_tetromino.tile_matrix

                # update the game grid by adding the tiles of the tetromino
                game_over = grid.update_grid(tiles_to_place)
                grid.clearLines()
                # current_tetromino.merge(grid)
                # end the main game loop if the game is over
                if game_over:
                    break
                # create the next tetromino to enter the game grid
                # by using the create_tetromino function defined below
                # set the position of the next tetromino
                next_tetromino.position()
                # change current tetromino to next tetromino
                current_tetromino = next_tetromino
                grid.current_tetromino = current_tetromino
                # create next tetromino
                next_tetromino = create_tetromino(grid_h, grid_w)
                grid.next_tetromino = next_tetromino

            # display the game grid and as well the current tetromino
        grid.display()



    print("Game over")


# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'L', 'J', 'S', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type, grid_height, grid_width)
    return tetromino


# Function for displaying a simple menu before starting the game
def display_game_menu(full_grid_height, full_grid_width):
    # colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/menu_image.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (full_grid_width - 1) / 2, full_grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = full_grid_width - 1.5, 2
    # coordinates of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(40)
    stddraw.setPenColor(text_color)
    text_to_display = "Start"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w:
                if button_blc_y <= mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
