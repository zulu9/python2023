# Tag 12

# Mutable / Imumtable objects

my_list = [1, "2", 3, "Pferd", 5]

print(id(my_list))

my_list[2] = 4
print(id(my_list))

# IDs of elements
print("IDs")
i = 0
for element in my_list:
    print(element, id(my_list[i]))
    print(element, id(element))
    i += 1
