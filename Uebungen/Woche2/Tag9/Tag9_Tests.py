# Tag 9 Tests
import matplotlib.pyplot as plt

# IDs
# x = int(3)
# print("X: ", id(x))
# y = 3.123232
# print("Y: ", id(y))
# z = -14
# z2 = 5000
# print("Z, Z2, 3, 3.123232: ", id(z), id(z2), id(3), id(3.123232))

# Strings

string = "Hallo"
print(id(string))
string2 = "Hallo"
print(id(string2))
string3 = "Hallo Welt"
print(id(string3))

string = "0123456789abcdefgABCDEFG          0123456789abcdefgABCDEFG"
i = 0
numbers = []
ids = []
for zeichen in string:
    numbers.append(i)
    i += 1
    eidie = id(zeichen)
    ids.append(eidie)
plt.plot(numbers, ids, color='b')
plt.show()

# Integers
numbers = []
ids = []
for i in range(0, 9):
    numbers.append(i)
    eidie = id(i)
    ids.append(eidie)
plt.plot(numbers, ids, color='b')
plt.show()

# Listen und Tupel
print("\n Listen und Tupels")
liste = [1, 2, 3, 4, 5, "1", "2", "3"]
liste2 = liste
liste3 = liste.copy()
print(id(liste))
print(id(liste2))
print(id(liste3))
liste3.append("X")
print(liste3)
print(id(liste3))


tupel = (1, 2, 3, 4, 5, "1", "2", "3")
tupel2 = (1, 2, 3, 4, 5, "1", "2", liste)
print(id(tupel))
print(id(tupel2))
for element in tupel2:
    print(id(element))
