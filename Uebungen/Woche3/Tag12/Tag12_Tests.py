# Tag 12

# Klassen
class Dog:
    def __init__(self, name, breed, age, color):
        self.name = name
        self.breed = breed
        self.age = age
        self.color = color

    def __str__(self):  # Magic Method
        return f"DOG {self.name}, \n\tBreed: {self.breed}, \n\tAge: {self.age}, \n\tColor: {self.color}, "


dog1 = (Dog('Hasso', 'Pudel', 2, 'green'))
dog2 = (Dog('Rüdiger', 'Schäferhund', 0, 'MISSING'))
dog3 = Dog('MISSING', 'MISSING', 0, 'MISSING')
print(dog1.name)
print(dog2.breed)
print(Dog)
print(dog1)
dog1.color = 'Pink'
print(dog1.color)
del dog1 .age  # Meistens eine dumme Idee
dog1.age = None
print(dog1.age)
# del dog2
print(dog2.name)


class Enemy:
    def __init__(self, e_type, level, hp, mp):
        self.e_type = e_type
        self.level = level
        self.HP = hp
        self.MP = mp

    def __str__(self):
        return f"GEGNER {self.e_type}, \n\tHP: {self.HP}, \n\tMP: {self.MP}, \n\tLevel: {self.level}, "


enemy1 = (Enemy("Maus", 1, 99, 20))
print(enemy1)


# TODO implement 2 magic methods
