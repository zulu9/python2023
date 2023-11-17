# Tag 10 Tests
import time
import sys

# Funktionen als Parameter
import math
myfun = math.sqrt

print(myfun(9))
print(type(myfun))
print(id(math.sqrt))
print(id(myfun))


def myquadrat(
        x: float) -> float:
    """

    :param x:
    :return:
    """
    return x**2


def mywurzel(
        x: float) -> float:
    """

    :param x:
    :return:
    """
    return x**0.5


def wrapper(
        fkt, x: float) -> float:
    """

    :param fkt:
    :param x:
    :return:
    """
    out = fkt(x)
    return out


print(wrapper(myquadrat, 4))

# Lambda
addone = lambda x: x+1   # not recommended
print(addone(7))
def addone(x): return x+1   # not recommended


hochdrei = lambda x: x**3
print(hochdrei(2))

# Lambda + Map
mylist = [1, 2, 3, 4]
results = map(lambda x: x**2, mylist)
results2 = map(math.sqrt, mylist)
print(mylist)
print(type(results))
print(list(results))
print(list(results2))


# Rekursion
def myfak(
        n: int) -> int:
    """

    :param n:
    :return:
    """
    if n == 1:
        return 1
    elif n > 1:
        return n * myfak(n-1)
    else:
        raise ValueError


print(myfak(5))


def mysum_loop(
        n: int) -> int:
    """
    :param n:
    :return:
    """
    summe = 0
    for i in range(0, n + 1):
        summe = summe + i
    return summe


mein_x = 10

starttime = time.time()
meine_summe = mysum_loop(mein_x)
print(meine_summe)
endtime = time.time()
print("Laufzeit Summe Loop:", (endtime - starttime) * 1000)


def mysum_recursive(
        n: int) -> int:
    """

    :param n:
    :return:
    """
    if n == 0:
        return 0
    elif n > 0:
        return n + mysum_recursive(n - 1)
    else:
        raise ValueError


sys.setrecursionlimit(mein_x+10)

starttime = time.time()
meine_summe = (mysum_recursive(mein_x))
print(meine_summe)
endtime = time.time()
print("Laufzeit Summe Rekursion:", (endtime - starttime) * 1000)
