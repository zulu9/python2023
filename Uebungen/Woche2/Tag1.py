# Loops
# -----
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

print("\nTiere")
was_ist = {"Affe": "klug", "Elefant": "groß", "Tiger": "gefährlich", "Pinguin": "Linuxfan"}
for tier in was_ist:
    print(tier, "ist", was_ist[tier])

print("\nBuchstaben aus Name")
name = "Karl Ranseier"
for buchstabe in name:
    print(buchstabe)

print("\nBuchstaben aus Name mit Nummer")
name = "Ben Utzer"
for buchstabennummer in range(len(name)):
    print(buchstabennummer+1, "\t", name[buchstabennummer])

print("\nZip")
mylist1 = [1, 2, "Pferd", ["KUH", 14], 13]
mylist2 = ["eins", "zwei", "drei", 4, 5, "sechs", ["sieben", 8]]
for i, j in zip(mylist1, mylist2):
    print("Mylist1:", i, "; Mylist2:", j)
