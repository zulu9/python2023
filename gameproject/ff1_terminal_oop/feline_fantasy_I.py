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
    play_thread = threading.Thread(
        target=playsound(path, False), daemon=True)
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

    def move(self, direction: str = "None"):
        """
        Objekte im Grid bewegen
        :param direction: Richtung, in die sich bewegt werden soll
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

        new_position = tuple(
            np.add(self.position, steps)
        )
        # Set new position
        if (  # Check if new position is out of grid
                new_position[0] != 0
                and new_position[1] != 0
                and new_position[0] < current_grid.size_x
                and new_position[1] < current_grid.size_y):
            self.position = new_position
        else:
            pass


class Player(Entitiy):
    def __init__(self,
                 name, type_id: int,
                 position: tuple,
                 steps: int,
                 health: int,
                 attack: int):
        """

        :param name:
        :param type_id:
        :param position:
        :param steps:
        :param health:
        :param attack:
        """
        super().__init__(type_id, position)
        self.name = name
        self.steps = steps
        self.health = health
        self.attack = attack

    def collide(self, type_id: int, position: tuple):  # TODO USE ATTACK AND ENEMY AP VALUES, CATCH ENEMIES
        if type_id in enemy_types:  # FIXME MAKE IT USE enemy.name_id
            self.health = self.health + 20
            my_state.score += 1
            for enemy in my_enemies:  # remove enemy from enemy list and delete object
                if enemy.position == position:
                    my_enemies.remove(enemy)
                    del enemy
        if type_id in hazzard_types:  # hazzards stay. no need to remove
            self.health = self.health - 30


class Decoration(Entitiy):
    pass


class Enemy(Entitiy):
    def __init__(self,
                 type_id: int,
                 position: tuple,
                 move_prob: float,
                 health: int,
                 points: int,
                 number_id: int,
                 attack: int = 0):
        """

        :param type_id:
        :param position:
        :param move_prob:
        :param health:
        :param points:
        :param number_id:
        """
        super().__init__(type_id, position)
        self.move_prob = move_prob
        self.health = health
        self.points = points
        self.number_id = number_id
        self.attack: attack


class Hazzard(Entitiy):
    def __init__(self,
                 type_id: int,
                 position: tuple,
                 attack: int):
        """

        :param type_id:
        :param position:
        :param attack:
        """
        super().__init__(type_id, position)
        self.attack = attack


class Graphicset:
    def __init__(self, name: str):
        """

        :param name: Name of the graphicsset. Must be placed in $PWD/res/$name.grf
        """
        self.name = name
        self.assignments = {}

    def read_grf_file(self):
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
                print("Could not load graphics!")
                sys.exit(1)
            finally:
                return self


class GameState:
    def __init__(self,
                 gametime: int,
                 health: int,
                 steps: int,
                 score: int,
                 graphics_name: str = "status"):
        """
        Current state of the Game
        :param gametime:
        :param health:
        :param steps:
        :param score:
        :param graphics_name:
        """
        self.gametime = gametime
        self.health = health
        self.steps = steps
        self.enemy_count = len(my_enemies)
        self.score = score
        self.graphics = Graphicset(graphics_name).read_grf_file()
        self.statusbar = []

    def update(self):  # Update Gamestate with current values
        self.health = round(my_players[0].health)
        self.steps = round(my_players[0].steps)
        self.gametime = round(time.time() - start_time)
        self.enemy_count = len(my_enemies)

    def print_statusbar(self):  # Paint Status bar TODO FIXME!!!
        """

        """
        #  ID of Symbol as defined in the status grf file, value to display
        self.statusbar = [
            [0, self.gametime],
            [1, self.health],
            [2, self.steps],
            [3, self.enemy_count],
            [4, self.score]
        ]
        #  Replace things with Symbols from status grf file and numbers full-width UTF-8 chars
        for item in self.statusbar:
            item[0] = self.graphics.assignments.get(item[0])
            item[1] = fullwidth_str(str(item[1]))
            print(f"{item[0]}: {item[1]:5}", end="")


class Grid:
    def __init__(self,
                 grid_name: str,
                 graphics_name: str,
                 size_x: int = 0,
                 size_y: int = 0):
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
        self.graphics = Graphicset(graphics_name).read_grf_file()
        self.values = []

    def create_rectangle(self, static_objects: list = None):  # FIXME USE entity.decorations object directly
        """
        Create a rectangular grid
        :return: Rectangle of 0s, surrounded by 1s and insert values for static game objects
        """

        # Create empty grid
        self.values = np.ones((self.size_x + 1, self.size_y + 1), dtype=np.int8)
        self.values[1:-1, 1:-1] = 0  # Free space
        # Insert static objects like decorations and hazzards
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

        # Move player
        if p_input is not None:
            my_players[0].move(p_input)  # Move Player
            my_players[0].steps -= 1
            my_players[0].health = my_players[0].health - 1  # Simulate Hunger
        #  EXPERIMENTAL MAKE PLAYER MOVE ITSELF RANDOMLY
        else:
            my_players[0].move(random.choice(["up", "down", "left", "right"]))

        # Move movable entities
        for enemy in my_enemies:
            if random.random() < enemy.move_prob:
                enemy.move(random.choice(["up", "down", "left", "right"]))

        # Update other things
        my_state.update()  # Update Game status
        #  my_player.health = my_player.health - (time.time() - start_time) / my_player.steps * 10  # Simulate Hunger

        # Switch graphics while running #EXPERIMENTAL
        if my_state.gametime % 2 == 0:
            self.graphics.name = "ff1_day"
        elif my_state.gametime % 3 or my_state.gametime % 7 == 0:
            self.graphics.name = "ff1_spooky"
        else:
            self.graphics.name = "ff1_night"
        self.graphics.read_grf_file()

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
                for enemy in my_enemies:  # Gegner einsetzen
                    if (row_num, el_num) == enemy.position:
                        element = enemy.type_id
                if (row_num, el_num) == my_players[0].position:  # We are at player position
                    if element in enemy_types:  # Player hat Gegner gefangen
                        my_players[0].collide(element, (row_num, el_num))
                        # catch_count += 1
                        # number_of_enemies -= 1
                        # e_current_positions.remove((row_num, el_num))  # Gegner aus Liste entfernen
                        # health_count += enemy_nutriticollideon  # Fressen
                    elif element in hazzard_types:  # Player ist in Hinderniss gelaufen
                        my_players[0].collide(element, (row_num, el_num))
                        # health_count -= obstacle_punishment  # Aua
                    element = my_players[0].type_id  # Insert player
                # Check the graphics assignment dict and replace elements with emojis etc
                element = graphicset.assignments.get(element)
                print(format(str(element), "<1"), end="")
                el_num += 1
            el_num = 0
            row_num += 1
            print()  # Final newline before status

        # Print Status Line
        my_state.print_statusbar()
        print()


# ##------MAIN LOOP------## #
# Configuration options
# Example Graphicsset with Entitiy Type IDs
# 0:🟩   0-10 Basic elements
# 1:🧱   Outer Wall
# 2:🐈   Player
# ...
# 10:🌻 10-20 Decorations
# 11:🍂
# 12:🌾
# ...
# 20:🔥 20-30 Hazzards
# ...
# 100:🐁 100+ Enemies
# ...

#
# ### CONFGIG ###
default_update_speed = 0.1  # Game speed. Default: 0.2s, minimum (=Fastest without flicker) on my system 0.01s

#  Create grid
# current_grid = Grid('ff1_level1', 'ff1_day').create_from_file()
current_grid = Grid(
    grid_name='ff1_level1',
    graphics_name="ff1_day",
    size_x=30, size_y=40
)

# Create Entities
# # The Players
player_types = [2]
my_players = []
number_of_players = 1  # FIXME SUPPORT MORE THAN ONE PLAYER OBJECT: CHANGE my_players[0]
for i in range(0, number_of_players):
    my_players.append(
        Player(
            name="Kisa",
            type_id=2,  # ID of the player as defined in the graphics set
            position=(1, 1),  # Start position
            steps=999,
            health=9999,
            attack=1)
    )


# # Neutral entities and other static objects at random positions
neutral_types = [10, 11, 12]  # List of IDs of different neutral types as defined in the graphics set
my_neutrals = []
number_of_neutrals = (current_grid.size_x + current_grid.size_y) // 2
for i in range(0, number_of_neutrals):
    my_neutrals.append(
        Decoration(
            type_id=random.choice(neutral_types),
            position=current_grid.get_random_position())
    )


# # Hazzards
hazzard_types = [20]  # List of IDs of different static hazzard types as defined in the graphics set
my_hazzards = []
number_of_hazzards = (current_grid.size_x + current_grid.size_y) // 2
for i in range(0, number_of_hazzards):
    my_hazzards.append(
        Hazzard(
            type_id=random.choice(hazzard_types),
            position=current_grid.get_random_position(),
            attack=30)
    )
current_grid.create_rectangle(static_objects=my_neutrals + my_hazzards)  # Add decorations to current grid


# # Enemies
enemy_types = [100]  # List of IDs of different enemy types as defined in the graphics set
my_enemies = []
number_of_enemies = (current_grid.size_x + current_grid.size_y) // 2  # Enemy count depending on gridsize
for i in range(0, number_of_enemies):
    my_enemies.append(
        Enemy(
            random.choice(enemy_types),
            current_grid.get_random_position(),
            move_prob=0.8,
            health=1,
            points=20,
            number_id=i)
    )


# Initial game state
my_state = GameState(
    gametime=3600,
    health=my_players[0].health,
    steps=my_players[0].steps,
    score=0,
    graphics_name="ff1_day_status"
)


# Start background music  # FIXME DOES NOT STOP PROPERLY
stop_playback = False
# play_soundfile('./res/music.mp3') # Soundfile to play

#  MAIN LOOP Evaluate Keyboard input and update grid
start_time = time.time()  # Start the clock
while True:
    my_state.gametime = round(start_time - time.time())  # Set the game clock
    try:
        # Abbruchbeningungen (WIN oder GAMEOVER)
        if my_players[0].health < 1:
            print("DU BIST TOT")
            break

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

        # Update grid and draw on screen
        current_grid.update(p_input=player_input)
        current_grid.paint(graphicset=current_grid.graphics)
        time.sleep(default_update_speed)

    except KeyboardInterrupt:  # CTRL-C was pressed
        print("BYE")
        for thread in threading.enumerate():
            print(thread.name)
            thread.join()  # FIXME Sound thread sitill does not exit
        sys.exit()
