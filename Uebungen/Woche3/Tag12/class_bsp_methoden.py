class Dog:
	def __init__(self, name, breed, age, color):
		self.name = name
		self.breed = breed
		self.age = age
		self.color = color

	def poop(self, surface):
		print(f"{self.name} has pooped on the {surface}")

	def drinking(self, what):
		if type(what) is Coffee:
			print(f"{self.name} thinks {what.name} is {what.taste} and has to much energy!")
			print("Oh no....")
			self.poop('carpet')
		else:
			print(f"{self.name} drinks the {what}")


class Coffee:
	name = 'Coffee'
	taste = 'yummy'

	def __str__(self):
		return f"{self.name} is {self.taste}!"

	def add_salt(self):
		self.taste = "bäh"
		print(self)


class Cat:
	def __init__(self, name, breed, age, color, attitude):
		self.name = name
		self.breed = breed
		self.age = age
		self.color = color
		self.attitude = attitude

	def check_attitude(self):
		print(f"{self.name} has a {self.attitude} attitude.")

	def petting(self, instrument):
		if 'hand' in instrument.lower():
			print(f"Nope, {self.name} scratched you and hisses at {instrument}.")
			self.check_attitude()
		else:
			self.attitude = "good"
			print(f"{self.name} likes being petted with a {instrument}.")
			self.check_attitude()

	def __gt__(self, other):
		if self.age > other.age:
			return True
		else:
			return False

	def __lt__(self, other):
		if self.age < other.age:
			return True
		else:
			return False


print("\n~~~~ Dog Class ~~~~\n")
dog1 = Dog('Shiva', 'Mud', 7, 'mostly black')
print(dog1)
dog1.poop('grass')

print(type(Coffee()))
dog1.drinking(Coffee())


print("\n~~~~ Coffee Class ~~~~\n")
print(Coffee())
my_coffee = Coffee()
print(my_coffee)
my_coffee.add_salt()

print("\n~~~~ Cat Class ~~~~\n")
cat1 = Cat('Medusa', 'Unknown', 300, 'Ginger', 'bad')
print(cat1.attitude)
cat1.petting('Handstaubsauger')
cat1.petting('Brush')
my_cat = Cat('Kisa', 'BKH', 2, 'Lilac', 'sweet')

if my_cat < cat1:
	print(f"{my_cat.name} is younger than {cat1.name}")
