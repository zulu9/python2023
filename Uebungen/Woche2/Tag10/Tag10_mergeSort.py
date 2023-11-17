# Merge Sort Rekursiv
import random
import math


def merge_sort(
        liste: list,
        level: int = 0):
    """
    Rekursives Merge Sort. ACHTUNG: Arbeitet an der Orignalliste. Kein Return!
    :param liste: Liste die sortiert werden soll
    :param level: Momentane Tiefe der Rekursion
    :return: gibbet nicht
    """
    level += 1
    if len(liste) > 1:
        mitte = len(liste) // 2
        links = liste[:mitte]
        rechts = liste[mitte:]

        print("--------------------------------------------",
              "\n\tLevel:\t", level,
              "\n\tOuter:\t", liste,
              "\n\tLinks:\t", links,
              "\n\tRechts:\t", rechts,
              "\n--------------------------------------------\n"
              )

        # Für beide Teillisten die Funktion wieder aufrufen
        merge_sort(links, level)
        merge_sort(rechts, level)

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


# randomlist = [132, 42, 23, 66, 5, 11, 132, -1, 777, 453, 52, 42, -15, -11]
upto = 60  # Anzahl der Zufallszahlen, die erzeugt werden sollen
randomlist = [random.randrange(-100, 100, 1) for i in range(upto)]
unsortiert = randomlist.copy() # Unosortiere Liste merken, weil wir glech am Original rumfuschen
merge_sort(randomlist)
print("Unsotiert:\t\t", unsortiert)
print("Sortiert:\t\t", randomlist)
print("Exp max LVL:\t", (math.ceil(math.log(upto, 2))))
