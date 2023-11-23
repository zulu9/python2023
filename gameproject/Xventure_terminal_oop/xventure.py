#  ---XTVENTURE 0.0.0.2 - The terminal emulator emoji Adventure Object Oriented---
# Needs:
#   * python 3.x + some Modules
#   * UTF-8 Terminal Emulator with Noto Color Emoji Font or similar(TODO TEST ON WINDOWS)
#   * On Linux: root due to used Keyboard-Libary (FIXME FIND BETTER LIBRARY)
#  BROKEN FIXME TODO

# ##------IMPORTS------## #
import numpy
import os
import time
import keyboard
import random


# ##------GLOBAL FUNCTIONS------## #
def fullwidth_str(text: str) -> str:
    """
    Translate string to fullwidth unicode characters to avoid weird spacing (Can't do Umlauts!)
    :param text: String to convert
    :return: Converted string
    """
    to_fullwidth = str.maketrans(
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~',
        '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～')
    return text.translate(to_fullwidth)


def clear():
    """
    Clears screen (needs "real" Terminal!)
    :return: No return
    """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

# ##------CLASSES------## #


class Grid:
    def __init__(self, name, sizex=0, sizey=0):
        """
        A grid in the game
        :param name: (file)name of the grid
        :param sizex: gridsize X
        :param sizey: gridsize Y
        """
        self.name = name
        self.sizex = sizex
        self.sizey = sizey
        self.values = []

    def create_rectangle(self):
        """
        Create a rectangular grid
        :return: Rectangle of 0s, surrounded by 1s
        """
        self.values = numpy.ones((self.sizex + 1, self.sizey + 1), dtype=numpy.int8)
        self.values[1:-1, 1:-1] = 0  # Freie innere Fläche definieren
        return self

    def create_from_file(self):  # TODO CHECK FILE FOR VALID FORMAT
        """
        Create a grid from a Textfile in the maps subdirectory (filename.lvl)
        :return:  Grid read from file
        """
        with open('./maps/' + self.name + '.lvl', 'r') as levelfile:
            try:
                for lines in levelfile:
                    elements = lines.strip().split(' ')
                    elements = [int(element) for element in elements]
                    self.values.append(elements)
            except ValueError:
                self.values = None
            finally:
                return self


# Tests TODO REPLACE WITH PROPER VERSION
def update_grid(current_grid: Grid, p_input: str = None):
    """
    Updates the grid on screen
    :param current_grid:  Name of the currently used grid
    :param p_input: Player input
    :return:
    """

    # Move player
    # if p_input != None:
    #    move(player_object, p_input)

    # Move movable entities
    # ....

    # Update other things
    # ---

    # Draw new Grid
    new_grid = current_grid  # FIXME
    print(new_grid)
    paint_grid(new_grid)

    # Add Status Line
    print(fullwidth_str(str(round(time.time() - start_time))))

    return print(p_input)  # FIXME REMOVE AFTER IMPLEMENTING MOVES


def paint_grid(grid: Grid):
    """
    # Actually paint the grid to screen
    :param grid: grid to be painted on screen
    :return: no return outputs directly to terminal
    """
    clear()
    row_num = 0
    el_num = 0
    for row in grid.values:
        for element in row:  # FIXME FIND A BETTER WAY TO REPLACE NUMBERS WITH EMOJIS (TRANSLATE FUNCTION?)
            if element == 1:  # Rehmen zeichnen
                element = "🧱"
            elif element == 0:  # Freie Fläche zeichnen
                element = "🟩"
            print(format(element, "<1"), end="")
            el_num += 1
        el_num = 0
        row_num += 1
        print()


# ##------MAIN LOOP------## #
# Configuration options
# TODO MOVE OPTIONS TO CONFIG FILE
default_update_speed = 0.1

#  Create grids
my_grid = Grid('level1').create_from_file()
# my_grid = Grid('level1', 30, 30).create_rectangle()


# print(type(my_grid_object))
#   input()
#  Evaluate Keyboard input and update grid
start_time = time.time()
while True:
    try:
        # Keyboard Eingaben
        if keyboard.is_pressed('left'):
            p_direction = 'left'
        elif keyboard.is_pressed('right'):
            p_direction = 'right'
        elif keyboard.is_pressed('down'):
            p_direction = 'down'
        elif keyboard.is_pressed('up'):
            p_direction = 'up'
        else:
            p_direction = None

        # Update grid on screen with new values
        update_grid(my_grid, p_direction)
        time.sleep(default_update_speed)

    except KeyboardInterrupt:  # CTRL-C was pressed
        break
