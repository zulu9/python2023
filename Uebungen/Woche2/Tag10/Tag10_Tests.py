# Tag 10 Tests

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
