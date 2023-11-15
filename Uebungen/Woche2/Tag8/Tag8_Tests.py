# TAG 8
# Uebungen während der Vorlesung
# Aufgabe 3 von Tag 7 mit default Parametern
def fancy_string(
        string: str = "Hier könnte Ihre Werbung stehen!",
        breite: int = 123) -> str:
    """
    :param string: Nachricht
    :param breite: Breite der Box
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


default = fancy_string()
version1 = fancy_string(breite=150)
version2 = fancy_string(string="Ihre Werbung")
version3 = fancy_string("Ihre Werbung", 50)

print(default)
print(version1)
print(version2)
print(version3)


mydict = {'1': 2, '3': 4, '5': 6}


def bsp3(
        adict: dict) -> None:
    """

    :param adict:
    :return:
    """
    print(adict)
    for key, value in adict.items():
        print("%s == %s" % (key, value))


bsp3(mydict)
