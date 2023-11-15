# Uebungen Tag 8
import math

# Aufgabe 1
print("\nAufgabe 1")


def even_odds(listen: list) -> tuple:
    """
    :param listen:
    :return:
    """
    evens = []
    odds = []
    for liste in listen:
        for element in liste:
            if element % 2 == 0:
                evens.append(element)
            else:
                odds.append(element)
    return evens, odds


gerade, ungerade = even_odds([[1, 2, 3, 4, 2048], [5, 6, 7, 8, 9, 12345]])
print(gerade)
print(ungerade)

# Aufgabe 2
print("\nAufgabe 2")


def count_chars(inputstring: str) -> dict:
    """

    :param inputstring:
    :return:
    """
    capitals = 0
    lowers = 0
    spaces = 0

    for zeichen in inputstring:
        if zeichen.isupper():
            capitals += 1
        elif zeichen.islower():
            lowers += 1
        elif zeichen.isspace():
            spaces += 1
    counts = {"Großbuchstaben": capitals, "Kleinbuchstaben": lowers, "Leerzeichen": spaces}
    return counts


teststring = "ABCabc defDEF    XYZ   xyz"
counted = count_chars(teststring)
print(counted)

# Aufgabe 3
# TODO
print("\nAufgabe 3")


def sortieren(eingabe: list or str, funktion: str = "alphabetisch", ordnung: str = "aufsteigend") -> list:
    """

    :param eingabe:
    :param funktion:
    :param ordnung:
    :return:
    """
    for element in eingabe:
        print(element)
    ausgabe = [eingabe, funktion, ordnung]
    return ausgabe


# Aufgabe 4
print("\nAufgabe 4")


def volkegel(grundflaeche: float, hoehe: float) -> float:
    """

    :param grundflaeche:
    :param hoehe:
    :return:
    """
    volume = (1 / 3) * grundflaeche * hoehe
    return volume


def volkugel(radius: float) -> float:
    """


    :param radius:
    :return:
    """
    volume = (4 / 3) * math.pi * pow(radius, 3)
    return volume


def volquader(laenge: float, breite: float, hoehe: float) -> float:
    """

    :param laenge:
    :param breite:
    :param hoehe:
    :return:
    """
    volume = laenge * breite * hoehe
    return volume


def volpyramide(grundseite: float, hoehe: float) -> float:
    """

    :param grundseite:
    :param hoehe:
    :return:
    """
    volume = (1 / 3) * pow(grundseite, 2) * hoehe
    return volume


def volinput(userinput: str = "") -> str:
    """

    :param userinput:
    :return:
    """
    allowedvols = ["Kegel", "Kugel", "Quader", "Pyramide"]
    while userinput not in allowedvols:
        userinput = input("Form angeben: ")
    if userinput == "Kugel":
        radius = input("Radius angeben: ")
        volume = volkugel(float(radius))
    elif userinput == "Kegel":
        grundflaeche = input("Grundfläche angeben: ")
        hoehe = input("Höhe angeben: ")
        volume = volkegel(float(grundflaeche), float(hoehe))
    elif userinput == "Quader":
        laenge = input("Länge angeben: ")
        breite = input("Breite angeben: ")
        hoehe = input("Höhe angeben: ")
        volume = volquader(float(laenge), float(breite), float(hoehe))
    elif userinput == "Pyramide":
        grundseite = input("Grundseite angeben: ")
        hoehe = input("Höhe angeben: ")
        volume = volpyramide(float(grundseite), float(hoehe))
    else:
        volume = "Hier ist was schiefgelaufen! Sorry!"

    output = "Das Volumen ist: " + str(volume)
    return output


voloutput = volinput()
print(voloutput)

# Aufgabe 5
print("\nAufgabe 5")
# TODO
