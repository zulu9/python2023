#  ---CATVENTURE 0.0.0.1 - The terminal emulator emoji Cat Adventure---
# Needs:
#   * python 3.x + einige Module
#   * UTF-8 Terminal Emulator mit Noto Color Emoji font oder Ähnlichem (TODO TEST ON WINDOWS)
#   * Unter Linux: Braucht root-Rechte wegen Keyboard-Libary (FIXME)

# ##------IMPORTS------## #
import numpy as np
import os
import time
import keyboard
import random
# TODO OPTIMIZE
# TODO OPTIONAL: Enemies that can kill you


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
    :return: Gibt eine Matrix aus Werten zurück, d aus 1 und 0 zurück.ie Elemente auf dem Spielfeld rerpäsentieren
    0 = Freies Feld,
    1 = Rahmen,
    2 = Gegner,
    3 = Gefahr / Hindnerniss
    4 = Neutrales Objekt / Deko
    5 = Neutrales Objekt / Deko
    6 = Neutrales Objekt / Deko
    """
    # Rahmen generieren
    grid = np.ones((gridsize + 1, gridsize + 1))
    grid[1:-1, 1:-1] = 0  # Freie innere Fläche definieren

    # Hindernisse und andere feste Objekte hinzufügen
    for _ in range(0, number_of_obstacles):
        grid[
            (random.randrange(current_gridsize - 1) + 1,
             random.randrange(current_gridsize - 1) + 1)
        ] = 3
    for _ in range(0, number_of_neutrals):
        grid[
            (random.randrange(current_gridsize - 1) + 1,
             random.randrange(current_gridsize - 1) + 1)
        ] = random.choice([4, 5, 6])
    return grid


def paintgrid(
        grid: list,
        player_position: tuple[int, int] = (1, 1),
        enemy_positions: list = None):
    """

    :param grid: Eine mit create_grid erzeugte Matrix
    :param player_position: Position des Spielers
    :param enemy_positions: Positionen der Gegner (Liste!)
    :return:
    """
    global catch_count
    global health_count
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
                    health_count += enemy_nutrition  # Fressen
                elif element == 3.0:  # Player ist in Hinderniss gelaufen
                    health_count -= obstacle_punishment  # Aua
                element = "🐈‍⬛"
            elif element == 1.0:  # Rehmen zeichnen
                element = "🧱"
            elif element == 0.0:  # Freie Fläche zeichnen
                element = "🟩"
            elif element == 2.0:  # Gegner zeichnen
                element = "🐁"
            elif element == 3.0:  # Hindernisse zeichnen
                element = "🔥"
            elif element == 4.0:  # Neutrales Objekt Typ 4 zeichnen
                element = "🍂"
            elif element == 5.0:  # Neutrales Objekt Typ 5 zeichnen
                element = "🌾"
            elif element == 6.0:  # Neutrales Objekt Typ 6 zeichnen
                element = "🌻"
            print(format(element, "<1"), end="")
            el_num += 1
        el_num = 0
        row_num += 1
        print()  # Leerzeile bevor nächste Zeile verarbeitet wird
    current_time = time.time()
    print("⏳", "(", round(current_time - time_count), "/", max_time_count, ")\t",
          "🧡", "(", round(health_count), ")\t",
          "🐾", step_count, "/", max_step_count, "\t"
          "🐁", number_of_enemies, "(", catch_count, "/", max_catch_count, ")\t")


def random_direction() -> str:
    """
    Hilfsfunktion für zufällige Gegnerbewegeung
    :return:
    """
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
    global health_count
    # Move player
    p_current_position = move(p_current_position, direction)
    # move enemies
    for i in range(0, number_of_enemies):
        if random.random() < e_move_prob:  # Gegner bewegt sich abhängig von der Wahrscheinlichkeit
            e_current_positions[i] = move(e_current_positions[i], random_direction())  # in zufällige Richtung
    # Update player state
    if playerinput:
        step_count += 1
    current_time = time.time()
    health_count = health_count - (step_count / (current_time - time_count)) * hunger_factor

    # Paint new grid
    paintgrid(current_grid, p_current_position, e_current_positions)
    time.sleep(tick_len)


def fancy_string(string: str, breite: int) -> str:  # FIXME STILL LOOKS LIKE SHIT
    fancystring = string
    return fancystring


def win(
        reason: str = "Gewonnen"):
    """

    :param reason: Grund für Win
    :return:
    """
    update_board()
    print(fancy_string(reason, 30))


def gameover(
        reason: str = "Game Over!"):
    """

    :param reason: Grund für Game Over
    :return:
    """
    update_board()
    print(fancy_string(reason, 30))

# ##------FUNKTIONEN ENDE------## #


# ##------MAIN GAME LOOP------## #
# Globale Option und Startparameter
current_gridsize = 30  # Spielfeldgröße (X^2)

max_time_count = 60  # Maximale Spielzeit in s
max_step_count = 500  # Maximale Schrittzahl

step_count = 1  # Schrittzähler am Anfang
health_count = 100  # HP am Anfang
hunger_factor = 0.1   # Hungerfaktor. HP nimmt mit Zeit und Schrittzahl ab. HP - (Schritte / Zeit) * Hungerfaktor)

enemy_nutrition = health_count // 3  # Punkte für gefangen Gegner
number_of_enemies = current_gridsize // 2  # Anzahl Gegner
e_move_prob = 0.8  # Wahrscheinlichkeit, dass sich ein Gegner pro Runde bewegt

catch_count = 0  # Anfangspunktzahl
max_catch_count = number_of_enemies // 2 + 1  # Zielpunktzahl

number_of_obstacles = current_gridsize // 2  # Anzahl der Hindernisse
obstacle_punishment = health_count  # HP-Verlust, wenn Player Hinderniss berührt

number_of_neutrals = current_gridsize  # Anzahl Objekte, die nichts besonderens tun

tick_len = 0.01  # Spielgeschwindigkeit / Zeit zwischen Moves. . Standard 0 = So schnell wie möglich.

# Startpositionen würfeln
p_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)

e_start_positions = []
for _ in range(0, number_of_enemies):  # Startpositionen der Gegner
    e_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
    e_start_positions.append(e_start_position)

# Anfangssituation zeichnen
current_grid = create_grid(current_gridsize)  # Initiales Grid erstellen
time_count = time.time()  # Startzeit merken
p_current_position = p_start_position  # Startposition merken
e_current_positions = e_start_positions  # Gegner Start positionen merken
paintgrid(current_grid, p_current_position, e_start_positions)  # Startgrid zeichnen
time.sleep(tick_len)
input("\nDu bist die Katze! Fange alle Mäuse und lauf nicht ins Feuer! \n\tEnter drücken zum Starten")

#  Keyboard input auswerten und Spielfeld aktualisieren bis Zielpunktzahl erreicht ist oder User abgebrochen hat
while True:
    current_time_count = round(time.time() - time_count)
    try:
        # Abbruchbeningungen (WIN oder GAMEOVER)
        if catch_count == max_catch_count:  # Wir haben gewonnen
            win("\n🎉\t GEWONNEN!!! \t🎉")
            break
        elif step_count > max_step_count:  # Keine Schritte mehr übrig
            gameover("\n☠️\tDu bist zu viel gelaufen!\t☠️")
            break
        elif health_count < 0:  # Wir sind gestorben
            gameover("\n☠️\tDu bist gestorben!\t☠️")
            break
        elif current_time_count > max_time_count:  # Wir haben die Zeit überschritten
            gameover("\n☠️\tZeitlimit überschritten\t☠️")
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
        time.sleep(0.1)  # Ein kleiner Delay, damit das Spiel nicht zu Schnell läuft

    except KeyboardInterrupt:  # STRG-C gedrückt
        gameover("Aufgegeben? 😿😿😿")
        break
