# TAG 8
# Uebungen während der Vorlesung
# Aufgabe 3 von Tag 7 mit default Parametern
def fancyString(string="Hier könnte Ihre Werbung stehen!", breite=123):
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


default = fancyString()
version1 = fancyString(breite=150)
version2 = fancyString(string="Ihre Werbung")
version3 = fancyString("Ihre Werbung", 50)

print(default)
print(version1)
print(version2)
print(version3)
