#  ---XTVENTURE 0.0.0.2 - The terminal emulator emoji Adventure Object Oriented---
# Needs:
#   * python 3.x + some Module
#   * UTF-8 Terminal Emulator with Noto Color Emoji Font or similar(TODO TEST ON WINDOWS)
#   * On Linux: root due to used Keyboard-Libary (FIXME FIND BETTER LIBRARY)

# ##------IMPORTS------## #
import numpy as np
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

        :param name: (file)name of the grid
        :param sizex: gridsize X
        :param sizey: gridsize Y
        """
        self.name = name
        self.sizex = sizex
        self.sizey = sizey

    def create_rectangle(self):
        """
        Create a rectangular grid
        :return: Rectangle of 0s, surrounded by 1s
        """
        grid = np.ones((self.sizex + 1, self.sizey + 1), dtype=np.int8)
        grid[1:-1, 1:-1] = 0  # Freie innere Fläche definieren
        return grid.tolist()

    def create_from_file(self):  # TODO CHECK FILE FOR VALID FORMAT
        """
        Create a grid from a Textfile in the maps subdirectory (filename.lvl)
        :return:  Grid read from file
        """
        grid = []
        with open('./maps/' + self.name + '.lvl', 'r') as levelfile:
            try:
                for lines in levelfile:
                    elements = lines.strip().split(' ')
                    elements = [int(element) for element in elements]
                    grid.append(elements)
            except ValueError:
                grid = None
            finally:
                return grid


# Tests TODO REPLACE WITH PROPER VERSION
def update_grid(current_grid: list, p_input: str = None):
    """
    Updates the grid on screen
    :param current_grid:  Name of the currently used grid
    :param p_input: Player input
    :return:
    """
    # if p_input != None:
    #    move(player_object, p_input)

    draw_grid(current_grid)
    print(fullwidth_str("HELLO"))
    return print(p_input)


def draw_grid(grid: list):
    clear()
    row_num = 0
    el_num = 0
    for row in grid:
        for element in row:
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
# TODO MOVE OPTIONS TO CONFIG FILE
start_time = time.time()
default_update_speed = 0.1

# my_grid = Grid('level1').create_from_file()
my_grid = Grid('level1', 30, 30).create_rectangle()

#  Evaluate Keyboard input and update grid
while True:
    current_time_count = round(time.time() - start_time)
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
