# Tag 11 Tests
import random
from functools import reduce

# Reduce
liste = []
anzahl = 20
maxzahl = 10
for i in range(anzahl):
    liste.append(random.randrange(maxzahl) + 1)

myfun = reduce(lambda x, y: x * y, liste)
print(liste)
print(myfun)
