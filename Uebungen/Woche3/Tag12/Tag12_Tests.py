class Cat:
    def __init__(self, name, breed, age, color):
        self.name = name
        self.breed = breed
        self.age = age
        self.color = color


cat1 = (Cat('Kisa', 'BKH', 2, 'lilac'))

print(cat1.name)
print(cat1.breed)
print(Cat)
print(cat1)
cat1.color = 'Pink'
print(cat1. color)
del cat1.age # Meistens eine dumme Idee
cat.age = None
print(cat1.age)
