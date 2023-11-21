class Dog:
	def __init__(self, name, breed, age, color):
		self.name = name
		self.breed = breed
		self.age = age
		self.color = color


dog1 = Dog('Shiva', 'Mud', 7, 'mostly black')
print(dog1)


class Coffee:
	name = 'Coffee'
	taste = 'yummy'

	def __str__(self):
		return f"{self.name} is {self.taste}!"


print(Coffee())
my_coffee = Coffee()
print(my_coffee)


class Cat:
	# attitude = 'bad'

	def __init__(self, name, breed, age, color, attitude):
		self.name = name
		self.breed = breed
		self.age = age
		self.color = color
		self.attitude = attitude

	def __str__(self):
		return f"{self.name} is a {self.attitude} {self.color} {self.breed}-Cat. She is {self.age} years old."

	def eat(self, food):
		return f"{self.name} is eating {food}"


cat1 = Cat('Medusa', 'Unknown', 300, 'Ginger', 'friendly')
print(cat1.attitude)

my_cat = Cat('Kisa', 'BKH', 2, 'Lilac', 'sweet')

print(my_cat)
print(my_cat.attitude)
print(cat1)

print(my_cat.eat("Fish"))
print(my_cat.eat)

print(type(my_cat))
print(type(my_cat.eat))
print(type(my_cat.eat("Fish")))

food = "Salmon"
my_food = "Pizza"
print(my_cat.eat(food))
print(my_cat.eat(my_food))
print(my_cat.eat)
