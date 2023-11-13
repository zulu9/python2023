# Loops
# -----
import gc
import time

my_list = [1, 2, 3, "MÖP", 5, [6, "sieben"], [8, 9, "zehn"]]
print("\nNormal")
for i in my_list:
    print(i)
print("\nMit Range:")
for i in range(0, len(my_list)):
    print(i)
print("\nVerschachtelt")
my_list2 = [[1], "doof", "3", ["MÖP"], [5], [6, "sieben"], [8, 9, "zehn"]]
for i in my_list2:
    for m in i:
        print(m)

print("\nBuchstaben aus Name")
name = "Karl Ranseier"
for buchstabe in name:
    print(buchstabe)

print("\nBuchstaben aus Name mit Nummer")
name = "Ben Utzer"
for buchstabennummer in range(len(name)):
    print(buchstabennummer + 1, "\t", name[buchstabennummer])

print("\nZip")
mylist1 = [1, 2, "Pferd", ["KUH", 14], 13]
mylist2 = ["eins", "zwei", "drei", 4, 5, "sechs", ["sieben", 8]]
print(zip(mylist1, mylist2))
print(list(zip(mylist1, mylist2)))
for i, j in zip(mylist1, mylist2):
    print("Mylist1:", i, "; Mylist2:", j)

print("\nEnumerate")
mylist_enum = ["a", "b", "c", "f", ["q", 2, "pr"], {"apple", "banana", "cherry"}]
print(mylist_enum)
for index, wert in enumerate(mylist_enum):
    print(index, ":", wert)

print("\nEnumerate on set")
myset_enum = {"apple", "banana", "cherry"}
# myset_enum = "langerString"
print(myset_enum)
print(type(myset_enum))
print(enumerate(myset_enum))
print(list(enumerate(myset_enum)))
for index, wert in enumerate(myset_enum):
    print(index, ":", wert)

print("\nDict von Tieren")
eigenschaften = {"Affe": "klug", "Elefant": ["groß", "hat Rüssel"], "Tiger": "gefährlich", "Pinguin": "Linuxfan"}
for tier in eigenschaften:
    print(tier, "ist", eigenschaften[tier])
for index, wert in eigenschaften.items():
    print(index, "ist", wert)

# Statements
# ----------
print("\n\nIf")
zahlen = [1, 5, 23, "Pommes", -3, 7, "Wurst"]
for zahl in zahlen:
    if type(zahl) is int:
        if zahl > 5:
            print("Zahl", zahl, "ist größer 5")
        elif zahl < 5:
            print("Zahl", zahl, "ist kleiner 5")
        else:
            print("Zahl", zahl, "ist gleich 5")
    else:
        print(zahl, "ist keine Zahl.")

# List comprehension
print("\nList comprehension")
mylist1 = [x*x for x in range(0, 50) if x * x < 50 and (x * x) % 4 == 0]
mylist2 = [x*x for x in range(0, 50) if x * x < 50]
mylist3 = [x*x for x in range(0, 50)]
print(mylist1)
print(mylist2)
print(mylist3)

# While loops
print("\nWhile Loops")
i = 1
maximum = 20
while i < maximum:
    print(i)
    i += 1
print("\n", i, "\n")
while i > 15:
    print(i)
    i -= 1

# Control statements break, continue
print("\nControl statements")
for i in ['a', 'b', 'c', 'd', 'e']:
    if i == 'c':
        print("break")
        break
    print(i)
print()
for i in ['a', 'b', 'c', 'd', 'e']:
    if i == 'c':
        print("continue")
        continue
    print(i)

# Laufzeiten
print("Laufzeiten")
start = time.time()
print(start)
time.sleep(1)
end = time.time()
print(end)
