# Loops
my_list = [1, 2, 3, "MÖP", 5]
for i in my_list:
    print(i)

print("\nMit Range:")
for i in range(0, len(my_list)):
    print(i)

print("\nTiere")
zoo = {"Affe": "klug", "Elefant": "groß", "Tiger": "gefährlich", "Pinguin":"Linuxfan"}
for tier in zoo:
    print(tier, "ist", zoo[tier])

print("\nBuchstaben aus Name")
name="Karl Ranseier,"
for buchstabe in name:
    print(buchstabe)
