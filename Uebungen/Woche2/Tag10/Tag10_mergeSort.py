# Merge Sort Rekursiv
import random
import math


def merge_sort(
        liste: list,
        level: int = 0,
        seite: str = "Main"):
    """
    Rekursives Merge Sort. ACHTUNG: Arbeitet an der Orignalliste. Kein Return!
    :param liste: Liste die sortiert werden soll
    :param level: Momentane Tiefe der Rekursion
    :param seite: Auf welcher Seite (Links oder Rechts) sind wir gerade?
    :return: gibbet nicht
    """
    level += 1
    if len(liste) > 1:
        mitte = math.ceil((len(liste) / 2))
        links = liste[:mitte]
        rechts = liste[mitte:]

        print("--------------------------------------------",
              "\n\tLevel:\t", level,
              "\n\tSeite:\t", seite,
              "\n\tOuter:\t", liste,
              "\n\tLinks:\t", links,
              "\n\tRechts:\t", rechts,
              "\n--------------------------------------------\n"
              )

        # Für beide Teillisten die Funktion wieder aufrufen
        merge_sort(links, level, "Links")
        merge_sort(rechts, level, "Rechts")

        # Zähler für die Sublisten
        l_num = 0
        r_num = 0

        # Zähler für die "äußere" Liste
        outer_num = 0

        # Wir haben in beiden Sublisten noch Elemente
        while l_num < len(links) and r_num < len(rechts):
            if links[l_num] <= rechts[r_num]:
                # Links ist kleiner oder gleich rechts: Speichere linken Wert
                liste[outer_num] = links[l_num]
                # Zöhle links einmal hoch
                l_num += 1
            else:
                # Sonst ist rechts kleiner und der rechte Wert wird gespeichert und der rechte Zähler erhöht
                liste[outer_num] = rechts[r_num]
                r_num += 1
            # Auf zum nächsten Element in der "äußeren" Liste
            outer_num += 1

        # Alle übrigen Elemente wieder zur "äußeren" Liste hinzufügen
        while l_num < len(links):
            liste[outer_num] = links[l_num]
            l_num += 1
            outer_num += 1

        while r_num < len(rechts):
            liste[outer_num] = rechts[r_num]
            r_num += 1
            outer_num += 1


# randomlist = [38, 27, 43, 3, 9, 82, 10]
upto = 5  # Anzahl der Zufallszahlen zwischen -100 und +100, die erzeugt werden sollen
randomlist = [random.randrange(-100, 100, 1) for i in range(upto)]
unsortiert = randomlist.copy()  # Unosortierte Liste merken, weil wir glech am Original rumfuschen
merge_sort(randomlist)
print("Unsotiert:\t\t", unsortiert)
print("Sortiert:\t\t", randomlist)
print("Exp max LVL:\t", (math.ceil(math.log(upto, 2))))
