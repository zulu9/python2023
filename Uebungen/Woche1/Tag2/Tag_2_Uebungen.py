import math
import numpy

x = 2 / 4

print(x)
print(type(x))

y = int(x)
print(y)
print(type(y))

z = 1000000
a = 1_000_000

print(z, a)
print(type(z), type(a))

expressions = [
    "3 > 2",
    "5 != 6",
    "5 == 2",
    "3 < 2 or 2 > 1",
    "5 != 9 and 7 < 10",
    "not 5 != 9 and not 7 < 10",
    "(not 5 != 9 and 7 < 10) or 2 * 3 > 7",
    "not (5 != 9 and 7 < 10) or 2 * 3 > 7"
]

for x in expressions:
    print(x,  " : ", eval(x))

print(math.sqrt(9))

a = float("inf")
b = -float("inf")
print(a - b)
print(type(a), type(b))

c = math.inf
d = -math.inf
print(c - d)
print(type(c), type(d))

print(math.pi*math.e)

print(math.log10(3), math.log2(3))

mylist = [1, 2, 3, 4]
print(numpy.average(mylist), numpy.sum(mylist), numpy.std(mylist))
