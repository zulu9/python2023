#  ---XTVENTURE 0.0.0.2 - The terminal emulator emoji Adventure Object Oriented---
# Needs:
#   * python 3.x + some Modules
#   * UTF-8 Terminal Emulator with Noto Color Emoji Font or similar(TODO TEST ON WINDOWS)
#   * On Linux: root due to used Keyboard-Libary (FIXME FIND BETTER LIBRARY)
#  BROKEN FIXME TODO

# ##------IMPORTS------## #
import numpy as np
import os
import time
from pynput import keyboard
import playsound
import random


# ##------GLOBAL FUNCTIONS------## #
# Keybord handling
def on_press(key):
    global Keyboard_Input
    Keyboard_Input = key


def on_release(key):
    global Keyboard_Input
    if str(key) == "Key.Q":
        exit(0)
    Keyboard_Input = None


# Initialize Keyboard listener
Keyboard_Input = None
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


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


class Entitiy:
    def __init__(self, name: str, type_id: int, position: tuple, attributes: list):
        self.name = name
        self.type_id = type_id
        self.position = position
        self.attributes = attributes

    def move(self, direction: str = "None") -> tuple[int, int]:
        """
        Objekte im Grid bewegen
        :param direction: Richtung, in die sich bewegt werden soll
        :return: neue Position des Objeks
        """
        if direction == "up":
            steps = (-1, 0)
        elif direction == "down":
            steps = (1, 0)
        elif direction == "left":
            steps = (0, -1)
        elif direction == "right":
            steps = (0, 1)
        else:
            steps = (0, 0)
        new_position = tuple(np.add(self.position, steps))
        if (
                new_position[0] != 0
                and new_position[1] != 0
                and new_position[0] < my_grid.size_x
                and new_position[1] < my_grid.size_y):
            self.position = new_position
            return new_position
        else:
            return self.position


class Player(Entitiy):
    pass


class Graphics:
    def __init__(self, name: str):
        self.name = name
        self.assignments = {}

    def read_from_file(self):  #
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
    def __init__(self, grid_name: str, graphics_name: str, size_x: int = 0, size_y: int = 0):
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
        self.graphics = Graphics(graphics_name).read_from_file()
        self.values = []

    def create_rectangle(self, static_objects: list = None):
        """
        Create a rectangular grid
        :return: Rectangle of 0s, surrounded by 1s
        """

        # Create empty grid
        self.values = np.ones((self.size_x + 1, self.size_y + 1), dtype=np.int8)
        self.values[1:-1, 1:-1] = 0  # Free space

        # Insert static objects like decorations
        if static_objects is not None:
            for thing in static_objects:
                self.values[thing.position] = thing.type_id
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

    def get_random_position(self) -> tuple[int, int]:
        """

        :return:  A random position inside the grid
        """
        g_random_position = (random.randrange(self.size_x - 1) + 1, random.randrange(self.size_y - 1) + 1)
        return g_random_position

    def update(self, p_input: str = None):
        """
        Updates the grid on screen
        :param p_input: Player input
        :return: no return
        """

        # Move player
        if p_input is not None:
            my_player.move(p_input)

        # Move movable entities
        # ....

        # Update other things
        #

        # Upgrade the grid

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
                # Draw Player
                if (row_num, el_num) == my_player.position:
                    element = 2
                # Check the graphics assignment dict and replace elements with emojis etc
                element = graphics.assignments.get(element)
                print(format(str(element), "<1"), end="")
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
start_time = time.time()  # Start the clock

#  Create grid
# my_grid = Grid('level1').create_from_file()
my_grid = Grid('ff_level1', "ff_day", 30, 30).create_rectangle()

# Create Entities
my_decorations = []
number_of_decorations = 30
for i in range(0, number_of_decorations):
    my_decorations.append(
        Entitiy("decoration" + str(i), random.choice([3, 4, 5]), my_grid.get_random_position(), [])
    )
my_grid.create_rectangle(my_decorations)


my_player = Entitiy("Kisa", 2, my_grid.get_random_position(), [])
playsound.playsound('./res/music.mp3', False)

my_grid.create_rectangle(my_decorations)
print(my_grid.values)

#  Evaluate Keyboard input and update grid
while True:
    try:
        print(Keyboard_Input)
        # Keyboard Eingaben
        if str(Keyboard_Input) == "Key.left":
            player_input = 'left'
        elif str(Keyboard_Input) == "Key.right":
            player_input = 'right'
        elif str(Keyboard_Input) == "Key.up":
            player_input = 'up'
        elif str(Keyboard_Input) == "Key.down":
            player_input = 'down'
        elif str(Keyboard_Input) == "Key.q":
            break
        else:
            player_input = None

        # current_time = round(start_time - time.time())
        # if current_time % 2 == 0:
        #     my_grid.graphics.name = "ff_night"
        # else:
        #     my_grid.graphics.name = "ff_day"
        # my_grid.graphics.read_from_file()

        # Update grid and draw on screen
        my_grid.update(player_input)
        my_grid.paint(my_grid.graphics)
        time.sleep(default_update_speed)

    except KeyboardInterrupt:  # CTRL-C was pressed
        break
