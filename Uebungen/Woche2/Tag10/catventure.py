import numpy as np
# import only system from os
import os
import time
import keyboard

start_time = time.time()


def clear():
    """
    Clears screen (needs "real" Terminal!)
    :return:
    """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def create_grid(
        gridsize: int) -> np.array:
    """

    :param gridsize: Größe des Spielfelds (+Rand)
    :return: Gibt eine Matrix aus 1 und 0 zurück. 1 = Rand, 0 = Frei
    """
    grid = np.ones((gridsize + 1, gridsize + 1))
    grid[1:-1, 1:-1] = 0
    return grid


def paintgrid(
        grid: list = create_grid(20),
        player_position: tuple[int, int] = (1, 1)):
    """

    :param grid: Eine mit create_grid erzeugte Matrix
    :param player_position: Position des Spielers
    :return:
    """
    clear()  # Bildschirm leeren
    row_num = 0
    el_num = 0
    # Zahlen in Matrix durch Emojis ersetzen (Grafik!)
    for row in grid:
        for element in row:
            if (row_num, el_num) == player_position:  # Player Emoji einsetzen
                element = "🐈"
            elif element == 1.0:
                element = "🧱"
            elif element == 0.0:
                element = "🟩"
            print(format(element, "<1"), end="")
            el_num += 1
        el_num = 0
        row_num += 1
        print()  # Leerzeile bevor nächste Zeile verarbeitet wird


def move(
        old_position: tuple[int, int],
        direction: str = "None") -> tuple[int, int]:
    """
    Objekte im Grid bewegen
    :param old_position: Momentane Position des Objekts
    :param direction: Richting, in die sich bewegt werden soll
    :return: Neue Position des Objeks
    """
    steps = (0, 0)
    if direction == "up":
        steps = (-1, 0)
    elif direction == "down":
        steps = (1, 0)
    elif direction == "left":
        steps = (0, -1)
    elif direction == "right":
        steps = (0, 1)
    new_position = tuple(np.add(old_position, steps))
    return new_position


def move_player(direction: str):
    """
    Spieler bewegen und Spielfeld neu aufbauen
    :param direction: Richtung in die sich Spieler bewegen soll
    :return:
    """
    global p_current_position
    p_current_position = move(p_current_position, direction)
    paintgrid(grid_layout1, p_current_position)
    time.sleep(tick_len)


# Globale Option
grid_layout1 = create_grid(20)
p_start_position = (1, 1)
tick_len = 0.2

# Startposition zeichnen
p_current_position = p_start_position
paintgrid(grid_layout1, p_start_position)
time.sleep(tick_len)


move_player("down")
move_player("down")
move_player("up")
move_player("right")
move_player("right")

keyboard.on_press("left")
while True:
    try:
        if keyboard.is_pressed('left'):
            move_player("left")
        elif keyboard.is_pressed('right'):
            move_player("right")
        elif keyboard.is_pressed('down'):
            move_player("down")
        elif keyboard.is_pressed('up'):
            move_player("up")
        time.sleep(0.1)
    except:
        break


end_time = time.time()
print("Laufzeit:\t", end_time-start_time, "s")
