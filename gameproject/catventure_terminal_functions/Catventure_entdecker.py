#  ---CATVENTURE 0.0.0.1 - The terminal emulator emoji Cat Adventure---
# Needs:
#   * python 3.x + einige Module
#   * UTF-8 Terminal Emulator mit Noto Color Emoji Font oder Ähnlichem (TODO TEST ON WINDOWS)
#   * Unter Linux: Braucht root-Rechte wegen Keyboard-Libary (FIXME)

import numpy as np
import random
import time

class Grid:

    current_gridsize = 30  # Spielfeldgröße (X^2) Default: 30
    number_of_obstacles = current_gridsize // 2  # Anzahl der Hindernisse
    number_of_substances = current_gridsize  # Anzahl Objekte, die nichts besonderens tun
    number_of_enemies = current_gridsize // 2  # Anzahl Gegner
    #global catch_count
    #global health_count
    #global e_current_positions
    #global number_of_enemies


    def __init__(self, gridsize, number_of_obstacles,number_of_substances, player_position: tuple[int, int] = (1, 1),enemy_positions: list = None):
        self.gridsize=gridsize
        self.number_of_obstacles=number_of_obstacles
        self.number_of_substances=number_of_substances
        self.player_position=player_position
        self.enemy_positions=enemy_positions

    def create_grid(self):
        """
        :param gridsize: Größe des Spielfelds (+Rand)
        :return: gibt eine Matrix aus Werten zurück, die Elemente auf dem Spielfeld rerpäsentieren
        0 = Freies Feld,
        1 = Rahmen,
        2 = Beute(Mäuse) c
        3 = Gefahr (var: number_of_obstacles)
        4 = Chemische Substanz 1
        5 = Chemische Substanz 2
        6 = Chemische Substanz 3
        """
        # Rahmen generieren
        current_gridsize = 30                                               # ToDO: current_gridsize to relocate

        grid = np.ones((self.gridsize + 1, self.gridsize + 1))
        grid[1:-1, 1:-1] = 0  # Freie innere Fläche definieren

        # Hindernisse und andere feste Objekte hinzufügen
        for _ in range(0, self.number_of_obstacles):
            grid[
                (random.randrange(current_gridsize - 1) + 1,
                 random.randrange(current_gridsize - 1) + 1)
            ] = 3
        for _ in range(0, self.number_of_substances):
            grid[
                (random.randrange(current_gridsize - 1) + 1,
                 random.randrange(current_gridsize - 1) + 1)
            ] = random.choice([4, 5, 6])
        return grid

    '''
    feld=Grid(30,4,4)
    print(feld.create_grid())
    '''

    # ToDo: Der untere Codeblock sollte einer Methode in der Class gamefunction zugewiesen werden!
    def paintgrid(self):
        """

        :param grid: Eine mit create_grid erzeugte Matrix
        :param player_position: Position des Spielers
        :param enemy_positions: Positionen der Gegner (Liste!)
        :return:
        """
        grid=self.create_grid(self)
        current_gridsize = 30           #ToDo: Current_gridsize der Klasse übergeben
        #ToDo clear()  # Bildschirm leeren
        row_num = 0
        el_num = 0
        # Startpositionen würfeln
        player_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
        enemy_positions = []
        for _ in range(0, self.number_of_enemies):  # Startpositionen der Gegner
            enemy_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
            enemy_positions.append(enemy_position)

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
                    element = "🐈"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 1.0:  # Rehmen zeichnen
                    element = "🧱"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 0.0:  # Freie Fläche zeichnen
                    element = "🟩"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 2.0:  # Gegner zeichnen
                    element = "🐁"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 3.0:  # Hindernisse zeichnen
                    element = "🔥"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 4.0:  # Neutrales Objekt Typ 4 zeichnen
                    element = "🍂"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 5.0:  # Neutrales Objekt Typ 5 zeichnen
                    element = "🌾"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                elif element == 6.0:  # Neutrales Objekt Typ 6 zeichnen
                    element = "🌻"               # ToDo: Die Emojis der Objekte sollten im object_dict in der class Entity hinterlegt sein
                print(format(element, "<1"), end="")
                el_num += 1
            el_num = 0
            row_num += 1

'''
feld=Grid(30,4,4)
print(feld.paintgrid())
'''


class Entity(Grid):
  #start_position=default_values für x und y
  # Der Dictionary objekt_eigenschaften erlaubt es, zum einen neue objekte im Spielraum zu kreieren\
  # und ihnen im dict auch beliebige Grundeigenschaften zu zuschreiben.

    objekt_dictionary = {"spieler": "spielt", "Beute": "Beute rennt weg und wird gefangen", "neutrales_objekt": "neutrales_objekt",
                       "steinmauer": "steinmauer"}
    def __init__(self,objekt_name):
      #ToDo:  Grid.__init__(position)             #start_x_position, start_y_position
        self.objekt_name = objekt_name

    def __call__(self, objekt_name):
       return self.objekt_dictionary[self.objekt_name]



class Spieler(Entity):
   #objekt_name = "spieler"
   def __init__(self, objekt_name= "spieler", start_x_position=7, start_y_position=7, old_position=[0, 0],direction: str="None"):
       self.objekt_name=objekt_name
       Entity.__init__(self,objekt_name)
       self.spielerposition = [start_x_position, start_y_position]
       #ToDo Grid.paintGrid(self.spielerposition)
       self.old_position=old_position           # ToDo: Das Objekt sollt nur ein Attribut self.position  durchweg im ganzen Spiel zugewiesen bekommen
       self.direction=direction

       #ToDo:
       #self.spielername=spielername       # Name für den Spieler ,spielername="Merlin"
       #self.niveau=niveau   # Erfahrungsstufe ( apprentice, intermediate, master) , niveau="apprentice"

       # ToDo: Die Methode move(() sollte vielleicht auch in eine andere Klasse relokalisiert werden.

   def move(self, old_position, direction):
       """
       Objekte im Grid bewegen
       :param old_position: momentane Position des Objekts
       :param direction: Richtung, in die sich bewegt werden soll
       :return: neue Position des Objeks
       """
       if self.direction == "up":
           steps = (-1, 0)
       elif self.direction == "down":
           steps = (1, 0)
       elif self.direction == "left":
           steps = (0, -1)
       elif self.direction == "right":
           steps = (0, 1)
       else:
           steps = (0, 0)
       new_position = tuple(np.add(self.old_position, steps))
       if (
               new_position[0] != 0
               and new_position[1] != 0
               and new_position[0] < current_gridsize
               and new_position[1] < current_gridsize):

           self.spielerposition=new_position
       else:
           self.spielerposition=old_position

class Beute(Entity):
    #objekt_name = "beute"

    def __init__(self, objekt_name="Beute", start_x_position=8, start_y_position=8, old_position=[0, 0], direction: str = "None"):
        self.objekt_name = objekt_name
        Entity.__init__(self, objekt_name)
        self.spielerposition = [start_x_position, start_y_position]
        self.old_position = old_position  # ToDo: Das Objekt sollt nur ein Attribut self.position  durchweg im ganzen Spiel zugewiesen bekommen
        self.direction = direction






merlin=Spieler()
print(merlin("spieler"))
Maus=Beute()
print(Maus)



'''
   def win(reason: str = "Gewonnen"):
       """

       :param reason: Grund für Win
       :return:
       """
       reason = reason.replace(" ", "⬜")  # Leerzeichen durch hübsche Blöcke ersetzen
       update_board()
       print(fancy_string(reason, current_gridsize))

   def gameover(
           reason: str = "Game Over!"):
       """

       :param reason: Grund für Game Over
       :return:
       """
       reason = reason.replace(" ", "⬜")  # Leerzeichen durch hübsche Blöcke ersetzen
       update_board()
       print(fancy_string(reason, current_gridsize))


class Substanzen(Entity):

class Natur(Entity):

class Spieloberflaeche:
   
   print()  # Leerzeile bevor nächste Zeile verarbeitet wird
   # Statuszeile
   current_time = time.time()
   statuszeile = "⏳" + str(max_time_count - round(current_time - start_time)) + "    " + \
                 "🧡" + str(round(health_count)) + "    " + \
                 "🐾" + str(max_step_count + 1 - step_count) + "    " + \
                 "🐁" + str(number_of_enemies) + "(" + str(catch_count) + "/" + str(max_catch_count) + ") "
   print(halfwidth_to_fullwidth(statuszeile))
   
   # String in Unicode Fullwidth übersetzen (Achtung: Kann keine Umlaute!)
   HALFWIDTH_TO_FULLWIDTH = str.maketrans(
       '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~',
       '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～')

   def halfwidth_to_fullwidth(s):
       return s.translate(HALFWIDTH_TO_FULLWIDTH)

   def fancy_string(
           string: str = "Hier könnte Ihre Werbung stehen!",
           breite: int = 30) -> str:
       """
       :param string: Nachricht
       :param breite: Breite der Box
       :return: fancystring
       """
       border = "🟧"
       padder = "⬜"
       # string gerade Anzahl zeichen und breite ungerade oder umgekehrt. Wir brauchen ein extra Zeichen
       if len(string) % 2 != breite % 2:
           topline = border + border
       else:
           topline = border

       for i in range(0, breite - 2):  # -2 Wegen den + am Anfang und Ende
           topline = topline + border

       topline = topline + border + "\n"
       padding = ""

       for i in range(0, int((breite - 1) / 2 - len(string) / 2)):
           padding = padding + padder

       middleline = border + padding + halfwidth_to_fullwidth(string) + padding + border + "\n"
       bottomline = topline
       fancystring = topline + middleline + bottomline
       return fancystring

class GameFunction:
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

   def update_board(
           direction: str = "None",
           playerinput: bool = False):
       """
       Spieler bewegen und Spielfeld neu aufbauen. Dies entpricht einer Runde. D.h. Gegner bewegen sich usw
       :param direction: Richtung, in die sich Spieler bewegen soll
       :param playerinput: wurde das Update durch Spielerbewegung ausgelöst?
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
       health_count = health_count - (step_count / (current_time - start_time)) * hunger_factor

       # Paint new grid
       paintgrid(current_grid, p_current_position, e_current_positions)
       time.sleep(tick_len)


   # ##------MAIN GAME LOOP------## #
 

   max_time_count = 60  # Maximale Spielzeit in s Default: 60
   max_step_count = current_gridsize ** 2 // 6  # Maximale Schrittzahl

   step_count = 1  # Schrittzähler am Anfang. Default: 1
   health_count = 99  # HP am Anfang. Default 99
   hunger_factor = 0.1  # Hungerfaktor. HP nimmt mit Zeit und Schrittzahl ab. HP - (Schritte / Zeit) * Hungerfaktor)

   enemy_nutrition = health_count // 3  # HP, die man für gefangenen Gegner bekommt
   
   e_move_prob = 0.8  # Wahrscheinlichkeit, dass sich ein Gegner pro Runde bewegt

   catch_count = 0  # Anfangspunktzahl. Default: 0
   max_catch_count = number_of_enemies // 2 + 1  # Zielpunktzahl
   
   
     # Globale Optionen und Startparameter
   
   obstacle_punishment = health_count // 3  # HP-Verlust, wenn Player Hinderniss berührt

   

   tick_len = 0.01  # Spielgeschwindigkeit / Zeit zwischen Moves. Default: 0.01

   # Startpositionen würfeln
   p_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)

   e_start_positions = []
   for _ in range(0, number_of_enemies):  # Startpositionen der Gegner
       e_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
       e_start_positions.append(e_start_position)

   
   # Startpositionen würfeln
   p_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)

   e_start_positions = []
   for _ in range(0, number_of_enemies):  # Startpositionen der Gegner
       e_start_position = (random.randrange(current_gridsize - 1) + 1, random.randrange(current_gridsize - 1) + 1)
       e_start_positions.append(e_start_position)

   # Anfangssituation zeichnen
   start_time = time.time()  # Startzeit merken
   current_grid = create_grid(current_gridsize)  # Initiales Grid erstellen
   p_current_position = p_start_position  # Startposition merken
   e_current_positions = e_start_positions  # Gegner Start positionen merken
   paintgrid(current_grid, p_current_position, e_start_positions)  # Startgrid zeichnen
   print(halfwidth_to_fullwidth("\nDU BIST 🐈!\nFANGE 🐁 UND LAUF NICHT DURCH 🔥!\n"))
   input(fancy_string("ENTER⬜DRUECKEN⬜ZUM⬜STARTEN"))
   start_time = time.time()  # Startzeit merken
   time.sleep(tick_len)
   
   
   
   
   
   

# ##------MAIN GAME LOOP------## #
# Globale Optionen und Startparameter
current_gridsize = 30  # Spielfeldgröße (X^2) Default: 30

max_time_count = 60  # Maximale Spielzeit in s Default: 60
max_step_count = current_gridsize ** 2 // 6  # Maximale Schrittzahl

step_count = 1  # Schrittzähler am Anfang. Default: 1
health_count = 99  # HP am Anfang. Default 99
hunger_factor = 0.1  # Hungerfaktor. HP nimmt mit Zeit und Schrittzahl ab. HP - (Schritte / Zeit) * Hungerfaktor)

enemy_nutrition = health_count // 3  # HP, die man für gefangenen Gegner bekommt
number_of_enemies = current_gridsize // 2  # Anzahl Gegner
e_move_prob = 0.8  # Wahrscheinlichkeit, dass sich ein Gegner pro Runde bewegt

catch_count = 0  # Anfangspunktzahl. Default: 0
max_catch_count = number_of_enemies // 2 + 1  # Zielpunktzahl

number_of_obstacles = current_gridsize // 2  # Anzahl der Hindernisse
obstacle_punishment = health_count // 3  # HP-Verlust, wenn Player Hinderniss berührt

number_of_neutrals = current_gridsize  # Anzahl Objekte, die nichts besonderens tun

tick_len = 1  # Spielgeschwindigkeit / Zeit zwischen Moves. Default: 0.01



# Anfangssituation zeichnen
start_time = time.time()  # Startzeit merken
current_grid = create_grid(current_gridsize)  # Initiales Grid erstellen
p_current_position = p_start_position  # Startposition merken
e_current_positions = e_start_positions  # Gegner Start positionen merken
paintgrid(current_grid, p_current_position, e_start_positions)  # Startgrid zeichnen
print(halfwidth_to_fullwidth("\nDU BIST 🐈!\nFANGE 🐁 UND LAUF NICHT DURCH 🔥!\n"))
input(fancy_string("ENTER⬜DRUECKEN⬜ZUM⬜STARTEN"))
start_time = time.time()  # Startzeit merken
time.sleep(tick_len)

#  Keyboard input auswerten und Spielfeld aktualisieren bis Zielpunktzahl erreicht ist oder User abgebrochen hat
while True:
   current_time_count = round(time.time() - start_time)
   try:
       # Abbruchbeningungen (WIN oder GAMEOVER)
       if catch_count == max_catch_count:  # Wir haben gewonnen
           win("🎉DU HAST GEWONNEN!!!🎉")
           break
       elif step_count >= max_step_count:  # Keine Schritte mehr übrig
           gameover("💀DU BIST ZU VIEL GELAUFEN!💀")
           break
       elif health_count <= 0:  # Wir sind gestorben
           gameover("💀DU BIST GESTORBEN!💀")
           break
       elif current_time_count >= max_time_count:  # Wir haben die Zeit überschritten
           gameover("⌛ZEITLIMIT UEBERSCHRITTEN!⌛")
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
       gameover("AUFGEGEBEN?")
       break

class Story:


# ##------FUNKTIONEN ANFANG------## #




def random_direction() -> str:
   """
   Hilfsfunktion für zufällige Gegnerbewegeung
   :return:
   """
   choice = random.choice(["up", "down", "left", "right"])
   return choice













#  Keyboard input auswerten und Spielfeld aktualisieren bis Zielpunktzahl erreicht ist oder User abgebrochen hat
while True:
   current_time_count = round(time.time() - start_time)
   try:
       # Abbruchbeningungen (WIN oder GAMEOVER)
       if catch_count == max_catch_count:  # Wir haben gewonnen
           win("🎉DU HAST GEWONNEN!!!🎉")
           break
       elif step_count >= max_step_count:  # Keine Schritte mehr übrig
           gameover("💀DU BIST ZU VIEL GELAUFEN!💀")
           break
       elif health_count <= 0:  # Wir sind gestorben
           gameover("💀DU BIST GESTORBEN!💀")
           break
       elif current_time_count >= max_time_count:  # Wir haben die Zeit überschritten
           gameover("⌛ZEITLIMIT UEBERSCHRITTEN!⌛")
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
       gameover("AUFGEGEBEN?")
       break
       


'''
