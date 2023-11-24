# Tag 14 Tests
# Vererbung
class Animal:
    """
    superclass for animals
    """
    def __init__(self, name, color, breed):
        self.name = name
        self.color = color
        self.breed = breed
        self.sound = "Never more"

    def make_sound(self):
        print(f"{self.name} says: {self.sound}")

    def sleep(self):
        print(f"Animal {self.name} is sleeping.")

    def __add__(self, other):
        return self + other


class Dog(Animal):
    """
    class for dogs
    """
    def __init__(self, name, color, breed):
        super().__init__(name, color, breed)
        self.name = str.upper(name)
        self.sound = "Wooof Woof"

    def sleep(self):
        print(f"The Dog {self.name} is sleeping and snores. ")


class Cat(Animal):
    """
    class for cats
    """
    def __init__(self, name, color, breed, free_roamer):
        Animal.__init__(self, name, color, breed)
        self.free_roamer = free_roamer
        self.sound = "Meoooow!"

    def sleep(self):
        super().sleep()
        print(f"{self.name} is so sweet sleeping. ")


class Bird(Animal):
    """
    class for birds
    """
    def __init__(self, name, color, breed, singing):
        super().__init__(name, color, breed)
        self.singing = singing
        self.singing = singing
        if self.singing:
            self.sound = "Chirp Chirp!"
        else:
            self.sound = "Kwack Kwack!"


my_cat = Cat(name="Kisa", color="lilac", breed="BKH", free_roamer=False)
my_dog = Dog("Mahoney", "black", "Promenadenmischung")
my_bird = Bird("Dicka", "black", breed="Wellensittich", singing="bisschen")
my_bird2 = Bird("Lisa", "white", "Chicken", False)
print("Meine Katze heißt:", my_cat.name)
print(my_dog.name, "is a", my_dog.breed)
print(my_bird.sound)
print(my_cat.__dir__())
# print(enumerate(my_bird))
print(dir(my_dog))
print(vars(my_bird))
# my_cat2 = Cat("Pummel")

print(my_cat.make_sound())
print(my_dog.sound)
sound = Animal.make_sound(my_dog)
print("Sound: ", sound)
# print("Meine Katze heißt:", my_cat.name)
# print(my_dog.name, "is a", my_dog.breed)
# print(my_bird.sound)
# print(my_cat.__dir__())
# # print(enumerate(my_bird))
# print(dir(my_dog))
# print(vars(my_bird))
# my_cat2 = Cat("Kisa")r

print(my_bird.make_sound())
print(my_bird2.make_sound())
my_cat.make_sound()
print(type(my_cat))
print(Cat.__bases__)
my_dog.sleep()
my_cat.sleep()
# my_catdog = my_cat + my_dog  # Geht nicht Rekursion

my_catdog = vars(my_cat) | vars(my_dog)
print(my_catdog)
