# Uebungen Tag7
import time
from hashlib import sha256

# Aufgabe 1
print("\nAufgabe 1")


def my_sum(x: int) -> int:
    """
    Summe von 0 bis X
    :param x:
    :return: sum
    """
    summe = 0
    for x in range(0, x+1):
        summe = summe + x
    return summe


starttime = time.time()
meine_summe = my_sum(4)
print(meine_summe)
endtime = time.time()
print("Laufzeit:", endtime-starttime)

# Aufgabe 2
print("\nAufgabe 2")


def my_quadrat(x: int) -> int:
    """
    Flächeninhalt eines Quadrats mit Kantenlänge x
    :param x:
    :return:
    """
    area = x*x
    return area


myquadrat = my_quadrat(4)
print(myquadrat)

# Aufgabe 3
print("\nAufgabe 3")


def fancy_string(string: str, breite: int) -> str:
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


starttime = time.time()
myfancystring = fancy_string("Fancy Schmancy gerade!", 40)
print(myfancystring)
myfancystring = fancy_string("Fancy Schmancy ungerade!!", 42)
print(myfancystring)
endtime = time.time()
print("Laufzeit:", endtime-starttime)

# Aufgabe 4
print("\nAufgabe 4")


def fancy_square(wort: str, zahl: int) -> dict:
    """

    :param wort:
    :param zahl:
    :return:
    """
    quadrat = zahl * zahl
    ausgabe = {wort: quadrat}
    print("Hallo aus der Funktion. Wort ist:", wort)
    return ausgabe


testme = fancy_square("Hallo", 4)
print(testme)
print(type(testme["Hallo"]))

# Aufgabe 5
print("\nAufgabe 5")


def my_fakultaet(zahl: int) -> int:
    """

    :param zahl:
    :return:
    """
    if zahl < 0:
        raise ValueError
    if zahl == 0:
        return 1
    else:
        temp = 1
        for i in range(2, zahl + 1):
            temp *= i
        return temp


starttime = time.time()
myfak = my_fakultaet(4)
print(myfak)
endtime = time.time()
print("Laufzeit:", endtime-starttime)

# Aufgabe 6
print("\nAufgabe 6")
starttime = time.time()


def gerade_zahlen(maxnum: int) -> list[int]:
    """

    :param maxnum:
    :return:
    """
    nums = []
    for num in range(1, maxnum):
        if num % 2 == 0:
            nums.append(num)
    return nums


evens = gerade_zahlen(30)
print(evens)


def summy_sum(mini: int, maxi: int, limit: int) -> list[int]:
    num = mini
    max_sum = limit
    sum_num = 0
    while num <= maxi:
        if num == 1:
            sum_num = num
        else:
            sum_num += num
        if sum_num + num - 1 > max_sum:
            break
        num += 1
    return [sum_num, num]


mySummy = summy_sum(1, 100, 1000)
print(mySummy)


def my_primes(xstart: int, xend: int) -> list[int]:
    """

    :param xstart:
    :param xend:
    :return:
    """
    primes = []
    for x in range(xstart, xend):
        is_prime = True
        for i in range(2, x):
            if x % i == 0:
                is_prime = False
        if is_prime:
            primes.append(x)
    return primes


foundprimes = my_primes(0, 100)
print(foundprimes)


def check_password(secret: str) -> None:
    """

    :param secret:
    :return:
    """
    user_input = True
    while user_input:
        user_input = input("Passwort eingeben: ")
        user_hash = sha256(user_input.encode('utf-8')).hexdigest()
        if user_hash == secret:
            print("Passwort richtig!")
            break
        else:
            print("Passwort falsch!")


check_password("33c5ebbb01d608c254b3b12413bdb03e46c12797e591770ccf20f5e2819929b2")  # Passwort ist "passwort"
endtime = time.time()
print("Laufzeit:", endtime-starttime)

# Aufgabe 7
print("\nAufgabe 7")


def check_bools(expr: str) -> bool:
    if eval(expr):
        return True
    else:
        return False


checked = check_bools("3 == 3")
print(checked)
