# Tag 15 Tests
from dataclasses import *

# Dataclasses
@dataclass
class Teilnehmer:
    age: int
    name: str = "muh"

    def print_attributes(self):
        print(f'{self.name} is {self.age} years old')


bsp_teilnehmer = Teilnehmer(2, 'Kisa')
print(bsp_teilnehmer)
bsp_teilnehmer.print_attributes()

bsp_teilnehmer2 = astuple(Teilnehmer(4, 'Mahoney'))
print(bsp_teilnehmer2)
# bsp_teilnehmer2.print_attributes()

# Iterators
mylist = ['a', 'b', 'c']
print(mylist)
mylist = iter(mylist)
print(mylist)
print(next(mylist))
print(next(mylist))
print(next(mylist))

# Generators
def counter(n):
    for i in range(n + 1):
        yield i

print(counter)
for num in counter(10):
    print(num)
