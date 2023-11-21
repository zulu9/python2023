#  ---XTVENTURE 0.0.0.2 - The terminal emulator emoji Adventure Object Oriented---
# Needs:
#   * python 3.x + einige Module
#   * UTF-8 Terminal Emulator mit Noto Color Emoji Font oder Ähnlichem (TODO TEST ON WINDOWS)
#   * Unter Linux: Braucht root-Rechte wegen Keyboard-Libary (FIXME)

# ##------IMPORTS------## #
import numpy as np
import os
import time
import keyboard
import random


class Grid:
    def __init__(self, name, sizex=0, sizey=0):
        self.name = name
        self.sizex = sizex
        self.sizey = sizey

    def create_rectangle(self):
        """
        :return: Rechteck aus Nullen, umrundet von Einsen
        """
        grid = np.ones((self.sizex + 1, self.sizey + 1))
        grid[1:-1, 1:-1] = 0  # Freie innere Fläche definieren
        return grid

    def create_from_file(self): # FIXME Output passt noch nicht
        """

        :return:  Aus Datei gelesenes Grid
        """
        grid = []
        with open("./maps/" + self.name + ".lvl") as levelfile:
            for line in levelfile:
                grid.append(line.rstrip())
                grid = list(grid)
        return grid


my_grid = Grid("level1", 10, 10).create_rectangle()
print(my_grid)
my_grid = Grid("level1").create_from_file()
print(my_grid)
