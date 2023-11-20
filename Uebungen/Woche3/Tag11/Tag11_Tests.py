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

# Try und except
myfun = "Hello"
try:
    print(myfun)
except Exception: # Broad exception. Nich machen!
    print("Something went wrong!")
else:
    print("Everything works fine")
finally:
    print("Wir sind durch")
