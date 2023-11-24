#  ---Feline Fantasy I - The XTERMinator 0.0.0.3 - The terminal emulator emoji Adventure---
# Needs:
#   * python 3.x + some Modules
#   * UTF-8 Terminal Emulator with Noto Color Emoji Font or similar(TODO TEST ON WINDOWS)

# ##------IMPORTS------## #
import numpy as np
import os
import sys
import time
import random
import threading
from playsound import playsound
from pynput import keyboard

# ##------GLOBAL FUNCTIONS------## #
# Keybord handling


def on_press(key):
    """
    Handle key presses
    :param key:
    :return:
    """
    global Keyboard_Input
    Keyboard_Input = key


def on_release(key):  # FIXME DOES NOT WORK AND MIGHT CAUSE DOUBLE EVENTS
    """
    handle key releases
    :param key:
    :return:
    """
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
# //END Initialize Keyboard listener

# Sound Handling


def play_soundfile(path):  # FIXME DOES NOT PROPERLY THREAD
    """

    :param path: Path to soundfile
    :return: no return. starts thread
    """
    global stop_playback
    play_thread = threading.Thread(target=playsound(path, False), daemon=True)
    play_thread.start()


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
    def __init__(self, type_id: int, position: tuple):
        """
        General class for entities
        :param type_id: Type (as integer ID) of the entity as defined in grid-file or function
        :param position: position of the entity on the grid
        """
        self.type_id = type_id
        self.position = position

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
        if current_grid.values[new_position] == 0:  # Free space. Good to go
            self.position = new_position  # Update position
            return self.position
        else:
            # COLLISION!
            return self.position


class Player(Entitiy):
    def __init__(self, name, type_id: int, position: tuple):
        """

        :param name: Player Name
        :param type_id: ID for player graphic
        :param position: Player position
        """
        super().__init__(type_id, position)
        self.name = name


class Decoration(Entitiy):
    pass


class Enemy(Entitiy):
    pass


class Fire(Entitiy):
    pass


class Graphicset:
    def __init__(self, name: str):
        """

        :param name: Name of the graphicsset. Must be placed in $PWD/res/$name.grf
        """
        self.name = name
        self.assignments = {}

    def read_from_file(self):  #
        """
        Read assignments from Textfile in the res subdirectory (filename.grf)
        :return:  Graphicset assignments
        """
        graphicset_file = os.path.dirname(__file__) + '/res/' + self.name + '.grf'
        with open(graphicset_file, encoding="utf-8", mode='r') as graphicsfile:  # TODO Make sure it works on Windows
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
        :param size_x: gridsize X in utf-8 full-width chars
        :param size_y: gridsize Y in utf-8 full-width chars
        """
        self.name = grid_name
        self.size_x = size_x
        self.size_y = size_y
        self.graphics = Graphicset(graphics_name).read_from_file()
        self.values = []

    def create_rectangle(self, static_objects: list = None):
        """
        Create a rectangular grid
        :return: Rectangle of 0s, surrounded by 1s and insert values for static game objects
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
        Create a grid from a Textfile in the res subdirectory ($PWD/res/$grid.name.lvl)
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
            else:
                self.size_x = len(self.values)
                self.size_y = len(self.values[0])
            finally:
                return self

    def get_random_position(self) -> tuple[int, int]:
        """
        A random position inside the grid
        :return:  tuple with the random position
        """
        g_random_position = (random.randrange(self.size_x - 1) + 1, random.randrange(self.size_y - 1) + 1)
        return g_random_position

    def update(self, p_input: str = None):
        """
        Updates the grid on screen
        :param p_input: Player input
        :return: no return, just updates stuff
        """

        # Move player FIXME Player movement broken. Maybe move to graphicset-class together with paint method?
        if p_input is not None:
            my_player.move(p_input)  # Move Player
            self.values[my_player.position] = my_player.type_id  # FIXME WARNING ABOUT TYPES: NUMPY?
        # Move movable entities
        # ....

        # Update other things
        #

        # Update the grid

    def paint(self, graphicset: Graphicset):
        """
        # Actually paint the grid to screen
        :param graphicset: graphics assignment to be used
        :return: no return. outputs directly to terminal
        """
        clear()
        row_num = 0
        el_num = 0
        for row in self.values:
            for element in row:
                # Check the graphics assignment dict and replace elements with emojis etc
                element = graphicset.assignments.get(element)
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
# current_grid = Grid('ff_level1', 'ff_day').create_from_file()
current_grid = Grid('ff_level1', "ff_snakemode", 30, 30).create_rectangle()

# Create Entities
# # Decorations and other static objects
my_decorations = []
number_of_decorations = (current_grid.size_x + current_grid.size_y) // 2
for i in range(0, number_of_decorations):
    my_decorations.append(
        Decoration(random.choice([3, 4, 5]), current_grid.get_random_position())
    )
current_grid.create_rectangle(my_decorations)  # Add decorations to current grid

# # The Player
my_player = Player("Kisa", 2, (1, 1))

# Start background music
stop_playback = False
play_soundfile('./res/music.mp3')

#  Evaluate Keyboard input and update grid
while True:
    try:
        # print(Keyboard_Input)
        # Keyboard Eingaben
        if str(Keyboard_Input) == "Key.left":
            player_input = 'left'
        elif str(Keyboard_Input) == "Key.right":
            player_input = 'right'
        elif str(Keyboard_Input) == "Key.up":
            player_input = 'up'
        elif str(Keyboard_Input) == "Key.down":
            player_input = 'down'
        elif str(Keyboard_Input) == "Key.q":  # FIXME Does not react to q. Only CTRL+C works
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
        current_grid.update(player_input)
        current_grid.paint(current_grid.graphics)
        time.sleep(default_update_speed)

    except KeyboardInterrupt:  # CTRL-C was pressed
        print("BYE")
        for thread in threading.enumerate():
            print(thread.name)
            thread.join()  # FIXME Sound thread sitill does not exit
        sys.exit()
