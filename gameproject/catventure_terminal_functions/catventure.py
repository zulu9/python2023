#  ---CATVENTURE 0.0.0.1 - The terminal emulator emoji Cat Adventure---
# Needs:
#   * python 3.x + some modules
#   * UTF-8 Terminal Emulator with Noto Color Emoji font or similar (TODO TEST ON WINDOWS)
#   * On Linux: needs root because of the keyboard module (FIXME)

import numpy as np
import os
import time
import keyboard
import random
# TODO OPTIMIZE
# OPTIONAL: Enemies that can kill you


# ##------FUNKTIONEN ANFANG------## #
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
        player_position: tuple[int, int] = (1, 1),
        enemy_positions: list = None):
    """

    :param grid: Eine mit create_grid erzeugte Matrix
    :param player_position: Position des Spielers
    :param enemy_positions: Positonen der Gegner (Liste!)
    :return:
    """
    global catch_count
    global hunger_count
    global e_current_positions
    global number_of_enemies

    clear()  # Bildschirm leeren
    row_num = 0
    el_num = 0
    # Zahlen in Matrix durch Emojis ersetzen (Grafik + Collision Detektion!)
    for row in grid:
        for element in row:
            for enemy_position in enemy_positions:  # Gegner einsetzen
                if (row_num, el_num) == enemy_position:
                    element = 2.0
            if (row_num, el_num) == player_position:  # Player Emoji einsetzen
                if element == 2.0:  # Player hat Gegner gefangen
                    catch_count += 1
                    number_of_enemies -= 1
                    e_current_positions.remove((row_num, el_num))  # Gegner aus Liste entfernen
                    hunger_count += hunger_enemy_nutrition  # Fressen
                element = "🐈"
            elif element == 1.0:  # Rehmen und Hindernisse zeichnen
                element = "🧱"
            elif element == 0.0:  # Freie Fläche zeichnen
                element = "🟩"
            elif element == 2.0:  # Gegner zeichnen
                element = "🐁"
            print(format(element, "<1"), end="")
            el_num += 1
        el_num = 0
        row_num += 1
        print()  # Leerzeile bevor nächste Zeile verarbeitet wird
    current_time = time.time()
    print("⏲️", "(", round(current_time - time_count), "/", max_time_count, ")\t",
          "🐾", step_count, "/", max_step_count, "\t"
          "🐁", number_of_enemies, "(", catch_count, "/", max_catch_count, ")\t",
          "🥓", "(", round(hunger_count), ")\t")


def random_direction() -> str:
    choice = random.choice(["up", "down", "left", "right"])
    return choice


def move(
        old_position: tuple[int, int],
        direction: str = "None") -> tuple[int, int]:
    """
    Objekte im Grid bewegen
    :param old_position: Momentane Position des Objekts
    :param direction: Richting, in die sich bewegt werden soll
    :return: Neue Position des Objeks
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
    new_position = tuple(np.add(old_position, steps))
    if (
            new_position[0] != 0
            and new_position[1] != 0
            and new_position[0] < current_gridsize
            and new_position[1] < current_gridsize):
        return new_position
    else:
        return old_position


def update_board(
        direction: str = "None",
        playerinput: bool = False):
    """
    Spieler bewegen und Spielfeld neu aufbauen. Dies entpricht einer Runde. D.h. Gegner bewegen sich usw
    :param direction: Richtung in die sich Spieler bewegen soll
    :param playerinput: Wurde das Update durch Spielerbewegung ausgelöst?
    :return:
    """
    global p_current_position
    global e_current_positions
    global step_count
    global hunger_count
    # Move player
    p_current_position = move(p_current_position, direction)
    # move enemies
    for i in range(0, number_of_enemies):
        if random.random() < e_move_prob:
            e_current_positions[i] = move(e_current_positions[i], random_direction())
    # Update player state
    if playerinput:
        step_count += 1
    current_time = time.time()
    hunger_count = hunger_count - (step_count / (current_time - time_count)) * hunger_factor

    # Paint new grid
    paintgrid(current_grid, p_current_position, e_current_positions)
    time.sleep(tick_len)


def fancy_string(string: str, breite: int) -> str:
    # FIXME Output looks like shit
    """

    :param string:
    :param breite:
    :return: fancystring
    """
    # string gerade Anzahl zeichen und breite ungerade oder umgekehrt. Wir brauchen ein extra Zeichen
    if len(string) % 2 != breite % 2:
        topline = "+-"
    else:
        topline = "+"

    for i in range(0, breite-2):  # -2 Wegen den + am Anfang und Ende
        topline = topline + "-"

    topline = topline + "+\n"

    padding = ""
    for i in range(0, int((breite-1)/2-len(string)/2)):
        padding = padding + " "

    middleline = "+" + padding + string + padding + "+\n"

    bottomline = topline

    fancystring = topline + "\n" + middleline + "\n" + bottomline
    return fancystring


def win(
        reason: str = "Gewonnen"):
    update_board()
    print(fancy_string(reason, 30))


def gameover(reason: str = "Game Over!"):
    update_board()
    print(fancy_string(reason, 30))

# ##------FUNKTIONEN ENDE------## #


# ##------MAIN GAME LOOP------## #
# Globale Option und Startparameter
current_gridsize = 30  # Spielfeldgröße (X^2)

max_time_count = 60  # Maximale Spielzeit in s

step_count = 1  # Schrittzähler
max_step_count = 500  # Maximale Schrittzahl

catch_count = 0  # Anfangspunktzahl
max_catch_count = 4  # Zielpunktzahl

hunger_count = 100  # Hungerwert am Anfang (Default 100 = satt)
max_hunger_count = 0  # Hungerwert für Game over (Default 0 = tod)
hunger_factor = 0.1   # Hungerfaktor Hunger = (Schritte / Zeit) * Hungerfaktor)
hunger_enemy_nutrition = 100  # Punkte für gefangen Gegner
number_of_enemies = 10  # Anzahl Gegner
e_move_prob = 0.8  # Wahrscheinlichkeit, dass sich ein Gegner bewegt

tick_len = 0  # Zeit zwischen Moves (Bestimmt Spielgeschwindigkeit, über SSH auf min 0.3 setzen)


# Startpositionen würfeln
p_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
e_start_positions = []
for _ in range(0, number_of_enemies):  # Startpositionen der Gegner
    e_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
    e_start_positions.append(e_start_position)

# Anfangssituation zeichnen
current_grid = create_grid(current_gridsize)  # Initiales Grid erstellen
time_count = time.time()  # Startzeit merken
p_current_position = p_start_position  # Startposition
e_current_positions = e_start_positions  # Gegner Start positionen
paintgrid(current_grid, p_current_position, e_start_positions)
time.sleep(tick_len)

#  Keyboard input auswerten und Spielfeld aktualisieren bis Zielpunktzahl erreicht ist oder User abgebrochen hat
while True:
    current_time_count = round(time.time() - time_count)
    try:
        # Abbruchbeningungen (WIN oder GAMEOVER)
        if catch_count == max_catch_count:  # Wir haben gewonnen
            win("🎉\t🎈🎈🎈\t🎊🎊🎊\t🎈🎈🎈\t🎉\n\t\tGEWONNEN!!!\n🎉\t🎈🎈🎈\t🎊🎊🎊\t🎈🎈🎈\t🎉\n")
            break
        elif step_count > max_step_count:  # Keine Schritte mehr übrig
            gameover("\t☠️Du bist zu viel gelaufen!\t☠️")
            break
        elif hunger_count < max_hunger_count:  # Wir sind verhungert
            gameover("☠️\nDu bist vehungert!\n☠️")
            break
        elif current_time_count > max_time_count:  # Wir haben die Zeit überschritten
            gameover("\n☠️Zeitlimit überschritten\n☠️")
            break
        # Keyboard Eingaben
        elif keyboard.is_pressed('left'):
            update_board("left", playerinput=True)
        elif keyboard.is_pressed('right'):
            update_board("right", playerinput=True)
        elif keyboard.is_pressed('down'):
            update_board("down", playerinput=True)
        elif keyboard.is_pressed('up'):
            update_board("up", playerinput=True)
        update_board()
        time.sleep(0.1)  # FIXME Ist irgendwie nötig sonst läuft es zu schnell

    except KeyboardInterrupt:  # STRG-C gedrückt
        gameover("Aufgegeben? 😿😿😿")
        break
