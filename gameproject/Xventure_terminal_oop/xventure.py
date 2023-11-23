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


class Graphics:
    def __init__(self, name):
        self.name = name
        self.assignments = {}

    def create_from_file(self):  #
        """
        Read assignments from Textfile in the res subdirectory (filename.grf)
        :return:  Graphic assignments read from file
        """
        graphics_file = os.path.dirname(__file__) + '/res/' + self.name + '.grf'
        with open(graphics_file, encoding="utf-8", mode='r') as graphicsfile:  # TODO Make sure it works on Windows too
            try:
                for lines in graphicsfile:
                    key, value = lines.strip().split(':')  # An : trennen
                    self.assignments.update({int(key): str(value)})
            except ValueError:
                self.assignments = None
            finally:
                return self


class Grid:
    def __init__(self, grid_name, graphics_name, size_x=0, size_y=0):
        """
        A grid in the game
        :param grid_name: (file)name of the grid
        :param graphics_name: (file)name of the graphics assignment
        :param size_x: gridsize X
        :param size_y: gridsize Y
        """
        self.name = grid_name
        self.size_x = size_x
        self.size_y = size_y
        self.graphics = Graphics(graphics_name).create_from_file()
        self.values = []

    def create_rectangle(self):
        """
        Create a rectangular grid
        :return: Rectangle of 0s, surrounded by 1s
        """
        self.values = numpy.ones((self.size_x + 1, self.size_y + 1), dtype=numpy.int8)
        self.values[1:-1, 1:-1] = 0  # Freie innere Fläche definieren
        return self

    def create_from_file(self):
        """
        Create a grid from a Textfile in the res subdirectory (filename.lvl)
        :return:  Grid read from file
        """
        grid_file = os.path.dirname(__file__) + '/res/' + self.name + '.lvl'
        with open(grid_file, encoding="utf-8", mode='r') as levelfile:  # TODO Make sure it works on Windows too
            try:
                for lines in levelfile:
                    elements = lines.strip().split(' ')  # An Leerzeichen trennen
                    elements = [int(element) for element in elements]  # Alles in Integer umwandeln
                    self.values.append(elements)
            except ValueError:
                self.values = None
            finally:
                return self

    def update(self, p_input: str = None):
        """
        Updates the grid on screen
        :param p_input: Player input
        :return: no return
        """

        # Move player
        # if p_input != None:
        #    move(player_object, p_input)

        # Move movable entities
        # ....

        # Update other things
        #
        self.paint(self.graphics)

    def paint(self, graphics: Graphics):
        """
        # Actually paint the grid to screen
        :param graphics: graphics assignment to be used
        :return: no return. outputs directly to terminal
        """
        clear()
        row_num = 0
        el_num = 0
        for row in self.values:
            for element in row:
                # Checkthe graphics assignment dict and replace elements with emojis etc
                element = graphics.assignments.get(element)
                print(format(element, "<1"), end="")
                el_num += 1
            el_num = 0
            row_num += 1
            print()

        # Add Status Line
        # FIXME MAKE STATUS LINE MORE FLEXIBLE / CONFIGURABLE. AS CLASS?
        gametime = fullwidth_str(str(round(time.time() - start_time)))
        print(gametime)


# ##------MAIN LOOP------## #
# Configuration options
# TODO MOVE OPTIONS TO CONFIG FILE
default_update_speed = 0.1

#  Create grids
# my_grid = Grid('level1').create_from_file()
my_grid = Grid('level1', "ff_day", 30, 30).create_rectangle()

# print(type(my_grid_object))
#   input()
#  Evaluate Keyboard input and update grid

start_time = time.time()
while True:
    try:
        # Keyboard Eingaben
        if keyboard.is_pressed('left'):
            player_input = 'left'
        elif keyboard.is_pressed('right'):
            player_input = 'right'
        elif keyboard.is_pressed('down'):
            player_input = 'down'
        elif keyboard.is_pressed('up'):
            player_input = 'up'
        else:
            player_input = None

        # Update grid on screen with new vagrlues
        my_grid.graphics.name = "ff_night"  # FIXME Changes in objects are not drawn :(
        my_grid.update(player_input)
        time.sleep(default_update_speed)

    except KeyboardInterrupt:  # CTRL-C was pressed
        break
